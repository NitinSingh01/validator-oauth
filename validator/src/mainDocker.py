import mysql.connector
import os
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = '1'
from flask import jsonify
from flask import Flask, request, redirect, url_for
from flask_cors import CORS
from flask import Flask, render_template, make_response
from flask_dance.contrib.github import make_github_blueprint, github
import config
app = Flask(__name__)
app.config["SECRET_KEY"]="SECRET KEY"
github_blueprint = make_github_blueprint(client_id='KEY GOES HERE',
                                         client_secret='KEY GOES HERE ')
app.register_blueprint(github_blueprint, url_prefix='/github_login')

CORS(app)
cors = CORS(app,resources={
		r"/*": {
			"origins": "*"
		}
})

@app.route('/', methods=["GET"])
def homepage():
    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        return "Successful authentication"

@app.route('/callback', methods=["GET"])
def callback():
    return "Something went wrong"
	

    
@app.route('/users',methods=['GET'])
def users():
    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
	
        db_connection = mysql.connector.connect(
        host="mysql1",
        user="sa",
        passwd="password",
        database="UID"
        )
        my_database = db_connection.cursor()
        sql_statement = "SELECT * FROM UID"
        my_database.execute(sql_statement)
        output = my_database.fetchall()
        resp = jsonify(output)
        return resp
		
@app.route('/users', methods=['POST'])
def add_user():
    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        _json = request.json
        _firstname = _json['FirstName']
        _lastname = _json['LastName']
        _email = _json['Email']
        _uid = _json['UID']
        sql = "INSERT INTO UID(UID, FirstName, LastName) VALUES(%s, %s, %s)"
        data = (_uid, _firstname, _lastname)
        db_connection = mysql.connector.connect(
        host="mysql1",
        user="sa",
        passwd="password",
        database="UID"
        )
        conn = db_connection.cursor()
        conn.execute(sql, data)
        db_connection.commit()
        url = 'https://us-central1-studious-lyceum-284904.cloudfunctions.net/function-2'
        myobj = {"topic":"Crt","message":{
        "receiver_email":_email,
        "subject":"Successful Sintval Registration",
        "message":_firstname +" " + _lastname+ ", you have been successfully registered."}}
        x = requests.post(url, data = myobj)
        return "Record Inserted"
	
@app.route('/validate', methods=['POST'])
def validate_user():
    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        _json = request.json
        _firstname = _json['FirstName']
        _lastname = _json['LastName']
        _uid = _json['UID']
        db_connection = mysql.connector.connect(
        host="mysql1",
        user="sa",
        passwd="password",
        database="UID"
        )
        conn = db_connection.cursor()
        sql = "SELECT * FROM UID WHERE UID=%s And FirstName=%s And LastName=%s"
        data = (_uid,_firstname,_lastname)
        conn.execute(sql,data)
        row = conn.fetchone()
        if row is None:
            return jsonify("UID not found. Please try again !")
        else: 
            return jsonify("Validation Successful")
	
	
		
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG_MODE)
