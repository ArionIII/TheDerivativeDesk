document.addEventListener("DOMContentLoaded", () => {
    const actionsList = document.getElementById("actions-list");
    const searchInput = document.getElementById("search-action");
    const suggestionsDiv = document.createElement("div"); // Suggestions dropdown
    suggestionsDiv.className = "suggestions hidden";
    document.querySelector(".search-bar").appendChild(suggestionsDiv);

    // Modal
    const modal = document.getElementById("see-more-modal");
    const modalContent = modal.querySelector(".modal-content");
    const closeModalBtn = modal.querySelector(".close-btn");

    // Fetch actions from the server
    const fetchActions = async (searchTerm = "", limit = 4) => {
        try {
            const response = await fetch(`/api/stocks?search=${searchTerm}&limit=${limit}`);
            if (!response.ok) throw new Error("Failed to fetch stocks");
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
                            <img 
                                src="/static/images/loading-spinner.gif" 
                                data-src="/api/stock-chart/${action.ticker}" 
                                alt="${action.ticker} chart" 
                                class="chart-img"
                            />
                        </div>
                    </li>`
            )
            .join("");

        // Attach lazy loading to the charts
        attachChartLoaders();
    };

    // Attach loaders to chart images
    const attachChartLoaders = () => {
        const charts = document.querySelectorAll(".chart-img");

        charts.forEach((chart) => {
            const img = new Image();
            img.src = chart.dataset.src;

            img.onload = () => {
                chart.src = img.src; // Replace placeholder once loaded
            };

            img.onerror = () => {
                chart.src = "/static/images/error-placeholder.png"; // Fallback image if loading fails
            };
        });
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

            // Replace the last action and shift others
            const currentActions = Array.from(actionsList.children)
                .map((child) => {
                    try {
                        return JSON.parse(child.dataset.action);
                    } catch (err) {
                        console.error("Error parsing action data:", err);
                        return null;
                    }
                })
                .filter((action) => action !== null); // Filter out null entries

            const newAction = {
                title,
                ticker,
                price: parseFloat(price),
                change: parseFloat(change),
            };

            if (currentActions.length > 0) {
                currentActions.pop(); // Remove the last action
                const updatedActions = [newAction, ...currentActions];
                renderActions(updatedActions);
            }

            // Reset search bar
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
        console.log(`Fetching details for ${ticker}`); // Debugging log
        const stockDetails = await fetchStockDetails(ticker);
    
        if (stockDetails) {
            console.log("Stock details:", stockDetails); // Debugging log
            document.getElementById("modal-action-title").textContent = `${stockDetails.name} (${stockDetails.ticker})`;
            document.getElementById("stock-sector").textContent = `Sector: ${stockDetails.sector || "N/A"}`;
            document.getElementById("stock-industry").textContent = `Industry: ${stockDetails.industry || "N/A"}`;
            document.getElementById("stock-market-cap").textContent = `Market Cap: ${stockDetails.market_cap || "N/A"}`;
            document.getElementById("stock-52-week-high").textContent = `52-Week High: $${stockDetails["52_week_high"] || "N/A"}`;
            document.getElementById("stock-52-week-low").textContent = `52-Week Low: $${stockDetails["52_week_low"] || "N/A"}`;
            document.getElementById("stock-volume").textContent = `Volume: ${stockDetails.volume || "N/A"}`;
    
            // Render the chart
            const ctx = document.getElementById("detailed-stock-chart").getContext("2d");
            renderChart(ctx, stockDetails.chart_data.dates, stockDetails.chart_data.prices, stockDetails.chart_data.volumes);
    
            // Show the modal
            const modal = document.getElementById("see-more-modal");
            modal.classList.add("show");
            console.log("Modal displayed"); // Debugging log
        } else {
            console.error("Failed to fetch stock details. Data is null.");
            alert("Failed to fetch stock details. Please try again.");
        }
    };
    

    // Fetch stock details and chart data
    const fetchStockDetails = async (ticker) => {
        try {
            const response = await fetch(`/api/stock-details/${ticker}`);
            if (!response.ok) throw new Error("Failed to fetch stock details");
            const data = await response.json();
            return data.details;
        } catch (error) {
            console.error("Error fetching stock details:", error);
            return null;
        }
    };

    // Render the chart using Chart.js
    let activeChart = null; // Stocke l'instance active du graphique

    const renderChart = (ctx, dates, prices, volumes) => {
        console.log("Dates:", dates);
        console.log("Prices:", prices);
        console.log("Volumes:", volumes);

        // Détruire l'ancien graphique si nécessaire
        if (activeChart) {
            activeChart.destroy();
        }

        // Créer un nouveau graphique
        activeChart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: dates,
                datasets: [
                    {
                        type: "line",
                        label: "Closing Price (USD)",
                        data: prices,
                        borderColor: "#007bff",
                        backgroundColor: "rgba(0, 123, 255, 0.1)",
                        borderWidth: 2,
                        yAxisID: "y1",
                    },
                    {
                        type: "bar",
                        label: "Volume",
                        data: volumes,
                        backgroundColor: "rgba(255, 193, 7, 0.5)",
                        yAxisID: "y2",
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y1: {
                        position: "left",
                        ticks: { color: "#007bff" },
                        title: { display: true, text: "Price (USD)", color: "#007bff" },
                    },
                    y2: {
                        position: "right",
                        ticks: { color: "#ffc107" },
                        title: { display: true, text: "Volume", color: "#ffc107" },
                    },
                    x: {
                        ticks: {
                            maxTicksLimit: 10,
                        },
                    },
                },
            },
        });
    };

    // Close modal
    closeModalBtn.addEventListener("click", () => {
        console.log("Closing modal..."); // Debugging log
        modal.classList.add("hidden");
        modal.style.display = "none";
    });

    // Close modal when clicking outside the content
    modal.addEventListener("click", (e) => {
        if (e.target === modal) {
            console.log("Clicked outside modal content, closing modal."); // Debugging log
            modal.classList.add("hidden");
            modal.style.display = "none";
        }
    });
});
