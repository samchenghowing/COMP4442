# https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-gs.html

import argparse
from os import walk
from pyspark.sql import SparkSession

from flask import Flask, request, jsonify, send_file

# DEFAULT_DATA_SOURCE = "s3://comp4442project2024spring/detail-records/detail_record_2017_01_02_08_00_00"
# DEFAULT_OUTPUT_URL  = "s3://comp4442project2024spring/result/csv"
DEFAULT_DATA_SOURCE = "./detail-records/detail_record_2017_01_02_08_00_00"
DEFAULT_OUTPUT_URL  = "./result/csv"

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
    
    data_source="./detail-records/detail_record_2017_01_02_08_00_00"

    with SparkSession.builder.appName("Calculate rapidly speedup").getOrCreate() as spark:
        # Load the restaurant violation CSV data
        if data_source is not None:
            df = spark.read \
                    .csv(data_source, inferSchema=True) \
                    .toDF("driverID","carPlateNumber","Latitude","Longtitude","Speed","Direction","siteName","Time", \
                          "isRapidlySpeedup","isRapidlySlowdown","isNeutralSlide","isNeutralSlideFinished","neutralSlideTime", \
                            "isOverspeed","isOverspeedFinished","isOverspeedFinished","overspeedTime","isFatigueDriving","isHthrottleStop","isOilLeak")

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
            df = spark.read \
                    .csv(data_source, inferSchema=True) \
                    .toDF("driverID","carPlateNumber","Latitude","Longtitude","Speed","Direction","siteName","Time", \
                          "isRapidlySpeedup","isRapidlySlowdown","isNeutralSlide","isNeutralSlideFinished","neutralSlideTime", \
                            "isOverspeed","isOverspeedFinished","isOverspeedFinished","overspeedTime","isFatigueDriving","isHthrottleStop","isOilLeak")

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