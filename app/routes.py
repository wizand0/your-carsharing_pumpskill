
from app import app, db
from app.models import Car, Car_Log
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



@app.route('/auto-detail/<item_id>', methods=['GET', 'POST'])
def item_detail(car_id):
    car = Car.query.get(car_id)
    form = AddToCartForm()
    if form.validate_on_submit():
        car_to_rent = Car_Log()
        car_to_rent.user = get_user()   # !!!!!!!!!!!!!!!!!!!!!!!!!!!
        car_to_rent.car = car
        db.session.add(car_to_rent)
        db.session.commit()
        return redirect(url_for('cart'))
    return render_template('auto_detail.html', car=car, form=form)



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

        if form.files.data:
            file_names = []
            files = request.files.getlist(form.files.name)
            for num, file in enumerate(files):
                file_content = file.stream.read()
                _, ext = os.path.splitext(file.filename)
                filename = "Post{}-{}{}".format(new_car.id, str(num), str(ext).lower())
                with open(os.path.join(app.root_path, 'static\images', filename), 'wb') as f:
                    f.write(file_content)
                    file_names.append(filename)
            new_car.images = file_names


        # files = form.files.data
        # for file in files:
        #     with open(os.path.join(app.config['STATIC_ROOT'], file), 'wb') as f:
        #         f.write(file.read())

        # media_file = []
        # for file in form.files.data:
        #     if file.filename:
        #         media_file.append(save_media(file))

        #success_url = url_for('auto_detail', new_car_id=new_car.id)

        db.session.add(new_car)
        db.session.commit()

        #return render_template('auto_detail.html', new_car=new_car, form=form)
        return redirect(url_for('add_car'))
    return render_template('auto_create.html', form=form)
