const modal = document.getElementById("packageModal");
const closeBtn = document.querySelector(".close-modal");
const buyChapterBtn = document.getElementById("buy-chapter-btn");
const chapterBuySelection = document.getElementById("chapter-buy-selection");
const chapterSelect = document.getElementById("chapter-select");
const chapterPaymentBtn = document.getElementById("chapter-payment-btn");

let currentBookId = null;
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

                chapterBuySelection.style.display = "none";

                chapterSelect.value = "";
                chapterSelect.style.display = "block";

                chapterPaymentBtn.style.display = "none";

                // Ο υπόλοιπος κώδικάς σου...


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
                        <option value="${chapter.id}">
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

    const chapterId = chapterSelect.value;

    if (chapterId) {

        // Κρύβουμε τη λίστα
        chapterSelect.style.display = "none";

        // Εμφανίζουμε το κουμπί πληρωμής
        chapterPaymentBtn.style.display = "block";

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

    window.location.href =
        `/chapter-payment/${currentBookId}/${chapterId}/`;

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