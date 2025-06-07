document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-collapse-target]").forEach(function (el) {
        el.addEventListener("click", function (e) {
            e.preventDefault();
            const id = el.getAttribute("data-collapse-target");
            const target = document.getElementById(id);
            if (target) {
                target.classList.toggle("hidden");
            }
        });
    });

    const filterButton = document.getElementById("filter-collapse");
    const filters = document.getElementById("filters");
    if (filterButton && filters) {
        filterButton.addEventListener("click", function (e) {
            e.preventDefault();
            filters.classList.toggle("hidden");
        });
    }

    const darkModeBtn = document.getElementById("dark-mode-toggle");
    const darkModal = document.getElementById("dark-modal");
    document.querySelectorAll(".dark-modal-close").forEach(function (btn) {
        btn.addEventListener("click", function (e) {
            e.preventDefault();
            if (darkModal) {
                darkModal.classList.add("hidden");
            }
        });
    });
    if (darkModeBtn && darkModal) {
        darkModeBtn.addEventListener("click", function (e) {
            e.preventDefault();
            darkModal.classList.toggle("hidden");
        });
    }
});
