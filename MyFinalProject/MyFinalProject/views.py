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
from MyFinalProject.Models.Forms import UFCForm
import matplotlib.pyplot as plt
import io
import base64from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvasfrom matplotlib.figure import Figure



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

@app.route('/query' , methods = ['GET' , 'POST'])
def query():

    form1 = UFCForm()
    chart = '/static/imgs/ufclogo1.png'

   
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

