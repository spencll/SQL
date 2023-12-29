# importing form class FlaskForm, use to link flask to WTForm
from flask_wtf import FlaskForm

# importing form fields
from wtforms import StringField, FloatField, URLField, SelectField, validators, BooleanField

# importing form validators 
from wtforms.validators import InputRequired, Optional, Email

class AddPetForm(FlaskForm):
    """Form for adding pets."""
    
    name=StringField('Pet name')
    species=SelectField('Cat, dog, or porcupine',choices=[('cat','cat'),('dog','dog'),('porcupine','porcupine')])
    photo_url=URLField('Photo URL')
    age=FloatField('Age', validators=[validators.number_range(min=0, max=30)])
    notes=StringField('Notes', validators=[Optional()])
    available=BooleanField('Availability')



