document.addEventListener("DOMContentLoaded", () => {
    const newsContainer = document.getElementById("news-container");
    let displayedNews = new Set();  // Stocke les news déjà affichées

    async function fetchNews() {
        try {
            const response = await fetch("/news");
            console.log("Response:", response);
            const news = await response.json();

            if (!Array.isArray(news) || news.length === 0) {
                newsContainer.innerHTML = "<li>No recent news available.</li>";
                return;
            }

            news.forEach((article, index) => {
                const newsIdentifier = article.title + article.link; // Identifiant unique
                
                if (!displayedNews.has(newsIdentifier)) {
                    displayedNews.add(newsIdentifier); // Ajoute aux news déjà affichées
                    
                    setTimeout(() => {
                        const item = document.createElement("li");
                        item.innerHTML = `<a href="${article.link}" target="_blank">${article.source}: ${article.title}</a>`;
                        newsContainer.prepend(item);

                        // Supprime la plus ancienne si on dépasse 20 news
                        if (newsContainer.children.length > 20) {
                            newsContainer.removeChild(newsContainer.lastChild);
                        }
                    }, index * 5000); // 5s entre chaque news
                }
            });

        } catch (error) {
            console.error("Error fetching news:", error);
        }
    }

    // Vérifie chaque seconde si on doit fetch les news
    fetchNews();
});

