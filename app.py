from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "$rtu&&3420@erWXVY"
app.permanent_session_lifetime = timedelta(minutes = 60)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable = False)
    username = db.Column(db.String(40), nullable = False)
    address = db.Column(db.String(80), nullable = False)
    phone_number = db.Column(db.Integer, nullable = False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    confirm_password = db.Column(db.String(100), nullable=False)

@app.route('/')
def login():

    if email in session:
        if email == "":
            return render_template('login.html')

    if 'email' in session:
        return redirect(url_for('home'))

    return render_template('login.html')


@app.route('/login_validation', methods=['POST', 'GET'])
def login_validation():
    if (request.method == "POST"):
    
        email = request.form['email']
        password = request.form['password']
    
        is_email_present = users.query.filter_by(email = email).first()
        is_password_present = users.query.filter_by(password = password).first()

        if email == "":
            session.pop('_flashes', None)
            flash('Email cannot be empty')
            return render_template("login.html")
        
        if password == "":
            session.pop('_flashes', None)
            flash('Password cannot be empty')
            return render_template("login.html")
        
        if is_email_present is not None:
            if is_password_present is None:
                session.pop('_flashes', None)
                flash('Incorrect password')
                return render_template("login.html")
            
            else:
                session.pop('_flashes', None)
                flash('Successful Login')

                # gather user_name
                user_info = users.query.filter_by(email = email).first();
                username = user_info.username

                # update session
                session['username'] = username
                session['email'] = email
                session.permanent = True
                return redirect(url_for('email'))
            
        else:
            session.pop('_flashes', None)
            flash('Account do not exist')
            return render_template('login.html')
    
    else:
        if 'email' in session:
            return redirect(url_for('email'))

        return render_template('login.html')
        

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/registration_validation', methods = ['POST','GET'])
def registration_validation():
    if (request.method == 'POST'):
        name = request.form['name']
        username = request.form['username']
        address = request.form['address']
        phone_number = request.form['phone_number']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # name cannot be empty
        if name == "":
            session.pop('_flashes', None)
            flash('Name cannot be empty')
            return render_template("register.html")
        
        # username cannot be empty
        if username == "":
            session.pop('_flashes', None)
            flash('User Name cannot be empty')
            return render_template("register.html")
        
        # address cannot be empty
        if address == "":
            session.pop('_flashes', None)
            flash('Address cannot be empty')
            return render_template("register.html")
        
        # email cannot be empty
        if email == "":
            session.pop('_flashes', None)
            flash('Email cannot be empty')
            return render_template("register.html")
        
        # password cannot be empty
        if password == "":
            session.pop('_flashes', None)
            flash('Password cannot be empty')
            return render_template("register.html")
    
        # will check if already an user    
        is_email_present = users.query.filter_by(email=email).first()

        # will check if username is already present
        is_username_present = users.query.filter_by(username=username).first()

        # will check if phone number is already present
        is_phone_number_present = users.query.filter_by(phone_number = phone_number).first()

        if is_username_present is not None:
            session.pop('_flashes', None)
            flash('User Name already exists')
            return render_template("register.html")

        if is_phone_number_present is not None:
            session.pop('_flashes', None)
            flash('Phone Number already exists')
            return render_template("register.html")

        if is_email_present is not None:
            session.pop('_flashes', None)
            flash('Email already exists')
            return render_template("register.html")

        if password != confirm_password:
            session.pop('_flashes', None)
            flash('Passwords do not match')
            return render_template('register.html')
        
        # register a new user
        register = users(name = name,username = username,address = address,phone_number = phone_number,email = email, password = password, confirm_password = confirm_password)

        if password == confirm_password:
            db.session.add(register)
            db.session.commit()
            session.pop('_flashes', None)
            flash('Account created Successfully')
            return redirect(url_for('login'))
        else:
            return render_template('register.html')

    return render_template("register.html")

@app.route('/home')
def home():
    if 'email' in session:
        return render_template('home.html')
    else:
        return render_template('login.html')

@app.route('/email')
def email():
    if 'email' in session:
        session.pop('_flashes', None)
        flash('Successfully logged in')
        return redirect(url_for('home'))
    else:
        return render_template('login.html')
    
@app.route('/recover_email')
def recover_email():
    return render_template('email_rendering_forgot_password.html')
    
@app.route('/forgot_password', methods = ['GET', 'POST'])
def forgot_password():
    if (request.method == 'POST'):
        email = request.form['email']

        if email == "":
            session.pop('_flashes', None)
            flash('Email address cannot be empty')
            return render_template('email_rendering_forgot_password.html')
        
        user_info = users.query.all()
        verify_email = ""
        for rows in user_info:
            email_id = rows.email
            if email_id == email:
                verify_email = email

        if verify_email != email:
            session.pop('_flashes', None)
            flash('Email address do not exist')
            return render_template('email_rendering_forgot_password.html')
        
        else:
            session.pop('_flashes', None)
            flash('Change your password')
            return render_template('forgot_password.html',email = email)
    
    return render_template('login.html')

@app.route('/update_password', methods = ['GET','POST'])
def update_password():
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['update_password']

        user_info = users.query.all()
        verify_email = ""
        for rows in user_info:
            email_id = rows.email
            if email_id == email:
                verify_email = email

        if verify_email != email:
            session.pop('_flashes',None)
            flash('Please do not change the email')
            return render_template('email_rendering_forgot_password.html')
        
        if new_password == "":
            session.pop('_flashes',None)
            flash('Password cannot be empty')
            return render_template('forgot_password.html')
        
        update_user_info = users.query.filter_by(email = email).first()
        update_user_info.password = new_password
        update_user_info.confirm_password = new_password
        db.session.add(update_user_info)
        db.session.commit()

        session.pop('_flashes',None)
        flash('Password changed successfully')

        return redirect(url_for('login'))

    return render_template('forgot_password.html')
    
    
@app.route('/profile')
def profile():
    # gather name, username, address, phone_number, email
    name = ""
    username = ""
    address = ""
    phone_number = ""
    email = session['email']
    user_info = users.query.all()
    for rows in user_info:
        email_id = rows.email
        if email_id == email:
            name = rows.name
            username = rows.username
            address = rows.address
            phone_number = rows.phone_number
    
    return render_template('profile.html',name = name,address = address,phone_number = phone_number,username = username,email = email)

@app.route('/facebook')
def facebook():
  return redirect('https://www.facebook.com/')

@app.route('/twitter')
def twitter():
  return redirect('https://twitter.com/')

@app.route('/instagram')
def instagram():
  return redirect('https://www.instagram.com/')

@app.route('/linkedin')
def linkedin():
  return redirect('https://in.linkedin.com/')

@app.route('/whatsapp')
def whatsapp():
  return redirect('https://www.whatsapp.com/')

@app.route('/logout')
def logout():
    session.pop('email',None)
    session.pop('_flashes', None)
    flash('Logged out successfully')
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
