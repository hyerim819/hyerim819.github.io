(function () {
  const toggle = document.querySelector('[data-menu-toggle]');
  const nav = document.querySelector('[data-site-nav]');

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      const open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('is-open', !open);
    });
  }

  const article = document.querySelector('[data-article-content]');
  const toc = document.querySelector('[data-generated-toc]');
  if (article && toc) {
    const headings = article.querySelectorAll('h2, h3');
    headings.forEach(function (heading, index) {
      if (!heading.id) heading.id = 'section-' + (index + 1);
      const link = document.createElement('a');
      link.href = '#' + heading.id;
      link.textContent = heading.textContent;
      if (heading.tagName === 'H3') link.className = 'toc-subitem';
      toc.appendChild(link);
    });
    if (!headings.length) toc.closest('.article-toc').hidden = true;
  }
})();
