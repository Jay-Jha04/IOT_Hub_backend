from provisioning_handler import ProvisioningHandler
from config_loader import Config
from pyfiglet import Figlet
from provisioning_handler import *
import os

from flask import Flask, jsonify, request, render_template, flash
import datetime
from datetime import datetime
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_jwt_extended import (create_access_token)
from flask_api import status
import pyodbc 

from os import scandir

import glob


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
        cur.execute("Insert into Things values ('"+str(user)+"','"+str(no_of_things)+"','pending')")
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

######### Provisioning certificate #####################

#Set Config path
CONFIG_PATH = 'config.ini'

config = Config(CONFIG_PATH)
config_parameters = config.get_section('SETTINGS')
secure_cert_path = config_parameters['SECURE_CERT_PATH']
bootstrap_cert = config_parameters['CLAIM_CERT']


def callback(payload):
    print(payload)

card = ""
@app.route('/provisioning-cert',methods=['POST'])
def run_provisioning(isRotation=False):
    
    provisioner = ProvisioningHandler(CONFIG_PATH)

    if isRotation:
        provisioner.get_official_certs(callback, isRotation=True)  
    else:
        #Check for availability of bootstrap cert 
        try:
             with open("{}/{}".format(secure_cert_path, bootstrap_cert)):
                # Call super-method to perform aquisition/activation
                # of certs, creation of thing, etc. Returns general
                # purpose callback at this point.
                # Instantiate provisioning handler, pass in path to config
                provisioner.get_official_certs(callback)
                card = request.get_json(['email'])
                search_dir = "C:/Users/jayjha/Desktop/BackendIoT/aws-iot-fleet-provisioning-master/certs"
 
                files = list(filter(os.path.isfile, glob.glob(search_dir + "/*.key")))
                files.sort(key=lambda x: os.path.getmtime(x))

                certi = list(filter(os.path.isfile, glob.glob(search_dir + "/*.crt")))
                certi.sort(key=lambda x: os.path.getmtime(x))

                   
                value = int(card['no_of_things'])
                val = int(card['no_of_things'])


                while val!=0:
                    p = files[-val]
                    c = certi[-val]
                    val-=1
                    
                    cur = cnxn.cursor()  
                    email = card['user']
                    no_of_things=card['no_of_things']
                    insert_stmt = (
                    "Insert into certificate_table(priv_key,cert_crt,Username) values (?,?,?)"
                    # "INSERT INTO  certificate_table(user_Input,priv_key,cert_crt) "
                    # "VALUES (%s,%s,%s) where email = '" + str(email) + "' and no_of_things = '" + str(no_of_things) + "'"
                    )

                    
                    data = (p, c,email)
                    print("iiiiiiiiiiiiiiiiiiii")
                    print(data)
                    
                    cur.execute(insert_stmt, data)
                    
                    cur.execute("UPDATE Things SET status = 'complete' WHERE Username = '" + str(email) + "'")

                    cnxn.commit()

             return jsonify({'status':"complete"}), status.HTTP_200_OK

        except IOError:
            print("### Bootstrap cert non-existent. Official cert may already be in place.")


app.run()

