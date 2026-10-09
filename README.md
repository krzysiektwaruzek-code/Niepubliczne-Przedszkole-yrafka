# Niepubliczne Przedszkole Żyrafka – strona wizytówka

Statyczna strona HTML/CSS/JS (bez buildu), gotowa do wgrania na Hostinger (`public_html`).

## Potwierdzone dane na stronie
Nazwa, rodzaj placówki (niepubliczne przedszkole), adres: ul. Maratońska 57a, 94-102 Łódź (Polesie).

## Do uzupełnienia (celowo nie wpisane – brak potwierdzenia)
Wyniki researchu: `docs/RESEARCH.md`. Szukaj komentarzy `TODO` w `index.html`:
- telefon, e-mail, godziny otwarcia (wraz z JSON-LD: `telephone`, `openingHoursSpecification`),
- opis placówki, oferta, opłaty, rekrutacja, prawdziwe zdjęcia i logo,
- polityka prywatności (link przy zgodzie w formularzu),
- domena: canonical, `og:url`, `og:image`, `robots.txt`, `sitemap.xml` (zamień `TWOJA-DOMENA.pl`),
- formularz: wpisz adres usługi w `data-endpoint` w `<form id="contact-form">`.

## Struktura (wiele podstron)
Podstrony generuje `python3 tools/build.py` (szablon CSS: `tools/style.template.css`, treści: słownik `PAGES`).
Strony `oferta`, `rekrutacja`, `galeria` mają `noindex` i nie są w sitemapie, dopóki zawierają same kafelki „Do uzupełnienia”.
