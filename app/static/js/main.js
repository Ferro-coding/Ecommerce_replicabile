// File JavaScript personalizzato
// AGGIUNGI QUI LE TUE FUNZIONALITÀ PERSONALIZZATE

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts dopo 5 secondi
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Conferma eliminazione
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm(this.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });
});

// Funzione per aggiornare il contatore del carrello
function updateCartCount() {
    // Implementa se vuoi aggiornare il contatore senza ricaricare la pagina
}
