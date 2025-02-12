document.addEventListener("DOMContentLoaded", () => {
    const searchInputTools = document.getElementById("search-input-tools");
    const suggestionsContainerTools = document.getElementById("suggestions-container-tools");

    searchInputTools.addEventListener("input", async (e) => {
        const query = e.target.value.trim();

        if (!query) {
            suggestionsContainerTools.innerHTML = "";
            suggestionsContainerTools.classList.remove("active");
            return;
        }

        try {
            const response = await fetch(`/suggest?q=${encodeURIComponent(query)}`);
            const suggestions = await response.json();

            if (suggestions.length > 0) {
                suggestionsContainerTools.innerHTML = suggestions
                    .map((s) => {
                        return `
                            <div class="suggestion-item-tools">
                                <a href="${s.url}">${s.name}</a>
                                <p>${s.description}</p>
                            </div>
                        `;
                    })
                    .join("");

                suggestionsContainerTools.classList.add("active");
            } else {
                suggestionsContainerTools.innerHTML = "";
                suggestionsContainerTools.classList.remove("active");
            }
        } catch (err) {
            console.error("Error fetching suggestions:", err);
        }
    });

    // 🔹 Cacher les suggestions si l'utilisateur clique en dehors
    document.addEventListener("click", (e) => {
        if (!suggestionsContainerTools.contains(e.target) && e.target !== searchInputTools) {
            suggestionsContainerTools.innerHTML = "";
            suggestionsContainerTools.classList.remove("active");
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    if (!localStorage.getItem("hideBanner")) {
        document.getElementById("site-banner").style.display = "block";
    }
});

function closeBanner() {
    document.getElementById("site-banner").style.display = "none";
    localStorage.setItem("hideBanner", "true");
}

document.addEventListener("DOMContentLoaded", function () {
    function isMobile() {
        return /Android|iPhone|iPad|iPod|Windows Phone/i.test(navigator.userAgent);
    }

    if (isMobile()) {
        document.body.innerHTML = `
            <div id="mobile-warning" style="
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: black;
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                text-align: center;
                font-size: 20px;
                padding: 20px;
            ">
                <p>This site is not available on mobile. Please visit it from a desktop or laptop.</p>
            </div>
        `;
    }
});


