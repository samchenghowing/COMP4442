# https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-gs.html

import argparse
from os import walk
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

from flask import Flask, request, jsonify, send_file

# DEFAULT_DATA_SOURCE = "s3://comp4442project2024spring/detail-records/detail_record_2017_01_02_08_00_00"
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
    calculate_rapidly_speedup()
    return "Hello World!"

@application.route("/getDriverByID", methods=['POST'])
def getDriverByID():
    json_data = request.get_json()
    driverID = json_data['driverID']
    
    data_source="./detail-records"

    with SparkSession.builder.appName("Calculate rapidly speedup").getOrCreate() as spark:
        if data_source is not None:
            df = spark.read.format("csv") \
                        .option("header", False) \
                        .schema(schema) \
                        .load(data_source)

        # Create an in-memory DataFrame to query
        df.createOrReplaceTempView("rapidly_speedup")

        # Create a DataFrame of the top 10 restaurants with the most Red violations
        top_rapidly_speedup = spark.sql("""SELECT count(*) 
          FROM rapidly_speedup 
          WHERE isRapidlySpeedup = '1' and driverID = {DID}
          """, DID=driverID)
        
        total_speedup_count = top_rapidly_speedup.collect()
        json_data = {"driverID": driverID, "total_speedup_count": total_speedup_count}

    return jsonify(json_data), 200

def calculate_rapidly_speedup(data_source=DEFAULT_DATA_SOURCE, output_uri=DEFAULT_OUTPUT_URL):
    """
    Processes sample food establishment inspection data and queries the data to find the top 10 establishments
    with the most Red violations from 2006 to 2020.

    :param data_source: The URI of your food establishment data CSV, such as 's3://DOC-EXAMPLE-BUCKET/food-establishment-data.csv'.
    :param output_uri: The URI where output is written, such as 's3://DOC-EXAMPLE-BUCKET/restaurant_violation_results'.
    """
    with SparkSession.builder.appName("Calculate rapidly speedup").getOrCreate() as spark:
        # Load the restaurant violation CSV data
        if data_source is not None:
            df = spark.read.format("csv") \
                        .option("header", False) \
                        .schema(schema) \
                        .load(data_source)

        # Create an in-memory DataFrame to query
        df.createOrReplaceTempView("rapidly_speedup")

        # Create a DataFrame of the top 10 restaurants with the most Red violations
        top_rapidly_speedup_drivers = spark.sql("""SELECT driverID, count(*) AS total_rapidly_speedup 
          FROM rapidly_speedup 
          WHERE isRapidlySpeedup = '1' 
          GROUP BY driverID 
          ORDER BY total_rapidly_speedup DESC LIMIT 10""")

        # Write the results to the specified output URI
        top_rapidly_speedup_drivers.write.option("header", "true").mode("overwrite").csv(output_uri)

if __name__ == "__main__":
    application.run(port=5000, debug=True)