#!/usr/bin/env python3
"""Generuje statyczne podstrony z jednego szablonu. Uruchom: python3 tools/build.py
Treści do uzupełnienia edytuj w słowniku PAGES poniżej (kafelki TODO)."""
import os, shutil, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = "Niepubliczne Przedszkole Żyrafka"
ADDR = "ul. Maratońska 57a, 94-102 Łódź"
MAPQ = "Marato%C5%84ska+57a%2C+94-102+%C5%81%C3%B3d%C5%BA"
DOMAIN = "https://TWOJA-DOMENA.pl"   # TODO: docelowa domena

NAV = [("", "Start"), ("o-nas", "O nas"), ("kadra", "Kadra"), ("placowka", "Placówka"), ("program", "Program"),
       ("cennik", "Cennik"), ("rekrutacja", "Rekrutacja"), ("opinie", "Opinie"), ("galeria", "Galeria")]

# ---------- ozdoby tła (SVG) ----------
SUN = ('<svg class="d-svg sun spin" width="150" height="150" viewBox="0 0 120 120" aria-hidden="true"><g stroke="#ffc93c" stroke-width="7" stroke-linecap="round">'
       + "".join(f'<line x1="60" y1="6" x2="60" y2="20" transform="rotate({a} 60 60)"/>' for a in range(0, 360, 30))
       + '</g><circle cx="60" cy="60" r="29" fill="#ffd45e"/><circle cx="52" cy="52" r="9" fill="#ffe7a0" opacity=".8"/></svg>')
def cloud(cls):
    return (f'<svg class="d-svg {cls} drift" width="160" height="72" viewBox="0 0 200 90" aria-hidden="true"><path fill="#fff" d="M40 80a30 30 0 010-60 40 40 0 0176-8 34 34 0 0136 26 27 27 0 01-4 42z"/></svg>')
HILLS = ('<svg class="hills" viewBox="0 0 1440 220" preserveAspectRatio="none" aria-hidden="true">'
         '<path class="h1" d="M0 120c180-70 360-70 540-20s360 60 540-10 270-40 360 0v130H0z"/>'
         '<path class="h2" d="M0 160c200-60 380-40 560 0s340 40 520-10 240-20 360 10v70H0z"/>'
         '<path class="h3" d="M0 200c240-40 480-30 720 0s480 20 720-10v30H0z"/></svg>')
HERO_BG = ('<div class="bg" aria-hidden="true"><div class="patch"></div>'
           '<div class="blob a"></div><div class="blob b"></div><div class="dots"></div><div class="ring float b"></div>'
           + SUN + cloud("cloud1") + cloud("cloud2") + cloud("cloud3") +
           '<i class="star s1 twinkle"></i><i class="star s2 twinkle b"></i><i class="star s3 twinkle c"></i><i class="star s4 twinkle b"></i>'
           '<i class="conf k1 float"></i><i class="conf k2 float b"></i><i class="conf k3 float c"></i></div>')
def sec_bg(blob="b-white", pos="pos-tl", dots="pos-br"):
    return f'<div class="bg" aria-hidden="true"><div class="patch"></div><div class="blob {blob} {pos}"></div><div class="dots {dots}"></div></div>'

# ---------- klocki ----------
def todo(title, hint="Treść zostanie dodana po otrzymaniu informacji od placówki."):
    return (f'<article class="tile tile--todo reveal"><span class="badge">Do uzupełnienia</span>'
            f'<h3>{title}</h3><p>{hint}</p></article>')
def link(title, text, href):
    return (f'<a class="tile tile--link reveal" href="{href}"><h3>{title}</h3><p>{text}</p><span class="go">Przejdź</span></a>')
def shot(n):
    return f'<div class="shot reveal">Zdjęcie {n}<span>Do uzupełnienia</span></div>'
def head(eyebrow, h2, extra=""):
    return f'<header class="section__head reveal"><p class="eyebrow">{eyebrow}</p><h2>{h2}</h2>{extra}</header>'
def section(cls, inner, bg=None, sid=""):
    i = f' id="{sid}"' if sid else ""
    return f'<section class="section {cls}"{i}>{bg or sec_bg()}<div class="wrap">{inner}</div></section>'
def phero(slug, title, lead):
    cur = dict(NAV).get(slug, title)
    return (f'<section class="phero">{HERO_BG}<div class="wrap hero__in">'
            f'<p class="crumbs reveal"><a href="../">Start</a> / {cur}</p>'
            f'<h1 class="reveal">{title}</h1><p class="lead reveal">{lead}</p></div>{HILLS}</section>')
CTA_CONTACT = section("s-plum", '<div class="cta reveal"><div><h2>Masz pytania?</h2><p class="lead" style="margin:.4rem 0 0">Napisz do nas – odpowiemy po otrzymaniu wiadomości.</p></div><a class="btn" href="{R}kontakt/">Umów spotkanie</a></div>',
                      sec_bg("b-pink", "pos-br", "pos-tl"))
MAP = lambda: (f'<div class="loc__map reveal" data-map="https://www.google.com/maps?q={MAPQ}&amp;output=embed"><div class="map-ph">'
               '<p><strong>Mapa Google</strong><br>Mapa wczytuje się po kliknięciu – wtedy Twoje dane trafiają do Google.</p>'
               '<button class="btn btn--dark" type="button" data-map-btn>Załaduj mapę</button></div></div>')
DIR = f'https://www.google.com/maps/dir/?api=1&amp;destination={MAPQ}'
FORM = '''<form class="form reveal" id="contact-form" novalidate data-endpoint="">
<!-- TODO: wpisz w data-endpoint adres usługi odbierającej formularze (np. Formspree / własny backend) -->
<div class="field"><label for="name">Imię i nazwisko</label><input id="name" name="name" type="text" autocomplete="name" required></div>
<div class="field"><label for="email">Adres e-mail</label><input id="email" name="email" type="email" autocomplete="email" required></div>
<div class="field"><label for="msg">Wiadomość</label><textarea id="msg" name="message" rows="5" required></textarea></div>
<div class="field field--check"><input id="consent" name="consent" type="checkbox" required><label for="consent">Wyrażam zgodę na przetwarzanie danych w celu odpowiedzi na wiadomość. <!-- TODO: link do polityki prywatności --></label></div>
<button class="btn" type="submit">Wyślij wiadomość</button><p class="form__status" id="form-status" role="status" aria-live="polite"></p></form>'''
LD = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Preschool","name":"Niepubliczne Przedszkole Żyrafka",
"address":{"@type":"PostalAddress","streetAddress":"Maratońska 57a","postalCode":"94-102","addressLocality":"Łódź","addressCountry":"PL"}}
</script>'''
# TODO: do JSON-LD dodaj telephone i openingHoursSpecification dopiero po potwierdzeniu z placówką.

# ---------- treść podstron ----------
CC = lambda R: CTA_CONTACT.replace("{R}", R)
def todo_page(slug, title, lead, eyebrow, h2, tiles, bgcls="s-sky", intro="", noindex=True, blob="b-white"):
    return dict(title=f"{title} – {NAME}", desc=f"{title} – {NAME}, Łódź, ul. Maratońska 57a.", noindex=noindex,
      body=lambda R: (phero(slug, title, lead)
        + section(bgcls, head(eyebrow, h2) + (f'<p class="about reveal" style="margin-bottom:1.8rem">{intro}</p>' if intro else "")
                  + '<div class="tiles" data-stagger>' + "".join(todo(t) if isinstance(t, str) else todo(*t) for t in tiles) + '</div>',
                  sec_bg(blob, "pos-tl", "pos-br"))
        + CC(R)))

PAGES = {}
PAGES[""] = dict(
  title=f"{NAME} – Łódź, ul. Maratońska 57a",
  desc="Niepubliczne Przedszkole Żyrafka w Łodzi (Polesie), ul. Maratońska 57a, 94-102 Łódź. Poznaj placówkę i umów spotkanie.",
  ld=True, body=lambda R: (
    f'<section class="hero">{HERO_BG}<div class="wrap hero__in">'
    '<p class="eyebrow reveal">Przedszkole niepubliczne · Łódź, Polesie</p>'
    '<h1 class="reveal">Niepubliczne Przedszkole <em>Żyrafka</em></h1>'
    f'<p class="lead reveal">Przedszkole niepubliczne w Łodzi, przy ul. Maratońskiej 57a.</p>'
    f'<div class="hero__cta reveal"><a class="btn" href="{R}kontakt/">Umów spotkanie</a><a class="btn btn--ghost" href="{R}placowka/">Zobacz placówkę</a></div>'
    f'</div>{HILLS}</section>'
    + section("s-cream", head("Znajdź to, czego szukasz", "Szybkie przejścia") +
        '<div class="tiles tiles--quick" data-stagger>'
        + link("O nas", "Kim jesteśmy.", R+"o-nas/") + link("Kadra", "Osoby, które opiekują się dziećmi.", R+"kadra/")
        + link("Placówka", "Adres, budynek i dojazd.", R+"placowka/") + link("Program", "Zajęcia i rytm dnia.", R+"program/")
        + link("Cennik", "Opłaty za pobyt.", R+"cennik/") + link("Rekrutacja", "Jak zapisać dziecko.", R+"rekrutacja/")
        + link("Opinie", "Co mówią rodzice.", R+"opinie/") + link("Galeria", "Zdjęcia z przedszkola.", R+"galeria/") + '</div>',
        sec_bg("b-sun", "pos-br", "pos-tl"))
    + section("s-sky", head("Witamy", "Przedszkole w sercu Polesia") +
        '<p class="about reveal">Niepubliczne Przedszkole Żyrafka to przedszkole niepubliczne w Łodzi, w dzielnicy Polesie, przy ul. Maratońskiej 57a.</p>'
        '<div class="tiles" style="margin-top:2rem" data-stagger>' + todo("Kilka słów o nas", "Krótki opis placówki zostanie dodany po otrzymaniu informacji od przedszkola.")
        + todo("Godziny otwarcia") + todo("Telefon i e-mail") + '</div>', sec_bg("b-white", "pos-tl", "pos-br"))
    + section("s-mint", head("Dla rodziców", "Najczęstsze pytania") +
        '<div class="tiles" data-stagger>' + todo("Ile kosztuje przedszkole?", "Informacje o opłatach pojawią się w zakładce Cennik.")
        + todo("Jak wygląda dzień dziecka?", "Opis rytmu dnia pojawi się w zakładce Program.")
        + todo("Jak zapisać dziecko?", "Zasady zapisów pojawią się w zakładce Rekrutacja.") + '</div>', sec_bg("b-sky", "pos-br", "pos-tl"))
    + section("s-peach", '<div class="loc"><div class="reveal"><p class="eyebrow">Jak dojechać</p><h2>Lokalizacja</h2>'
        f'<address>{NAME}<br>ul. Maratońska 57a<br>94-102 Łódź</address>'
        f'<a class="btn btn--dark" target="_blank" rel="noopener" href="{DIR}">Wyznacz trasę<span class="sr"> (nowa karta)</span></a></div>{MAP()}</div>',
        sec_bg("b-white", "pos-tl", "pos-br"), "lokalizacja")
    + CC(R)))

PAGES["o-nas"] = dict(
  title=f"O nas – {NAME}", desc="Informacje o Niepublicznym Przedszkolu Żyrafka w Łodzi na Polesiu, ul. Maratońska 57a.",
  body=lambda R: (phero("o-nas", "O nas", "Przedszkole niepubliczne w Łodzi, na Polesiu.")
    + section("s-cream", '<div class="split"><div>' + head("Podstawowe informacje", "Nasza placówka") +
        '<p class="about reveal">Poniżej znajdziesz potwierdzone dane o przedszkolu. Pozostałe sekcje uzupełnimy wspólnie z placówką.</p></div>'
        f'<div class="factbox reveal"><dl><dt>Nazwa</dt><dd>{NAME}</dd><dt>Rodzaj</dt><dd>Przedszkole niepubliczne</dd><dt>Adres</dt><dd>ul. Maratońska 57a, 94-102 Łódź</dd><dt>Dzielnica</dt><dd>Łódź-Polesie</dd></dl></div></div>',
        sec_bg("b-sun", "pos-br", "pos-tl"))
    + section("s-lilac", head("Więcej o nas", "Do uzupełnienia") +
        '<div class="tiles" data-stagger>' + todo("Misja i wartości") + todo("Nasze podejście do dzieci") + todo("Historia przedszkola") + todo("Grupy wiekowe") + '</div>',
        sec_bg("b-white", "pos-tl", "pos-br"))
    + CC(R)))
PAGES["kadra"] = todo_page("kadra", "Kadra", "Osoby, które opiekują się Twoim dzieckiem.", "Zespół", "Poznaj naszą kadrę",
    ["Dyrektor", "Nauczyciele", "Opiekunowie", "Specjaliści i terapeuci", "Pozostały personel"],
    intro="Przedstawimy tu zespół po otrzymaniu informacji i zgód od placówki.", bgcls="s-peach")
PAGES["placowka"] = dict(
  title=f"Placówka – {NAME}", desc="Adres, lokalizacja i dojazd do Niepublicznego Przedszkola Żyrafka, ul. Maratońska 57a, Łódź.",
  body=lambda R: (phero("placowka", "Placówka", "Gdzie jesteśmy i jak do nas trafić.")
    + section("s-sky", '<div class="loc"><div class="reveal"><p class="eyebrow">Adres</p><h2>Jak dojechać</h2>'
        f'<address>{NAME}<br>ul. Maratońska 57a<br>94-102 Łódź (Polesie)</address>'
        f'<a class="btn btn--dark" target="_blank" rel="noopener" href="{DIR}">Wyznacz trasę<span class="sr"> (nowa karta)</span></a></div>{MAP()}</div>',
        sec_bg("b-white", "pos-tl", "pos-br"))
    + section("s-mint", head("Miejsce", "Do uzupełnienia") +
        '<div class="tiles" data-stagger>' + todo("Sale i wyposażenie") + todo("Ogród i plac zabaw") + todo("Bezpieczeństwo") + todo("Parking i komunikacja miejska") + '</div>',
        sec_bg("b-sky", "pos-br", "pos-tl"))
    + CC(R)))
PAGES["program"] = todo_page("program", "Program", "Jak wygląda dzień i nauka w przedszkolu.", "Edukacja", "Do uzupełnienia",
    ["Program wychowania przedszkolnego", "Rytm dnia", "Zajęcia dodatkowe", "Wyżywienie", "Języki obce", "Wycieczki i wydarzenia"], bgcls="s-lilac")
PAGES["cennik"] = todo_page("cennik", "Cennik", "Opłaty za pobyt dziecka w przedszkolu.", "Opłaty", "Do uzupełnienia",
    ["Czesne", "Opłata wpisowa", "Wyżywienie", "Godziny dodatkowe", "Rabaty i zniżki"], bgcls="s-cream",
    intro="Cennik zostanie opublikowany dopiero po przekazaniu go przez placówkę.", blob="b-sun")
PAGES["rekrutacja"] = todo_page("rekrutacja", "Rekrutacja", "Chcesz zapisać dziecko? Zapytaj o szczegóły.", "Zapisy", "Do uzupełnienia",
    ["Zasady przyjęć", "Terminy", "Wymagane dokumenty", "Dokumenty do pobrania", "Dzień adaptacyjny"], bgcls="s-mint", blob="b-sky")
PAGES["opinie"] = todo_page("opinie", "Opinie", "Co mówią rodzice.", "Rodzice", "Do uzupełnienia",
    [("Opinie rodziców", "Opublikujemy wyłącznie prawdziwe opinie, po uzyskaniu zgody ich autorów."), "Podziękowania", "Dodaj swoją opinię"], bgcls="s-peach")
PAGES["galeria"] = dict(
  title=f"Galeria – {NAME}", desc="Galeria zdjęć Niepublicznego Przedszkola Żyrafka w Łodzi.", noindex=True,
  body=lambda R: (phero("galeria", "Galeria", "Zdjęcia z życia przedszkola.")
    + section("s-sky", head("Zdjęcia", "Miejsce na prawdziwe zdjęcia") +
        '<p class="about reveal" style="margin-bottom:1.8rem">Dodamy tu zdjęcia, gdy przedszkole je dostarczy.</p><div class="gal" data-stagger>' + "".join(shot(i) for i in range(1, 9)) + '</div>',
        sec_bg("b-white", "pos-tl", "pos-br"))
    + CC(R)))
PAGES["kontakt"] = dict(
  title=f"Kontakt – {NAME}", desc="Kontakt z Niepublicznym Przedszkolem Żyrafka, ul. Maratońska 57a, 94-102 Łódź. Umów spotkanie.", ld=True,
  body=lambda R: (phero("kontakt", "Kontakt", "Umów spotkanie lub odwiedź nas na Polesiu.")
    + section("s-cream", '<div class="contact"><div class="reveal"><p class="eyebrow">Dane</p><h2>Jak się z nami skontaktować</h2>'
        f'<address class="about">{NAME}<br>ul. Maratońska 57a<br>94-102 Łódź</address>'
        '<div class="stack">' + todo("Telefon").replace("reveal", "") + todo("E-mail").replace("reveal", "") + todo("Godziny otwarcia").replace("reveal", "") + '</div>'
        '<!-- TODO: telefon (<a href="tel:+48…">), e-mail, godziny; uzupełnij też JSON-LD -->'
        f'</div>{FORM}</div>', sec_bg("b-sun", "pos-br", "pos-tl"))
    + section("s-sky", '<div class="loc"><div class="reveal"><p class="eyebrow">Jak dojechać</p><h2>Mapa</h2>'
        f'<address>ul. Maratońska 57a<br>94-102 Łódź</address><a class="btn btn--dark" target="_blank" rel="noopener" href="{DIR}">Wyznacz trasę<span class="sr"> (nowa karta)</span></a></div>{MAP()}</div>',
        sec_bg("b-white", "pos-tl", "pos-br"))))

def url_of(slug): return "/" if slug == "" else f"/{slug}/"

VER = ""
def render(slug, p):
    R = "" if slug == "" else "../"
    nav = "".join(f'<a href="{R}{s}{"/" if s else ""}"' + (' aria-current="page"' if s == slug else "") + f'>{t}</a>' for s, t in NAV)
    nav += f'<a class="btn btn--sm" href="{R}kontakt/"' + (' aria-current="page"' if slug == "kontakt" else "") + '>Kontakt</a>'
    foot_links = "".join(f'<li><a href="{R}{s}{"/" if s else ""}">{t}</a></li>' for s, t in NAV + [("kontakt", "Kontakt")])
    robots = '<meta name="robots" content="noindex, follow">\n  ' if p.get("noindex") else ""
    return f'''<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{p["title"]}</title>
  <meta name="description" content="{p["desc"]}">
  {robots}<meta name="theme-color" content="#fffaf0">
  <!-- TODO: po ustaleniu domeny dodaj <link rel="canonical" href="{DOMAIN}{url_of(slug)}"> oraz og:url / og:image -->
  <meta property="og:type" content="website"><meta property="og:locale" content="pl_PL">
  <meta property="og:title" content="{p["title"]}"><meta property="og:description" content="{p["desc"]}">
  <meta name="twitter:card" content="summary"><meta name="twitter:title" content="{p["title"]}"><meta name="twitter:description" content="{p["desc"]}">
  <link rel="stylesheet" href="{R}css/style.css?v={VER}">
  {LD if p.get("ld") else ""}
</head>
<body>
  <a class="skip" href="#main">Przejdź do treści</a>
  <header class="header" id="top"><div class="wrap header__in">
    <a class="brand" href="{R or "./"}" aria-label="{NAME} – strona główna"><span>Przedszkole Żyrafka<small>Łódź · Polesie</small></span></a>
    <button class="burger" id="burger" aria-expanded="false" aria-controls="nav" aria-label="Otwórz menu"><span></span><span></span><span></span></button>
    <nav class="nav" id="nav" aria-label="Główna nawigacja">{nav}</nav>
  </div></header>
  <main id="main">
{p["body"](R)}
  </main>
  <footer class="footer"><div class="bg" aria-hidden="true"><div class="patch"></div></div><div class="wrap">
    <div class="footer__grid">
      <div><h3>{NAME}</h3><p>ul. Maratońska 57a<br>94-102 Łódź</p></div>
      <div><h3>Strony</h3><ul>{foot_links}</ul></div>
      <div><h3>Kontakt</h3><p>Dane kontaktowe zostaną uzupełnione.<br><a href="{R}kontakt/">Formularz kontaktowy</a></p></div>
    </div>
    <p class="footer__bar">© <span id="year">2026</span> {NAME}</p>
  </div></footer>
  <script src="{R}js/main.js?v={VER}" defer></script>
</body>
</html>
'''

def main():
    global VER
    spots = open(os.path.join(ROOT, "tools/pattern.txt")).read().strip()
    css = open(os.path.join(ROOT, "tools/style.template.css"), encoding="utf-8").read().replace("%%SPOTS%%", spots)
    open(os.path.join(ROOT, "css/style.css"), "w", encoding="utf-8").write(css)
    VER = hashlib.md5((css + open(os.path.join(ROOT, "js/main.js"), encoding="utf-8").read()).encode()).hexdigest()[:8]
    for slug, p in PAGES.items():
        d = os.path.join(ROOT, slug) if slug else ROOT
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(render(slug, p))
    urls = "".join(f"  <url><loc>{DOMAIN}{url_of(s)}</loc></url>\n" for s, p in PAGES.items() if not p.get("noindex"))
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<!-- TODO: zamień TWOJA-DOMENA.pl na docelową domenę; po uzupełnieniu treści usuń noindex z uzupełnionych podstron (kadra, program, cennik, rekrutacja, opinie, galeria) i dodaj je tutaj (tools/build.py) -->\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')
    print("OK:", ", ".join(url_of(s) for s in PAGES))
main()
