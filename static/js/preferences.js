let preferences = {
    "theme": "dark",
    "locale": "en",
    "time_format": "12",
    "apartment": null
};

for (let key in preferences) {
    const value = localStorage.getItem(key);
    if (value) {
        preferences[key] = value;
    }
}

function setPreference(key, value) {
    localStorage.setItem(key, value);
    preferences[key] = value;
}
function toggleLocale() {
    let locale = preferences['locale'];

    if (locale === 'da') {
        setPreference('locale', 'en');
    } else {
        setPreference('locale', 'da');
    }
    setLocale();
    updateLocale().then(() => {
        window.location.reload();
    });
}

function setLocale() {
    let locale = preferences['locale'];
    const button = document.getElementById('language')
    if (button) {
        if (locale === 'en') {
            button.textContent = '🇩🇰';
            button.title = 'Dansk';
        } else if (locale === 'da') {
            button.textContent = '🇬🇧';
            button.title = 'English';
        }
    }
}

function updateLocale() {
    const locale = localStorage.getItem('locale') || 'en';

    return fetch('/set-locale', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Locale': locale
        },
        body: JSON.stringify({ locale: locale })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Locale sent to the server:', data.locale);
    })
    .catch(error => {
        console.error('Error sending locale to the server:', error);
    });
};

function updateApartment() {
    const apartment = localStorage.getItem('apartment') || null;

    if (!apartment) {
        return
    }
    return fetch('/set-apartment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Apartment': apartment
        },
        body: JSON.stringify({ apartment: apartment })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Apartment sent to the server:', data.apartment);
    })
    .catch(error => {
        console.error('Error sending apartment to the server:', error);
    });
};

function setApartmentPreference() {
    const apartment = document.getElementById('apartment').value;

    function validateApartment() {
        const apartment = document.getElementById('apartment')
        if (apartment.value < apartment.min || apartment.value > apartment.max) {
            console.log(`Please enter an apartment number between ${apartment.min} and ${apartment.max}.`);
            return false;
        } else {
            return true;
        }
    }

    if (validateApartment(apartment)) {
        setPreference('apartment', apartment);
        console.log(`Apartment number set: ${apartment}`);
    } else {
        console.log('No apartment number entered');
    }
}
