from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import InputRequired

app = Flask(__name__)
app.secret_key = 'your_secret_key'


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


def login(data):
    print(data)
    return data['username']
    # form = LoginForm()
    # if form.validate_on_submit():
    #     # Check if the username and password are correct
    #     if form.username.data == 'gtan' and form.password.data == '123':
    #         # Redirect to the protected page
    #         return redirect(url_for('admin'))
    #     else:
    #         # Show an error message
    #         form.username.errors.append('Invalid username or password')
    # return render_template('home.html', form=form)


@app.route('/admin')
def protected():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run()
