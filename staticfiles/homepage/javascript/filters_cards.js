document.addEventListener("DOMContentLoaded", () => {

    const cards = [...document.querySelectorAll(".card")];

    const levelButtons = document.querySelectorAll("#level-container .filter-btn");

    const subjectStep = document.getElementById("subject-step");
    const classStep = document.getElementById("class-step");

    const subjectContainer = document.getElementById("subject-container");
    const classContainer = document.getElementById("class-container");

    const emptyMessage = document.getElementById("empty-message");

    const mainBox = document.getElementById("school-main-box");

    let selectedLevel = "";
    let selectedSubject = "";
    let selectedClass = "";

    // ============================================
    // Αρχική κατάσταση
    // ============================================

    subjectStep.classList.add("hidden");
    classStep.classList.add("hidden");

    cards.forEach(card => {

        card.style.display = "none";

    });

    mainBox.style.display = "none";

    // ============================================
    // Εμφάνιση καρτών
    // ============================================

    function showCards() {

        let found = false;

        cards.forEach(card => {

            const show =
                card.dataset.level === selectedLevel &&
                card.dataset.subject === selectedSubject &&
                card.dataset.class === selectedClass;

            card.style.display = show ? "" : "none";

            if (show) {
                found = true;
            }

        });

        if (found) {

            emptyMessage.style.display = "none";
            mainBox.style.display = "";

        } else {

            emptyMessage.style.display = "block";
            mainBox.style.display = "none";

        }

    }

    // ============================================
    // Δημιουργία μαθημάτων
    // ============================================

    function buildSubjects() {

        subjectContainer.innerHTML = "";

        const subjects = new Set();

        cards.forEach(card => {

            if (card.dataset.level === selectedLevel) {

                subjects.add(card.dataset.subject);

            }

        });

        [...subjects].sort().forEach(subject => {

            const button = document.createElement("button");

            button.className = "filter-btn";

            button.dataset.subject = subject;

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

            selectedLevel = button.dataset.level;

            selectedSubject = "";
            selectedClass = "";

            /// Κρύψε όλες τις κάρτες
            cards.forEach(card => {
                card.style.display = "none";
            });

            emptyMessage.style.display = "block";
            mainBox.style.display = "none";

            classStep.classList.add("hidden");

            classContainer.innerHTML = "";

            subjectStep.classList.remove("hidden");

            buildSubjects();

        });

    });
        // ============================================
    // Δημιουργία τάξεων
    // ============================================

    function buildClasses() {

        classContainer.innerHTML = "";

        const classes = new Set();

        cards.forEach(card => {

            if (
                card.dataset.level === selectedLevel &&
                card.dataset.subject === selectedSubject
            ) {

                classes.add(card.dataset.class);

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

        const buttons =
            subjectContainer.querySelectorAll(".filter-btn");

        buttons.forEach(button => {

            button.addEventListener("click", () => {

                buttons.forEach(btn =>
                    btn.classList.remove("active")
                );

                button.classList.add("active");

                selectedSubject = button.dataset.subject;

                selectedClass = "";
                cards.forEach(card => {
                    card.style.display = "none";
                });

                mainBox.style.display = "none";

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

        const buttons =
            classContainer.querySelectorAll(".filter-btn");

        buttons.forEach(button => {

            button.addEventListener("click", () => {

                buttons.forEach(btn =>
                    btn.classList.remove("active")
                );

                button.classList.add("active");

                selectedClass = button.dataset.class;

                emptyMessage.style.display = "none";

                showCards();

            });

        });

    }

});