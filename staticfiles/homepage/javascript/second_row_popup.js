
function openInfoModal(id) {
    const modal = document.getElementById('info-modal-' + id);
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden'; // Κλειδώνει το scroll της σελίδας
    }
}

function closeInfoModal(id) {
    const modal = document.getElementById('info-modal-' + id);
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto'; // Επαναφέρει το scroll της σελίδας
    }
}

// Κλείσιμο όταν ο χρήστης κάνει κλικ έξω από το παράθυρο
window.addEventListener('click', function(event) {
    if (event.target.classList.contains('information-modal')) {
        event.target.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
});