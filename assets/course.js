(function () {
  document.querySelectorAll('.codecard').forEach(function (card) {
    var button = card.querySelector('.copy');
    var code = card.querySelector('code');
    if (!button || !code) return;

    button.addEventListener('click', function () {
      var text = code.innerText;
      function finished() {
        button.textContent = 'Copied ✓';
        button.classList.add('done');
        window.setTimeout(function () {
          button.textContent = 'Copy';
          button.classList.remove('done');
        }, 1600);
      }

      function fallback() {
        var area = document.createElement('textarea');
        area.value = text;
        area.setAttribute('readonly', '');
        area.style.position = 'fixed';
        area.style.opacity = '0';
        document.body.appendChild(area);
        area.select();
        document.execCommand('copy');
        area.remove();
        finished();
      }

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(finished, fallback);
      } else {
        fallback();
      }
    });
  });

  var storagePrefix = 'learn-ml-models:';

  function readStatus(slug) {
    try { return window.localStorage.getItem(storagePrefix + slug) === 'done'; }
    catch (error) { return false; }
  }

  function writeStatus(slug, done) {
    try {
      if (done) window.localStorage.setItem(storagePrefix + slug, 'done');
      else window.localStorage.removeItem(storagePrefix + slug);
    } catch (error) {}
  }

  document.querySelectorAll('[data-complete]').forEach(function (button) {
    var slug = button.getAttribute('data-complete');
    function paint() {
      var done = readStatus(slug);
      button.textContent = done ? 'Completed ✓' : 'Mark complete';
      button.classList.toggle('is-done', done);
      button.setAttribute('aria-pressed', done ? 'true' : 'false');
    }
    button.addEventListener('click', function () {
      writeStatus(slug, !readStatus(slug));
      paint();
    });
    paint();
  });

  var lessonSlugs = ['start', 'knn', 'linear-regression', 'logistic-regression',
    'decision-trees', 'random-forests', 'gradient-boosting'];

  document.querySelectorAll('[data-progress-for]').forEach(function (label) {
    var slug = label.getAttribute('data-progress-for');
    var done = readStatus(slug);
    label.textContent = done ? 'Completed ✓' : 'Not started';
    label.classList.toggle('done', done);
  });

  document.querySelectorAll('[data-course-progress]').forEach(function (label) {
    var completed = lessonSlugs.filter(readStatus).length;
    label.textContent = completed + ' of ' + lessonSlugs.length + ' complete';
  });
})();
