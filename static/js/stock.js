document.addEventListener("DOMContentLoaded", () => {
    const actionsList = document.getElementById("actions-list");
    const searchInput = document.getElementById("search-action");
    const suggestionsDiv = document.createElement("div"); // Suggestions dropdown
    suggestionsDiv.className = "suggestions hidden";
    document.querySelector(".search-bar").appendChild(suggestionsDiv);

    // Fetch actions from the server
    const fetchActions = async (searchTerm = "", limit = 4) => {
        try {
            const response = await fetch(`/api/stocks?search=${searchTerm}&limit=${limit}`);
            if (!response.ok) {
                throw new Error("Failed to fetch stocks");
            }
            const data = await response.json();
            return data.stocks || [];
        } catch (error) {
            console.error("Error fetching stocks:", error);
            return [];
        }
    };

    // Render actions on the page
    const renderActions = (actions) => {
        actionsList.innerHTML = actions
            .map(
                (action) =>
                    `<li class="action-item" data-action='${JSON.stringify(action)}'>
                        <div class="action-info">
                            <h4>
                                ${action.title} (${action.ticker})
                                <button class="see-more-btn" onclick="openSeeMore('${action.ticker}')">See More</button>
                            </h4>
                            <p>Price: $${action.price}</p>
                            <p style="color: ${action.change > 0 ? "green" : "red"};">
                                Change: ${action.change > 0 ? "+" : ""}${(action.change * 100).toFixed(2)}%
                            </p>
                        </div>
                        <div class="action-chart">
                            <img src="/api/stock-chart/${action.ticker}" alt="${action.ticker} chart" />
                        </div>
                    </li>`
            )
            .join("");
    };
    

    // Render search suggestions
    const renderSuggestions = (stocks) => {
        suggestionsDiv.innerHTML = stocks
            .map(
                (stock) =>
                    `<p class="suggestion-item" 
                        data-title="${stock.title}" 
                        data-ticker="${stock.ticker}" 
                        data-price="${stock.price}" 
                        data-change="${stock.change}">
                        ${stock.title} (${stock.ticker})
                    </p>`
            )
            .join("");

        suggestionsDiv.classList.remove("hidden");
    };

    // Hide suggestions
    const hideSuggestions = () => {
        suggestionsDiv.innerHTML = "";
        suggestionsDiv.classList.add("hidden");
    };

    // Search input event
    searchInput.addEventListener("input", async (e) => {
        const searchTerm = e.target.value.trim();
        if (searchTerm) {
            const suggestions = await fetchActions(searchTerm, 10); // Fetch more for suggestions
            renderSuggestions(suggestions);
        } else {
            hideSuggestions();
        }
    });

    // Handle suggestion click
    suggestionsDiv.addEventListener("click", (e) => {
        if (e.target.classList.contains("suggestion-item")) {
            const { title, ticker, price, change } = e.target.dataset;
    
            // Remplacer la dernière action et décaler les autres
            const currentActions = Array.from(actionsList.children).map((child) => {
                try {
                    return JSON.parse(child.dataset.action);
                } catch (err) {
                    console.error("Error parsing action data:", err);
                    return null; // Si erreur, ignore l'action
                }
            }).filter((action) => action !== null); // Filtrer les entrées nulles
    
            const newAction = {
                title,
                ticker,
                price: parseFloat(price),
                change: parseFloat(change),
            };
    
            if (currentActions.length > 0) {
                currentActions.pop(); // Supprimer la dernière action
                const updatedActions = [newAction, ...currentActions];
    
                renderActions(updatedActions);
            }
    
            // Réinitialiser la barre de recherche
            searchInput.value = "";
            hideSuggestions();
        }
    });
    

    // Fetch and render actions
    const loadActions = async (searchTerm = "") => {
        const actions = await fetchActions(searchTerm);
        renderActions(actions);
    };

    // Load initial actions
    loadActions();

    // Modal handling
    window.openSeeMore = async (ticker) => {
        alert(`Showing details for ${ticker}`);
    };

    // Close suggestions on outside click
    document.addEventListener("click", (e) => {
        if (!e.target.closest(".search-bar")) {
            hideSuggestions();
        }
    });
});
