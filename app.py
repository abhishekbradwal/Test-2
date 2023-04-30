from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "$rtu&&3420@erWXVY"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    confirm_password = db.Column(db.String(100), nullable=False)

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login_validation', methods=['POST', 'GET'])
def login_validation():
    if (request.method == "POST"):
        email = request.form['email']
        password = request.form['password']

        login = users.query.filter_by(email=email, password=password).first()

        if email == "":
            flash('Email cannot be empty')
            return render_template("login.html")
        
        if password == "":
            flash('Password cannot be empty')
            return render_template("login.html")

        if login is not None:
            flash('Successful Login')
            return redirect(url_for('home'))
        else:
            flash('Account do not exist')
            return render_template('login.html')
        
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/registration_validation', methods = ['POST','GET'])
def registration_validation():
    if (request.method == 'POST'):
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # email cannot be empty
        if email == "":
            flash('Email cannot be empty')
            return render_template("register.html")
        
        # password cannot be empty
        if password == "":
            flash('Password cannot be empty')
            return render_template("register.html")
    
        
        #will check if already an user    
        is_email_present = users.query.filter_by(email=email).first()

        if is_email_present is not None:
            flash('Email already exists')
            return render_template("register.html")

        if password != confirm_password:
            flash('Passwords do not match')
            return render_template('register.html')
        
        # register a new user
        register = users(email = email, password = password, confirm_password = confirm_password)

        if password == confirm_password:
            db.session.add(register)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return render_template('register.html')

    return render_template("register.html")

@app.route('/home')
def home():
    return render_template('home.html')

# @app.route('/logout')
# def logout():
#     return redirect(url_for('login'))

# @app.route('/user')
# def user():
#     if "email_id" in session:
#         email_id = session["email_id"]
#         return redirect('home')
#     else:
#         return redirect('login')


if __name__ == '__main__':
    app.run(debug=True)
