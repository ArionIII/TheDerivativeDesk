document.addEventListener("DOMContentLoaded", function () {
  function isGooglebot() {
    return /Googlebot|AdsBot-Google-Mobile|Mediapartners-Google/i.test(
      navigator.userAgent,
    );
  }

  function isMobile() {
    return (
      /Android|iPhone|iPad|iPod|Windows Phone/i.test(navigator.userAgent) ||
      window.innerWidth < 768
    );
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (!isGooglebot() && isMobile()) {
      const warningDiv = document.createElement("div");
      warningDiv.id = "mobile-warning";
      warningDiv.style = `
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
            `;
      warningDiv.innerHTML = `<p>This site is not available on mobile. Please visit it from a desktop or laptop.</p>`;

      document.body.innerHTML = "";
      document.body.appendChild(warningDiv);
    }
  });

  // 🔍 Gestion du champ de recherche et suggestions
  const searchInputTools = document.getElementById("search-input-tools");
  const suggestionsContainerTools = document.getElementById(
    "suggestions-container-tools",
  );

  if (searchInputTools && suggestionsContainerTools) {
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

    //  Cacher les suggestions si l'utilisateur clique en dehors
    document.addEventListener("click", (e) => {
      if (
        !suggestionsContainerTools.contains(e.target) &&
        e.target !== searchInputTools
      ) {
        suggestionsContainerTools.innerHTML = "";
        suggestionsContainerTools.classList.remove("active");
      }
    });
  }

  // 🎉 Gestion de l'affichage de la bannière
  if (!localStorage.getItem("hideBanner")) {
    const siteBanner = document.getElementById("site-banner");
    if (siteBanner) {
      siteBanner.style.display = "block";
    }
  }
});

function closeBanner() {
  const siteBanner = document.getElementById("site-banner");
  if (siteBanner) {
    siteBanner.style.display = "none";
    localStorage.setItem("hideBanner", "true");
  }
}
