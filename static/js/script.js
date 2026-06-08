/* =====================================
   Smart Hospital System
   Global JavaScript Functions
===================================== */

/* Password Visibility Toggle */
function togglePassword() {

    const passwordField = document.getElementById("password");
    const toggleIcon = document.getElementById("toggleIcon");

    if (!passwordField || !toggleIcon) {
        return;
    }

    if (passwordField.type === "password") {
        passwordField.type = "text";
        toggleIcon.classList.remove("fa-eye");
        toggleIcon.classList.add("fa-eye-slash");
    } else {
        passwordField.type = "password";
        toggleIcon.classList.remove("fa-eye-slash");
        toggleIcon.classList.add("fa-eye");
    }
}

/* Auto Close Alerts */
document.addEventListener("DOMContentLoaded", function () {

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alertBox) {

        setTimeout(function () {

            alertBox.classList.remove("show");

            setTimeout(function () {
                alertBox.remove();
            }, 300);

        }, 4000);

    });

});

/* Confirm Logout */
document.addEventListener("DOMContentLoaded", function () {

    const logoutButton = document.querySelector(
        'a[href*="logout"]'
    );

    if (logoutButton) {

        logoutButton.addEventListener("click", function (event) {

            const confirmLogout = confirm(
                "Are you sure you want to logout?"
            );

            if (!confirmLogout) {
                event.preventDefault();
            }

        });

    }

});

/* Loading Effect on Form Submit */
document.addEventListener("DOMContentLoaded", function () {

    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {

        form.addEventListener("submit", function () {

            const submitButton = form.querySelector(
                'button[type="submit"]'
            );

            if (submitButton) {

                submitButton.disabled = true;

                const originalText = submitButton.innerHTML;

                submitButton.innerHTML =
                    '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';

                setTimeout(function () {
                    submitButton.innerHTML = originalText;
                }, 5000);

            }

        });

    });

});

/* Animate Statistics Cards */
document.addEventListener("DOMContentLoaded", function () {

    const cards = document.querySelectorAll(".stats-card");

    cards.forEach(function (card, index) {

        card.style.opacity = "0";
        card.style.transform = "translateY(20px)";

        setTimeout(function () {

            card.style.transition = "all 0.5s ease";
            card.style.opacity = "1";
            card.style.transform = "translateY(0)";

        }, index * 150);

    });

});

/* Highlight Active Navigation Link */
document.addEventListener("DOMContentLoaded", function () {

    const currentUrl = window.location.pathname;

    const navLinks = document.querySelectorAll(".nav-link");

    navLinks.forEach(function (link) {

        const href = link.getAttribute("href");

        if (href && currentUrl === href) {

            link.classList.add("active");

        }

    });

});

/* Smooth Scroll */
document.addEventListener("DOMContentLoaded", function () {

    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(function (link) {

        link.addEventListener("click", function (e) {

            e.preventDefault();

            const target = document.querySelector(
                this.getAttribute("href")
            );

            if (target) {

                target.scrollIntoView({
                    behavior: "smooth"
                });

            }

        });

    });

});

/* Appointment Date Validation */
document.addEventListener("DOMContentLoaded", function () {

    const dateInput = document.getElementById(
        "appointmentDate"
    );

    if (dateInput) {

        const today = new Date()
            .toISOString()
            .split("T")[0];

        dateInput.min = today;

    }

});

/* Table Row Hover Enhancement */
document.addEventListener("DOMContentLoaded", function () {

    const rows = document.querySelectorAll(
        ".table tbody tr"
    );

    rows.forEach(function (row) {

        row.addEventListener("mouseenter", function () {
            row.style.cursor = "pointer";
        });

    });

});

/* Dashboard Welcome Animation */
document.addEventListener("DOMContentLoaded", function () {

    const banner = document.querySelector(
        ".dashboard-banner"
    );

    if (banner) {

        banner.style.opacity = "0";
        banner.style.transform = "translateY(20px)";

        setTimeout(function () {

            banner.style.transition = "all 0.6s ease";
            banner.style.opacity = "1";
            banner.style.transform = "translateY(0)";

        }, 100);

    }

});

/* Console Message */
console.log(
    "Smart Hospital System Loaded Successfully"
);