const topicsModal = document.getElementById("topicsModal");
const topicsCloseBtn = topicsModal.querySelector(".close-modal");

document.querySelectorAll(".topics-details-btn").forEach(btn => {

    btn.addEventListener("click", (e) => {

        // Επειδή το button μπορεί να βρίσκεται μέσα σε <a>
        e.preventDefault();
        e.stopPropagation();

        const card = btn.closest(".topics-card");
        const topicsId = card.dataset.id;

        fetch(`/topics/${topicsId}/`)
            .then(response => {

                if (!response.ok) {
                    throw new Error("Failed to load topics.");
                }

                return response.json();

            })

            .then(data => {

                // ==========================
                // HEADER
                // ==========================

                document.getElementById("topics-popup-image").src = data.image;
                document.getElementById("topics-popup-image").alt = data.title;

                document.getElementById("topics-popup-title").textContent = data.title;

                document.getElementById("topics-popup-category").textContent = data.category;
                document.getElementById("topics-popup-level").textContent = data.level;


                // ==========================
                // DESCRIPTION
                // ==========================

                document.getElementById("topics-popup-description").textContent =
                    data.description;


                // ==========================
                // FEATURES
                // ==========================

                const features =
                    document.getElementById("topics-popup-features");

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
                // CONTENTS
                // ==========================

                const contents =
                    document.getElementById("topics-popup-contents");

                contents.innerHTML = "";

                data.contents.forEach(content => {

                    let videosHtml = "";

                    // ==========================
                    // VIDEOS
                    // ==========================

                    content.videos.forEach(video => {

                        videosHtml += `

                            <div class="video-item">

                                <span class="video-icon">
                                    🎥
                                </span>

                                <span class="video-title">

                                    ${
                                        video.is_free

                                            ? `<a href="${video.url}">
                                                ${video.title}
                                               </a>`

                                            : video.title
                                    }

                                </span>

                                <span class="video-lock ${video.is_free ? 'free' : 'locked'}">

                                    ${video.is_free ? '🔓 Free' : '🔒 Locked'}

                                </span>

                            </div>

                        `;

                    });


                    // ==========================
                    // CONTENT
                    // ==========================

                    contents.innerHTML += `

                        <div class="chapter-item">

                            <div class="chapter-header">

                                <span>

                                    ${content.order}. ${content.title}

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


                // ==========================
                // OPEN MODAL
                // ==========================

                topicsModal.style.display = "block";


                // ==========================
                // ACCORDION
                // ==========================

                document
                    .querySelectorAll("#topics-popup-contents .chapter-header")
                    .forEach(header => {

                        header.addEventListener("click", () => {

                            const videos =
                                header.nextElementSibling;

                            const arrow =
                                header.querySelector(".chapter-arrow");

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

                alert("Αδυναμία φόρτωσης του προγράμματος.");

            });

    });

});


// ==========================
// CLOSE BUTTON
// ==========================

topicsCloseBtn.addEventListener("click", () => {

    topicsModal.style.display = "none";

});


// ==========================
// CLICK OUTSIDE MODAL
// ==========================

window.addEventListener("click", (e) => {

    if (e.target === topicsModal) {

        topicsModal.style.display = "none";

    }

});


// ==========================
// BUY TOPICS
// ==========================

const buyTopicsBtn =
    document.getElementById("buy-topics-btn");

buyTopicsBtn.addEventListener("click", () => {

    window.location.href =
        buyTopicsBtn.dataset.url;

});