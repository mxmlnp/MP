from flask import *
import mysql.connector

DB_NAME='sch688_vvedenie'
DB_USER='sch688_vvedenie'
DB_HOST='185.114.247.43'
DB_PASS="Querty123"


app = Flask(__name__)




@app.route("/reg")
def reg():
    return render_template('reg.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/")
def info():
    return render_template('info.html')

@app.route("/register", methods=['POST'])
def user_reg():
    cnx = mysql.connector.connect(
        host=DB_HOST,
        port=3306,
        user=DB_USER,
        password=DB_PASS)
    cur = cnx.cursor()
    req=request.get_json()
    st = (req['name'], req['email'], req['password'])
    cur.execute("INSERT INTO users (name,email,password) VALUES (%s,%s,%s)")

    row = cur.fetchone()
    cnx.close()
    return "Current date is: {0}".format(row[0])

app.run()




