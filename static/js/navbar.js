document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.querySelector(".navbar-search input[name='q']");
    const searchContainer = document.querySelector(".navbar-search");
    const suggestionsContainer = document.createElement("div");
    suggestionsContainer.classList.add("suggestions-container");
    searchContainer.appendChild(suggestionsContainer);

    console.log("searchInput found:", searchInput);
    console.log("searchContainer found:", searchContainer);
    console.log("suggestionsContainer added:", suggestionsContainer);

    searchInput.addEventListener("input", async (e) => {
        const query = e.target.value.trim();

        // Clear suggestions if input is empty
        if (!query) {
            suggestionsContainer.innerHTML = "";
            suggestionsContainer.classList.remove("active"); // Hide container
            return;
        }

        try {
            const response = await fetch(`/suggest?q=${encodeURIComponent(query)}`);
            const suggestions = await response.json();
            console.log("suggestions found:", suggestions);
            if (suggestions.length > 0) {
                // Populate suggestions
                suggestionsContainer.innerHTML = suggestions
                    .map((s) => {
                        const highlightedTitle = s.name.replace(
                            new RegExp(`(${query})`, "gi"),
                            `<span class="highlight">$1</span>`
                        );
                        const highlightedDescription = s.description.replace(
                            new RegExp(`(${query})`, "gi"),
                            `<span class="highlight">$1</span>`
                        );

                        return `
                            <div class="suggestion-item">
                                <a href="${s.url}">${highlightedTitle}</a>
                                <p>${highlightedDescription}</p>
                            </div>
                        `;
                    })
                    .join("");

                console.log("suggestionsContainer HTML:", suggestionsContainer.innerHTML);
                suggestionsContainer.classList.add("active"); // Show container
                console.log("suggestionsContainer classes:", suggestionsContainer.classList);
                
            } else {
                suggestionsContainer.innerHTML = ""; // No suggestions
                suggestionsContainer.classList.remove("active"); // Hide container
            }
        } catch (err) {
            console.error("Error fetching suggestions:", err);
        }
    });

    // Close suggestions when clicking outside
    document.addEventListener("click", (e) => {
        if (!suggestionsContainer.contains(e.target) && e.target !== searchInput) {
            suggestionsContainer.innerHTML = ""; // Clear suggestions
            suggestionsContainer.classList.remove("active"); // Hide container
        }
    });
});
