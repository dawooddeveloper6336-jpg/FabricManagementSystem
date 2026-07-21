document.addEventListener('DOMContentLoaded', function() {
    // --- Global modal backdrop cleanup ---
    document.addEventListener('hidden.bs.modal', function() {
        document.querySelectorAll('.modal-backdrop').forEach(function(el) {
            el.remove();
        });
        document.body.classList.remove('modal-open');
        document.body.style.overflow = '';
        document.body.style.paddingRight = '';
    });
});