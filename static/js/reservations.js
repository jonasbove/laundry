function cancelReservation(event) {
    reservation_id = event.target.dataset.id;
    const data = {
        reservation_id: reservation_id,
    };
    fetch('/delete_reservation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        location.reload(true);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function cancelAllReservations() {
    apartment_number = localStorage.getItem('apartment');
    const data = {
        apartment: apartment_number,
    };
    fetch('/delete_reservations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        location.reload(true);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}