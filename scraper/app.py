from flask import Flask, render_template, request, redirect, url_for, session,flash
import re
import mysql.connector
from mysql.connector import errorcode
import os
from configparser import ConfigParser
from werkzeug.utils import secure_filename
import datetime
import requests
import json
from functools import wraps



def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if  session.get('loggedin')==True:
            return f(*args, **kwargs)
        else:
            # flash("You need to login first")
            return redirect(url_for('login'))

    return wrap
# Replace the deviceToken key with the device Token for which you want to send push notification.
# Replace serverToken key with your serverKey from Firebase Console

now = datetime.datetime.utcnow()

ALLOWED_EXTENSIONS = {'glb'}
  
configur = ConfigParser(interpolation=None)
print (configur.read('config.ini'))
  
app = Flask(__name__)
UPLOAD_FOLDER = configur.get("Upload","path")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your secret key'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

MYSQL_HOST = configur.get("Database","servername")
MYSQL_USER = configur.get("Database","username")
MYSQL_PASSWORD = configur.get("Database","password")
MYSQL_DB = configur.get("Database","database")

FCM_TOKEN = configur.get("FCMToken","token")


def connect_db():
    cnx = mysql.connector.connect(
        user=MYSQL_USER, 
        password=MYSQL_PASSWORD,
        host=MYSQL_HOST,
        database=MYSQL_DB
    )

    print("Database connected")

    return cnx

cnx = connect_db()
def send_push_notification(device_token):
    serverToken = FCM_TOKEN
    deviceToken = device_token

    headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key=' + serverToken,
        }

    body = {
            'notification': {'title': '3D Model is ready',
                                'body': '3D Model is uploaded'
                                },
            'to':
                deviceToken,
            'priority': 'high',
            #   'data': dataPayLoad,
            }
    response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
    print(response.status_code)

    print(response.json())

    return 1

# get data to populate table
def get_table_data():
    query = '''SELECT vid.ID as file_id
                ,vid.title
                ,vid.FileUrl as file_url
                ,vid.FileSize as file_size
                ,vid.CreatedAt as video_upload_date
                ,concat(usr.FirstName,' ',usr.LastName) as name
                ,IFNULL(d.filepath,'No') as 'model_path' 
                ,d.uploaddate as model_upload_date
                ,acc.username as model_uploaded_by
                FROM mabelvideo as vid 
                LEFT JOIN usersmaster as usr on usr.ID=vid.UserId 
                LEFT JOIN uploaded_3d_model as d on vid.ID=d.fileid
                LEFT JOIN accounts as acc on d.uploadby=acc.id
                order by video_upload_date desc
                '''

    global cnx
    if not cnx.is_connected():
        cnx = connect_db()
    else :
        pass
    cursor_get = cnx.cursor(dictionary=True)
    cursor_get.execute(query)
    result = cursor_get.fetchall()
    return result

#update table when model is uploaded and send push notification to user
def update_model_details(id,path):
    global cnx
    now = datetime.datetime.utcnow()
    if not cnx.is_connected():
        cnx = connect_db()
    else :
        pass
    cursor_insert = cnx.cursor()
    cursor_delete=  cnx.cursor()
    delete_query=f"DELETE FROM uploaded_3d_model where fileid={id};"
    cursor_delete.execute (delete_query)
    cnx.commit()
    insert_query=f"INSERT INTO  uploaded_3d_model(fileid,filepath,uploaddate,uploadby) values({id},'{path}','{now.strftime('%Y-%m-%d %H:%M:%S')}',{int(session['id'])});"
    cursor_insert.execute (insert_query)
    cnx.commit()

    cursor_get = cnx.cursor(buffered=True)
    query=f"select DISTINCT n.DeviceToken from mabelvideo as m inner join user_notification as n on m.UserId=n.UserId Where n.IsActive=1 and n.DeviceToken is not null and m.ID={id} "
    cursor_get.execute(query)
    if cursor_get.rowcount>0:
        results=cursor_get.fetchone()
        print(results)
        for row in results:
            flash('Model Upload Notification sent to User')
            send_push_notification(row[0])
    else:
            flash('No Device Token found for user')


@app.route('/')
@login_required
def index():
    return redirect(url_for('login'))


@app.route('/table')
@login_required
def table():
    data=get_table_data()
    # print(data)
    return render_template('index.html',data=data)

@app.route('/login', methods =['GET', 'POST'])
def login():
    global cnx
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        if not cnx.is_connected():
            cnx = connect_db()
        else :
            pass
        cursor = cnx.cursor(dictionary=True)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return redirect(url_for('table'))
            # return render_template('index.html', data=get_table_data())
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/upload', methods =['POST'])
@login_required
def upload():
 if request.method == 'POST':
    f = request.files['file']
    id = request.form.get('id')
    print(id)
    path=os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
    print(path)
    f.save( path)
    update_model_details(id,path)
    flash('Model Uploaded Sucessfully!')
    return redirect(url_for('table'))

@app.route('/register', methods =['GET', 'POST'])
def register():
    global cnx
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if not cnx.is_connected():
            cnx = connect_db()
        else :
            pass
        cursor = cnx.cursor(dictionary=True)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

if __name__=='__main__':
    app.run(
        host='0.0.0.0', port=5000,debug=True
        )
