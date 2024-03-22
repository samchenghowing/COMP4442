# https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-gs.html

import argparse
import datetime, time 
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

from flask import Flask, request, jsonify, send_file

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

application = Flask(__name__)

@application.route("/")
def index():
    return "Your Flask App Works!"

@application.route("/hello")
def hello():
    # testing
    json_data = getDriverSummary("hanhui1000002", "2017-01-01 00:00:00", "2017-01-02 00:00:00")
    return jsonify(json_data), 200

@application.route("/getDriverByID", methods=['POST'])
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
            "cumulative_oil_leak_count": cumulative_oil_leak_count
        }
        return json_data

if __name__ == "__main__":
    application.run(port=5000, debug=debugMode)