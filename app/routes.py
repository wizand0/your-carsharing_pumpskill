from datetime import datetime, timedelta

from app import app, db
from app.models import Car, Car_Log
from flask import render_template, request, redirect, url_for

import os

from app.models import Car
from app.forms import CarCreationForm


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
    car_Log = Car_Log.query.filter_by(car_id=car_id).all()
    check_transmission = None
    check_status = None
    if car.cars_transmition == True:
        check_transmission = 'Автомат'
    elif car.cars_transmition == False:
        check_transmission = 'Механика'

    if car.availability == True:
        check_status = 'Свободен'
    else:
        check_status = 'Занят'

    if request.method == 'POST':
        if request.form.get("delete"):
            db.session.delete(car)
            for one_log in car_Log:
                db.session.delete(one_log)
            db.session.commit()
            return redirect(url_for('index'))

        if request.form.get("change"):
            new_name = request.form['new_name']
            new_description = request.form['new_description']
            new_price = request.form['new_price']
            new_transmission = request.form['new_transmission']
            new_image = request.form['new_image_url']

            if new_name:
                car.name = request.form['new_name']
            if new_description:
                car.description = request.form['new_description']
            if new_price:
                car.price_per_minute = request.form['new_price']
            if new_transmission:
                car.cars_transmition = int(request.form['new_transmission'])
            if new_image:
                car.image = request.form['new_image_url']

            db.session.commit()


        if request.form.get("rent"):
            if request.method == 'POST':
                if car.status:
                    check_status = 'Занят'
                    Car.query.filter_by(id=car_id).update({"status": 0})
                    db.session.add(Car_Log(car_id=car_id, rent_start=datetime.now() + timedelta(hours=3)))
                    db.session.commit()

        if request.form.get("free"):
            if request.method == 'POST':
                if not car.availability:
                    Car.query.filter_by(car_id=car_id).update({"availability": 1})
                    for one_log in car_Log:
                        if one_log.time_end is None:
                            car_Log.time_end = datetime.now() + timedelta(hours=3)
                            count_date_sec = (one_log.time_end - one_log.time_begin).seconds
                            count_date = divmod(count_date_sec, 60)
                            cost = car.price_per_minute * count_date[0] + car.price_per_minute / 60 * count_date[1]
                            one_log.cost = cost
                            db.session.commit()

    context = {
        'car_id': car.car_id,
        'name': car.name,
        'description': car.description,
        'price_per_minute': car.price_per_minute,
        'cars_transmition': car.cars_transmition,
        'image': car.image,
        'status': car.availability,
        'car_Log': car_Log,
    }
    return render_template('auto_detail.html', **context)
    # return render_template('auto_detail.html', car=car)


@app.route('/add-car', methods=['POST', 'GET'])
def create_auto():
    form = CarCreationForm()
        #   form.car.choices = [(car.id, car.name) for car in Car.query.all()]
    if form.validate_on_submit():
        new_car = Car()
        new_car.name = form.name.data
        new_car.description = form.description.data
        new_car.price_per_minute = str(form.price_per_minute.data)
        new_car.cars_transmition = form.cars_transmition.data
        new_car.availability = form.availability.data

        if 'Автоматическая' in new_car.cars_transmition:
            new_car.cars_transmition = True
        else:
            new_car.cars_transmition = False





    # if request.method == 'POST':
    #     name = request.form['name']
    #     description = request.form['description']
    #     price = str(request.form['price'])
    #     transmission = int(request.form['transmission'])

        if ',' in new_car.price_per_minute:
            new_car.price_per_minute =  new_car.price_per_minute.replace(',', '.')

        float_price = float( new_car.price_per_minute)

        db.session.add(Car(name=new_car.name, description=new_car.description, price_per_minute=float_price, cars_transmition=new_car.cars_transmition))
        db.session.commit()
        return redirect(url_for('index'))

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















# @app.route('/auto_detail/<id>', methods=['GET', 'POST'])
# def car_detail(id):
#     car = Car.query.get(id)
#     # form = AddToCartForm()
#     # if form.validate_on_submit():
#     #     car_to_rent = Car_Log()
#     #     car_to_rent.user = get_user()   # !!!!!!!!!!!!!!!!!!!!!!!!!!!
#     #     car_to_rent.car = car
#     #     db.session.add(car_to_rent)
#     #     db.session.commit()
#     #     return redirect(url_for('cart'))
#     return render_template('auto_detail.html', car=car)  # , form=form
#
#
# @app.route('/add-car', methods=['GET', 'POST'])
# def add_car():
#     form = CarCreationForm()
#     #   form.car.choices = [(car.id, car.name) for car in Car.query.all()]
#     if form.validate_on_submit():
#         new_car = Car()
#         new_car.name = form.name.data
#         new_car.description = form.description.data
#         new_car.price_per_minute = form.price_per_minute.data
#         new_car.cars_transmition = form.cars_transmition.data
#         new_car.availability = form.availability.data
#
#         file = form.files.data
#         if allowed_file(file.filename):
#             image = f'images/cars/{file.filename}'
#             file.save(os.path.join(app.config['STATIC_ROOT'], image))
#             new_car.image = image
#
#
#         # image = f'images/{file.filename}'
#         # file.save(os.path.join(app.config['STATIC_ROOT'], image))
#         # new_car.image = image
#
#         db.session.add(new_car)
#         db.session.commit()
#
#
#         return redirect(url_for('auto_detail', id=form.new_car.data))
#     return render_template('auto_create.html', form=form)
#
#         #success_url = url_for('car_detail', id=id)
#
#     #db.session.add(new_car)
#
#
#         # if form.files.data:
#         #     file_names = []
#         #     files = request.files.getlist(form.files.name)
#         #     for num, file in enumerate(files):
#         #         file_content = file.stream.read()
#         #         _, ext = os.path.splitext(file.filename)
#         #         filename = "Post{}-{}{}".format(new_car.id, str(num), str(ext).lower())
#         #         with open(os.path.join(app.root_path, 'static\images', filename), 'wb') as f:
#         #             f.write(file_content)
#         #             file_names.append(filename)
#         #     new_car.images = file_names
#
#         # files = form.files.data
#         # for file in files:
#         #     with open(os.path.join(app.config['STATIC_ROOT'], file), 'wb') as f:
#         #         f.write(file.read())
#
#         # media_file = []
#         # for file in form.files.data:
#         #     if file.filename:
#         #         media_file.append(save_media(file))
#
