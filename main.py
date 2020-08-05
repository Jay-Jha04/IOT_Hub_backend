# from flask import Flask, jsonify, request, render_template, flash
# import datetime
# from flask_mysqldb import MySQL
# from datetime import datetime
# from flask_cors import CORS
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
# from flask_jwt_extended import (create_access_token)
# from flask_sqlalchemy import SQLAlchemy
# import pyodbc 


# #app = Flask(__name__)

# #app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://JAYJHA/iot'


# # print("Hello***************************")

# # app.config['MYSQL_HOST'] = 'localhost'
# # app.config['MYSQL_USER'] = 'root'
# # app.config['MYSQL_PASSWORD'] = 'root123'
# # app.config['MYSQL_DB'] = 'iot'
# # app.config['SECRET_KEY'] = 'secret'
# # app.config['JWT_SECRET_KEY'] = 'secretkey'



# conn = pyodbc.connect('Driver={SQL Server};'
#                       'Server=JAYJHA;'
#                       'Database=iot;'
#                       'Trusted_Connection=yes;')


# print("After connection************************")
# # mysql = MySQL(app)
# #db = SQLAlchemy(app)
# #bcrypt = Bcrypt(app)
# #jwt = JWTManager(app)

# CORS(app)

# @app.route('/userlogin', methods = ['POST'])
# def userlogin():
#     print("Enter in function******************")
#     cursor = conn.cursor()
#     email =request.get_json()["Username"]
#     password = request.get_json()["Password"]
#     print("email :***************"+ email)
#     #result = ""
#     cursor.execute("Select * from users where email = '" + str(email) + "' and password = '" + str(password) + "'")
#     rv=cursor.fetchone()
#     print(rv)
#     #access_token = create_access_token(identity=email)
#     # #print(cursor)
#     # if rv == None:
#     #     result = jsonify({"error":"Invalid Username or Password"})
#     #     #print(result)
#     # else:
#     #     access_token = create_access_token(email)
#     #result = jsonify({"token":access_token})
#     #return result

# # @app.route('/adminlogin', methods = ['POST'])
# # def adminlogin():
# #     cur = mysql.connection.cursor()
# #     email =request.get_json()['email']
# #     password = request.get_json()['password']
# #     result = ""
# #     cur.execute("Select * from users where email = '" + str(email) + "' and password = '" + str(password) + "'")
# #     rv=cur.fetchone()
# #     if rv == None:
# #         result = jsonify({"error":"Invalid Username or Password"})
# #     else:
# #         access_token = create_access_token(identity = rv[2])
# #         result = jsonify({"token":access_token})

# #     return result


# # @app.route('/userhome', methods = ['POST'])
# # @jwt_required
# # def userhome():
# #     no_of_things = request.get_json()['no_of_things']
# #     if(no_of_things == None):
# #         return jsonify({"error":"Please enter some value"})
# #     else:
# #         user = get_jwt_identity()
# #         #session = db.session()
# #         #cur = session.execute(sql).cursor
# #         #cur = db.session.cursor()
# #         create_time = datetime.now()
# #         cur.execute("UPDATE users SET no_of_things = '" + str(no_of_things) + "', create_time = '" + str(create_time) + "' WHERE email = '" + str(user) + "'")
# #         db.session.commit()
# #         result = {
# #             'no_of _things':no_of_things,
# #             'create_time':create_time
# #             }
# #         return jsonify({'result':result})
    


# if __name__ == "__main__":
#     app.run(debug=True)

