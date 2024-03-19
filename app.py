# https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-gs.html

import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

from flask import Flask, request, jsonify, send_file

# DEFAULT_DATA_SOURCE = "s3://comp4442project2024spring/detail-records"
# DEFAULT_OUTPUT_URL  = "s3://comp4442project2024spring/result/csv"
DEFAULT_DATA_SOURCE = "./detail-records"
DEFAULT_OUTPUT_URL  = "./result/csv"

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
    return "Hello World!"

@application.route("/getDriverByID", methods=['POST'])
def getDriverByID():
    json_data = request.get_json()
    driverID = json_data['driverID']

    json_data = getDriverSummary(driverID, 0, 10)
    return jsonify(json_data), 200

def getDriverSummary(driverID, startDate, endDate, data_source=DEFAULT_DATA_SOURCE, output_uri=DEFAULT_OUTPUT_URL):
    """
    a) Generate a summary to show the driving behavior of each driver. 
    You are required to display the driving behavior information during the given period in a HTML table.

    :param driverID: The requested id of the driver
    :param period: The given driving period of the driver
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

        # Create a DataFrame of driver_summary
        # top_rapidly_speedup = spark.sql("""SELECT driverID, count(*) 
        #     FROM driver_summary 
        #     WHERE isRapidlySpeedup = '1' and driverID = {DID}
        #     GROUP BY driverID
        #     """, DID=driverID)

        top_rapidly_speedup = spark.sql("""SELECT * 
            FROM driver_summary 
            WHERE isRapidlySpeedup = '1' and driverID = {DID}
            """, DID=driverID)
        
        total_speedup_count = top_rapidly_speedup.collect()
        json_data = {"driverID": driverID, "total_speedup_count": total_speedup_count}
        return json_data

if __name__ == "__main__":
    application.run(port=5000, debug=True)