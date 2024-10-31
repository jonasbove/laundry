function showDialog(id) {
    dialog = document.getElementById(id);
    dialog.showModal();
}

function closeDialog(id) {
    document.getElementById(id).close();
}

function updateVh() {
    // Calculate 1vh in pixels based on the current window height
    let vh = window.innerHeight * 0.01;
    // Set the value in a CSS variable
    document.documentElement.style.setProperty('--vh', `${vh}px`);
}

// Run the function on initial load
updateVh();

// Update the variable on window resize (e.g., when the address bar hides/shows)
window.addEventListener('resize', updateVh);