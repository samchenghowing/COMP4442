from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

import csv, json, os
import datetime, time 

debugMode = True
if debugMode:
    DEFAULT_DATA_SOURCE = "./detail-records"
    DEFAULT_OUTPUT_URL  = "./result/csv"
else:
    DEFAULT_DATA_SOURCE = "s3://comp4442sparkapp/detail-records"
    DEFAULT_OUTPUT_URL  = "s3://comp4442sparkapp/result/csv"

application = Flask(__name__)
CORS(application) # for frontend

@application.route("/")
def index():
    return "Welcome to the backend of COMP4442 Project! <br> \
            Please access the frontend at this URL: \
            "

@application.route("/getDriverSummary", methods=['POST', 'GET'])
def getDriverSummary():
    for root,dirs,files in os.walk(DEFAULT_OUTPUT_URL):
        for file in files:
            if file.endswith(".csv"):
                csv_path = os.path.join(DEFAULT_OUTPUT_URL, file)
                csv_file = csv.DictReader(open(csv_path, 'r', encoding="utf8"))

    # Created a list and adds the rows to the list
    json_list = []
    for row in csv_file:
        json_list.append(row)

    return json.dumps(json_list), 200

@application.route("/getDriverSpeed")
def getDriverSpeed():
    json_data = request.get_json()
    startTime = json_data['startTime']
    endTime = json_data['endTime']

    # return every driver's speed and isOverspeed at the time period
    # Use spark in beanstalk??
    
	# sql = "select ctime,num from Monitor"
	# cur.execute(sql)
	# datas = []
	# for i in cur.fetchall():
	# 	datas.append([i[0], i[1]])
	# if len(datas) > 0 :
	# 	tmp_time = datas[-1][0]
	# return json.dumps(datas)
 
    return jsonify(json_data), 200

if __name__ == "__main__":
    application.run(port=5000, debug=True)