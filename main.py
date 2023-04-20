from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'my_secret_key'


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
    if 'username' in session:
        # Display the logged-in user on the dashboard
        return render_template('user/userDashboard.html', username=session['username'])
    else:
        # If the user isn't logged in, redirect them to the login page
        return (render_template('home.html'))


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
def dashboard():
    if 'username' in session:
        # Retrieve the logged-in user from the session
        username = session['username']

        # Connect to the MySQL database
        cnx = mysql.connector.connect(user='root', password='',
                                      host='localhost', database='ticket_db')
        cursor = conn.cursor()

        # Execute a query to retrieve the required fields for the logged-in user
        query = "SELECT username, names, email, phone, address FROM customer WHERE username = %s"
        cursor.execute(query, (username,))
        records = cursor.fetchall()

        # Close the cursor and database connection
        cursor.close()
        cnx.close()

        # Pass the records to the template
        return render_template('user/profile.html', username=username, records=records)
    else:
        # If the user isn't logged in, redirect them to the login page
        return redirect('/')

#view single record
@app.route('/viewEvent/<event_id>')
def viewEvent(event_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE event_id = %s", (event_id,))
    data = cursor.fetchall()[0]
    cursor.close()
    return (render_template('user/viewEvent.html', data=data))

#view single customers
@app.route('/viewCustomer/<customer_id>')
def viewCustomer(customer_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer WHERE customer_id = %s", (customer_id,))
    data = cursor.fetchall()[0]
    cursor.close()
    return (render_template('user/viewEvent.html', data=data))


#user login
# Define the login route
@app.route('/userLogin', methods=['GET', 'POST'])
def userLogin():
    if request.method == 'POST':
        # Retrieve username and password from the form
        username = request.form['username']
        password = request.form['password']

        # Retrieve user information from the database using the username
        mycursor = conn.cursor()
        sql = "SELECT * FROM customer WHERE username = %s"
        val = (username,)
        mycursor.execute(sql, val)
        user = mycursor.fetchone()

        # Compare the retrieved password with the password entered by the user
        if user and password == user[6]:
            # Log in the user and redirect them to the dashboard
            session['username'] = username
            return redirect('/userDashboard')
        else:
            # If the passwords don't match, show an error message
            return render_template('home.html', error='Invalid username or password')

    return render_template('home.html')



#user logout
@app.route('/userLogout')
def userLogout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)