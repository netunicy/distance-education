console.log("filters_cards_topics.js loaded");
document.addEventListener("DOMContentLoaded", () => {

    const trainingMainBox = document.getElementById("training-main-box");

    const cards = [...trainingMainBox.querySelectorAll(".training-card")];

    const levelButtons = document.querySelectorAll("#training-level-container .filter-btn");

    const subjectStep = document.getElementById("training-subject-step");
    const classStep = document.getElementById("training-class-step");

    const subjectContainer = document.getElementById("training-subject-container");
    const classContainer = document.getElementById("training-class-container");

    const emptyMessage = document.getElementById("training-empty-message");
    const mainBox = document.getElementById("training-main-box");

    let selectedCategory = "";
    let selectedTraining = "";
    let selectedLevel = "";

    // ============================================
    // Αρχική κατάσταση
    // ============================================

    subjectStep.classList.add("hidden");
    classStep.classList.add("hidden");

    cards.forEach(card => {

        card.style.display = "none";

    });
    trainingMainBox.style.display = "none";

    // ============================================
    // Εμφάνιση καρτών
    // ============================================

    function showCards() {

        let found = false;

        cards.forEach(card => {

            const show =
                card.dataset.category === selectedCategory &&
                card.dataset.training === selectedTraining &&
                card.dataset.level === selectedLevel;

            card.style.display = show ? "" : "none";

            if (show) {
                found = true;
            }

        });

        if (found) {

            emptyMessage.style.display = "none";
            trainingMainBox.style.display = "";

        } else {

            emptyMessage.style.display = "block";
            trainingMainBox.style.display = "none";

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

                subjects.add(card.dataset.training);

            }

        });

        [...subjects].sort().forEach(subject => {

            const button = document.createElement("button");

            button.className = "filter-btn";
            button.dataset.training = subject;
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
            selectedTraining = "";
            selectedLevel = "";

            cards.forEach(card => {

                card.style.display = "none";

            });

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
                card.dataset.training === selectedTraining
            ) {

                classes.add(card.dataset.level);

            }

        });

        [...classes].sort().forEach(className => {

            const button = document.createElement("button");

            button.className = "filter-btn";
            button.dataset.class = className;
            button.textContent = className;

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

                selectedTraining = button.dataset.training;
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