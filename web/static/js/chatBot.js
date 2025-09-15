document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('searchForm');
    const resultsDiv = document.getElementById('results');
    const userMessageDiv = document.getElementById('userMessage');
    const responseMessageDiv = document.getElementById('responseMessage');
    const responseContainer = document.getElementById('responseContainer');

    form.addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent the default form submission

        const query = document.getElementById('query').value;

        // Display user's message
        userMessageDiv.textContent = query;
        userMessageDiv.style.display = 'block';

        // Clear the input field
        document.getElementById('query').value = '';

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
                // Clear previous results
                resultsDiv.innerHTML = '';
                responseMessageDiv.innerHTML = '';
                responseMessageDiv.style.display = 'none';

                if (data.message === "Search results for your query") {
                    responseMessageDiv.textContent = data.message;
                    responseMessageDiv.style.display = 'block';
                    responseContainer.style.display = 'block';

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
                    responseMessageDiv.textContent = data.message;
                    responseMessageDiv.style.display = 'block';
                    responseContainer.style.display = 'block';
                }
            } else {
                responseMessageDiv.textContent = `Error: ${data.error}`;
                responseMessageDiv.style.display = 'block';
                responseContainer.style.display = 'block';
            }
        } catch (error) {
            responseMessageDiv.textContent = `Error: ${error.message}`;
            responseMessageDiv.style.display = 'block';
            responseContainer.style.display = 'block';
        }
    });
});
