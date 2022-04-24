from datetime import datetime, timedelta

from app import app, db
from app.models import Car, Car_Log
from flask import render_template, request, redirect, url_for

import os

from app.models import Car
from app.forms import CarCreationForm, CarRentForm


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


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


@app.route('/auto_detail/<int:car_id>', methods=['POST', 'GET'])
def auto_detail(car_id):
    car = Car.query.get(car_id)
    car_log = Car_Log.query.filter_by(car_id=car_id).all()

    form = CarRentForm()

    if request.method == 'POST':
        # value = request.form.get('value', '')
        # new_car_log = car_log()

        # if value == 'rent':
        if request.form.get('rent') == 'rent':
            new_car_log = Car_Log()
            car.availability = 0
            new_car_log.car_id = car.car_id
            new_car_log.time_begin = datetime.now()
            db.session.add(new_car_log)
            db.session.commit()

        # if value == 'free':
        if request.form.get('free') == 'free':
            new_car_log = db.session.query(Car_Log).filter(Car_Log.car_id == car_id).order_by(
                Car_Log.time_begin.desc()).first()

            car.availability = 1

            new_car_log.time_end = datetime.now()
            new_car_log.time_sum = new_car_log.time_end - new_car_log.time_begin
            new_car_log.time_sum = int(new_car_log.time_sum.seconds / 60)
            new_car_log.cost = new_car_log.time_sum * car.price_per_minute / 60
            db.session.commit()

            print(new_car_log.car_id)
            print(new_car_log.time_begin)
            print(new_car_log.time_end)
            print(new_car_log.time_sum)


        return redirect(url_for('auto_detail', car_id=car.car_id))


    context = {
        'car_id': car.car_id,
        'name': car.name,
        'description': car.description,
        'price_per_minute': car.price_per_minute,
        'cars_transmition': car.cars_transmition,
        # 'image': car.image,
        'availability': car.availability,
        'car_log': car_log,
        'form': form
    }
    return render_template('auto_detail.html', **context)


@app.route('/add-car', methods=['POST', 'GET'])
def create_auto():
    form = CarCreationForm()
    if form.validate_on_submit():
        new_car = Car()
        new_car.name = form.name.data
        new_car.description = form.description.data
        new_car.price_per_minute = str(form.price_per_minute.data)
        new_car.cars_transmition = form.cars_transmition.data
        new_car.availability = True

        if 'Manual' in new_car.cars_transmition:
            new_car.cars_transmition = False
        else:
            new_car.cars_transmition = True

        file = form.logo.data
        print(file)
        if allowed_file(file):
            logo = f'images/cars/{file}'
            print(logo)
            file.save(os.path.join(app.config['STATIC_ROOT'], logo))
            new_car.logo = logo

        if ',' in new_car.price_per_minute:
            new_car.price_per_minute = new_car.price_per_minute.replace(',', '.')

        db.session.add(new_car)

        db.session.commit()

        return redirect(url_for('auto_detail', car_id=new_car.car_id))

    return render_template('auto_create.html', form=form)


@app.route('/rental_log', methods=['POST', 'GET'])
def rental_log():
    total_list = db.session.query(Car.image, Car.name, Car_Log.rent_id, Car_Log.time_begin, Car_Log.time_end,
                                  Car_Log.cost).outerjoin(Car_Log, Car.car_id == Car_Log.car_id).all()
    rental_obj = db.session.query(Car.image, Car.name, db.func.count(Car_Log.rent_id).label('rent_count'),
                                  db.func.sum(Car_Log.cost).label('rent_cost')).outerjoin(Car_Log,
                                                                                          Car.car_id == Car_Log.car_id).group_by(
        Car.name).all()

    list_el = []
    for row in rental_obj:
        el = row._asdict()
        list_el.append(el)

    rental_dict = {}

    for element in total_list:
        if (element.time_begin and element.time_end) is None:
            pass
        else:
            if element.name in rental_dict:
                rental_dict[element.name] += int(((element.time_end - element.time_begin).total_seconds())) / 60
            else:
                rental_dict[element.name] = int(((element.time_end - element.time_begin).total_seconds())) / 60
    context = {
        'list_el': list_el,
        'rental_dict': rental_dict,
    }
    return render_template('rental_log.html', **context)
