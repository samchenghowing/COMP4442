from flask import Flask, request, jsonify, render_template
import csv, json, os
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

@application.route("/")
def index():
    return "Welcome to the backend of COMP4442 Project! <br> \
            Please access the frontend at this URL: \
            "

@application.route("/getDriverSummary")
def getDriverSummary():
    for root,dirs,files in os.walk(DEFAULT_OUTPUT_URL):
        for file in files:
            if file.endswith(".csv"):
                csv_file = csv.DictReader(open(file, 'r'))

    # Created a list and adds the rows to the list
    json_list = []
    for row in csv_file:
        json_list.append(row)

    return json.dumps(json_list), 200

tmp_time = 0
@application.route("/data")
def getdata():
    json_data = request.get_json()
    time = json_data['time']

	# global tmp_time
	# if tmp_time > 0 :
	# 	sql = "select ctime,num from Monitor where ctime >%s" %(tmp_time)
	# else:
    #     s = "01/01/2017"
    #     tmp_time = time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple())
	# 	sql = "select ctime,num from Monitor"

	# cur.execute(sql)
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