"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from MyFinalProject import app
from flask import request

import pandas as pd

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from MyFinalProject.Models.Forms import ExpandForm
from MyFinalProject.Models.Forms import CollapseForm



from os import path
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'The first argument to the field'


@app.route('/')
@app.route('/home')
def home():

    print("Home")

    """Renders the home page."""
    
    return render_template(
        'index.html',
        title='Home Page',
        img_UFC = '/static/imgs/ufclogo1.png',
        year=datetime.now().year
    )

@app.route('/contact')
def contact():

    print("Contact")

    """Renders the contact page."""

    return render_template(
        'contact.html',
        year=datetime.now().year,
        img_tichonet = '/static/imgs/tichonet.png'
    )

@app.route('/about')
def about():

    print("About")

    """Renders the about page."""
    return render_template(
        'about.html',
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