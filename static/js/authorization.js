
function login() {
    const password = document.getElementById('password').value;
    
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Store the password in LocalStorage
            localStorage.setItem('password', password);
            
            // Redirect to the protected route
            window.location.href = '/';
        } else {
            alert('Incorrect password, please try again.');
        }
    })
    .catch(error => {
        console.error('Error during login:', error);
    });
}

window.onload = function() {
    const storedPassword = localStorage.getItem('password');
    if (storedPassword) {
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ password: storedPassword })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = '/';
            } else {
                console.log('Stored password is incorrect');
            }
        })
        .catch(error => {
            console.error('Error during auto-login:', error);
        });
    }
};