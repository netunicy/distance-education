document.addEventListener("DOMContentLoaded", () => {

    const mainBox = document.getElementById("training-main-box");
    const grid = mainBox?.querySelector(".main_card");

    if (!mainBox || !grid) return;

    function resizeMainBox() {

        const cards = [...grid.querySelectorAll(".training-card")]
            .filter(card => getComputedStyle(card).display !== "none");

        if (cards.length === 0) {

            mainBox.style.width = "";
            return;

        }

        // Πρώτη σειρά
        const firstTop = cards[0].offsetTop;

        const firstRow = cards.filter(card => card.offsetTop === firstTop);

        const first = firstRow[0].getBoundingClientRect();
        const last = firstRow[firstRow.length - 1].getBoundingClientRect();

        // Πλάτος πρώτης σειράς
        const contentWidth = last.right - first.left;

        const padding = 32;

        let width = contentWidth + padding;

        const maxWidth = window.innerWidth - 32;

        if (width > maxWidth) {
            width = maxWidth;
        }

        mainBox.style.width = width + "px";

    }

    const observer = new MutationObserver(() => {

        resizeMainBox();

    });

    observer.observe(grid, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ["style", "class"]
    });

    window.addEventListener("resize", resizeMainBox);

    resizeMainBox();

});