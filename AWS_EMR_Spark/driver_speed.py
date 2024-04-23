# https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-gs.html

import argparse

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

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

def getDriverSpeed(data_source, output_uri, start_time, end_time):
    """
    b) Generate a summary to show the driving speed of each driver of the given period. 

    :param data_source: The URI of your food establishment data CSV, such as 's3://DOC-EXAMPLE-BUCKET/food-establishment-data.csv'.
    :param output_uri: The URI where output is written, such as 's3://DOC-EXAMPLE-BUCKET/restaurant_violation_results'.
    :param start_time: The start time requsted, such as '2017-01-01 00:00:00'
    :param end_time: The end time requsted, such as '2017-01-07 00:00:00'
    """
    with SparkSession.builder.appName("Generate driver speed").getOrCreate() as spark:
        if data_source is not None:
            df = spark.read.format("csv") \
                        .option("header", False) \
                        .schema(schema) \
                        .load(data_source)

        # Create an in-memory DataFrame to query
        df.createOrReplaceTempView("driver_speed")

        cumulative_result = spark.sql("""
            SELECT driverID, carPlateNumber, 
                isOverspeed, Speed, Time
            FROM driver_speed
            WHERE Time >= {start} AND Time <= {end}
        """, start=start_time, end=end_time)

        cumulative_result.write.option("header", "true").mode("overwrite").csv(output_uri)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--data_source', help="The URI for you CSV restaurant data, like an S3 bucket location.")
    parser.add_argument(
        '--output_uri', help="The URI where output is saved, like an S3 bucket location.")
    parser.add_argument(
        '--start_time', help="The start time requsted, like '2017-01-01 00:00:00'.")
    parser.add_argument(
        '--end_time', help="The end time requsted, like '2017-01-07 00:00:00'.")
    args = parser.parse_args()

    getDriverSpeed(args.data_source, args.output_uri, args.start_time, args.end_time)
