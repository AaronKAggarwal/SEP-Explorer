const articleBoxes = document.querySelectorAll('.article-box');
const popup = document.getElementById('article-popup');
const popupTitle = document.getElementById('popup-title');
const popupSnippet = document.getElementById('popup-snippet');
const popupLink = document.getElementById('popup-link');
const closeBtn = document.querySelector('.close');

document.addEventListener('DOMContentLoaded', function() {
    const readMoreLinks = document.querySelectorAll('.read-more');
    const popup = document.getElementById('article-popup');
    const popupTitle = document.getElementById('popup-title');
    const popupSnippet = document.getElementById('popup-snippet');
    const readMoreButton = document.getElementById('right-button');
    const closeBtn = document.querySelector('.close');

    readMoreLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const snippet = this.getAttribute('data-snippet');
            const title = this.closest('.card').querySelector('h2').textContent;
            const url = this.getAttribute('data-url')

            popupTitle.textContent = title;
            popupSnippet.textContent = snippet;
            readMoreButton.href = url;
            popup.style.display = 'block';
        });
    });

    closeBtn.addEventListener('click', () => {
        popup.style.display = 'none';
    });

    window.addEventListener('click', event => {
        if (event.target === popup) {
            popup.style.display = 'none';
        }
    });
});

articleBoxes.forEach(articleBox => {
  articleBox.addEventListener('click', () => {
    const title = articleBox.dataset.title;
    const url = articleBox.dataset.url;
    const snippet = articleBox.dataset.snippet;

    popupTitle.textContent = title;
    popupSnippet.textContent = snippet;
    popupLink.href = url;
    popup.style.display = 'block';
  });
});

closeBtn.addEventListener('click', () => {
  popup.style.display = 'none';
});

window.addEventListener('click', event => {
  if (event.target === popup) {
    popup.style.display = 'none';
  }
});
