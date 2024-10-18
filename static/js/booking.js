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
    const week = document.getElementById('week').dataset.week;
    if (reservations.length === 0) {
        alert("You haven't selected any reservation slots.");
    }
    else if (apartment === '') {
        alert("You haven't typed in your apartment number.");
    } else {
        preferences['apartment'] = apartment;
        const data = {
            week: week,
            apartment: apartment,
            reservations: reservations
        };
        fetch('/save_reservations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            alert('Your reservations were saved.');
            console.log('Success:', data);
            location.reload(true);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
}

async function fetchFromAPI(resource) {
    try {
        const response = await fetch(`/api/${resource}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`Error fetching ${resource}:`, error);
    }
}

async function fetchFromAPIFilter(resource, filter) {
    try {
        const response = await fetch(`/api/${resource}/${filter}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`Error fetching ${resource}/${filter}:`, error);
    }
}

async function updateReservedSlots() {
    const week = document.getElementById('week').dataset.week;
    const data = await fetchFromAPIFilter('reservations', week);
    data.forEach(function(reservation) {
        const selector = `.slot[data-interval="${reservation.interval}"][data-machine="${reservation.machine}"][data-day="${reservation.day}"]`;
        const slot = document.querySelector(selector);
        slot.classList.add('reserved');
        slot.textContent = reservation.apartment;
        slot.setAttribute('disabled', 'true');
    });
}