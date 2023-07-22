from flask import Flask, render_template, url_for, redirect, request, flash, session, jsonify,Response
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from data_man import statistics,dgraph1
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')
SECRET_KEY = os.environ.get('SECRET_KEY')

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.permanent_session_lifetime = timedelta(minutes = 600)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable = False)
    username = db.Column(db.String(40), nullable = False)
    address = db.Column(db.String(80), nullable = False)
    phone_number = db.Column(db.Integer, nullable = False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    confirm_password = db.Column(db.String(100), nullable=False)
    relation = db.relationship('owner', backref = 'users')

class owner(db.Model):
    _customer_id = db.Column("id", db.Integer, primary_key=True)
    customer_name = db.Column(db.String(40), nullable = False)
    customer_username = db.Column(db.String(40), nullable = False)
    customer_address = db.Column(db.String(80), nullable = False)
    customer_phone_number = db.Column(db.Integer, nullable = False)
    customer_email = db.Column(db.String(100), nullable=False)

    customer_product_category_page = db.Column(db.String(40), nullable = False)
    customer_product_category_page_index = db.Column(db.String(40), nullable = False)
    customer_product_price = db.Column(db.String(40), nullable = False)
    customer_product_heading = db.Column(db.String(40), nullable = False)
    customer_product_description = db.Column(db.String(40), nullable = False)

    users_id = db.Column(db.Integer, db.ForeignKey('users.id') )

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

        if email==EMAIL and password==PASSWORD:
            session['email']=email
            return redirect(url_for('Owner'))

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

@app.route('/Owner')
def Owner():
    # session['email'] = email 
    nusers,norders,popproduct,osum=statistics()
    return render_template('sample.html',norders=norders,nusers=nusers,popproduct=popproduct,osum=osum)

@app.route('/plot1.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    table=dgraph1()
    axis.bar(table.index,table['customer_product_price'],color ='maroon')
    axis.set_ylabel('SALES IN DOLORS $', labelpad=15, color='#333333')
    axis.set_xlabel('CATEGORY', labelpad=15, color='#333333')
    axis.set_xticklabels(axis.get_xticklabels(), rotation=45, ha="right")
    return fig


@app.route('/plot2.png')
def plot_png2():
    fig = create_figure2()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure2():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    table=dgraph1()
    axis.pie(table['customer_product_price'],labels=table.index)
    return fig

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

@app.route('/settings')
def settings():
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
    return render_template('settings.html',name = name,address = address,phone_number = phone_number,username = username,email = email)

@app.route('/render_name')
def render_name():
    name = ""
    email = session['email']
    user_info = users.query.all()
    for rows in user_info:
        email_id = rows.email
        if email_id == email:
            name = rows.name
    return render_template('update_name.html',name = name)

@app.route('/update_name',methods = ['GET','POST'])
def update_name():

    # initial user name
    name = ""
    email = session['email']
    user_info = users.query.all()
    for rows in user_info:
        email_id = rows.email
        if email_id == email:
            name = rows.name

    if request.method == 'POST':
        new_name = request.form['update_name']

        if name == new_name:
            session.pop('_flashes',None)
            flash('New Name cannot be same')
            return redirect(url_for('render_name'))
        
        if new_name == "":
            session.pop('_flashes',None)
            flash('New Name cannot be empty')
            return redirect(url_for('render_name'))

        else:
            session.pop('_flashes',None)
            flash('Name successfully changed')

            update_user_info = users.query.filter_by(email = email).first()
            update_user_info.name = new_name
            db.session.add(update_user_info)
            db.session.commit()

            return redirect(url_for('settings'))

    return render_template('update_name.html')

@app.route('/render_address')
def render_address():
    address = ""
    email = session['email']
    user_info = users.query.all()
    for rows in user_info:
        email_id = rows.email
        if email_id == email:
            address = rows.address
    return render_template('update_address.html',address = address)

@app.route('/update_address',methods = ['GET','POST'])
def update_address():

    # initial user address
    address = ""
    email = session['email']
    user_info = users.query.all()
    for rows in user_info:
        email_id = rows.email
        if email_id == email:
            address = rows.address

    if request.method == 'POST':
        new_address = request.form['update_address']

        if address == new_address:
            session.pop('_flashes',None)
            flash('New Address cannot be same')
            return redirect(url_for('render_address'))
        
        if new_address == "":
            session.pop('_flashes',None)
            flash('Address cannot be empty')
            return redirect(url_for('render_address'))

        else:
            session.pop('_flashes',None)
            flash('Address successfully changed')

            update_user_info = users.query.filter_by(email = email).first()
            update_user_info.address = new_address
            db.session.add(update_user_info)
            db.session.commit()

            return redirect(url_for('settings'))

    return render_template('update_address.html')

@app.route('/render_phone_number')
def render_phone_number():
    phone_number = ""
    email = session['email']
    user_info = users.query.all()
    for rows in user_info:
        email_id = rows.email
        if email_id == email:
            phone_number = rows.phone_number

    return render_template('update_phone_number.html',phone_number = phone_number)

@app.route('/update_phone_number',methods = ['GET','POST'])
def update_phone_number():

    # initial user phone number
    phone_number = ""
    email = session['email']
    user_info = users.query.all()
    for rows in user_info:
        email_id = rows.email
        if email_id == email:
            phone_number = rows.phone_number

    if request.method == 'POST':
        new_phone_number = request.form['update_phone_number']

        if phone_number == new_phone_number:
            session.pop('_flashes',None)
            flash('New Phone Number cannot be same')
            return redirect(url_for('render_phone_number'))
        
        _count = 0; _count_int = 0; _count_size = 0; flag = True
        for index in new_phone_number:
            if index == '-':
                if _count_size == 3 or _count_size == 7:
                    _count = _count + 1
                else:
                    flag = False
            if index == '0' or index == '1' or index == '2' or index == '3' or index == '4':
                _count_int = _count_int + 1
            if index == '5' or index == '6' or index == '7' or index == '8' or index == '9':
                _count_int = _count_int + 1
            _count_size = _count_size + 1

        if _count_int == 10 and _count == 2 and _count_size == 12 and flag == True:
            session.pop('_flashes',None)
            flash('Phone Number successfully changed')
            update_user_info = users.query.filter_by(email = email).first()
            update_user_info.phone_number = new_phone_number
            db.session.add(update_user_info)
            db.session.commit()

            return redirect(url_for('settings'))
        
        else:
            session.pop('_flashes',None)
            flash('Please type in current phone number format')
            return redirect(url_for('render_phone_number'))

    return render_template('update_phone_number.html')

# render previous page
@app.route('/render_previous_page', methods = ['GET','POST'])
def render_previous_page():
    session.pop('_flashes',None)
    if request.method == 'POST':
        if 'category_page' in request.form:
            category_page = request.form['category_page']

            # category is the html page
            category = ""
            _count = len(category_page)
            _count = _count - 2

            for index in range(_count):
                category = category + category_page[index]


            category = category + '.html'
            session.pop('_flashes',None)
            flash('Order cancelled')
            return render_template(f'{category}')
    
    session.pop('_flashes',None)
    return render_template('home.html')

# placed order
@app.route('/place_order', methods = ['POST','GET'])
def place_order():
    if request.method == 'POST':
        category = request.form['category']
        price = float(request.form['price'])
        heading = request.form['heading']
        description = request.form['description']

        session.pop('_flashes',None)

        return render_template('place_order.html', category=category, price = price, heading = heading, description = description)
    
# order confirmed
@app.route('/confirmed_order', methods = ['GET', 'POST'])
def confirmed_order():
    if request.method == 'POST':

        # product details
        confirmed_category_page = request.form['confirmed_category_page']
        confirmed_price = request.form['confirmed_price']
        confirmed_heading = request.form['confirmed_heading']
        confirmed_description = request.form['confirmed_description']

        #user details
        name = ""; username = ""; address = ""; phone_number = ""; 
        email = session['email']
        user_info = users.query.all()
        for rows in user_info:
            email_id = rows.email
            if email_id == email:
                name = rows.name
                username = rows.username
                address = rows.address
                phone_number = rows.phone_number

        # category is the html page
        category = ""
        _count = len(confirmed_category_page)
        _count = _count - 2

        for index in range(_count):
            category = category + confirmed_category_page[index]

        category_name = category
        category = category + '.html'

        user_info = owner(customer_name = name,customer_username = username,customer_address = address,customer_phone_number = phone_number,customer_email = email,customer_product_category_page = category_name,customer_product_category_page_index = confirmed_category_page,customer_product_price = confirmed_price,customer_product_heading = confirmed_heading,customer_product_description = confirmed_description)
        db.session.add(user_info)
        db.session.commit()

        session.pop('_flashes',None)
        flash('Order placed successfully')
        return render_template(f'{category}',confirmed_category_page = confirmed_category_page, confirmed_price = confirmed_price,confirmed_heading = confirmed_heading, confirmed_description = confirmed_description)
    
    session.pop('_flashes',None)
    return render_template('home.html')

#########################################################
@app.route('/myorders')
def myorders():
    email = session['email']; username = "";
    customer_product_category_page = "";
    customer_product_price = float(0); customer_product_heading = "";
    user_info = owner.query.all(); cnt_product = 0
    customer_product_category_page_index = ""; customer_product_description = "";
    my_orders = [[]]
    for rows in user_info:
        email_id = rows.customer_email
        my_orders_section = []

        if email_id == email:
            username = rows.customer_username
            customer_product_category_page = rows.customer_product_category_page
            customer_product_heading = rows.customer_product_heading
            customer_product_price = float(rows.customer_product_price)
            customer_product_category_page_index = rows.customer_product_category_page_index
            customer_product_description = rows.customer_product_description
            cnt_product += 1
            my_orders_section.append(username)
            my_orders_section.append(customer_product_category_page);
            my_orders_section.append(customer_product_heading)
            my_orders_section.append(customer_product_price)
            my_orders_section.append(customer_product_category_page_index)
            my_orders_section.append(customer_product_description)
            my_orders.append(my_orders_section)

    return render_template('myorders.html',cnt_product = cnt_product,my_orders = my_orders)

@app.route('/render_image', methods = ['GET','POST'])
def render_image():
    if request.method == 'POST':
        customer_product_category_page_index = request.form['customer_product_category_page_index']
        customer_product_heading = request.form['customer_product_heading']
        customer_product_description = request.form['customer_product_description']
        cost_price = request.form['cost_price']
        return render_template('show_image.html',customer_product_category_page_index = customer_product_category_page_index,customer_product_heading = customer_product_heading,customer_product_description = customer_product_description,cost_price = cost_price)

    return redirect('myorders')
#########################################################

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

@app.route('/living_room')
def living_room():
    session.pop('_flashes',None)
    return render_template('living_room.html')

@app.route('/bedroom')
def bedroom():
    session.pop('_flashes',None)
    return render_template('bedroom.html')

@app.route('/mattress')
def mattress():
    session.pop('_flashes',None)
    return render_template('mattress.html')

@app.route('/kitchen')
def kitchen():
    session.pop('_flashes',None)
    return render_template('kitchen.html')

@app.route('/baby_kids')
def baby_kids():
    session.pop('_flashes',None)
    return render_template('baby_kids.html')

@app.route('/outdoor')
def outdoor():
    session.pop('_flashes',None)
    return render_template('outdoor.html')

@app.route('/home_office')
def home_office():
    session.pop('_flashes',None)
    return render_template('home_office.html')

@app.route('/home_decor')
def home_decor():
    session.pop('_flashes',None)
    return render_template('home_decor.html')

@app.route('/rugs')
def rugs():
    session.pop('_flashes',None)
    return render_template('rugs.html')

@app.route('/lighting')
def lighting():
    session.pop('_flashes',None)
    return render_template('lighting.html')


@app.route('/logout')
def logout():
    session.pop('email',None)
    session.pop('_flashes', None)
    flash('Logged out successfully')
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)