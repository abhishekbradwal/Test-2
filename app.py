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

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login_validation', methods=['POST', 'GET'])
def login_validation():
    if (request.method == "POST"):
        email = request.form['email']
        password = request.form['password']

        login = users.query.filter_by(email=email, password=password).first()

        if login is not None:
            return redirect(url_for('home'))
        
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

        print(f'{email}')
        print(f'{password}')
        print(f'{confirm_password}')

        register = users(email = email, password = password, confirm_password = confirm_password)

        if password == confirm_password:
            db.session.add(register)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return render_template('register.html')

    return render_template("register.html")

@app.route('/')
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
