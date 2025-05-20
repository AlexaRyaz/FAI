from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db
from app.forms import RegistrationForm, LoginForm, TravelFormForm
from app.models import User, TravelForm
from flask_login import login_user, current_user, logout_user, login_required
from app.utils import convert_currency, calculate_total_cost, get_timezone, convert_time
from app.airports import airports
import pytz
from datetime import datetime

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Ваш аккаунт успешно создан! Теперь вы можете войти.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Ошибка входа. Проверьте email и пароль.', 'danger')
    return render_template('login.html', title='Вход', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    forms = TravelForm.query.filter_by(user_id=current_user.id).all()
    selected_currency = request.args.get('currency', 'USD')  # По умолчанию USD
    return render_template(
        'dashboard.html',
        title='Личный кабинет',
        forms=forms,
        selected_currency=selected_currency,
        convert_currency=convert_currency,
        calculate_total_cost=calculate_total_cost,
        convert_time=convert_time  # Передаем функцию конвертации времени
    )

@app.route('/create_form', methods=['GET', 'POST'])
@login_required
def create_form():
    form = TravelFormForm(airports=airports)
    if form.validate_on_submit():
        # Определяем временные зоны для аэропортов отправления и прибытия
        departure_airport = next((airport for airport in airports if airport['icao'] == form.departure_icao.data), None)
        arrival_airport = next((airport for airport in airports if airport['icao'] == form.arrival_icao.data), None)

        departure_timezone = departure_airport['timezone'] if departure_airport else None
        arrival_timezone = arrival_airport['timezone'] if arrival_airport else None

        # Сохраняем время в локальной временной зоне
        departure_time_local = form.departure_time.data.strftime('%H:%M') if form.departure_time.data else None
        arrival_time_local = form.arrival_time.data.strftime('%H:%M') if form.arrival_time.data else None

        travel_form = TravelForm(
            user_id=current_user.id,
            departure_icao=form.departure_icao.data,
            arrival_icao=form.arrival_icao.data,
            intermediate_points=form.intermediate_points.data,
            departure_time_local=departure_time_local,  # Сохраняем время в локальной временной зоне
            arrival_time_local=arrival_time_local,      # Сохраняем время в локальной временной зоне
            departure_timezone=departure_timezone,      # Временная зона отправления
            arrival_timezone=arrival_timezone,          # Временная зона прибытия
            flight_number=form.flight_number.data,
            hotel_name=form.hotel_name.data,
            cost=form.cost.data,
            currency=form.currency.data,
            base_currency=form.base_currency.data
        )
        db.session.add(travel_form)
        db.session.commit()
        flash('Ваша форма успешно отправлена!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('create_form.html', title='Создать форму', form=form)

@app.route('/delete_form/<int:form_id>', methods=['POST'])
@login_required
def delete_form(form_id):
    form = TravelForm.query.get_or_404(form_id)
    if form.user_id != current_user.id:
        abort(403)
    db.session.delete(form)
    db.session.commit()
    flash('Ваша форма успешно удалена!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/set_currency', methods=['POST'])
@login_required
def set_currency():
    selected_currency = request.form.get('selected_currency', 'USD')
    return redirect(url_for('dashboard', currency=selected_currency))
