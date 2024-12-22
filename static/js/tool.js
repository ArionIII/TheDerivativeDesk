document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("tool-form");
    const results = document.getElementById("results");
    const chartElement = document.getElementById("chart");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // Collect form data
        const formData = new FormData(form);
        const inputData = Object.fromEntries(formData.entries());

        // Remove empty optional inputs before sending
        for (const key in inputData) {
            if (inputData[key].trim() === "") {
                delete inputData[key];
            }
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

            // Update results
            results.querySelectorAll("span").forEach((span, index) => {
                const resultKey = Object.keys(resultData)[index];
                span.textContent = resultData[resultKey] || "N/A";
            });

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

    // Real-time optional input validation
    form.querySelectorAll("input").forEach((input) => {
        if (input.hasAttribute("optional")) {
            input.addEventListener("input", () => {
                // Optional inputs can be left empty, so no error unless the value is invalid
                if (input.value && input.type === "number" && parseFloat(input.value) < 0) {
                    input.setCustomValidity("Value cannot be negative.");
                } else {
                    input.setCustomValidity("");
                }
            });
        }
    });
});
