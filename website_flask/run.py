from flask import Flask, redirect, render_template, request
import pyodbc
from flask import send_from_directory, send_file
import os


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login/", methods=["GET", "POST"], strict_slashes=False)
def login_page():
    username = request.form['username']
    password = request.form['password']
    server = 'test.database.windows.net'
    database = 'test'
    driver= '{ODBC Driver 18 for SQL Server}'

    data={}

    try:
        with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
            data["success"]='true' 
    except:
        data["success"]='false'
    
    return data


@app.route("/enter", methods=["GET", "POST"])
def entra():
    password = 'mysupersecretpassword'
    username = 'adminoftheservice'
    server = 'test.database.windows.net'
    database = 'test'
    driver= '{ODBC Driver 18 for SQL Server}'

    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            query = "SELECT name, email FROM users"
            cursor.execute(query)
            myresult = cursor.fetchall()
        
            users=[list(x) for x in myresult]

            titles=['name','email']

            return render_template('home.html', titles=titles, users=users, len = len(users))


@app.route("/search", methods=["GET", "POST"])
def search():
    user = request.form['username']
    password = 'mysupersecretpassword'
    username = 'adminoftheservice'
    server = 'test.database.windows.net'
    database = 'test'
    driver= '{ODBC Driver 18 for SQL Server}'

    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            query = "SELECT name, email FROM users WHERE name='"+user+"'"
            cursor.execute(query)
            myresult = cursor.fetchall()
            users=[list(x) for x in myresult]
            titles=['name','email']

            return render_template('home.html', titles=titles, users=users, len = len(users))

@app.route("/upload", methods=["GET", "POST"])
def upload():
    from azure.storage.blob import BlobClient
    from azure.identity import DefaultAzureCredential

    blob_client = BlobClient(
        account_url='https://test.blob.core.windows.net',
        container_name='test',
        blob_name= 'eicar.txt',
        credential='sp=racwdli&st=2021-06-05T14:51:22Z&se=2023-07-03T22:51:22Z&sip=1.2.3.4-255.255.255.255&sv=2022-11-02&sr=c&sig=eeAlcJ4Y4RB1ioQOejBk6JOohn%2BBy4cAIrjbDWvkidw%4D'
    )

    upload_return = blob_client.upload_blob(data=b"X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*", 
                                            overwrite=True)

    password = 'mysupersecretpassword'
    username = 'adminoftheservice'
    server = 'test.database.windows.net'
    database = 'test'
    driver= '{ODBC Driver 18 for SQL Server}'

    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            query = "SELECT name, email FROM users"
            cursor.execute(query)
            myresult = cursor.fetchall()
        
            users=[list(x) for x in myresult]

            titles=['name','email']

            return render_template('home.html', titles=titles, users=users, len = len(users), user1 = "user1")


@app.route('/download_file')
def download_file():
    # Returning file from appended path
    return send_file('static/files/info.txt', as_attachment=True)



@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run()
