import requests
from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()

@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    if username == "":
        error = "Please enter username"
        return render_template('login.html', error=error)
    password = request.form.get('password')
    if password == "":
        error = "Please enter password"
        return render_template('login.html', error=error)
    cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
    records = list(cursor.fetchall())
    if (len(records) == 0):
        error = "Incorrect login/password"
        return render_template('login.html', error=error)
    return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])

if __name__ == '__main__':
    app.run()
