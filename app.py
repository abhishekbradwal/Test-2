from flask import Flask, render_template, request
from markupsafe import escape

app = Flask(__name__)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login_validation', methods = ['POST'])
def login_validation():
    email_id = request.form.get('email_id')
    password_id = request.form.get('password_id')
    return f"the email is {email_id} and the password is {password_id}"

if __name__ == '__main__':
    app.run(debug = True)