document.addEventListener("DOMContentLoaded", () => {
    const newsList = document.getElementById("news-list");
    const loader = document.createElement("div");
    loader.classList.add("spinner");
    newsList.appendChild(loader); // Ajoute le spinner au début

    async function fetchNews() {
        try {
            newsList.innerHTML = `<li class="loading-message">Loading news... <div class="spinner"></div></li>`;

            const response = await fetch("/api/news");
            const news = await response.json();

            if (!Array.isArray(news) || news.length === 0) {
                newsList.innerHTML = "<li>No recent news available.</li>";
                return;
            }

            newsList.innerHTML = ""; // Vide la liste avant d'ajouter de nouvelles news

            news.forEach((article) => {
                const item = document.createElement("li");
                item.innerHTML = `
                    <a href="${article.link}" target="_blank">
                        <strong>${article.source}:</strong> ${article.title}
                    </a>
                    <span class="news-date">${formatDate(article.published)}</span>
                `;
                newsList.appendChild(item);
            });

        } catch (error) {
            console.error("Error fetching news:", error);
            newsList.innerHTML = "<li>Error loading news.</li>";
        }
    }

    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString(); // Affiche uniquement "JJ/MM/AAAA"
    }

    fetchNews();
    setInterval(fetchNews, 60000); // Rafraîchit toutes les minutes
});
