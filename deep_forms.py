from flask_wtf import FlaskForm
from wtforms import Form, StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    choices = [('Artist', 'Artist'),
               ('Album', 'Album'),
               ('Publisher', 'Publisher')]
    select = SelectField('Search for music:', choices=choices)
    search = StringField("", validators = [DataRequired()])
    submit = SubmitField("Get Recommendations")
    