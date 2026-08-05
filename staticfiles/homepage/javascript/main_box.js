document.querySelectorAll(".main-box").forEach(mainBox => {

    const grid = mainBox.querySelector(".main_card");
    if (!grid) return;

    function resizeMainBox() {

        const cards = [...grid.children]
            .filter(card => getComputedStyle(card).display !== "none");

        if (cards.length === 0) {
            mainBox.style.display = "none";
            return;
        }

mainBox.style.display = "";

        const firstTop = cards[0].offsetTop;

        const cardsInFirstRow = cards.filter(card => card.offsetTop === firstTop).length;

        const cardWidth = 250;
        const gap = 20;
        const padding = 40; // 20px αριστερά + 20px δεξιά

        const width =
            (cardsInFirstRow * cardWidth) +
            ((cardsInFirstRow - 1) * gap) +
            padding;

        mainBox.style.width = width + "px";

    }

    const observer = new MutationObserver(resizeMainBox);

    observer.observe(grid, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ["style", "class"]
    });

    window.addEventListener("resize", resizeMainBox);

    resizeMainBox();

});