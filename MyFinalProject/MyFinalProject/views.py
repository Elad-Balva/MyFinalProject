"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, flash, redirect
from MyFinalProject import app
from flask import request

import pandas as pd

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from MyFinalProject.Models.Forms import ExpandForm
from MyFinalProject.Models.Forms import CollapseForm
from MyFinalProject.Models.Forms import UFCForm
import matplotlib.pyplot as plt
import io
import base64from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvasfrom matplotlib.figure import Figure
from MyFinalProject.Models.QueryFormStructure import QueryFormStructure 
from MyFinalProject.Models.QueryFormStructure import LoginFormStructure 
from MyFinalProject.Models.QueryFormStructure import UserRegistrationFormStructure
from MyFinalProject.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines

from os import path
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

db_Functions = create_LocalDatabaseServiceRoutines()
app.config['SECRET_KEY'] = 'The first argument to the field'


@app.route('/')
@app.route('/home')
def home():

    print("Home")

    """Renders the home page."""
    
    return render_template(
        'index.html',
        title='Home',
        img_UFC = '/static/imgs/ufclogo1.png',
        year=datetime.now().year
    )

@app.route('/contact')
def contact():

    print("Contact")

    """Renders the contact page."""

    return render_template(
        'contact.html',
        title='Contacts',
        year=datetime.now().year,
        img_tichonet = '/static/imgs/tichonet.png'
    )

@app.route('/about')
def about():

    print("About")

    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        img_tichonet = '/static/imgs/tichonet.png'
    )

@app.route('/data')
def data():

    print("Data")

    """Renders the about page."""
    return render_template(
        'data.html',
        title='Data',
        year=datetime.now().year,
        message='My data page.',
        img_trump = '/static/imgs/ufc7.jpg',
        img_obama = '/static/imgs/ufc2.jpg',
        img_bush = '/static/imgs/ufc5.jpg',
        img_clinton = '/static/imgs/ufc4.jpg'
    )

@app.route('/data/ufcdata' , methods = ['GET' , 'POST'])
def ufcdata():

    form1 = ExpandForm()
    form2 = CollapseForm()
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/data.csv'))
    raw_data_table = ''

    if request.method == 'POST':
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.to_html(classes = 'table table-hover')
        if request.form['action'] == 'Collapse' and form2.validate_on_submit():
            raw_data_table = ''

    

    return render_template(
        'ufcdata.html',
        title='Data',
        year=datetime.now().year,
        message='UFC dataset page:',
        img_trump = '/static/imgs/ufc12.jpg',
        img_obama = '/static/imgs/ufc13.jpg',
        img_bush = '/static/imgs/ufc15.jpg',
        img_clinton = '/static/imgs/ufc14.jpg',
        raw_data_table = raw_data_table,
        form1 = form1,
        form2 = form2
    )

@app.route('/query' , methods = ['GET' , 'POST'])
def query():

    form1 = UFCForm()
    chart = '/static/imgs/ufc100.jpg'

   
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/data.csv'))

    l = list(df["weight_class"])
    l = list(set(l))
    l = list(zip(l,l))
    form1.weight_class.choices = l


    if request.method == 'POST':
        category = form1.weight_class.data
        df = df[["R_fighter", "B_fighter", "Winner", "weight_class"]]
        df = df[df.weight_class == category]
        df = df.drop("weight_class", 1)
        def myselect(x,y,w):
            if w == "Red":
                return x
            else:
                return y
        df["Winner_name"] = df.apply(lambda x: myselect(x.R_fighter, x.B_fighter, x.Winner),axis = 1)
        s = df.groupby("Winner_name").size().sort_values(ascending = False)
        s = s[0:10]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        fig.subplots_adjust(bottom=0.4)
        s.plot(ax = ax , kind = 'bar', figsize = (24, 8) , fontsize = 22 , grid = True)
        chart = plot_to_img(fig)

    
    return render_template(
        'query.html',
        form1 = form1,
        chart = chart
    )

def plot_to_img(fig):    pngImage = io.BytesIO()    FigureCanvas(fig).print_png(pngImage)    pngImageB64String = "data:image/png;base64,"    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')    return pngImageB64String

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            # Here you should put what to do (or were to go) if registration was good
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register',
        year=datetime.now().year,
        repository_name='Pandas',
        )

# -------------------------------------------------------
# Login page
# This page is the filter before the data analysis
# -------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
          return redirect('query')
            #return redirect('<were to go if login is good!')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login',
        year=datetime.now().year,
        repository_name='Pandas',
        )
