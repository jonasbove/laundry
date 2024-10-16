from flask import Flask, render_template, request, jsonify, send_from_directory
from models import SessionLocal
from models.reservation import Reservation

app = Flask(__name__)
session = SessionLocal()

@app.route("/")
def index():
    return render_template('index.html', active='index')

@app.route("/booking")
def booking():
    reservations = session.query(Reservation).all()
    reservations_data = [
        {
            'interval': reservation.interval,
            'day': reservation.day,
            'machine': reservation.machine,
            'apartment': reservation.apartment
        }
        for reservation in reservations
    ]
    return render_template('booking.html', active='booking', reservations=reservations, reservations_data=reservations_data)

@app.route("/reservations")
def reservations():
    reservations = session.query(Reservation).all()
    return render_template('reservations.html', active='reservations', reservations=reservations)

@app.route('/save_reservations', methods=['POST'])
def save_reservations():
    data = request.json
    apartment = data.get('apartment')
    reservations = data.get('reservations')
    
    print(reservations)
    for reservation in reservations:
        new_reservation = Reservation(interval=reservation['interval'], day=reservation['day'], machine=reservation['machine'], apartment=apartment)
        session.add(new_reservation)
    session.commit()
    return jsonify({'status': 'success', 'message': 'Reservations saved'}), 200

@app.route("/robots.txt")
def robots_txt():
    return send_from_directory(app.static_folder, "robots.txt")

if __name__ == '__main__':
    app.run(debug=True)