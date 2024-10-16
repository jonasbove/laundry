let reservations = [];

function addSlot(event) {
    const slot = event.target;
    const interval = slot.dataset.interval;
    const machine = slot.dataset.machine;
    const day = slot.dataset.day;

    const reservation = { interval, machine, day };
    const index = reservations.findIndex(
        item => item.interval === interval && item.machine === machine && item.day === day
    );

    if (index === -1) {
        reservations.push(reservation);
        slot.style.backgroundColor = "#4488ff";
    } else {
        reservations.splice(index, 1);
        slot.style.backgroundColor = "";
    }

    const book = document.getElementById('book');
    if (reservations.length === 0) {
        book.classList.remove('greenlit');
    } else {
        book.classList.add('greenlit')
    }
}

function validateApartment() {
    const apartment = document.getElementById('apartment')
    if (apartment.value < apartment.min || apartment.value > apartment.max) {
        alert(`Please enter an apartment number between ${apartment.min} and ${apartment.max}.`);
        return false;
    } else {
        return true;
    }
}

function bookSlots() {
    const apartment = document.getElementById('apartment').value;
    if (reservations.length === 0) {
        alert("You haven't selected any reservation slots.");
    }
    else if (apartment === '') {
        alert("You haven't typed in your apartment number.");
    } else if (validateApartment(apartment)) {
        const data = {
            apartment: apartment,
            reservations: reservations
        };
        fetch('/save_reservations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data   )
        })
        .then(response => response.json())
        .then(data => {
            alert('Reservations saved successfully');
            console.log('Success:', data);
            location.reload(true);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
}

function updateReservedSlots(data) {
    data.forEach(function(reservation) {
        const selector = `.slot[data-interval="${reservation.interval}"][data-machine="${reservation.machine}"][data-day="${reservation.day}"]`;
        const slot = document.querySelector(selector);

        if (slot) {
            slot.classList.add('reserved');
            slot.textContent = reservation.apartment;
            slot.setAttribute('disabled', 'true');
        }
    });
}