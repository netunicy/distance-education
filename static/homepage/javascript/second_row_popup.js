function openInfoModal(id) {
    const modal = document.getElementById('info-modal-' + id);

    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

function closeInfoModal(id) {
    const modal = document.getElementById('info-modal-' + id);

    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}


// Κλείσιμο όταν ο χρήστης κάνει κλικ έξω από το παράθυρο
window.addEventListener('click', function(event) {
    if (event.target.classList.contains('information-modal')) {
        event.target.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
});


// Links του Footer
document.querySelectorAll('.footer-info-link').forEach(function(link) {
    link.addEventListener('click', function(event) {
        event.preventDefault();

        const id = this.dataset.id;
        openInfoModal(id);
    });
});