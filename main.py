from flask import Flask, render_template, request, redirect, url_for, sessions


app = Flask(__name__)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/')
def home():
    return render_template('home.html')

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

@app.route('/regist')
def regist():
    return (render_template('regist.html'))

@app.route('/setting')
def setting():
    return (render_template('admin-setting.html'))

@app.route('/ticket')
def ticket():
    return (render_template('admin-ticket.html'))

@app.route('/profile')
def profile():
    return (render_template('profile.html'))

@app.route('/booking')
def booking():
    return (render_template('admin-booking.html'))

@app.route('/customers')
def customers():
    return (render_template('admin-customers.html'))

@app.route('/ad-events')
def ad_events():
    return (render_template('ad-events.html'))

# app.run(host='localhost', port=5000)

# app = Flask(__name__)
# app.debug = True

if __name__ == "__main__":
    app.run(debug=True)