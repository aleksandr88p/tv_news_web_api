document.getElementById('get-top-shows-button').addEventListener('click', function() {
    fetch('/api/top_shows', {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('top-shows-container');
        container.innerHTML = '';  // Clear previous results

        Object.entries(data).forEach(([platform, shows]) => {
            const platformDiv = document.createElement('div');
            platformDiv.className = 'platform';

            const platformNameDiv = document.createElement('div');
            platformNameDiv.textContent = platform;
            platformDiv.appendChild(platformNameDiv);
            platformNameDiv.className = 'platform-title';

            const movieDiv = document.createElement('div');
            movieDiv.textContent = `Movie: ${shows.Movie}`;
            platformDiv.appendChild(movieDiv);
            movieDiv.className = 'show-type';

            const tvShowDiv = document.createElement('div');
            tvShowDiv.textContent = `TV SHOW: ${shows['TV SHOW']}`;
            platformDiv.appendChild(tvShowDiv);
            tvShowDiv.className = 'show-type';


            container.appendChild(platformDiv);
        });
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});


