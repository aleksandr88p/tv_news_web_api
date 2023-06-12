document.getElementById('date-selection-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const count = document.getElementById('article-count').value;
  const response = await fetch(`/api/box_office/dates/${count}`);
  const data = await response.json();
  const container = document.getElementById('date-buttons-container');
  container.innerHTML = '';
  data.last_dates.forEach(date => {
    const button = document.createElement('button');
    button.textContent = date;
    button.onclick = function() { loadArticleSummary(date); };
    container.appendChild(button);
  });
});

function loadArticleSummary(date) {
  // Отправить запрос на получение сводки статьи по выбранной дате
  fetch(`/api/box_office/${date}`)
    .then(response => response.json())
    .then(data => {
      const summaryContainer = document.getElementById('box-office-summary-container');
      const summaryText = document.getElementById('summary-text');
      summaryText.textContent = data.summary;

    })
    .catch(error => console.error('Error:', error));
}

