console.log('TOOL.JS LOADED')
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("tool-form");
    const results = document.getElementById("results");
    const chartElement = document.getElementById("chart");
    let activeChart = null;

    form.setAttribute("novalidate", true); // Disable native validation

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // Custom form validation
        const isValid = validateForm();
        if (!isValid) {
            alert("Please complete the required fields or remove conflicting inputs.");
            return;
        }

        // Collect form data
        const formData = new FormData(form);
        const inputData = {};

        // Process inputs
        formData.forEach((value, key) => {
            const inputElement = document.querySelector(`[name="${key}"]`);

            // Handle CSV inputs
            if (inputElement && inputElement.type === "file" && inputElement.files.length > 0) {
                const dataTarget = inputElement.getAttribute("data_target");

                if (dataTarget) {
                    // If CSV has a data_target, remove the target input
                    formData.delete(dataTarget);
                }

                // Add the file to the inputData for backend processing
                inputData[key] = inputElement.files[0];
            } else {
                // Add other inputs (non-file inputs)
                inputData[key] = value;
            }
        });

        try {
            console.log("Sending data to the server:", inputData);

            // Prepare the request payload
            const requestPayload = new FormData();
            Object.entries(inputData).forEach(([key, value]) => {
                requestPayload.append(key, value);
            });
            console.log("Request payload:", requestPayload);
            // Send data to the server for calculation
            const response = await fetch(window.location.pathname, {
                method: "POST",
                body: requestPayload, // Send as FormData to handle file uploads
            });

            if (!response.ok) {
                throw new Error("Failed to fetch results from the server.");
            }

            const resultData = await response.json();

            // Update results dynamically
            if (resultData.error) {
                results.innerHTML = `<p class="error">${resultData.error}</p>`;
                return;
            }
            // Si c'est un tool de visualization en temps réel
            if (resultData.is_live) {
                updateChart(resultData, "live-chart"); // ✅ Gère automatiquement le graphique live
            }


            const graphs = {};
            const cleanResultData = {};
            Object.keys(resultData).forEach(key => {
                if (key.startsWith("graph_")) {
                    graphs[key] = resultData[key];  // Stocke les graphes dans un objet séparé
                } else {
                    cleanResultData[key] = resultData[key];  // Garde les autres valeurs
                }
            });

            if (Object.keys(graphs).length > 0) {
                console.log("Graphs:", graphs);
                insertGraphs(graphs);
            }
            console.log('JUST BEFORE DOWNLOAD FILES')
            if (isAllFiles(resultData)) {
                console.log('IS ALL FILES TRUE')
                results.innerHTML = `<p class="success">Your files were successfully downloaded.</p>`;
                downloadFiles(resultData);
                console.log("Files:", resultData);
            } else {
                console.log('IS ALL FILES FALSE')
                results.innerHTML = formatResultData(resultData);
                console.log("Results:", resultData);
            }

            // Update visualization (if chart exists)
            
            if (!chartElement) {
                console.warn("Chart element not found");
                return;
            }
            if (chartElement) {
                const ctx = chartElement.getContext("2d");
            
                // Si un graphique existe déjà, on le détruit avant de recréer le nouveau
                if (activeChart) {
                    activeChart.destroy();
                }
            
                activeChart = new Chart(ctx, {
                    type: "line",
                    data: {
                        labels: Array.from({ length: 10 }, (_, i) => i),
                        datasets: [
                            {
                                label: "Forward Price Over Time",
                                data: Array.from({ length: 10 }, () => Math.random() * 100),
                                backgroundColor: "rgba(255, 140, 0, 0.5)",
                            },
                        ],
                    },
                });
            }
        } catch (error) {
            console.error("Error during submission:", error);
            alert("An error occurred while calculating results. Please try again.");
        }
    });

    function insertGraphs(graphs) {
        Object.keys(graphs).forEach((key, index) => {
            const graphUrl = graphs[key];  // URL de l'image du graph
            const graphImage = document.getElementById(`graph-${index + 1}`); // ID basé sur le loop.index
    
            if (graphImage) {
                graphImage.src = graphUrl; // Met à jour l'image avec l'URL correcte
                graphImage.alt = `Graph ${index + 1}`; // Ajoute une description alternative
            } else {
                console.warn(`Graph image element with ID 'graph-${index + 1}' not found.`);
            }
        });
    }
    

    // Helper function to format result data
    function formatResultData(data) {
        console.log("DATA RESULT", data);
        if (typeof data === "object" && data !== null) {
            return (
                `<ul>` +
                Object.values(data) // On récupère uniquement les valeurs des objets (sans afficher les clés)
                    .map((value) => {
                        if (Array.isArray(value) && value.length === 2) {
                            // On suppose que chaque tableau contient ["display_name", valeur]
                            return `<li><strong>${value[0]}</strong> ${value[1]}</li>`;
                        }
                        return ""; // Ignorer les entrées qui ne correspondent pas au format attendu
                    })
                    .join("") +
                `</ul>`
            );
        }
        return `<p>${data}</p>`;
    }
    
    

    // Manage mutual exclusivity for CSV inputs with data_target
    const csvInputs = document.querySelectorAll('input[type="file"][data_target]');
    csvInputs.forEach((csvInput) => {
        const targetInputId = csvInput.getAttribute("data_target");
        const targetInput = document.getElementById(targetInputId);

        csvInput.addEventListener("change", () => {
            if (csvInput.files.length > 0) {
                if (targetInput) {
                    targetInput.disabled = true; // Disable target input if CSV is provided
                    targetInput.setAttribute("optional", "true"); // Mark as optional
                }
            } else {
                if (targetInput) {
                    targetInput.disabled = false; // Enable target input if CSV is cleared
                    targetInput.setAttribute("optional", "false"); // Mark as non-optional
                }
            }
        });

        if (targetInput) {
            targetInput.addEventListener("input", () => {
                if (targetInput.value.trim() !== "") {
                    csvInput.disabled = true; // Disable CSV input if target input is filled
                } else {
                    csvInput.disabled = false; // Enable CSV input if target input is cleared
                }
            });
        }
    });

    // Handle download button click
    // IS ALL FILES est TRUE si tous les éléments de l'objet sont des fichiers valides, ET NE PREND PAS EN COMPTE LES LIENS VERS GRAPHS
    function isAllFiles(data) {
        console.log("DATA", data);
        
        if (typeof data !== "object" || data === null) {
            return false; // Si data n'est pas un objet ou est null, ce n'est pas un fichier
        }
    
        const values = Object.values(data);
    
        // Vérifier si tous les éléments sont des fichiers valides (dans "static/outputs/" ou "/static/graphs/")
        const allFilePaths = values.every(value => 
            (typeof value === "string" && 
                (value.startsWith("static/outputs/") || value.startsWith("/static/graphs/")) // ✅ Accepter aussi les .png
            ) ||
            (typeof value === "object" && value !== null && isAllFiles(value)) // Vérifier récursivement pour les dictionnaires imbriqués
        );
    
        return values.length > 0 && allFilePaths;
    }
    
    
    
    
    
// NE DOWNLOAD PAS LES PNG, POUR NE PAS DOWNLOAD LES GRAPHS (inutile)
    function downloadFiles(files) {
        Object.values(files).forEach(fileUrl => {
            // Vérifier si le fichier est une image .png et l'ignorer
            if (fileUrl.endsWith(".png")) {
                console.log("Skipping download for image:", fileUrl);
                return; // Ignore ce fichier et passe au suivant
            }
    
            // Construire l'URL complet en supprimant les "/" en trop
            const fullUrl = window.location.origin + "/" + fileUrl.replace(/^\/+/, "");  
    
            console.log("Downloading file:", fullUrl);
    
            // Créer un élément <a> pour déclencher le téléchargement
            const link = document.createElement("a");
            link.href = fullUrl;
            link.download = fileUrl.split("/").pop(); // Extraire uniquement le nom du fichier
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
    }
    
    

    // Validate form inputs
    function validateForm() {
        let isValid = true;

        // Check for optional=False inputs
        form.querySelectorAll("[optional='false']").forEach((input) => {
            if (input.disabled) {
                return; // Skip disabled inputs
            }

            if (input.type === "file" && input.files.length > 0) {
                const dataTarget = input.getAttribute("data_target");
                if (dataTarget) {
                    // If a CSV input is provided, ensure its target is ignored
                    const targetInput = document.getElementById(dataTarget);
                    if (targetInput) {
                        targetInput.disabled = true; // Ensure the target input is ignored
                    }
                }
                return; // CSV input is valid
            }

            if (input.type !== "file" && input.value.trim() !== "") {
                return; // Non-file input is valid
            }

            // If neither condition is met, the field is invalid
            isValid = false;
        });

        return isValid;
    }
});

const activeCharts = {}; // ✅ Stockage dynamique des graphiques actifs

function updateChart(resultData, chartId) {
    console.log(`🔥 Updating chart: ${chartId}`);

    // ✅ Si un graphique est déjà actif → le supprimer
    if (activeCharts[chartId]) {
        activeCharts[chartId].destroy?.(); // ✅ Si c'est Chart.js, on détruit le graphique
        Plotly.purge(chartId); // ✅ Si c'est Plotly, on le supprime aussi
    }

    const ctx = document.getElementById(chartId);

    if (resultData.z_axis) {
        // ✅ Mode 3D → Utilisation de Plotly.js
        console.log("🌐 Plotting 3D Surface Chart");

        const trace = {
            x: resultData.x_axis.value,
            y: resultData.y_axis.value,
            z: resultData.z_axis.value,
            type: 'surface',
            colorscale: 'Viridis'
        };

        const layout = {
            title: '3D Surface Plot',
            autosize: true,
            scene: {
                xaxis: { title: resultData.x_axis.label },
                yaxis: { title: resultData.y_axis.label },
                zaxis: { title: resultData.z_axis.label }
            }
        };

        Plotly.newPlot(chartId, [trace], layout);
        activeCharts[chartId] = Plotly; // ✅ Stocker l'objet Plotly
    } else {
        // ✅ Mode 2D → Utilisation de Chart.js
        console.log("📈 Plotting 2D Line Chart");

        const datasets = Object.keys(resultData)
            .filter(key => !["is_live", "x_axis", "y_axis", "z_axis"].includes(key))
            .map(key => {
                const series = resultData[key];
                return {
                    label: series.label,
                    data: series.data,
                    borderColor: series.borderColor,
                    fill: series.fill || false,
                };
            });

        activeCharts[chartId] = new Chart(ctx.getContext("2d"), {
            type: "line",
            data: {
                labels: resultData.x_axis.value,
                datasets: datasets
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: resultData.x_axis.label
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: resultData.y_axis.label
                        }
                    }
                }
            }
        });
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("tool-form");
    const sliders = form.querySelectorAll("input, select"); // ✅ Récupère tous les sliders et selects

    sliders.forEach(slider => {
        slider.addEventListener("input", () => {
            console.log(`🔄 Value changed: ${slider.name} → ${slider.value}`);
            updateLiveChart(); // ✅ Déclenche une mise à jour automatique
        });
    });
});

async function updateLiveChart() {
    console.log("🔥 Updating live chart...");

    // ✅ Récupérer les valeurs du formulaire
    const inputData = {};
    const formElements = document.getElementById("tool-form").elements;
    
    for (const element of formElements) {
        if (element.name) {
            inputData[element.name] = element.value;
        }
    }

    console.log("🔎 Data sent to backend:", inputData);

    try {
        const response = await fetch(window.location.pathname, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(inputData)
        });

        if (!response.ok) throw new Error("Failed to update live chart");

        const resultData = await response.json();

        console.log("✅ New chart data received:", resultData);

        // ✅ Appeler le gestionnaire de graphique avec les nouvelles données
        if (resultData.is_live) {
            updateChart(resultData, "live-chart");
        } else {
            updateChart(resultData, "static-chart");
        }

    } catch (error) {
        console.error("❌ Error updating chart:", error);
    }
}
