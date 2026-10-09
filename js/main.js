(function () {
  'use strict';
  document.documentElement.classList.add('js');
  var $ = function (id) { return document.getElementById(id); };

  var burger = $('burger'), nav = $('nav'), header = document.querySelector('.header');
  function setMenu(open) {
    nav.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Zamknij menu' : 'Otwórz menu');
  }
  burger.addEventListener('click', function () { setMenu(!nav.classList.contains('open')); });
  nav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });

  function onScroll() { header.classList.toggle('scrolled', window.scrollY > 8); }
  onScroll(); window.addEventListener('scroll', onScroll, { passive: true });

  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -5% 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else { items.forEach(function (el) { el.classList.add('in'); }); }

  var y = $('year'); if (y) y.textContent = new Date().getFullYear();

  var form = $('contact-form'), status = $('form-status');
  if (!form) return;
  function say(msg, cls) { status.textContent = msg; status.className = 'form__status ' + cls; }
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var bad = false;
    form.querySelectorAll('[required]').forEach(function (f) {
      var ok = f.type === 'checkbox' ? f.checked : f.checkValidity() && f.value.trim() !== '';
      f.classList.toggle('err', !ok); f.setAttribute('aria-invalid', String(!ok));
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
