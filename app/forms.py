from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, FileField, BooleanField
from wtforms.validators import DataRequired



class CarCreationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    price_per_minute = FloatField('Цена в минуту', validators=[DataRequired()])
    cars_transmition = SelectField('cars_transmition', choices=[('auto', 'Автоматическая'), ('Manual', 'Ручная')], validators=[DataRequired()])
    #files = MultipleFileField('images')
    availability = BooleanField('availability')


    logo = FileField()

class CarRentForm(FlaskForm):
    pass