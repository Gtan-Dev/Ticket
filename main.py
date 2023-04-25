from flask import Flask, render_template,flash, request, redirect, url_for, session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = 'my_secret_key'
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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

    if not username:
        return render_template('home.html', error = 'Please enter username')
    elif not names:
        return render_template('home.html', error = 'Please enter names')
    elif not phone:
        return render_template('home.html', error = 'Please enter phone')
    elif not email:
        return render_template('home.html', error = 'Please enter email')
    elif not address:
        return render_template('home.html', error = 'Please enter address')
    elif not password:
        return render_template('home.html', error = 'Please enter passowrd')
    elif not confirm_password:
        return render_template('home.html', error = 'Please add confirmation password')
    
    if len(password) < 4 or len(password) >= 10:
        return render_template('home.html', error = 'Password must be between 4 and 8 characters long')
    
    if len(phone) < 10:
        return render_template('home.html', error = 'Phone number must be at least 10 digits long')

    if password != confirm_password:
        return render_template('home.html', error = 'Password do not match')
    
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
    cursor = conn.cursor()
    cursor.execute("SELECT name,names,events.date FROM books, events,customer WHERE books.event_id=events.event_id AND books.customer_id=customer.customer_id")
    rows = cursor.fetchall()
    
    return (render_template('admin/admin-booking.html', rows=rows))


#Route to retrieve events from database to admin page
@app.route('/ad-events')
def listEvents():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()
    
    return (render_template('admin/ad-events.html', rows=rows))

@app.route('/editevent/id/<id>')
def editEvent(id):
    # id = int(id)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `events` WHERE `event_id`="+id+"")
    data = cursor.fetchall()
    return render_template('admin/editevent.html',data=data[0])

#Route to retrieve customer from database to admin page
@app.route('/customers')
def retrieveCustomer():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer")
    rows = cursor.fetchall()
    
    return (render_template('admin/admin-customers.html', rows=rows))


@app.route('/createevent')
def createEvent():
    return (render_template('admin/createevent.html'))

@app.route('/editevent')
def editevent():
    return (render_template('admin/editevent.html'))

@app.route('/updateEvent')
def updateEvent():
    return (render_template('admin/ad-events.html'))

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
    description = request.form.get('desc')
    number = request.form.get('ticket')
    file = request.files['image']
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

     # Create a cursor object
    cursor = conn.cursor()

    sql = "INSERT INTO `events` (`name`, `date`, `time`, `location`, `ticket_price`, `description`, `number`, `image`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
    value = (name, date, time, location, ticket_price, description, number, filename)
    cursor.execute(sql, value)
    conn.commit()
    return render_template('admin/createevent.html', success = 'Event created successfully !')


@app.route('/modifyEvent', methods=['POST'])
def modifyEvent():
    # get the data from the request
    user_id = request.form.get('my_id')
    name = request.form.get('name')
    date = request.form.get('date')
    time = request.form.get('time')
    location = request.form.get('location')
    ticket_price = request.form.get('ticket_price')

    file = request.files['image']
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    cur = conn.cursor()
    cur.execute("UPDATE events SET name = %s, date = %s, time = %s, location = %s, ticket_price = %s, image = %s WHERE event_id = %s", (name, date, time, location, ticket_price, filename, user_id))
    conn.commit()
    
    return render_template('admin/ad-events.html', msg = 'Event updated successfully')

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    mycursor = conn.cursor()
    sql = "DELETE FROM events WHERE event_id = %s"
    val = (id,)
    mycursor.execute(sql, val)
    conn.commit()
    return render_template('admin/ad-events.html', success = 'Event cancelled successful !')


 #Users routes
@app.route('/userDashboard')
def userDashboard():
    if 'username' in session:
        # Display the logged-in user on the dashboard
        return render_template('user/userDashboard.html', username=session['username'])
    else:
        # If the user isn't logged in, redirect them to the login page
        return (render_template('home.html'))
    

#retrieve events to user's page
@app.route('/allevents')
def allevents():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()
    
    return (render_template('user/allevents.html', rows=rows ))


@app.route('/userbooking')
def userbooking():
    if 'username' in session:
        # Retrieve the logged-in user from the session
        username = session['username']
        cursor = conn.cursor()
        cursor.execute("SELECT name,names,events.date FROM books, events,customer WHERE books.username='"+username+"'AND books.event_id=events.event_id AND books.customer_id=customer.customer_id")
        records = cursor.fetchall()
        # Pass the records to the template
        return render_template('user/booking.html', username=username, records=records)
    else:
        return redirect('/')


#retrieve users to user dashboard
@app.route('/userprofile')
def dashboard():
    if 'username' in session:
        # Retrieve the logged-in user from the session
        username = session['username']
        cursor = conn.cursor()
        query = "SELECT username, names, email, phone, address FROM customer WHERE username = %s"
        cursor.execute(query, (username,))
        records = cursor.fetchall()
        
        # Pass the records to the template
        return render_template('user/profile.html', username = username, records=records)
    else:
        return redirect('/')


#view single record
@app.route('/viewEvent/<event_id>')
def viewEvent(event_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE event_id = %s", (event_id,))
    data = cursor.fetchall()[0]
    
    return (render_template('user/viewEvent.html', data=data))


#view single customers
@app.route('/viewCustomer/<customer_id>')
def viewCustomer(customer_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer WHERE customer_id = %s", (customer_id,))
    data = cursor.fetchall()[0]
    
    return (render_template('user/viewEvent.html', data=data))


# Define the login route
@app.route('/userLogin', methods=['GET', 'POST'])
def userLogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Retrieve user information from the database using the username
        mycursor = conn.cursor()
        sql = "SELECT * FROM customer WHERE username = %s"
        val = (username,)
        mycursor.execute(sql, val)
        user = mycursor.fetchone()

        # Compare the retrieved password with the password entered by the user
        if not username:
            return render_template('home.html', loginError = 'Username is empty')
        
        elif not password:
            return render_template('home.html', loginError = 'Password is empty')
        
        elif user and password == user[6]:
            session['username'] = username
            return redirect('/userDashboard')
        else:
            return render_template('home.html', loginError='Invalid username or password, Please try again !')
        

    return render_template('home.html')

#user logout
@app.route('/userLogout')
def userLogout():
    session.clear()
    return redirect('/')

# book event routes
@app.route('/bookevent/<int:id>')
def book(id):
    username = session['username']
    sql = "SELECT * FROM `customer` WHERE `username` = %s limit 1"
    cursor = conn.cursor()
    cursor.execute(sql,(username,))
    user = cursor.fetchone()
    ev = "SELECT number FROM `events` WHERE `event_id` = %s limit 1"
    cursor = conn.cursor()
    cursor.execute(ev,(id,))
    evn = cursor.fetchone()
    userId = user[0]
    sizee = evn[0]

    if sizee > 0:
        # save event bookings

        sql = "INSERT INTO `books`(`customer_id`, `event_id`, `username`) VALUES (%s,%s,%s)"
        cursor.execute(sql,(userId,id,username))
        conn.commit()
        
        # updated event and remove bookings
        sql = "UPDATE `events` SET `number` = `number`-1 WHERE `event_id` = %s"
        cursor.execute(sql,(id,))
        conn.commit()
        return redirect('/allevents')
    else:
        flash('Ticket for this event have been finished!')
        return redirect('/allevents')

if __name__ == "__main__":
    app.run(debug=True)