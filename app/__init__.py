from flask import Flask  # Импортируем класс Flask из модуля flask
from flask_sqlalchemy import SQLAlchemy  # Импортируем расширение для работы с SQLAlchemy
from flask_login import LoginManager  # Импортируем менеджер для управления аутентификацией и авторизацией пользователей
import os  # Импортируем модуль os для работы с операционной системой

app = Flask(__name__)  # Создаём экземпляр приложения Flask

# Устанавливаем секретный ключ для приложения, который используется для подписи сессий
app.config['SECRET_KEY'] = 'cemerinANDchon'

# Указываем URI базы данных, которую будем использовать
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Отключаем отслеживание модификаций в SQLAlchemy, чтобы избежать лишних уведомлений
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Устанавливаем API-ключ для работы с TimezoneDB
app.config['TIMEZONEDB_API_KEY'] = 'HWO1KKUC1SOK'

db = SQLAlchemy(app)  # Инициализируем расширение SQLAlchemy для работы с базой данных

login_manager = LoginManager(app)  # Инициализируем менеджер для управления логином
login_manager.login_view = 'login'  # Указываем вид (view), который будет использоваться для входа в систему

from app import routes, models  # Импортируем модули с маршрутами и моделями
