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
    username = db.Column(db.String(40), nullable = False)
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
    
        login = users.query.filter_by(email=email, password=password).first()
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

                # check if session exists
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
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # username cannot be empty
        if username == "":
            session.pop('_flashes', None)
            flash('User Name cannot be empty')
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
    
        
        #will check if already an user    
        is_email_present = users.query.filter_by(email=email).first()

        #will check if username is already present
        is_username_present = users.query.filter_by(username=username).first()

        if is_username_present is not None:
            session.pop('_flashes', None)
            flash('User Name already exists')
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
        register = users(username = username,email = email, password = password, confirm_password = confirm_password)

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

@app.route('/logout')
def logout():
    session.pop('email',None)
    session.pop('_flashes', None)
    flash('Logged out successfully')
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
