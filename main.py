from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

connection = mysql.connector.connect(
 host='localhost',
    port='3306',
    database='ticket_booking_db',
    user='root',
    password=''
)
cursor = connection.cursor()
app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
        record = cursor.fetchall()
        if record:
            session['loggedin'] = True
            session['username'] = username
            return redirect(url_for('admin'))
        else:
            msg = 'Invalid credentials'
    return render_template('login.html', msg = msg)

@app.route('/admin')
def admin():
    return render_template('admin.html', username = session['username'])

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/eventDetails')
def eventDetails():
    return render_template('eventDetails.html')

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/regist')
def regist():
    return (render_template('regist.html'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

app.run(host='localhost', port=5000)

app = Flask(__name__)
app.debug = True
