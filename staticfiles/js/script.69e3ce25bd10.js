document.addEventListener('DOMContentLoaded', function() {

    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

    $(document).ready(function() {
        function dismissErrorMessages() {
            setTimeout(function() {
                $('.alert.alert-danger').fadeOut('slow', function() {
                    $(this).remove();
                });
            }, 3000);
        }
    
        dismissErrorMessages();
    });

});
