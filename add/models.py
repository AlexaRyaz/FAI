from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class TravelForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    departure_icao = db.Column(db.String(4), nullable=False)
    arrival_icao = db.Column(db.String(4), nullable=False)
    intermediate_points = db.Column(db.Text)
    departure_time_local = db.Column(db.String(5))  # Время отправления в локальной временной зоне (формат HH:MM)
    arrival_time_local = db.Column(db.String(5))   # Время прибытия в локальной временной зоне (формат HH:MM)
    departure_timezone = db.Column(db.String(50))  # Временная зона отправления
    arrival_timezone = db.Column(db.String(50))    # Временная зона прибытия
    flight_number = db.Column(db.String(50))
    hotel_name = db.Column(db.String(100))
    cost = db.Column(db.Float)  # Стоимость этапа
    currency = db.Column(db.String(3))  # Код валюты (например, USD, EUR, RUB)
    base_currency = db.Column(db.String(3))  # Базовая валюта для расчета

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
