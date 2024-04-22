# https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-gs.html

import argparse

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

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

def getDriverSummary(data_source=DEFAULT_DATA_SOURCE, output_uri=DEFAULT_OUTPUT_URL):
    """
    a) Generate a summary to show the driving behavior of each driver. 
    You are required to display the driving behavior information during the given period in a HTML table.
    The information includes but not limited to the car plate number, the cumulative 
    number of times of overspeed and fatigue driving, the total time of overspeed and neutral slide.

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

        cumulative_result = spark.sql("""
            SELECT driverID, carPlateNumber, 
                SUM(isOverspeed) AS cumulative_overspeed_count,
                SUM(isFatigueDriving) AS cumulative_fatigue_count,
                SUM(overspeedTime) AS total_overspeed_time,
                SUM(neutralSlideTime) AS total_neutral_slide_time,
                SUM(isHthrottleStop) AS cumulative_hthrottle_stop_count,
                SUM(isOilLeak) AS cumulative_oil_leak_count
            FROM driver_summary
            GROUP BY driverID, carPlateNumber
        """)
        cumulative_result.write.option("header", "true").mode("overwrite").csv(output_uri)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--data_source', help="The URI for you CSV restaurant data, like an S3 bucket location.")
    parser.add_argument(
        '--output_uri', help="The URI where output is saved, like an S3 bucket location.")
    args = parser.parse_args()

    getDriverSummary(args.data_source, args.output_uri)
