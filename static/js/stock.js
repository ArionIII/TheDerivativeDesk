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
            console.log(data)
            return data.stocks || [];
        } catch (error) {
            console.error("Error fetching stocks:", error);
            return [];
        }
    };

    const renderActions = (actions) => {
        actionsList.innerHTML = ""; // Efface l'ancienne liste avant de rerendre
        
        actions.forEach(action => {
            const actionItem = document.createElement("li");
            actionItem.classList.add("action-item");
            actionItem.dataset.action = JSON.stringify(action);
    
            actionItem.innerHTML = `
                <div class="action-info">
                    <h4>
                        ${action.title} (${action.ticker})
                        <button class="see-more-btn" onclick="openSeeMore('${action.ticker}')">See More</button>
                        <button class="see-more-btn" onclick="openSeeNews('${action.ticker}')">See News</button>
                    </h4>
                    <p>Price: $${action.price !== null && !isNaN(action.price) ? action.price : "N/A"}</p>
                    <p style="color: ${action.change > 0 ? "green" : "red"};">
                        Change (1d): ${action.change !== null && !isNaN(action.change) ? (action.change * 100).toFixed(2) + "%" : "N/A"}
                    </p>
                    <p style="color: ${action.change_monthly > 0 ? "green" : "red"};">
                        Change (30d): ${action.change_monthly !== null && !isNaN(action.change_monthly) ? (action.change_monthly * 100).toFixed(2) + "%" : "N/A"}
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
            `;
    
            actionsList.appendChild(actionItem);
        });
    
        attachChartLoaders(); // Charge les graphiques correctement après le rendu
    };
    
    

    // Attach loaders to chart images
    const attachChartLoaders = () => {
        const charts = document.querySelectorAll(".chart-img");
    
        charts.forEach((chart) => {
            const img = new Image();
            img.src = chart.dataset.src;
    
            img.onload = () => {
                console.log(`Image loaded successfully for ${chart.dataset.src}`);
                chart.src = img.src;
                chart.classList.remove("error-chart"); // Enlève la classe si l'image est chargée correctement
            };
    
            img.onerror = () => {
                console.error(`Error loading image for ${chart.dataset.src}`);
                chart.src = "/static/images/error-placeholder.png"; // Fallback image
                chart.classList.add("error-chart"); // Ajoute la classe CSS spéciale
            };
        });
    };
    
    

    // Render search suggestions
    const renderSuggestions = (stocks) => {
        suggestionsDiv.innerHTML = ""; // Effacer les anciennes suggestions
    
        stocks.forEach((stock) => {
            const item = document.createElement("p");
            item.classList.add("suggestion-item");
            item.dataset.title = stock.title;
            item.dataset.ticker = stock.ticker;
            item.dataset.price = stock.price;
            item.dataset.change = stock.change;
            item.dataset.change_monthly = stock.change_monthly;
            item.innerHTML = `<strong>🛠️ ${stock.title} (${stock.ticker})</strong>`;
    
            item.addEventListener("click", () => {
                console.log(`Clicked suggestion: ${stock.ticker}`);
                selectStock(stock);
            });
    
            suggestionsDiv.appendChild(item);
        });
    
        suggestionsDiv.classList.remove("hidden");
    };


    const selectStock = async (stock) => {
        console.log("Selected stock:", stock);
    
        // Vérifier si le stock est déjà affiché
        const existingStock = Array.from(actionsList.children)
            .some((child) => JSON.parse(child.dataset.action || "{}").ticker === stock.ticker);
    
        if (existingStock) {
            console.log(`Stock ${stock.ticker} already exists, skipping.`);
            return;
        }
    
        // 🔹 Récupérer les détails du stock avec `detailed=true`
        const response = await fetch(`/api/stocks?search=${stock.ticker}&limit=1&detailed=true`);
        const data = await response.json();
        
        if (!data.stocks || data.stocks.length === 0) {
            console.error(`Failed to fetch detailed data for ${stock.ticker}`);
            return;
        }
    
        const stockDetails = data.stocks[0];
    
        // 🔹 Construire l'objet avec des valeurs correctes
        const newAction = {
            title: stockDetails.title,
            ticker: stockDetails.ticker,
            price: stockDetails.price !== null && !isNaN(stockDetails.price) ? stockDetails.price : "N/A",
            change: stockDetails.change !== null && !isNaN(stockDetails.change) ? stockDetails.change : "N/A",
            change_monthly: stockDetails.change_monthly !== null && !isNaN(stockDetails.change_monthly) ? stockDetails.change_monthly : "N/A",
        };
    
        const currentActions = Array.from(actionsList.children)
            .map((child) => JSON.parse(child.dataset.action || "{}"))
            .filter((action) => action && action.ticker);
    
        currentActions.pop(); // Supprime le dernier élément
        const updatedActions = [newAction, ...currentActions];
    
        renderActions(updatedActions);
    
        searchInput.value = "";
        hideSuggestions();
    };
    
    
    

    // Hide suggestions
    const hideSuggestions = () => {
        console.log("Hiding suggestions..."); // Debugging log
        suggestionsDiv.innerHTML = "";
        suggestionsDiv.classList.add("hidden");
    };

    // Handle clicks outside of search input or suggestions
    document.addEventListener("click", (e) => {
        if (!searchInput.contains(e.target) && !suggestionsDiv.contains(e.target)) {
            hideSuggestions();
    }
});

    // Search input event
    searchInput.addEventListener("input", async (e) => {
        const searchTerm = e.target.value.trim();
        if (searchTerm) {
            const suggestions = await fetchActions(searchTerm, 10); // Fetch more for suggestions
            renderSuggestions(suggestions);
            setTimeout(() => {
                document.addEventListener("click", outsideClickHandler);
            }, 200);
        } else {
            hideSuggestions();
        }
    });

    const outsideClickHandler = (e) => {
        if (!searchInput.contains(e.target) && !suggestionsDiv.contains(e.target)) {
            hideSuggestions();
            document.removeEventListener("click", outsideClickHandler); // Nettoyer l'écouteur après fermeture
        }
    };

    // Handle suggestion click
    suggestionsDiv.addEventListener("click", (e) => {
        if (e.target.classList.contains("suggestion-item")) {
            const { title, ticker, price, change, change_monthly } = e.target.dataset;

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
                change_monthly: parseFloat(change_monthly)
            };
            console.log("New action:", newAction); // Debugging log

            if (currentActions.length > 0) {
                currentActions.pop(); // Remove the last action
                const updatedActions = [newAction, ...currentActions];
                // renderActions(updatedActions);
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
        // 🔹 Informations générales
        document.getElementById("modal-action-title").textContent = `${stockDetails.name} (${stockDetails.ticker})`;
        document.getElementById("stock-sector").textContent = `Sector: ${stockDetails.sector || "N/A"}`;
        document.getElementById("stock-industry").textContent = `Industry: ${stockDetails.industry || "N/A"}`;
        document.getElementById("stock-market-cap").textContent = `Market Cap: ${formatNumber(stockDetails.market_cap)}`;
        document.getElementById("stock-exchange").textContent = `Exchange: ${stockDetails.exchange || "N/A"}`;
        document.getElementById("stock-currency").textContent = `Currency: ${stockDetails.currency || "N/A"}`;
        document.getElementById("stock-website").innerHTML = `<a href="${stockDetails.website}" target="_blank">${stockDetails.website}</a>`;

        // 🔹 Prix et performances
        document.getElementById("stock-current-price").textContent = `Current Price: $${stockDetails.current_price || "N/A"}`;
        document.getElementById("stock-52-week-high").textContent = `52-Week High: $${stockDetails["52_week_high"] || "N/A"}`;
        document.getElementById("stock-52-week-low").textContent = `52-Week Low: $${stockDetails["52_week_low"] || "N/A"}`;
        document.getElementById("stock-day-high").textContent = `Day High: $${stockDetails.day_high || "N/A"}`;
        document.getElementById("stock-day-low").textContent = `Day Low: $${stockDetails.day_low || "N/A"}`;
        document.getElementById("stock-volume").textContent = `Volume: ${formatNumber(stockDetails.volume)}`;
        document.getElementById("stock-average-volume").textContent = `Avg Volume (10d): ${formatNumber(stockDetails.average_volume_10d)}`;

        // 🔹 Ratios financiers
        document.getElementById("stock-pe-ratio").textContent = `P/E Ratio: ${stockDetails.pe_ratio || "N/A"}`;
        document.getElementById("stock-forward-pe").textContent = `Forward P/E: ${stockDetails.forward_pe || "N/A"}`;
        document.getElementById("stock-peg-ratio").textContent = `PEG Ratio: ${stockDetails.peg_ratio || "N/A"}`;
        document.getElementById("stock-price-to-book").textContent = `P/B Ratio: ${stockDetails.price_to_book || "N/A"}`;
        document.getElementById("stock-price-to-sales").textContent = `P/S Ratio: ${stockDetails.price_to_sales || "N/A"}`;

        // 🔹 Rentabilité et marges
        document.getElementById("stock-roa").textContent = `Return on Assets (ROA): ${formatPercentage(stockDetails.return_on_assets)}`;
        document.getElementById("stock-roe").textContent = `Return on Equity (ROE): ${formatPercentage(stockDetails.return_on_equity)}`;
        document.getElementById("stock-profit-margins").textContent = `Profit Margins: ${formatPercentage(stockDetails.profit_margins)}`;
        document.getElementById("stock-operating-margins").textContent = `Operating Margins: ${formatPercentage(stockDetails.operating_margins)}`;
        document.getElementById("stock-ebitda").textContent = `EBITDA: ${formatNumber(stockDetails.ebitda)}`;

        // 🔹 Dividendes et Cashflow
        document.getElementById("stock-dividend-yield").textContent = `Dividend Yield: ${formatPercentage(stockDetails.dividend_yield)}`;
        document.getElementById("stock-dividend-rate").textContent = `Dividend Rate: $${stockDetails.dividend_rate || "N/A"}`;
        document.getElementById("stock-payout-ratio").textContent = `Payout Ratio: ${formatPercentage(stockDetails.payout_ratio)}`;
        document.getElementById("stock-free-cashflow").textContent = `Free Cash Flow: ${formatNumber(stockDetails.free_cashflow)}`;

        // 🔹 Analyst Ratings
        document.getElementById("stock-recommendation").textContent = `Recommendation: ${stockDetails.recommendation || "N/A"}`;
        document.getElementById("stock-target-price").textContent = `Target Price: $${stockDetails.target_mean_price || "N/A"}`;
        document.getElementById("stock-target-high").textContent = `Target High: $${stockDetails.target_high_price || "N/A"}`;
        document.getElementById("stock-target-low").textContent = `Target Low: $${stockDetails.target_low_price || "N/A"}`;

        // 🔹 Render the stock chart
        const ctx = document.getElementById("detailed-stock-chart").getContext("2d");
        ensureChartRender(ctx, stockDetails.chart_data.dates, stockDetails.chart_data.prices, stockDetails.chart_data.volumes);


        // 🔹 Show the modal
        const modal = document.getElementById("see-more-modal");
        modal.classList.add("show");
        modal.style.display = "block"
        console.log("Modal displayed"); // Debugging log
    } else {
        console.error("Failed to fetch stock details. Data is null.");
        alert("Failed to fetch stock details. Please try again.");
    }
};

// 🔹 Utilitaires pour formater les nombres et pourcentages
const formatNumber = (num) => {
    return num !== "N/A" && num !== null ? num.toLocaleString() : "N/A";
};

const formatPercentage = (num) => {
    return num !== "N/A" && num !== null ? `${(num * 100).toFixed(2)}%` : "N/A";
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
        console.log("Rendering chart...");
    
        if (!dates || !prices || !volumes || dates.length === 0 || prices.length === 0 || volumes.length === 0) {
            console.error("Chart data is missing or empty. Skipping chart rendering.");
            return;
        }
    
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
    const ensureChartRender = (ctx, dates, prices, volumes) => {
        if (!Array.isArray(dates) || !Array.isArray(prices) || dates.length === 0 || prices.length === 0) {
            console.error(`Skipping chart rendering: Missing data for ${ctx.canvas.id}`);
            ctx.canvas.parentNode.innerHTML = "<p style='color:red;'>Chart unavailable</p>";
            return;
        }
    
        setTimeout(() => {
            renderChart(ctx, dates, prices, volumes);
        }, 500);
    };
    
    
    

    // Close modal
    closeModalBtn.addEventListener("click", () => {
        console.log("Closing modal..."); // Debugging log
        modal.classList.add("hidden");
        modal.style.display = "none";

    });

    // Close modal when clicking outside the content
    modal.addEventListener("click", (e) => {
    if (!modal.contains(e.target) || e.target === modal) {
        console.log("Clicked outside modal content, closing modal."); // Debugging log
        closeModal();
    }
});


    // SEE NEWS
    // Modal for news
    const newsModal = document.createElement("div");
    newsModal.id = "see-news-modal";
    newsModal.className = "modal hidden";
    newsModal.innerHTML = `
    <div class="modal-content">
        <span class="close-btn-see-news" onclick="closeNewsModal()">&times;</span>
        <h2 id="modal-news-title">Stock News</h2>
        <div id="news-container"></div>
        <button class="close-news-button" onclick="closeNewsModal()">Close</button>
    </div>
`;

    document.body.appendChild(newsModal);

    // Fetch stock news
    const fetchStockNews = async (ticker) => {
        try {
            const response = await fetch(`/api/stock-news/${ticker}`);
            if (!response.ok) throw new Error("Failed to fetch stock news");
            const data = await response.json();
            return data.news || [];
        } catch (error) {
            console.error("Error fetching stock news:", error);
            return [];
        }
    };

    // Open "See News" modal
    window.openSeeNews = async (ticker) => {
        console.log(`Fetching news for ${ticker}`); // Debugging log

        const newsArticles = await fetchStockNews(ticker);
        if (newsArticles.length === 0) {
            document.getElementById("news-container").innerHTML = "<p>No news available.</p>";
        } else {
            document.getElementById("modal-news-title").textContent = `Latest News for ${ticker}`;
            document.getElementById("news-container").innerHTML = newsArticles.map(article => `
                <div class="news-item">
                    <h3><a href="${article.link}" target="_blank">${article.title}</a></h3>
                    <p><strong>${article.published}</strong></p>
                    <p>${article.summary}</p>
                </div>
            `).join("");
        }

        newsModal.classList.remove("hidden");
        newsModal.style.display = "block";
    };

    // Close "See News" modal
    window.closeNewsModal = () => {
        console.log("Closing news modal..."); // Debugging log
        newsModal.classList.add("hidden");
        newsModal.style.display = "none";
    };



});

function closeModal() {
    console.log("Closing modal..."); // Debugging log
    const modal = document.getElementById("see-more-modal");
    if (modal) {
        modal.classList.add("hidden");
        modal.style.display = "none";
    }
}
