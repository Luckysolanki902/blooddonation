import secrets
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TelField
from wtforms.validators import DataRequired, Email, Length
from flask_mail import Mail, Message
import logging

app = Flask(__name__, static_url_path='/static')
Bootstrap(app)


# Set the generated secret key for CSRF protection
app.config['SECRET_KEY'] = secrets.token_hex(16)

# Configure the logging module
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'luckysolanki902@gmail.com'
app.config['MAIL_PASSWORD'] = 'rgmowrqyiedscozm'

mail = Mail(app)

class DonorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mobile = TelField('Mobile', validators=[DataRequired(), Length(min=10, max=10)])
    bloodgroup = SelectField('Blood Group', choices=[
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-')
    ])
    address = StringField('Address')
    submit = SubmitField('Register')

# Function to send thank-you emails to donors
def send_thank_you_email(name, email):
    try:
        msg = Message('Thank you for registering!', sender='luckysolanki902.com', recipients=[email])
        msg.body = f"Hello {name},\n\nThank you for registering for our blood donation event.\nWe appreciate your support."
        mail.send(msg)

        logger.info(f"Thank-you email sent to {email}")

    except Exception as e:
        logger.error(f"Error sending thank-you email to {email}: {str(e)}")

# Function to send form submission information to the NGO
def send_submission_info(name, email, mobile, bloodgroup, address):
    try:
        msg = Message('New Donor Registration', sender='luckysolanki902.com', recipients=['donate.blood.gift@gmail.com'])
        msg.body = f"New donor registration:\nName: {name}\nEmail: {email}\nMobile: {mobile}\nBlood Group: {bloodgroup}\nAddress: {address}"
        mail.send(msg)
        # Insert data into MongoDB
        # mongo.db.donors.insert_one({
        #     'name': name,
        #     'email': email,
        #     'mobile': mobile,
        #     'bloodgroup': bloodgroup,
        #     'address': address
        # })

        logger.info(f"Form submission information sent to NGO for {name}")

    except Exception as e:
        logger.error(f"Error sending form submission information for {name}: {str(e)}")

# Define the root route for both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def index():
    form = DonorForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data

        # Send a thank-you email to the donor
        send_thank_you_email(name, email)

        flash('Thank you for registering!', 'success')
        return redirect(url_for('index'))

    return render_template('index.html', form=form)

# Define the registration route to render 'registration.html'
@app.route('/registration', methods=['GET', 'POST'])
# Define the registration route to render 'registration.html'
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = DonorForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        mobile = form.mobile.data
        bloodgroup = form.bloodgroup.data
        address = form.address.data

        # Send a thank-you email to the donor
        send_thank_you_email(name, email)

        # Send the form submission information to the NGO, including blood group and address
        send_submission_info(name, email, mobile, bloodgroup, address)

        flash('Thank you for registering!', 'success')
        return redirect(url_for('index'))

    return render_template('registration.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
