
from app import app, db
from app.models import Car
from flask import render_template, request, redirect, url_for

import os

from app.models import Car
from app.forms import CarCreationForm

@app.route('/index')
@app.route('/')
def index():
    car_list = Car.query.all()
    context = {'car_list': car_list}
    return render_template('index.html', **context)

    context = {
        'car_list': car_list,
    }
    return render_template('index.html', **context)


@app.route('/add-car', methods=['GET', 'POST'])
def add_car():
    form = CarCreationForm()
 #   form.car.choices = [(car.id, car.name) for car in Car.query.all()]
    if form.validate_on_submit():
        new_car = Car()
        new_car.name = form.name.data
        new_car.description = form.description.data
        new_car.price_per_minute = form.price_per_minute.data
        new_car.cars_transmition = form.cars_transmition.data
        new_car.availability = form.availability.data
        db.session.add(new_car)
        db.session.commit()
        return render_template('index.html')
        #return redirect(url_for('auto_detail.html', car_id=form.car.data))
    return render_template('auto_create.html', form=form)
