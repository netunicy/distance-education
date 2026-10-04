// ==========================================
// TOPICS MODAL
// ==========================================

const topicsModal = document.getElementById("topicsModal");

const topicsCloseBtn =
    topicsModal.querySelector(".close-modal");

const buyTopicsBtn =
    document.getElementById("buy-topics-btn");

let currentTopicsId = null;
let currentTopicsViewUrl = "";


// ==========================================
// OPEN TOPICS MODAL
// ==========================================

document.querySelectorAll(".topics-details-btn").forEach(btn => {

    btn.addEventListener("click", (e) => {

        e.preventDefault();
        e.stopPropagation();

        const card = btn.closest(".topics-card");

        if (!card || !card.dataset.id) {
            return;
        }

        const topicsId = card.dataset.id;

        // Αποτρέπουμε τη χρήση δεδομένων
        // από προηγούμενο πρόγραμμα.

        currentTopicsId = null;
        currentTopicsViewUrl = "";

        buyTopicsBtn.disabled = true;


        // ==================================
        // FETCH TOPICS
        // ==================================

        fetch(`/topics/${topicsId}/`)

            .then(response => {

                if (!response.ok) {

                    throw new Error(
                        "Failed to load topics."
                    );

                }

                return response.json();

            })

            .then(data => {


                // ==========================
                // TOPICS ACCESS
                // ==========================

                currentTopicsId = topicsId;

                currentTopicsViewUrl =
                    data.topics_view_url || "";


                if (data.has_topics_access) {

                    buyTopicsBtn.textContent =
                        "Προβολή Προγράμματος";

                    buyTopicsBtn.dataset.action =
                        "view";

                } else {

                    buyTopicsBtn.textContent =
                        "Αγορά Προγράμματος";

                    buyTopicsBtn.dataset.action =
                        "payment";

                }

                buyTopicsBtn.disabled = false;


                // ==========================
                // HEADER
                // ==========================

                const popupImage =
                    document.getElementById(
                        "topics-popup-image"
                    );

                popupImage.src = data.image || "";

                popupImage.alt = data.title || "";


                document.getElementById(
                    "topics-popup-title"
                ).textContent = data.title || "";


                document.getElementById(
                    "topics-popup-category"
                ).textContent = data.category || "";


                document.getElementById(
                    "topics-popup-level"
                ).textContent = data.level || "";



                // ==========================
                // DESCRIPTION
                // ==========================

                document.getElementById(
                    "topics-popup-description"
                ).textContent = data.description || "";



                // ==========================
                // FEATURES
                // ==========================

                const features =
                    document.getElementById(
                        "topics-popup-features"
                    );

                features.innerHTML = "";


                const includes =
                    Array.isArray(data.includes)
                        ? data.includes
                        : [];


                if (includes.length === 0) {

                    features.innerHTML = `
                        <div class="feature-item">
                            Δεν υπάρχουν διαθέσιμες πληροφορίες.
                        </div>
                    `;

                } else {

                    includes.forEach(item => {

                        const featureItem =
                            document.createElement("div");

                        featureItem.className =
                            "feature-item";

                        featureItem.textContent =
                            `✔ ${item}`;

                        features.appendChild(
                            featureItem
                        );

                    });

                }



                // ==========================
                // CONTENTS
                // ==========================

                const contents =
                    document.getElementById(
                        "topics-popup-contents"
                    );

                contents.innerHTML = "";


                const topicsContents =
                    Array.isArray(data.contents)
                        ? data.contents
                        : [];


                if (topicsContents.length === 0) {

                    contents.innerHTML = `
                        <div class="feature-item">
                            Δεν υπάρχουν διαθέσιμα περιεχόμενα.
                        </div>
                    `;

                } else {


                    topicsContents.forEach(content => {


                        // ==================
                        // CHAPTER
                        // ==================

                        const chapterItem =
                            document.createElement("div");

                        chapterItem.className =
                            "chapter-item";


                        const chapterHeader =
                            document.createElement("div");

                        chapterHeader.className =
                            "chapter-header";


                        const chapterTitle =
                            document.createElement("span");

                        chapterTitle.textContent =
                            `${content.order}. ${content.title}`;


                        const chapterArrow =
                            document.createElement("span");

                        chapterArrow.className =
                            "chapter-arrow";

                        chapterArrow.textContent = "▶";


                        chapterHeader.appendChild(
                            chapterTitle
                        );

                        chapterHeader.appendChild(
                            chapterArrow
                        );



                        // ==================
                        // CHAPTER VIDEOS
                        // ==================

                        const chapterVideos =
                            document.createElement("div");

                        chapterVideos.className =
                            "chapter-videos";


                        const videos =
                            Array.isArray(content.videos)
                                ? content.videos
                                : [];


                        videos.forEach(video => {


                            const videoItem =
                                document.createElement("div");

                            videoItem.className =
                                "video-item";



                            // VIDEO ICON

                            const videoIcon =
                                document.createElement("span");

                            videoIcon.className =
                                "video-icon";

                            videoIcon.textContent = "🎥";



                            // VIDEO TITLE

                            const videoTitle =
                                document.createElement("span");

                            videoTitle.className =
                                "video-title";


                            if (video.has_access && video.url) {

                                const videoLink =
                                    document.createElement("a");

                                videoLink.href =
                                    video.url;

                                videoLink.textContent =
                                    video.title || "";

                                videoTitle.appendChild(
                                    videoLink
                                );

                            } else {

                                videoTitle.textContent =
                                    video.title || "";

                            }



                            // VIDEO ACCESS

                            const videoLock = document.createElement("span");

                            if (video.is_free) {

                                videoLock.className = "video-lock free";
                                videoLock.textContent = "🔓 Free";

                            } else if (video.has_access) {

                                videoLock.className = "video-lock free";
                                videoLock.textContent = "🔓 Διαθέσιμο";

                            } else {

                                videoLock.className = "video-lock locked";
                                videoLock.textContent = "🔒 Locked";

                            }


                            // APPEND VIDEO

                            videoItem.appendChild(
                                videoIcon
                            );

                            videoItem.appendChild(
                                videoTitle
                            );

                            videoItem.appendChild(
                                videoLock
                            );

                            chapterVideos.appendChild(
                                videoItem
                            );

                        });



                        // ==================
                        // ACCORDION
                        // ==================

                        chapterHeader.addEventListener(
                            "click",
                            () => {

                                if (
                                    chapterVideos.classList.contains(
                                        "open"
                                    )
                                ) {

                                    chapterVideos.classList.remove(
                                        "open"
                                    );

                                    chapterArrow.textContent =
                                        "▶";

                                } else {

                                    chapterVideos.classList.add(
                                        "open"
                                    );

                                    chapterArrow.textContent =
                                        "▼";

                                }

                            }
                        );



                        // ==================
                        // APPEND CHAPTER
                        // ==================

                        chapterItem.appendChild(
                            chapterHeader
                        );

                        chapterItem.appendChild(
                            chapterVideos
                        );

                        contents.appendChild(
                            chapterItem
                        );

                    });

                }



                // ==========================
                // OPEN MODAL
                // ==========================

                topicsModal.style.display =
                    "block";


            })


            // ==============================
            // ERROR
            // ==============================

            .catch(error => {

                console.error(error);

                buyTopicsBtn.disabled = false;

                alert(
                    "Αδυναμία φόρτωσης του προγράμματος."
                );

            });

    });

});



// ==========================================
// ΑΓΟΡΑ / ΠΡΟΒΟΛΗ ΠΡΟΓΡΑΜΜΑΤΟΣ
// ==========================================

buyTopicsBtn.addEventListener("click", () => {


    if (!currentTopicsId) {

        return;

    }


    const action =
        buyTopicsBtn.dataset.action;



    // ======================================
    // ΠΡΟΒΟΛΗ ΑΓΟΡΑΣΜΕΝΟΥ ΠΡΟΓΡΑΜΜΑΤΟΣ
    // ======================================

    if (action === "view") {

        const contentsSection =
            document.getElementById(
                "topics-contents-section"
            );

        if (contentsSection) {

            contentsSection.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        }

        return;
    }



    // ======================================
    // ΑΓΟΡΑ ΠΡΟΓΡΑΜΜΑΤΟΣ
    // ======================================

    if (action === "payment") {

        window.location.href =
            `/topic/payment/${currentTopicsId}/`;

    }


});



// ==========================================
// CLOSE MODAL
// ==========================================

topicsCloseBtn.addEventListener(
    "click",
    () => {

        topicsModal.style.display =
            "none";

    }
);



// ==========================================
// CLICK OUTSIDE MODAL
// ==========================================

window.addEventListener("click", (e) => {


    if (e.target === topicsModal) {

        topicsModal.style.display =
            "none";

    }


});