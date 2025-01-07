document.addEventListener("DOMContentLoaded", () => {
    const actionsList = document.getElementById("actions-list");
    const searchBtn = document.getElementById("search-btn");
    const searchInput = document.getElementById("search-action");
    const modal = document.getElementById("see-more-modal");
    const closeModalBtn = modal.querySelector(".close-btn");

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

    const renderActions = (actions) => {
        actionsList.innerHTML = actions
            .map(
                (action) =>
                    `<li class="action-item">
                        <div class="action-info">
                            <h4>${action.title} (${action.ticker})</h4>
                            <p>Price: $${action.price}</p>
                            <p>Change: ${action.change > 0 ? "+" : ""}${(action.change * 100).toFixed(2)}%</p>
                        </div>
                        <div class="action-chart">
                            <img src="/api/stock-chart/${action.ticker}" alt="${action.ticker} chart" />
                        </div>
                    </li>`
            )
            .join("");
    };
    

    const loadActions = async (searchTerm = "") => {
        const actions = await fetchActions(searchTerm);
        renderActions(actions);
    };

    searchBtn.addEventListener("click", () => {
        loadActions(searchInput.value);
    });

    loadActions(); // Initial load
});
