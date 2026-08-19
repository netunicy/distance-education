const modal = document.getElementById("packageModal");
const closeBtn = document.querySelector(".close-modal");
const buyChapterBtn = document.getElementById("buy-chapter-btn");
const buyBookBtn = document.getElementById("buy-book-btn");
const chapterBuySelection = document.getElementById("chapter-buy-selection");
const chapterSelect = document.getElementById("chapter-select");
const chapterPaymentBtn = document.getElementById("chapter-payment-btn");

let currentBookId = null;
let currentBookViewUrl = "";
document.querySelectorAll(".details-btn").forEach(btn => {

    btn.addEventListener("click", () => {

        const card = btn.closest(".card");
        const bookId = card.dataset.id;
        currentBookId = bookId;

        fetch(`/book/${bookId}/`)
            .then(response => {

                if (!response.ok) {
                    throw new Error("Failed to load book.");
                }

                return response.json();

            })

            .then(data => {

                currentBookViewUrl = data.book_view_url || "";
                chapterBuySelection.style.display = "none";
                chapterSelect.value = "";
                chapterSelect.style.display = "block";
                chapterPaymentBtn.style.display = "none";
                // ==========================
                // BOOK ACCESS
                // ==========================

                if (data.has_book_access) {

                    buyBookBtn.textContent = "Προβολή Βιβλίου";
                    buyBookBtn.dataset.action = "view";

                } else {

                    buyBookBtn.textContent = "Αγορά Βιβλίου";
                    buyBookBtn.dataset.action = "payment";

                }

                // ==========================
                // HEADER
                // ==========================

                document.getElementById("popup-image").src = data.image;
                document.getElementById("popup-image").alt = data.title;

                document.getElementById("popup-title").textContent = data.title;

                document.getElementById("popup-stage").textContent = data.stage;
                document.getElementById("popup-subject").textContent = data.subject;
                document.getElementById("popup-class").textContent = data.class;
                document.getElementById("popup-edition").textContent = data.edition || "";

                // ==========================
                // DESCRIPTION
                // ==========================

                document.getElementById("popup-description").textContent =
                    data.description;

                // ==========================
                // FEATURES
                // ==========================

                const features = document.getElementById("popup-features");

                features.innerHTML = "";

                if (data.includes.length === 0) {

                    features.innerHTML = `
                        <div class="feature-item">
                            Δεν υπάρχουν διαθέσιμες πληροφορίες.
                        </div>
                    `;

                } else {

                    data.includes.forEach(item => {

                        features.innerHTML += `
                            <div class="feature-item">
                                ✔ ${item}
                            </div>
                        `;

                    });

                }

                // ==========================
                // CHAPTER BUY SELECT
                // ==========================

                chapterSelect.innerHTML = `
                    <option value="">Επίλεξε κεφάλαιο</option>
                `;

                data.chapters.forEach(chapter => {

                    chapterSelect.innerHTML += `
                        <option 
                            value="${chapter.id}"
                            data-access="${chapter.has_access}"
                            data-view-url="${chapter.view_url}"
                        >
                            ${chapter.order}. ${chapter.title}
                        </option>
                    `;

                });
                // ==========================
                // CHAPTERS
                // ==========================

                const chapters = document.getElementById("popup-chapters");

                chapters.innerHTML = "";

                data.chapters.forEach(chapter => {

                    let videosHtml = "";

                    chapter.videos.forEach(video => {

                        videosHtml += `
                            <div class="video-item">

                                <span class="video-icon">🎥</span>

                                <span class="video-title">
                                    ${
                                        video.is_free
                                            ? `<a href="/video/${video.id}/">Σελίδα ${video.page} - ${video.activity_title}</a>`
                                            : `Σελίδα ${video.page} - ${video.activity_title}`
                                    }
                                </span>

                                <span class="video-lock ${video.is_free ? 'free' : 'locked'}">
                                    ${video.is_free ? '🔓 Free' : '🔒 Locked'}
                                </span>

                            </div>
                        `;

                    });

                    chapters.innerHTML += `

                        <div class="chapter-item">

                            <div class="chapter-header">

                                <span>

                                    ${chapter.order}. ${chapter.title}

                                </span>

                                <span class="chapter-arrow">

                                    ▶

                                </span>

                            </div>

                            <div class="chapter-videos">

                                ${videosHtml}

                            </div>

                        </div>

                    `;

                });

                modal.style.display = "block";
                document.querySelectorAll(".chapter-header").forEach(header => {

                    header.addEventListener("click", () => {

                        const videos = header.nextElementSibling;
                        const arrow = header.querySelector(".chapter-arrow");

                        if (videos.classList.contains("open")) {

                            videos.classList.remove("open");
                            arrow.textContent = "▶";

                        } else {

                            videos.classList.add("open");
                            arrow.textContent = "▼";

                        }

                    });

                });

            })

            .catch(error => {

                console.error(error);

                alert("Αδυναμία φόρτωσης του βιβλίου.");

            });

    });

});

buyChapterBtn.addEventListener("click", () => {

    if (chapterBuySelection.style.display === "none") {

        chapterBuySelection.style.display = "block";

    } else {

        chapterBuySelection.style.display = "none";

    }

});

// ==========================================
// ΕΠΙΛΟΓΗ ΚΕΦΑΛΑΙΟΥ
// ==========================================

chapterSelect.addEventListener("change", () => {

    const selectedOption =
        chapterSelect.options[chapterSelect.selectedIndex];

    const chapterId = selectedOption.value;

    if (!chapterId) {
        chapterPaymentBtn.style.display = "none";
        return;
    }

    const hasAccess =
        selectedOption.dataset.access === "true";

    // Κρύβουμε τη λίστα μόλις επιλεγεί κεφάλαιο
    chapterSelect.style.display = "none";

    // Εμφανίζουμε το κουμπί
    chapterPaymentBtn.style.display = "block";

    if (hasAccess) {

        chapterPaymentBtn.textContent = "Προβολή";
        chapterPaymentBtn.dataset.action = "view";

    } else {

        chapterPaymentBtn.textContent = "Συνέχεια στην πληρωμή";
        chapterPaymentBtn.dataset.action = "payment";

    }

});

// ==========================================
// ΣΥΝΕΧΕΙΑ ΣΤΗΝ ΠΛΗΡΩΜΗ
// ==========================================

chapterPaymentBtn.addEventListener("click", () => {

    const chapterId = chapterSelect.value;

    if (!currentBookId || !chapterId) {
        return;
    }

    const action = chapterPaymentBtn.dataset.action;

    // ==========================================
    // ΠΡΟΒΟΛΗ ΑΓΟΡΑΣΜΕΝΟΥ ΚΕΦΑΛΑΙΟΥ
    // ==========================================

    if (action === "view") {

        const selectedOption =
            chapterSelect.options[chapterSelect.selectedIndex];

        const viewUrl =
            selectedOption.dataset.viewUrl;

        if (viewUrl) {
            window.location.href = viewUrl;
        }

        return;
    }


    // ==========================================
    // ΠΛΗΡΩΜΗ
    // ==========================================

    if (action === "payment") {

        window.location.href =
            `/chapter-payment/${currentBookId}/${chapterId}/`;

    }

});

// ==========================================
// ΑΓΟΡΑ / ΠΡΟΒΟΛΗ ΟΛΟΚΛΗΡΟΥ ΒΙΒΛΙΟΥ
// ==========================================

buyBookBtn.addEventListener("click", () => {

    if (!currentBookId) {
        return;
    }

    const action = buyBookBtn.dataset.action;


    // ==========================================
    // ΠΡΟΒΟΛΗ ΑΓΟΡΑΣΜΕΝΟΥ ΒΙΒΛΙΟΥ
    // ==========================================

    if (action === "view") {

        if (currentBookViewUrl) {
            window.location.href = currentBookViewUrl;
        }

        return;
    }


    // ==========================================
    // ΑΓΟΡΑ ΒΙΒΛΙΟΥ
    // ==========================================

    if (action === "payment") {

        window.location.href =
            `/book-payment/${currentBookId}/`;

    }

});

// ==========================================
// ΚΛΕΙΣΙΜΟ POPUP
// ==========================================

closeBtn.addEventListener("click", () => {

    modal.style.display = "none";

});

window.addEventListener("click", (e) => {

    if (e.target === modal) {

        modal.style.display = "none";

    }

});