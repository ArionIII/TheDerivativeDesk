document.addEventListener("DOMContentLoaded", () => {
    const searchForm = document.querySelector(".navbar-search");
    const searchInput = searchForm.querySelector("input[name='q']");
    const resultsContainer = document.getElementById("search-results");
    const noResultsMessage = document.getElementById("no-results");

    // Handle form submission
    searchForm.addEventListener("submit", (event) => {
        event.preventDefault();
        const query = searchInput.value.trim();
        if (query) {
            performSearch(query);
        }
    });

    // Perform search via AJAX
    async function performSearch(query) {
        try {
            const response = await fetch(`/search?q=${encodeURIComponent(query)}`, {
                headers: {
                    "X-Requested-With": "XMLHttpRequest", // Identify as AJAX
                },
            });
            const results = await response.json();

            // Update results dynamically
            updateResults(results);
        } catch (error) {
            console.error("Error fetching search results:", error);
        }
    }

    // Update results in the DOM
    function updateResults(results) {
        resultsContainer.innerHTML = ""; // Clear current results

        if (results.length > 0) {
            results.forEach((tool) => {
                const resultItem = document.createElement("li");
                resultItem.innerHTML = `
                    <a href="${tool.url}">
                        <h3>${tool.name}</h3>
                        <p>${tool.description}</p>
                    </a>
                `;
                resultsContainer.appendChild(resultItem);
            });
            noResultsMessage.style.display = "none";
        } else {
            noResultsMessage.style.display = "block";
        }
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.querySelector(".navbar-search input[name='q']");
    const suggestionsContainer = document.createElement("div");
    suggestionsContainer.classList.add("suggestions-container");
    searchInput.parentNode.appendChild(suggestionsContainer);

    searchInput.addEventListener("input", async (e) => {
        const query = e.target.value.trim();

        // Clear suggestions if input is empty
        if (!query) {
            suggestionsContainer.innerHTML = "";
            return;
        }

        try {
            const response = await fetch(`/suggest?q=${encodeURIComponent(query)}`);
            const suggestions = await response.json();

            // Populate suggestions
            suggestionsContainer.innerHTML = suggestions
            .map(
                (s) =>
                    `<a href="${s.url}" class="suggestion-item">
                        <div>
                            <strong>${s.name}</strong>
                            <p>${s.description}</p>
                        </div>
                    </a>`
            )
            .join("");


        } catch (err) {
            console.error("Error fetching suggestions:", err);
        }
    });

    // Style suggestions container
    document.addEventListener("click", (e) => {
        if (!suggestionsContainer.contains(e.target) && e.target !== searchInput) {
            suggestionsContainer.innerHTML = ""; // Close suggestions if clicked outside
        }
    });
});
