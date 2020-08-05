from flask import Flask, jsonify, request, render_template, flash
import datetime
from datetime import datetime
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_jwt_extended import (create_access_token)
from flask_api import status
import pyodbc 


app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'secret'
app.config['JWT_SECRET_KEY'] = 'secretkey'

CORS(app)

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=JAYJHA;DATABASE=iot;UID=;PWD=')

jwt = JWTManager(app)

@app.route('/userlogin', methods = ['POST'])
def userlogin():
    email =request.get_json()["Username"]
    password = request.get_json()["Password"]

    cursor = cnxn.cursor()
    cursor.execute("Select * from users where email = '" + str(email) + "' and password = '" + str(password) + "'")
    row = cursor.fetchone()
    if row == None:
        return jsonify({"error":"Invalid Username or Password"}), status.HTTP_403_FORBIDDEN
    else:
        access_token = create_access_token(email)
        return jsonify({"token":access_token}), status.HTTP_200_OK
    

@app.route('/userhome', methods = ['POST'])
def userhome():
    card = request.get_json(['email'])
    print(card['email'])
    if(card == None):
        return jsonify({"error":"Please enter some value"}), status.HTTP_406_NOT_ACCEPTABLE
    else:
        user = card['email']
        no_of_things=card['Things']
        cur = cnxn.cursor()
        #create_time = datetime.now()
        cur.execute("Insert into Things values ('"+str(user)+"','"+str(no_of_things)+"','"+user+"')")
        cnxn.commit()
        result = {
            'no_of _things':no_of_things,
            }
        return jsonify({'result':result}), status.HTTP_200_OK


@app.route('/adminhome', methods = ['GET'])
def adminhome():
    cur = cnxn.cursor()
    result = cur.execute("Select * from Things")
    rows = result.fetchall()
    data = []
    for row in rows:
        data.append(list(row))
    
    return jsonify({'result':data}), status.HTTP_200_OK


