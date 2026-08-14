const trainingModal = document.getElementById("trainingModal");
const trainingCloseBtn = trainingModal.querySelector(".close-modal");

document.querySelectorAll(".training-details-btn").forEach(btn => {

    btn.addEventListener("click", () => {

        const card = btn.closest(".training-card");
        const trainingId = card.dataset.id;

        fetch(`/training/${trainingId}/`)
            .then(response => {

                if (!response.ok) {
                    throw new Error("Failed to load training.");
                }

                return response.json();

            })

            .then(data => {

                // ==========================
                // HEADER
                // ==========================

                document.getElementById("training-popup-image").src = data.image;
                document.getElementById("training-popup-image").alt = data.title;

                document.getElementById("training-popup-title").textContent = data.title;

                document.getElementById("training-popup-category").textContent = data.category;
                document.getElementById("training-popup-level").textContent = data.level;

                // ==========================
                // DESCRIPTION
                // ==========================

                document.getElementById("training-popup-description").textContent =
                    data.description;

                // ==========================
                // FEATURES
                // ==========================

                const features = document.getElementById("training-popup-features");

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

                const contents = document.getElementById("training-popup-contents");

                contents.innerHTML = "";

                if (data.contents.length === 0) {

                    contents.innerHTML = `
                        <div class="feature-item">
                            Δεν υπάρχουν διαθέσιμες ενότητες.
                        </div>
                    `;

                } else {

                    data.contents.forEach(content => {

                        contents.innerHTML += `

                            <div class="chapter-item">

                                <div class="chapter-header">

                                    <span>
                                        ${content.order}. ${content.title}
                                    </span>

                                    <span class="video-lock ${content.has_free_video ? 'free' : 'locked'}">
                                        ${content.has_free_video ? '🔓 Unlocked' : '🔒 Locked'}
                                    </span>

                                </div>

                                ${content.description ? `
                                    <div class="chapter-videos open">

                                        <div class="video-item">

                                            <span class="video-title">

                                                ${
                                                    content.has_free_video

                                                    ?

                                                    `<a href="${content.video_url}">
                                                        ${content.description}
                                                    </a>`

                                                    :

                                                    content.description
                                                }

                                            </span>

                                        </div>

                                    </div>
                                ` : ""}

                            </div>

                        `;

                    });

                }

                // ==========================
                // OPEN / CLOSE DESCRIPTION
                // ==========================

                document.querySelectorAll("#training-popup-contents .chapter-header")
                    .forEach(header => {

                        header.addEventListener("click", () => {

                            const body = header.nextElementSibling;

                            if (!body) return;

                            body.classList.toggle("open");

                        });

                    });

                trainingModal.style.display = "block";

            })

            .catch(error => {

                console.error(error);

                alert("Αδυναμία φόρτωσης του προγράμματος.");

            });

    });

});

trainingCloseBtn.addEventListener("click", () => {
    trainingModal.style.display = "none";
});

window.addEventListener("click", (e) => {

    if (e.target === trainingModal) {

        trainingModal.style.display = "none";

    }

});

const buyTrainingBtn = document.getElementById("buy-training-btn");

buyTrainingBtn.addEventListener("click", () => {

    window.location.href = buyTrainingBtn.dataset.url;

});