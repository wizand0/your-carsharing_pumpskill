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


@app.route('/auto_detail/<id>', methods=['GET', 'POST'])
def car_detail(id):
    car = Car.query.get(id)
    # form = AddToCartForm()
    # if form.validate_on_submit():
    #     car_to_rent = Car_Log()
    #     car_to_rent.user = get_user()   # !!!!!!!!!!!!!!!!!!!!!!!!!!!
    #     car_to_rent.car = car
    #     db.session.add(car_to_rent)
    #     db.session.commit()
    #     return redirect(url_for('cart'))
    return render_template('auto_detail.html', car=car)  # , form=form


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

        file = form.files.data
        if allowed_file(file.filename):
            image = f'images/cars/{file.filename}'
            file.save(os.path.join(app.config['STATIC_ROOT'], image))
            new_car.image = image


        # image = f'images/{file.filename}'
        # file.save(os.path.join(app.config['STATIC_ROOT'], image))
        # new_car.image = image

        db.session.add(new_car)
        db.session.commit()


        return redirect(url_for('auto_detail', id=form.new_car.data))
    return render_template('auto_create.html', form=form)

        #success_url = url_for('car_detail', id=id)

    #db.session.add(new_car)


        # if form.files.data:
        #     file_names = []
        #     files = request.files.getlist(form.files.name)
        #     for num, file in enumerate(files):
        #         file_content = file.stream.read()
        #         _, ext = os.path.splitext(file.filename)
        #         filename = "Post{}-{}{}".format(new_car.id, str(num), str(ext).lower())
        #         with open(os.path.join(app.root_path, 'static\images', filename), 'wb') as f:
        #             f.write(file_content)
        #             file_names.append(filename)
        #     new_car.images = file_names

        # files = form.files.data
        # for file in files:
        #     with open(os.path.join(app.config['STATIC_ROOT'], file), 'wb') as f:
        #         f.write(file.read())

        # media_file = []
        # for file in form.files.data:
        #     if file.filename:
        #         media_file.append(save_media(file))

