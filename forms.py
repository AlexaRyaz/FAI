from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FloatField, SelectField
from wtforms.fields import TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(message="Это поле обязательно"), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(message="Это поле обязательно"), Email(message="Введите корректный email")])
    password = PasswordField('Пароль', validators=[DataRequired(message="Это поле обязательно")])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(message="Это поле обязательно"), EqualTo('password', message="Пароли должны совпадать")])
    submit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message="Это поле обязательно"), Email(message="Введите корректный email")])
    password = PasswordField('Пароль', validators=[DataRequired(message="Это поле обязательно")])
    submit = SubmitField('Войти')

class TravelFormForm(FlaskForm):
    departure_icao = SelectField('Аэропорт вылета', choices=[], validators=[DataRequired(message="Это поле обязательно")])
    arrival_icao = SelectField('Аэропорт прилета', choices=[], validators=[DataRequired(message="Это поле обязательно")])
    intermediate_points = TextAreaField('Промежуточные точки', validators=[Optional()])
    departure_time = TimeField('Время отправления', format='%H:%M', validators=[Optional()])
    arrival_time = TimeField('Время прибытия', format='%H:%M', validators=[Optional()])
    flight_number = StringField('Номер рейса', validators=[Optional()])
    hotel_name = StringField('Название гостиницы', validators=[Optional()])
    cost = FloatField('Стоимость', validators=[Optional()])
    currency = SelectField('Валюта', choices=[
        ('USD', 'USD - Доллар США'),
        ('EUR', 'EUR - Евро'),
        ('RUB', 'RUB - Российский рубль'),
        ('GBP', 'GBP - Фунт стерлингов'),
        ('JPY', 'JPY - Японская йена'),
    ], validators=[Optional()])
    timezone = StringField('Временная зона', validators=[Optional()])
    base_currency = SelectField('Базовая валюта', choices=[
        ('USD', 'USD - Доллар США'),
        ('EUR', 'EUR - Евро'),
        ('RUB', 'RUB - Российский рубль'),
        ('GBP', 'GBP - Фунт стерлингов'),
        ('JPY', 'JPY - Японская йена'),
    ], validators=[Optional()])
    submit = SubmitField('Отправить')

    def __init__(self, airports, *args, **kwargs):  # Добавляем airports в конструктор
        super(TravelFormForm, self).__init__(*args, **kwargs)
        self.departure_icao.choices = [(airport['icao'], f"{airport['name']} ({airport['icao']})") for airport in airports]
        self.arrival_icao.choices = [(airport['icao'], f"{airport['name']} ({airport['icao']})") for airport in airports]