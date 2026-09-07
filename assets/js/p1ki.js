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

  const notebook = document.querySelector('[data-notebook-app]');
  if (notebook) {
    const entry = notebook.querySelector('[data-notebook-entry]');
    const desktop = notebook.querySelector('[data-notebook-desktop]');
    const homePanel = notebook.querySelector('[data-notebook-home-panel]');
    const panels = notebook.querySelectorAll('[data-notebook-panel]');
    const folderButtons = notebook.querySelectorAll('[data-notebook-folder]');

    function showHome() {
      panels.forEach(function (panel) { panel.hidden = true; });
      homePanel.hidden = false;
      const firstFolder = notebook.querySelector('[data-notebook-folder]');
      if (firstFolder) firstFolder.focus();
    }

    function enterNotebook() {
      entry.hidden = true;
      desktop.hidden = false;
      showHome();
    }

    const enterButton = notebook.querySelector('[data-notebook-enter]');
    if (enterButton) enterButton.addEventListener('click', enterNotebook);

    folderButtons.forEach(function (button) {
      button.addEventListener('click', function () {
        const target = button.getAttribute('data-notebook-folder');
        const panel = notebook.querySelector('[data-notebook-panel="' + target + '"]');
        homePanel.hidden = true;
        panels.forEach(function (item) { item.hidden = true; });
        if (panel) {
          panel.hidden = false;
          const back = panel.querySelector('[data-notebook-home]');
          if (back) back.focus();
        }
      });
    });

    notebook.querySelectorAll('[data-notebook-home]').forEach(function (button) {
      button.addEventListener('click', showHome);
    });

    const returnButton = notebook.querySelector('[data-notebook-return]');
    if (returnButton) {
      returnButton.addEventListener('click', function () {
        desktop.hidden = true;
        entry.hidden = false;
        if (enterButton) enterButton.focus();
      });
    }
  }
})();
