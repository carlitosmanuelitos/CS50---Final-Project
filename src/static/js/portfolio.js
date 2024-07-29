document.addEventListener('DOMContentLoaded', function() {
    const tickerInput = document.querySelector('input[name="ticker"]');
    if (tickerInput) {
        tickerInput.addEventListener('input', function() {
            const query = this.value;
            if (query.length > 1) {
                fetch(`/api/stock_search?query=${query}`)
                    .then(response => response.json())
                    .then(data => {
                        // Implement autocomplete suggestion display here
                        console.log(data);
                    });
            }
        });
    }
});