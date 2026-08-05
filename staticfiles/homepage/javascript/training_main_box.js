document.addEventListener("DOMContentLoaded", () => {

    const mainBox = document.getElementById("training-main-box");
    if (!mainBox) return;

    const grid = mainBox.querySelector(".main_card");
    if (!grid) return;

    function resizeTrainingBox() {

        const cards = [...grid.querySelectorAll(".training-card")]
            .filter(card => getComputedStyle(card).display !== "none");

        if (!cards.length) {

            mainBox.style.width = "";
            return;

        }

        const firstTop = cards[0].offsetTop;

        const firstRow = cards.filter(card => card.offsetTop === firstTop);

        const cardWidth = firstRow[0].offsetWidth;

        const gap = 20;

        const padding = 32;

        let width =
            (cardWidth * firstRow.length) +
            (gap * (firstRow.length - 1)) +
            padding;

        const maxWidth = window.innerWidth - 32;

        if (width > maxWidth) {
            width = maxWidth;
        }

        mainBox.style.width = width + "px";
    }

    const observer = new MutationObserver(resizeTrainingBox);

    observer.observe(grid, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ["style", "class"]
    });

    window.addEventListener("resize", resizeTrainingBox);

    resizeTrainingBox();

});