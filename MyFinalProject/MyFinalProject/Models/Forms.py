from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import Form, BooleanField, PasswordField
from wtforms import TextField, TextAreaField, SelectField, DateField
from wtforms import validators, ValidationError

from wtforms.validators import DataRequired
from wtforms.validators import InputRequired



# class for the expend button
class ExpandForm(FlaskForm):
    submit1 = SubmitField('Expand')
    name="Expand" 
    value="Expand"

# class for the collapse button
class CollapseForm(FlaskForm):
    submit2 = SubmitField('Collapse')
    name="Collapse" 
    value="Collapse"

# class for the query page
class UFCForm(FlaskForm):
    weight_class = SelectField('Select a weight class:' , validators = [DataRequired] )
    submit = SubmitField('submit')
