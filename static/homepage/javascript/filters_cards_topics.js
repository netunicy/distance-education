console.log("filters_cards_topics.js loaded");

document.addEventListener("DOMContentLoaded", () => {

    const topicsMainBox = document.getElementById("topics-main-box");

    const cards = [...topicsMainBox.querySelectorAll(".topics-card")];

    const levelButtons = document.querySelectorAll("#topics-level-container .filter-btn");

    const subjectStep = document.getElementById("topics-subject-step");
    const classStep = document.getElementById("topics-class-step");

    const subjectContainer = document.getElementById("topics-subject-container");
    const classContainer = document.getElementById("topics-class-container");

    const emptyMessage = document.getElementById("topics-empty-message");
    const mainBox = document.getElementById("topics-main-box");

    let selectedCategory = "";
    let selectedTopics = "";
    let selectedLevel = "";

    // ============================================
    // Αρχική κατάσταση
    // ============================================

    subjectStep.classList.add("hidden");
    classStep.classList.add("hidden");

    cards.forEach(card => {
        card.style.display = "none";
    });

    topicsMainBox.style.display = "none";

    // ============================================
    // Εμφάνιση καρτών
    // ============================================

    function showCards() {

        let found = false;

        cards.forEach(card => {

            const show =
                card.dataset.category === selectedCategory &&
                card.dataset.topics === selectedTopics &&
                card.dataset.level === selectedLevel;

            card.style.display = show ? "" : "none";

            if (show) {
                found = true;
            }

        });

        if (found) {

            emptyMessage.style.display = "none";
            topicsMainBox.style.display = "";

        } else {

            emptyMessage.style.display = "block";
            topicsMainBox.style.display = "none";

        }

    }

    // ============================================
    // Δημιουργία προγραμμάτων
    // ============================================

    function buildSubjects() {

        subjectContainer.innerHTML = "";

        const subjects = new Set();

        cards.forEach(card => {

            if (card.dataset.category === selectedCategory) {
                subjects.add(card.dataset.topics);
            }

        });

        [...subjects].sort().forEach(subject => {

            const button = document.createElement("button");

            button.className = "filter-btn";
            button.dataset.topics = subject;
            button.textContent = subject;

            subjectContainer.appendChild(button);

        });

        activateSubjects();

    }

    // ============================================
    // LEVEL
    // ============================================

    levelButtons.forEach(button => {

        button.addEventListener("click", () => {

            levelButtons.forEach(btn => btn.classList.remove("active"));

            button.classList.add("active");

            selectedCategory = button.dataset.level;
            selectedTopics = "";
            selectedLevel = "";

            cards.forEach(card => {
                card.style.display = "none";
            });

            topicsMainBox.style.display = "none";
            emptyMessage.style.display = "block";

            classStep.classList.add("hidden");
            classContainer.innerHTML = "";

            subjectStep.classList.remove("hidden");

            buildSubjects();

        });

    });

    // ============================================
    // Δημιουργία επιπέδων
    // ============================================

    function buildClasses() {

        classContainer.innerHTML = "";

        const classes = new Set();

        cards.forEach(card => {

            if (
                card.dataset.category === selectedCategory &&
                card.dataset.topics === selectedTopics
            ) {
                classes.add(card.dataset.level);
            }

        });

        [...classes].sort().forEach(className => {

            const button = document.createElement("button");

            button.className = "filter-btn";
            button.dataset.class = className;

            const levelLabels = {
                "Beginner": "Βασικό",
                "Intermediate": "Ενδιάμεσο",
                "Advanced": "Προχωρημένο"
            };

            button.textContent = levelLabels[className] || className;

            classContainer.appendChild(button);

        });

        activateClasses();

    }

    // ============================================
    // SUBJECT
    // ============================================

    function activateSubjects() {

        const buttons = subjectContainer.querySelectorAll(".filter-btn");

        buttons.forEach(button => {

            button.addEventListener("click", () => {

                buttons.forEach(btn => btn.classList.remove("active"));

                button.classList.add("active");

                selectedTopics = button.dataset.topics;
                selectedLevel = "";

                cards.forEach(card => {
                    card.style.display = "none";
                });

                emptyMessage.style.display = "block";

                classContainer.innerHTML = "";

                classStep.classList.remove("hidden");

                buildClasses();

            });

        });

    }

    // ============================================
    // CLASS
    // ============================================

    function activateClasses() {

        const buttons = classContainer.querySelectorAll(".filter-btn");

        buttons.forEach(button => {

            button.addEventListener("click", () => {

                buttons.forEach(btn => btn.classList.remove("active"));

                button.classList.add("active");

                selectedLevel = button.dataset.class;

                showCards();

            });

        });

    }

});