from flask import Flask, render_template, session, current_app, request, redirect, jsonify, send_from_directory, make_response
from models import SessionLocal
from models.reservation import Reservation
from datetime import datetime, time, timedelta
from user_agents import parse
import locale as pylocale
import secrets
import json
import pytz
import os
from dotenv import load_dotenv

load_dotenv('.env')
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.jinja_env.cache = {}
db_session = SessionLocal()
PASSWORD = os.getenv('PASSWORD')
SUPPORTED_LOCALES = ['en', 'da']

# Internal functions
def reservation_to_dict(reservation):
    return {
        'day': reservation.day,
        'interval': reservation.interval,
        'machine': reservation.machine,
        'apartment': reservation.apartment,
        'week': reservation.week,
    }

def get_week_dates(timezone, target_week):
    now = datetime.now(timezone)
    current_week = now.isocalendar()[1]
    week_diff = target_week - current_week
    current_monday = now - timedelta(days=now.weekday())
    target_monday = current_monday + timedelta(weeks=week_diff)
    target_sunday = target_monday + timedelta(days=6)
    locale = get_locale()
    if locale == 'da':
        pylocale.setlocale(pylocale.LC_TIME, 'da_DK.UTF-8')
        formatted_monday = target_monday.strftime("%d. %B")
        formatted_sunday = target_sunday.strftime("%d. %B")
    else:
        pylocale.setlocale(pylocale.LC_TIME, 'en_US.UTF-8')
        formatted_monday = target_monday.strftime("%B %d")
        formatted_sunday = target_sunday.strftime("%B %d")
    pylocale.setlocale(pylocale.LC_TIME, 'C')
    return formatted_monday, formatted_sunday

def get_weekday_date(timezone, target_week, target_day):
    now = datetime.now(timezone)
    current_week = now.isocalendar()[1]
    year = now.year
    if target_week < current_week:
        year += 1
    target_date = datetime.fromisocalendar(year, target_week, 1).replace(tzinfo=timezone)
    target_date += timedelta(days=target_day)
    locale = get_locale()
    if locale == 'da':
        pylocale.setlocale(pylocale.LC_TIME, 'da_DK.UTF-8')
        formatted_day = target_date.strftime("%d. %B")
    else:
        pylocale.setlocale(pylocale.LC_TIME, 'en_US.UTF-8')
        formatted_day = target_date.strftime("%B %d")
    pylocale.setlocale(pylocale.LC_TIME, 'C')
    return formatted_day
    
def week_cap(current_week: int, week: int):
    if (week > current_week+2):
        week = current_week+2
    if (week < current_week-2):
        week = current_week-2
    return week

def get_locale():
    locale = session.get('locale', 'en')
    return locale
   
def is_mobile_user():
    user_agent = request.headers.get('User-Agent')
    parsed_user_agent = parse(user_agent)
    if parsed_user_agent.is_mobile:
        return True
    else:
        return False
    
def session_check():
        check = True
        if 'locale' not in session:
            check = False
        return check
# Routes
@app.route("/")
def index():
    if 'authorized' in session:
        return render_template('index.html', active='index')
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.json.get('password')
        
        if password == PASSWORD:
            session['authorized'] = True
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Incorrect password'}), 401
    
    return render_template('login.html')

@app.route("/booking")
def booking():
    if 'authorized' in session:
        timezone = pytz.timezone('Europe/Copenhagen')
        current_week = datetime.now(timezone).isocalendar()[1]
        week = week_cap(int(current_week), int(request.args.get('week', default=current_week, type=int)))
        reservations = db_session.query(Reservation).all()
        apartment = session.get('apartment', False)
        timezone = pytz.timezone('Europe/Copenhagen')
        week_start, week_end = get_week_dates(timezone, week)
        user_agent = request.headers.get('User-Agent')
        parsed_user_agent = parse(user_agent)
        if parsed_user_agent.is_mobile:
            today = int(datetime.now(timezone).isoweekday())
            day = int(request.args.get('day', default=today, type=int))
            date = get_weekday_date(timezone, week, day)
            
            return render_template('booking_mobile.html', active='booking', reservations=reservations, week=week, current_week=current_week, week_start=week_start, week_end=week_end, apartment=apartment, locale=get_locale(), session=session_check(), day=day, date=date)
        return render_template('booking.html', active='booking', reservations=reservations, week=week, week_start=week_start, week_end=week_end, apartment=apartment, locale=get_locale(), session=session_check())
    else:
        return redirect('/login')

@app.route("/reservations")
def reservations():
    if 'authorized' in session:
        apartment = session.get('apartment')
        if apartment:
            reservations = db_session.query(Reservation).order_by(Reservation.week, Reservation.day, Reservation.interval).filter(Reservation.apartment == apartment).all()
        else:
            return redirect('/booking')
        return render_template('reservations.html', active='reservations', reservations=reservations, apartment=apartment)
    else:
        return redirect('/login')
   
@app.route("/settings")
def settings():
    if 'authorized' in session:
        user_agent = request.headers.get('User-Agent')
        parsed_user_agent = parse(user_agent)
        if parsed_user_agent.is_mobile:
            apartment = session.get('apartment')
            return render_template('settings_mobile.html', apartment=apartment, active='settings')
        else:
            return 'Not made yet, lol 🤣'
    else:
        return redirect('/login')

@app.route("/robots.txt")
def robots_txt():
    return send_from_directory(app.static_folder, "robots.txt")

# Setters and getters
@app.route('/save_reservations', methods=['POST'])
def save_reservations():
    if 'authorized' in session:
        data = request.json
        week = data.get('week')
        apartment = data.get('apartment')
        reservations = data.get('reservations')
        session['apartment'] = apartment
        
        for reservation in reservations:
            new_reservation = Reservation(interval=reservation['interval'], day=reservation['day'], machine=reservation['machine'], apartment=apartment, week=week)
            db_session.add(new_reservation)
        db_session.commit()
        return jsonify({'status': 'success', 'message': 'Reservations saved'}), 200
    else:
        return redirect('/login')

@app.route('/delete_reservation', methods=['POST'])
def delete_reservation():
    if 'authorized' in session:
        data = request.json
        reservation_id = data.get('reservation_id')
        reservation = db_session.query(Reservation).filter(Reservation.id == reservation_id).first()
        db_session.delete(reservation)
        db_session.commit()
        return jsonify({'status': 'success', 'message': f'Reservation with ID {reservation_id} removed'}), 200
    else:
        return redirect('/login')
    
@app.route('/delete_reservations', methods=['POST'])
def delete_reservations():
    if 'authorized' in session:
        data = request.json
        apartment = data.get('apartment')
        db_session.query(Reservation).filter(Reservation.apartment == apartment).delete()
        db_session.commit()
        return jsonify({'status': 'success', 'message': f'Reservations from apartment {apartment} removed'}), 200
    else:
        return redirect('/login')
    
@app.route('/set-locale', methods=['POST'])
def set_locale():
    if 'authorized' in session: 
        data = request.get_json()
        locale = data.get('locale', 'en')

        session['locale'] = locale

        return jsonify({'locale': locale})
    else:
        return redirect('/login')

@app.route('/set-apartment', methods=['POST'])
def set_apartment():
    if 'authorized' in session:
        data = request.get_json()
        apartment = data.get('apartment', False)

        if apartment:
            session['apartment'] = apartment
            
        return jsonify({'apartment': apartment})
    else:
        return redirect('/login')

# API
@app.route('/api/reservations')
def reservations_api():
    if 'authorized' in session:    
        reservations = db_session.query(Reservation).all()
        reservations_list = [reservation_to_dict(r) for r in reservations]
        return jsonify(reservations_list)
    else:
        return redirect('/login')

@app.route('/api/reservations/<int:week>')
def reservations_week_api(week):
    if 'authorized' in session:  
        reservations = db_session.query(Reservation).filter(Reservation.week == week).all()
        reservations_list = [reservation_to_dict(r) for r in reservations]
        return jsonify(reservations_list)
    else:
        return redirect('/login')

@app.route('/api/preferences')
def preferences_api():
    return 'Not implemented yet 😢'

# Template filters
@app.template_filter('format_time')
def format_time_filter(value):
    locale = get_locale()
        
    if isinstance(value, int):
        value = time(value, 0).strftime("%H:%M")
        
    if isinstance(value, str):
        value = datetime.strptime(value, "%H:%M").time()

    if isinstance(value, time):
        if locale == 'da':
            formatted_time = value.strftime("%H:%M")
        else:
            formatted_time = value.strftime("%I %p")

    return formatted_time

@app.template_filter('format_interval')
def format_interval_filter(value, position=None):
    locale = get_locale()
    start = time(int(value), 0).strftime("%H:%M")
    end = time((int(value)+1)%24, 0).strftime("%H:%M")
    
    if locale != 'da':
        start = time(int(value), 0).strftime("%I %p")
        end = time((int(value)+1)%24, 0).strftime("%I %p")
    if position == 'start':
        return start
    elif position == 'end':
        return end
    return f'{start} - {end}'

@app.template_filter('format_day')
def format_day_filter(day, **kwargs):
    locale = get_locale()
    formatted_day = localize(day+24, locale=locale)
    return formatted_day

@app.template_filter('format_week_interval')
def format_week_interval(week, position=None):
    timezone = pytz.timezone('Europe/Copenhagen')
    week_start, week_end = get_week_dates(timezone, week)
        
    if position == 'start':
        return week_start
    elif position == 'end':
        return week_end
    else:
        return week_start, week_end
    
@app.template_filter('localize')
def localize(number, **kwargs):
    locale = get_locale()
    locale_file_path = f'locales/{locale}.json'

    try:
        with current_app.open_resource(locale_file_path) as locale_file:
            locale_data = json.load(locale_file)
    except FileNotFoundError:
        with current_app.open_resource('locales/en.json') as locale_file:
            locale_data = json.load(locale_file)

    localized_text = locale_data.get(str(number), f"Missing text for {number}")

    if isinstance(localized_text, str):
        return localized_text.format(**kwargs)

    return localized_text

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)