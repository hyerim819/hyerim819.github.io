(function () {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.getRegistrations().then(function (registrations) {
      registrations.forEach(function (registration) {
        registration.unregister();
      });
    });
  }

  if ('caches' in window) {
    caches.keys().then(function (keys) {
      keys.forEach(function (key) {
        caches.delete(key);
      });
    });
  }

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

  if (article) {
    article.querySelectorAll('div.highlighter-rouge').forEach(function (block) {
      const code = block.querySelector('pre code');
      if (!code) return;

      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'code-copy-button';
      button.setAttribute('aria-label', '코드 복사');
      button.title = '코드 복사';
      button.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="8" y="8" width="11" height="11" rx="1.5"></rect><path d="M16 8V5.5A1.5 1.5 0 0 0 14.5 4h-10A1.5 1.5 0 0 0 3 5.5v10A1.5 1.5 0 0 0 4.5 17H8"></path></svg>';

      button.addEventListener('click', async function () {
        try {
          await navigator.clipboard.writeText(code.textContent);
          button.classList.add('is-copied');
          button.setAttribute('aria-label', '복사 완료');
          button.title = '복사 완료';
          window.setTimeout(function () {
            button.classList.remove('is-copied');
            button.setAttribute('aria-label', '코드 복사');
            button.title = '코드 복사';
          }, 1400);
        } catch (error) {
          button.setAttribute('aria-label', '복사 실패');
          button.title = '복사 실패';
        }
      });

      block.appendChild(button);
    });
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

    const notebookView = new URLSearchParams(window.location.search).get('view');
    if (notebookView === 'home') {
      enterNotebook();
    } else if (window.location.search || window.location.hash) {
      window.history.replaceState({}, '', '/');
    }

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
        window.history.replaceState({}, '', '/');
        if (enterButton) enterButton.focus();
      });
    }
  }
})();
