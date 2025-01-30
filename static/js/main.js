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
