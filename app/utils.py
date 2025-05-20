import requests
from datetime import datetime
import pytz

def convert_time(time_str, from_tz, to_tz):
    if not time_str or not from_tz or not to_tz:
        return time_str

    try:
        # Преобразуем строку времени в объект datetime
        time_obj = datetime.strptime(time_str, '%H:%M')
        # Устанавливаем исходную временную зону
        from_zone = pytz.timezone(from_tz)
        time_obj = from_zone.localize(time_obj)
        # Конвертируем в целевую временную зону
        to_zone = pytz.timezone(to_tz)
        time_obj = time_obj.astimezone(to_zone)
        # Возвращаем время в формате 'HH:MM'
        return time_obj.strftime('%H:%M')
    except Exception as e:
        print(f"Ошибка конвертации времени: {e}")
        return time_str

def get_exchange_rates(base_currency="USD"):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['rates']
    else:
        return None

def convert_currency(amount, from_currency, to_currency):
    rates = get_exchange_rates(base_currency=from_currency)
    if rates and to_currency in rates:
        return amount * rates[to_currency]
    return None

def get_timezone(city, api_key):
    url = f"http://api.timezonedb.com/v2.1/get-time-zone"
    params = {
        "key": api_key,
        "format": "json",
        "by": "city",
        "city": city
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('zoneName')
    return None

def calculate_total_cost(forms, base_currency):
    total_cost = 0
    for form in forms:
        if form.currency != base_currency:
            converted_cost = convert_currency(form.cost, form.currency, base_currency)
            if converted_cost:
                total_cost += converted_cost
        else:
            total_cost += form.cost
    return round(total_cost, 2)
