from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)


# MySQL connection configuration
config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'ticket_db'
}

# Create a MySQL connection object
conn = mysql.connector.connect(**config)


#Admin routes

@app.route('/admin')
def admin():
    return render_template('admin/admin.html')

@app.route('/')
def home():
    return render_template('home.html')

#Regist new customer route

@app.route('/regist', methods=['GET', 'POST'])
def regist():
    username = request.form.get('username')
    names = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')
    cursor = conn.cursor()

    sql = "INSERT INTO `customer` (`username`, `names`, `email`, `phone`, `address`, `password`, `confirm_password`) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    value = (username, names, email, phone, address, password, confirm_password)
    cursor.execute(sql, value)
    conn.commit()
    return render_template('home.html', success = 'User has created successful.')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/eventDetails')
def eventDetails():
    return render_template('eventDetails.html')

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/setting')
def setting():
    return (render_template('admin/admin-setting.html'))

@app.route('/booking')
def booking():
    return (render_template('admin/admin-booking.html'))

#Route to retrieve events from database to admin page
@app.route('/ad-events')
def listEvents():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()
    cursor.close()
    return (render_template('admin/ad-events.html', rows=rows))

#Route to retrieve customer from database to admin page
@app.route('/customers')
def retrieveCustomer():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer")
    rows = cursor.fetchall()
    cursor.close()
    return (render_template('admin/admin-customers.html', rows=rows))


@app.route('/createevent')
def createEvent():
    return (render_template('admin/createevent.html'))

@app.route('/editevent')
def editevent():
    return (render_template('admin/editevent.html'))

@app.route('/searchevent')
def searchevent():
    return (render_template('admin/ticket-purchase/searchevent.html'))

@app.route('/purchaseticket')
def purchaseTicket():
    return (render_template('admin/ticket-purchase/purchase-ticket.html'))

#route to add an event to database
@app.route('/addEvent', methods=['GET', 'POST'])
def store():
    name = request.form.get('name')
    date = request.form.get('date')
    time = request.form.get('time')
    location = request.form.get('location')
    ticket_price = request.form.get('ticket_price')

     # Create a cursor object
    cursor = conn.cursor()

    sql = "INSERT INTO `events` (`name`, `date`, `time`, `location`, `ticket_price`) VALUES(%s, %s, %s, %s, %s)"
    value = (name, date, time, location, ticket_price)
    cursor.execute(sql, value)
    conn.commit()
    return render_template('admin/createevent.html', success = 'Event created successfully !')
 

 #Users routes

@app.route('/userDashboard')
def userDashboard():
    return (render_template('user/userDashboard.html'))

@app.route('/allevents')
def allevents():
    # Create a cursor object to execute MySQL queries
    cursor = conn.cursor()
    # Execute the query to select all users from the users table
    cursor.execute("SELECT * FROM events")
    # Fetch all rows of the query result
    rows = cursor.fetchall()
    # Close the cursor
    cursor.close()
    return (render_template('user/allevents.html', rows=rows ))

@app.route('/userbooking')
def userbooking():
    return (render_template('user/booking.html'))

#retrieve users to user dashboard
@app.route('/userprofile')
def userProfile():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer")
    rows = cursor.fetchall()
    cursor.close()
    return (render_template('user/profile.html', rows=rows))

#view single record
@app.route('/viewEvent/<event_id>')
def viewEvent(event_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE event_id = %s", (event_id,))
    data = cursor.fetchall()[0]
    cursor.close()
    return (render_template('user/viewEvent.html', data=data))

@app.route('//userlogout')
def userLogout():
    return (render_template('user/userlogout.html'))

if __name__ == "__main__":
    app.run(debug=True)