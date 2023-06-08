document.getElementById('news-digest-form').addEventListener('submit', function(event) {
  event.preventDefault();
  var days = document.getElementById('news-digest-days-input').value;
  var query = document.getElementById('news-digest-query-input').value;

  // Display "Please wait, generating articles" message
  var loadingMessage = document.createElement('p');
  loadingMessage.textContent = 'Please wait, generating articles...';
  document.getElementById('news-digest-results-container').appendChild(loadingMessage);  // изменено здесь

  // Progress bar
  var progressBar = document.createElement('progress');
  progressBar.setAttribute('value', '0');
  progressBar.setAttribute('max', '100');
  document.getElementById('news-digest-results-container').appendChild(progressBar);  // и здесь

  var formData = new URLSearchParams();
  formData.append('days', days);
  formData.append('query', query);

  fetch('/news_digest/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: formData.toString()
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
      document.getElementById('news-digest-results-container').appendChild(errorMessage);  // и здесь
    } else {
      // Display results
      var resultsContainer = document.getElementById('news-digest-results-container');  // и здесь
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
