function updateRemainingTimeInputs() {
    const forms = document.querySelectorAll("form");

    forms.forEach(function(form) {
        const statusSelect = form.querySelector(".status-select");
        const remainingInput = form.querySelector(".remaining-input");

        if (!statusSelect || !remainingInput) {
            return;
        }

        function toggleRemainingInput() {
            if (statusSelect.value === "使用中") {
                remainingInput.disabled = false;
            } else {
                remainingInput.value = 0;
                remainingInput.disabled = true;
            }
        }

        statusSelect.addEventListener("change", toggleRemainingInput);
        toggleRemainingInput();
    });
}

document.addEventListener("DOMContentLoaded", function() {
    updateRemainingTimeInputs();
});
