from flask import Flask, request, jsonify, render_template
import json
import mysql.connector
import datetime, time 


# to be moved to driver_summary.py
# #############
# https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-gs.html
import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
debugMode = True
if debugMode:
    DEFAULT_DATA_SOURCE = "./detail-records"
    DEFAULT_OUTPUT_URL  = "./result/csv"
else:
    DEFAULT_DATA_SOURCE = "s3://comp4442project2024spring/detail-records"
    DEFAULT_OUTPUT_URL  = "s3://comp4442project2024spring/result/csv"
schema = StructType() \
      .add("driverID",StringType(),True) \
      .add("carPlateNumber",StringType(),True) \
      .add("Latitude",DoubleType(),True) \
      .add("Longtitude",DoubleType(),True) \
      .add("Speed",IntegerType(),True) \
      .add("Direction",IntegerType(),True) \
      .add("siteName",StringType(),True) \
      .add("Time",DateType(),True) \
      .add("isRapidlySpeedup",IntegerType(),True) \
      .add("isRapidlySlowdown",IntegerType(),True) \
      .add("isNeutralSlide",IntegerType(),True) \
      .add("isNeutralSlideFinished",IntegerType(),True) \
      .add("neutralSlideTime",IntegerType(),True) \
      .add("isOverspeed",IntegerType(),True) \
      .add("isOverspeedFinished",IntegerType(),True) \
      .add("overspeedTime",IntegerType(),True) \
      .add("isFatigueDriving",IntegerType(),True) \
      .add("isHthrottleStop",IntegerType(),True) \
      .add("isOilLeak",IntegerType(),True)
# #############
# end to be moved to driver_summary.py


application = Flask(__name__)

def db_connection():
    mydb = mysql.connector.connect( host = 'database-1.cti2wk8aib5l.us-east-1.rds.amazonaws.com',
    user = 'admin',
    port = '3306',
    database = 'lab6',
    passwd = '12345678',
    autocommit = True)

    #print("successfully connect to the database")
    
    return mydb

mydb = db_connection()
cur = mydb.cursor()

@application.route("/")
def index():
    return render_template("monitor.html")

@application.route("/hello")
def hello():
    # testing
    json_data = getDriverSummary("hanhui1000002", "2017-01-01 00:00:00", "2017-01-02 00:00:00")
    return jsonify(json_data), 200

@application.route("/api/getDriverByID", methods=['POST'])
def getDriverByID():
    json_data = request.get_json()
    driverID = json_data['driverID']

    json_data = getDriverSummary(driverID, "2017-01-01 00:00:00", "2017-01-02 00:00:00")
    return jsonify(json_data), 200

def getDriverSummary(driverID, startDate, endDate, data_source=DEFAULT_DATA_SOURCE, output_uri=DEFAULT_OUTPUT_URL):
    """
    a) Generate a summary to show the driving behavior of each driver. 
    You are required to display the driving behavior information during the given period in a HTML table.
    The information includes but not limited to the car plate number, the cumulative 
    number of times of overspeed and fatigue driving, the total time of overspeed and neutral slide.

    :param driverID: The requested ID of the driver
    :param startDate: The given start date driving period
    :param endDate: The given end date driving period
    :param data_source: The URI of your food establishment data CSV, such as 's3://DOC-EXAMPLE-BUCKET/food-establishment-data.csv'.
    :param output_uri: The URI where output is written, such as 's3://DOC-EXAMPLE-BUCKET/restaurant_violation_results'.
    """
    with SparkSession.builder.appName("Generate driver summary").getOrCreate() as spark:
        if data_source is not None:
            df = spark.read.format("csv") \
                        .option("header", False) \
                        .schema(schema) \
                        .load(data_source)

        # Create an in-memory DataFrame to query
        df.createOrReplaceTempView("driver_summary")

        distinct_driver_ids = df.select(col('driverID')).distinct()

        # Show the distinct driverID values
        distinct_driver_ids.show()

        # get carPlateNumber
        carPlateNumber_result = spark.sql("""
        SELECT carPlateNumber
            FROM driver_summary
            WHERE driverID = {DID}
        """, DID=driverID)
        carPlateNumber = carPlateNumber_result.first().carPlateNumber

        # get cumulative number of overspeed
        cumulative_overspeed_result = spark.sql("""
        SELECT COUNT(*) AS cumulative_overspeed_count
            FROM driver_summary
            WHERE isOverspeed = 1 AND driverID = {DID} AND Time >= {start} AND Time <= {end}
        """, DID=driverID, start=startDate, end=endDate)
        cumulative_overspeed_count = cumulative_overspeed_result.first().cumulative_overspeed_count

        # get cumulative number of fatigue driving
        cumulative_fatigue_result = spark.sql("""
            SELECT COUNT(*) AS cumulative_fatigue_count
            FROM driver_summary
            WHERE isFatigueDriving = 1 AND driverID = {DID} AND Time >= {start} AND Time <= {end}
        """, DID=driverID, start=startDate, end=endDate)
        cumulative_fatigue_count = cumulative_fatigue_result.first().cumulative_fatigue_count

        # # get total time of overspeed
        total_overspeed_time_result = spark.sql("""
            SELECT SUM(overspeedTime) AS total_overspeed_time
            FROM driver_summary
            WHERE driverID = {DID} AND Time >= {start} AND Time <= {end}
        """, DID=driverID, start=startDate, end=endDate)
        total_overspeed_time = total_overspeed_time_result.first().total_overspeed_time

        # # get total time of neutral slide
        total_neutral_slide_time_result = spark.sql("""
            SELECT SUM(neutralSlideTime) AS total_neutral_slide_time
            FROM driver_summary
            WHERE driverID = {DID} AND Time >= {start} AND Time <= {end}
        """, DID=driverID, start=startDate, end=endDate)
        total_neutral_slide_time = total_neutral_slide_time_result.first().total_neutral_slide_time

        # get cumulative number of hthrottle stop
        cumulative_hthrottle_stop_result = spark.sql("""
            SELECT COUNT(*) AS cumulative_hthrottle_stop_count
            FROM driver_summary
            WHERE isHthrottleStop = 1 AND driverID = {DID} AND Time >= {start} AND Time <= {end}
        """, DID=driverID, start=startDate, end=endDate)
        cumulative_hthrottle_stop_count = cumulative_hthrottle_stop_result.first().cumulative_hthrottle_stop_count

        # get cumulative number of oil leak
        cumulative_oil_leak_result = spark.sql("""
            SELECT COUNT(*) AS cumulative_oil_leak_count
            FROM driver_summary
            WHERE isOilLeak = 1 AND driverID = {DID} AND Time >= {start} AND Time <= {end}
        """, DID=driverID, start=startDate, end=endDate)
        cumulative_oil_leak_count = cumulative_oil_leak_result.first().cumulative_oil_leak_count


        json_data = {
            "driverID": driverID,
            "carPlateNumber": carPlateNumber,
            "cumulative_overspeed_count": cumulative_overspeed_count,
            "cumulative_fatigue_count": cumulative_fatigue_count,
            "total_overspeed_time": total_overspeed_time,
            "total_neutral_slide_time": total_neutral_slide_time,
            "cumulative_hthrottle_stop_count": cumulative_hthrottle_stop_count,
            "cumulative_oil_leak_count": cumulative_oil_leak_count,
            "endDate": endDate
        }
        return json_data

tmp_time = 0
@application.route("/data")
def getdata():
	# global tmp_time
	# if tmp_time > 0 :
	# 	sql = "select ctime,num from Monitor where ctime >%s" %(tmp_time)
	# else:
    #     s = "01/01/2017"
    #     tmp_time = time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple())
	# 	sql = "select ctime,num from Monitor"

	# cur.execute(sql)
    json_data = getDriverSummary("hanhui1000002", "2017-01-01 00:00:00", "2017-01-02 00:00:00")
    tmp_time = json_data['endDate']
    return jsonify(json_data), 200

	# datas = []
	# for i in cur.fetchall():
	# 	datas.append([i[0], i[1]])

	# if len(datas) > 0 :
	# 	tmp_time = datas[-1][0]

	# return json.dumps(datas)

if __name__ == "__main__":
    application.run(port=5000, debug=debugMode, CORS_HEADERS='Content-Type')