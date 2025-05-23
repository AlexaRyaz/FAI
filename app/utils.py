import requests
from datetime import datetime
import pytz


def convert_time(time_str, from_tz, to_tz):
    """Конвертирует время между временными зонами"""
    if not time_str or not from_tz or not to_tz:
        return time_str

    try:
        # Создаем datetime объект с фиктивной датой (2000-01-01)
        dt_naive = datetime.strptime(time_str, '%H:%M')
        dt_with_date = datetime(2000, 1, 1, dt_naive.hour, dt_naive.minute)

        # Устанавливаем исходную и целевую временные зоны
        from_zone = pytz.timezone(from_tz)
        to_zone = pytz.timezone(to_tz)

        # Локализуем время и конвертируем
        dt_from = from_zone.localize(dt_with_date)
        dt_to = dt_from.astimezone(to_zone)

        return dt_to.strftime('%H:%M')
    except Exception as e:
        print(f"Ошибка конвертации времени: {e}")
        return time_str


def get_exchange_rates(base_currency="USD"):
    """Получает текущие курсы валют с API"""
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['rates']
    else:
        return None


def convert_currency(amount, from_currency, to_currency):
    """Конвертирует сумму между валютами"""
    if amount is None:
        return 0
    rates = get_exchange_rates(base_currency=from_currency)
    if rates and to_currency in rates:
        return amount * rates[to_currency]
    return 0


def calculate_total_cost(forms, selected_currency):
    """Считает общую стоимость всех форм в выбранной валюте"""
    total_cost = 0
    for form in forms:
        if form.cost is None:
            continue
        converted = convert_currency(form.cost, form.currency, selected_currency)
        if converted is not None:
            total_cost += converted
    return round(total_cost, 2)
