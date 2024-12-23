document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("tool-form");
    const results = document.getElementById("results");
    const chartElement = document.getElementById("chart");
    const toggleInput = document.getElementById("toggle-input");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // Collect form data
        const formData = new FormData(form);
        const inputData = Object.fromEntries(formData.entries());

        // Remove empty optional inputs before sending
        Object.keys(inputData).forEach((key) => {
            if (inputData[key].trim() === "") {
                delete inputData[key];
            }
        });

        // Add toggle value to data if toggle exists
        if (toggleInput) {
            inputData["long_position"] = toggleInput.checked;
        }

        try {
            // Send data to the server for calculation
            const response = await fetch(window.location.pathname, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(inputData),
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

            results.innerHTML = formatResultData(resultData);

            // Update visualization (if chart exists)
            if (chartElement) {
                const ctx = chartElement.getContext("2d");
                new Chart(ctx, {
                    type: "line",
                    data: {
                        labels: Array.from({ length: 10 }, (_, i) => i), // Example labels
                        datasets: [
                            {
                                label: "Forward Price Over Time",
                                data: Array.from({ length: 10 }, () => Math.random() * 100), // Example data
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

    // Helper function to format result data
    function formatResultData(data) {
        if (typeof data === "object" && data !== null) {
            return (
                `<ul>` +
                Object.values(data)
                    .map((value) => {
                        if (Array.isArray(value) && value.length === 2) {
                            return `<li>${value[0]} <strong>${value[1]}</strong></li>`;
                        } else if (typeof value === "object" && value !== null) {
                            return `<li>${formatResultData(value)}</li>`;
                        } else {
                            return `<li>${value !== null ? value : "N/A"}</li>`;
                        }
                    })
                    .join("") +
                `</ul>`
            );
        }
        return `<p>${data}</p>`;
    }
});
