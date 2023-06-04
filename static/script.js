document.getElementById('generate-form').addEventListener('submit', function(event) {
  event.preventDefault();
  var days = document.getElementById('days-input').value;

  // Display "Please wait, generating articles" message
  var loadingMessage = document.createElement('p');
  loadingMessage.textContent = 'Please wait, generating articles...';
  document.getElementById('results-container').appendChild(loadingMessage);

  // Progress bar
  var progressBar = document.createElement('progress');
  progressBar.setAttribute('value', '0');
  progressBar.setAttribute('max', '100');
  document.getElementById('results-container').appendChild(progressBar);

  fetch('/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: 'days=' + encodeURIComponent(days)
  })
  .then(response => response.json())
  .then(data => {
    // Remove "Please wait, generating articles" message
    loadingMessage.remove();

    // Remove progress bar
    progressBar.remove();

    if (data.error) {
      // Display error message
      var errorMessage = document.createElement('p');
      errorMessage.textContent = 'An error occurred while generating articles. Please try again.';
      document.getElementById('results-container').appendChild(errorMessage);
    } else {
      // Display results
      var resultsContainer = document.getElementById('results-container');
      resultsContainer.innerHTML = '';

      Object.values(data.summaries).forEach(summary => {
        var groupDiv = document.createElement('div');
        groupDiv.classList.add('group');

        var summaryParagraph = document.createElement('p');
        summaryParagraph.textContent = summary;

        groupDiv.appendChild(summaryParagraph);
        resultsContainer.appendChild(groupDiv);
      });
    }
  });
});