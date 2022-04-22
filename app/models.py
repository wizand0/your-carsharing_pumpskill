from datetime import datetime

from flask import url_for

from app import db


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(250))
    price_per_minute = db.Column(db.Float(9, 2))
    cars_transmition = db.Column(db.String(20))
    # images = db.relationship('Images', backref='car', cascade='all,delete')
    image = db.Column(db.String())
    created = db.Column(db.DateTime, default=datetime.now())
    availability = db.Column(db.Boolean, default=True)
    total_time = db.Column(db.Float)
    total_rent = db.Column(db.Float)

    def __repr__(self):
        return self.name

    def logo_url(self):
        return f'/static/{self.image}' if self.image else ''

    def get_absolute_url(self):
        return url_for('car_detail', id=self.id)


pr = db.relationship('Journal', backref='car')


class Car_Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    time_begin = db.Column(db.DateTime, default=datetime.utcnow)
    time_end = db.Column(db.DateTime, default=datetime.utcnow)
    total_cost = db.Column(db.Integer, default=1)


class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    file = db.Column(db.String(200))

    def __repr__(self):
        return self.file


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    users_car = db.relationship('UsersCars', backref='user', cascade='all,delete')

    def __repr__(self):
        return self.name


class UsersCars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))