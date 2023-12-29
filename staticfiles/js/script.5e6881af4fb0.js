document.addEventListener("DOMContentLoaded", function() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

    // Function to dismiss error messages after a delay
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

    // Function to toggle the mobile menu
    function toggleMobileMenu() {
        var menu = document.getElementById("mobileMenu");
        if (menu.style.display === "block") {
            menu.style.display = "none";
        } else {
            menu.style.display = "block";
        }
    }

    // Function to close the mobile menu
    function closeMobileMenu() {
        document.getElementById("mobileMenu").style.display = "none";
    }

    // Attach the toggle function to the menu icon
    var menuIcon = document.querySelector('.mobile-nav-toggle');
    if(menuIcon) {
        menuIcon.addEventListener('click', toggleMobileMenu);
    }

    // Attach the close function to the close button
    var closeButton = document.querySelector('.mobile-menu .btn-close');
    if(closeButton) {
        closeButton.addEventListener('click', closeMobileMenu);
    }
});
