import json
from datetime import datetime, timedelta
from flask import Flask,request,jsonify, session
from flask_cors import CORS, cross_origin
from flask_socketio import emit, join_room, leave_room, SocketIO
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Client IPDict
IPDict = {}

app = Flask(__name__)
cors = CORS(app)
app.config.update(DEBUG=True, CORS_HEADERS='Content-Type')
socketio = SocketIO(app, cors_allowed_origins="*", engineio_logger=True)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    return conn

def checkpassword(name, password):
    conn = get_db_connection()
    sql_select_query = """select * from users where name = ?"""
    user = conn.execute(sql_select_query, (name,)).fetchone()
    conn.close()

    if user is None:
        json_data = {"isvalid":False,"from client": request.remote_addr,
                        "attempt count": IPDict[request.remote_addr][0],
                        "status": "User not exist in database!"}
        return json_data

    hashedpw = user.get('pwHash')
    if check_password_hash(hashedpw, password):
        # update the format of hash before send to client
        user["pwHash"] = password
        IPDict[request.remote_addr].append(user.get('id'))
        json_data = {"isvalid":True, "from client": request.remote_addr,
                    "attempt count": IPDict[request.remote_addr][0], "User info": user}
        return json_data
    else:
        json_data = {"isvalid":False, "from client": request.remote_addr,
                    "attempt count": IPDict[request.remote_addr][0], "status": "password not match"}
        return json_data

# This route is for testing use only.
@app.route("/")
def main():
    return "Wellcome to COMP3334 Backend!" 

# This route is for testing use only.
@app.route('/api/users')
@cross_origin()
def get_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return users, 200

@app.route('/api/signup', methods=['POST'])
@cross_origin()
def signup():
    json_data = request.get_json()
    name = json_data['name']
    password = json_data['pwHash']

    # check if user exist in database
    conn = get_db_connection()
    sql_select_query = """select * from users where name = ?"""
    res = conn.execute(sql_select_query, (name,)).fetchone()
    if res is not None:
        json_data = {"signup":False, "status": "User alreafy exist in database!"}
        return jsonify(json_data), 200

    # TO-DO: email verify

    hash = generate_password_hash(password)
    conn.execute("INSERT INTO users (name, pwHash, confirmed) VALUES (?, ?, ?)",
                (name, hash, 0)
                )
    
    conn.commit()
    conn.close()

    json_data = {"signup":True}
    return jsonify(json_data), 200

@app.route('/api/login', methods=['POST'])
@cross_origin()
def login():

    # check if brute force trying password to login
    if request.remote_addr not in IPDict:
        IPDict[request.remote_addr] = [0, datetime.now()]
    else:
        # reset the count to unblock user after 5 minutes
        if datetime.now() - IPDict[request.remote_addr][1] > timedelta(minutes=5):
            IPDict[request.remote_addr] = [0, datetime.now()]

        if IPDict[request.remote_addr][0] == 5:
            json_data = {"isvalid":False, "from client": request.remote_addr, 
                          "attempt count": IPDict[request.remote_addr][0], 
                          "status": "This IP is blocked 5 minutes since too many\
                                    failed login attempts"}
            return jsonify(json_data), 200
        IPDict[request.remote_addr][0] = IPDict[request.remote_addr][0] + 1

    json_data = request.get_json()
    name = json_data['name']
    password = json_data['pwHash']

    json_data = checkpassword(name, password)
    return jsonify(json_data), 200

    # check if brute force trying password to login
    if request.remote_addr not in IPDict:
        IPDict[request.remote_addr] = [0, datetime.now()]
    else:
        # reset the count to unblock user after 5 minutes
        if datetime.now() - IPDict[request.remote_addr][1] > timedelta(minutes=5):
            IPDict[request.remote_addr] = [0, datetime.now()]

        if IPDict[request.remote_addr][0] == 5:
            json_data = {
                "isvalid":False, "from client": request.remote_addr, 
                "attempt count": IPDict[request.remote_addr][0], 
                "status": "This IP is blocked 5 minutes since too many\
                    failed login attempts"}
            return jsonify(json_data), 200
        IPDict[request.remote_addr][0] = IPDict[request.remote_addr][0] + 1

    json_data = request.get_json()

    json_response = checkpassword(json_data['name'], json_data['pwHash'])
    return json_response, 200

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    data_dict = json.loads(message["msg"])
    room = int(data_dict["room"])
    join_room(room)
    emit('status', {'msg': data_dict["name"] + ' has entered the room.'}, room=room)

@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    data_dict = json.loads(message["msg"])
    room = int(data_dict["room"])
    emit('message', {'msg': message}, room=room)

@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    data_dict = json.loads(message["msg"])
    room = int(data_dict["room"])
    leave_room(room)
    emit('status', {'msg': data_dict["name"] + ' has left the room.'}, room=room)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
