const header = document.getElementsByTagName('header')[0];

let startX = 0;
let endX = 0;

header.addEventListener('touchstart', (e) => {
    startX = e.touches[0].clientX;
});

header.addEventListener('touchmove', (e) => {
    e.preventDefault();
});

header.addEventListener('touchend', (e) => {
    endX = e.changedTouches[0].clientX;
    const diffX = endX - startX;
    if (diffX > 50) {
        console.log('-1 day');
        startX = 0;
        endX = 0;
    } else if (diffX < -50) {
        console.log('+1 day');
    }
});

function showDialog(id) {
    dialog = document.getElementById(id);
    dialog.showModal();
}

function closeDialog(id) {
    document.getElementById(id).close();
}