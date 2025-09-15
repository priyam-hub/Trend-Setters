// Wait until DOM is fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // ========================
    // SEARCH FORM LOGIC
    // ========================
    const form = document.getElementById('searchForm');
    const resultsDiv = document.getElementById('results');

    if (form) {
        form.addEventListener('submit', async function (event) {
            event.preventDefault(); // Prevent default form submission

            const query = document.getElementById('query').value;

            try {
                const response = await fetch('/search', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ query: query })
                });

                const data = await response.json();

                if (response.ok) {
                    if (data.message === "Search results for your query") {
                        // Clear previous results
                        resultsDiv.innerHTML = '';

                        // Limit results to 3
                        const limitedResults = data.results.slice(0, 3);

                        // Create a card for each result
                        const resultsCards = limitedResults.map(result => {
                            return `
                                <div class="card">
                                    <img src="${result.img}" alt="${result.name}" class="card-img">
                                    <div class="card-body">
                                        <h3 class="card-title">${result.name}</h3>
                                        <p class="card-price">$${result.price}</p>
                                        <p class="card-rating">Rating: ${result.avg_rating} (${result.ratingCount} reviews)</p>
                                    </div>
                                </div>
                            `;
                        }).join('');

                        resultsDiv.innerHTML = resultsCards;
                    } else {
                        resultsDiv.innerHTML = `<p>${data.message}</p>`;
                    }
                } else {
                    resultsDiv.innerHTML = `<p>Error: ${data.error}</p>`;
                }
            } catch (error) {
                resultsDiv.innerHTML = `<p>Error: ${error.message}</p>`;
            }
        });
    }

    // ========================
    // MODAL LOGIC
    // ========================
    const modal = document.querySelector("[data-modal]");
    const modalOverlay = document.querySelector("[data-modal-overlay]");
    const modalCloseBtn = document.querySelector("[data-modal-close]");
    const startButton = document.getElementById("startButton");

    if (modal && modalOverlay && modalCloseBtn) {
        // Open modal
        function openModal() {
            modal.classList.add("active");
        }

        // Close modal
        function closeModal() {
            modal.classList.remove("active");
        }

        // Close when clicking button
        modalCloseBtn.addEventListener("click", closeModal);

        // Close when clicking overlay
        modalOverlay.addEventListener("click", closeModal);

        // Close modal when clicking "Start Chat" (and let the link redirect)
        if (startButton) {
            startButton.addEventListener("click", function () {
                closeModal();
                // Redirect handled by <a href="/chatbot">
            });
        }

        // OPTIONAL: auto-open modal after 5 seconds
        setTimeout(openModal, 5000);
    }
});
