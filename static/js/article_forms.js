document.addEventListener("DOMContentLoaded", function () {
    const selector = document.getElementById("article-type");
    if (!selector) {
        return;
    }
    function switchForm() {
        const selected = selector.value;
        document.querySelectorAll(".article-form").forEach((div) => {
            div.classList.add("hidden");
        });
        const active = document.getElementById("form-" + selected);
        if (active) {
            active.classList.remove("hidden");
        }
    }
    selector.addEventListener("change", switchForm);
    switchForm();
});
