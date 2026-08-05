document.addEventListener("DOMContentLoaded", function () {

    const tooltip = document.createElement("div");
    tooltip.className = "custom-tooltip";
    document.body.appendChild(tooltip);

    document.querySelectorAll(".has-tooltip").forEach(item => {

        function positionTooltip() {

            tooltip.innerHTML = item.dataset.tooltip;

            tooltip.style.visibility = "visible";
            tooltip.style.opacity = "1";

            // Η κάρτα και όχι η παράγραφος
            const card = item.closest(".card, .training-card");
            const rect = card.getBoundingClientRect();

            // Υπολογισμός αφού εμφανιστεί
            const tooltipWidth = tooltip.offsetWidth;
            const tooltipHeight = tooltip.offsetHeight;

            let left = rect.right + 15;

            // Κέντρο ως προς την κάρτα
            let top = rect.top + (rect.height - tooltipHeight) / 2;

            // Αν δεν χωράει δεξιά
            if (left + tooltipWidth > window.innerWidth - 10) {
                left = rect.left - tooltipWidth - 15;
            }

            // Αν δεν χωράει αριστερά
            if (left < 10) {
                left = 10;
            }

            // Αν βγαίνει κάτω
            if (top + tooltipHeight > window.innerHeight - 10) {
                top = window.innerHeight - tooltipHeight - 10;
            }

            // Αν βγαίνει πάνω
            if (top < 10) {
                top = 10;
            }

            tooltip.style.left = left + "px";
            tooltip.style.top = top + "px";
        }

        item.addEventListener("mouseenter", positionTooltip);

        item.addEventListener("mousemove", positionTooltip);

        item.addEventListener("mouseleave", function () {

            tooltip.style.opacity = "0";
            tooltip.style.visibility = "hidden";

        });

    });

});