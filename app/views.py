from flask import render_template

from app import app
from app.models import Car


@app.route('/index')
@app.route('/')
def index():
    car_list = Car.query.all()
    context = {'car_list': car_list}
    return render_template('index.html', **context)

    context = {
        'brands_list': brands_list,
        'items_list': items_list,
    }
    return render_template('index.html', **context)