from flask import url_for

from app import db
from datetime import datetime


class Car(db.Model):
    car_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(250))
    price_per_minute = db.Column(db.Float(9, 2))
    cars_transmition = db.Column(db.Boolean, default=1)
    # images = db.relationship('Images', backref='car', cascade='all,delete')
    image = db.Column(db.String())
    availability = db.Column(db.Boolean, default=1)
    logo = db.Column(db.String())

    def get_absolute_url(self):
        return url_for('auto_detail', id=self.id)


class Car_Log(db.Model):
    rent_id = db.Column(db.Integer, primary_key = True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.car_id'))
    time_begin = db.Column(db.DateTime, default = datetime.now)
    time_end = db.Column(db.DateTime)
    time_sum = db.Column(db.Float())
    cost = db.Column(db.Float)


class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.car_id'))
    file = db.Column(db.String(200))

    def __repr__(self):
        return self.file
