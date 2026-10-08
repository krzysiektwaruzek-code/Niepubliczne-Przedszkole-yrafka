(function () {
  'use strict';
  document.documentElement.classList.add('js');

  var burger = document.getElementById('burger');
  var nav = document.getElementById('nav');
  function setMenu(open) {
    nav.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Zamknij menu' : 'Otwórz menu');
  }
  burger.addEventListener('click', function () { setMenu(!nav.classList.contains('open')); });
  nav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });

  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  document.getElementById('year').textContent = new Date().getFullYear();

  var form = document.getElementById('contact-form');
  var status = document.getElementById('form-status');
  function say(msg, cls) { status.textContent = msg; status.className = 'form__status ' + cls; }
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var bad = false;
    form.querySelectorAll('[required]').forEach(function (f) {
      var ok = f.type === 'checkbox' ? f.checked : f.checkValidity() && f.value.trim() !== '';
      f.classList.toggle('err', !ok);
      f.setAttribute('aria-invalid', String(!ok));
      if (!ok && !bad) { bad = true; f.focus(); }
    });
    if (bad) { say('Uzupełnij poprawnie zaznaczone pola.', 'is-error'); return; }
    var endpoint = form.getAttribute('data-endpoint');
    if (!endpoint) { say('Formularz nie jest jeszcze podłączony – wiadomość nie została wysłana.', 'is-info'); return; }
    say('Wysyłanie…', 'is-info');
    fetch(endpoint, { method: 'POST', headers: { Accept: 'application/json' }, body: new FormData(form) })
      .then(function (r) { if (!r.ok) throw new Error(); form.reset(); say('Dziękujemy, wiadomość została wysłana.', 'is-info'); })
      .catch(function () { say('Nie udało się wysłać wiadomości. Spróbuj ponownie później.', 'is-error'); });
  });
})();
