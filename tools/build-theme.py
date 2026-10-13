# -*- coding: utf-8 -*-
"""Porte la boutique statique vers le theme Shopify (../rawstate-shopify).

  python tools/build-shop.py     # d'abord : regenere les pages statiques
  python tools/build-theme.py    # puis : regenere le theme

Le theme est un derive mecanique des pages generees : on ne l'edite pas a la
main. Ce script ecrit layout/theme.liquid, templates/, snippets/ et recopie
dans assets/ les scripts, la feuille de style et les seules images utilisees.
Il ne touche jamais a config/ ni a locales/ (geres par l'admin Shopify).

Correspondance des adresses :
  index.html              /                         templates/index.liquid
  the-fold.html           /products/rawstate-the-fold
  <fiche>.html            /products/<fiche>         templates/product.liquid + snippets/fiche-*.liquid
  rituels.html            /pages/rituels            templates/page.rituels.liquid
  cgv.html, ...           /pages/cgv, ...           templates/page.<nom>.liquid

Paiement : theme.liquid injecte window.RAW_SHOP (variantes Shopify retrouvees
par SKU), que cart.js utilise pour remplir le panier Shopify.
"""
import io, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
THEME = os.path.join(os.path.dirname(ROOT), 'rawstate-shopify')

# page statique -> handle du produit Shopify
PRODUITS = [
    ('the-fold', 'rawstate-the-fold'),
    ('tapis-liege', 'tapis-liege'),
    ('planche-acupression', 'planche-acupression'),
    ('bloc-yoga', 'bloc-yoga'),
    ('roue-liege', 'roue-liege'),
    ('chaussettes-antiderapantes', 'chaussettes-antiderapantes'),
    ('gants-antiderapants', 'gants-antiderapants'),
    ('gourde-transparente', 'gourde-transparente'),
    ('rituel-essentiel', 'rituel-essentiel'),
    ('rituel-studio', 'rituel-studio'),
    ('rituel-recup', 'rituel-recup'),
]
LEGALES = ['mentions-legales', 'confidentialite', 'cgv', 'politique-retour']

# les .mp4 sont refuses dans assets/ d'un theme : servis depuis les Fichiers Shopify
HORS_THEME = {
    'programme-21jours.mp4':
        'https://cdn.shopify.com/s/files/1/1091/2448/5458/files/programme-21jours.mp4?v=1787505287',
}

LIENS = {'index.html': '/', 'rituels.html': '/pages/rituels'}
for page, handle in PRODUITS:
    LIENS[page + '.html'] = '/products/' + handle
for page in LEGALES:
    LIENS[page + '.html'] = '/pages/' + page

utilises = set()      # fichiers de assets/ references par le theme


def lire(chemin):
    return io.open(chemin, encoding='utf-8').read()

def page(nom):
    s = lire(os.path.join(ROOT, nom + '.html'))
    assert '{{' not in s and '{%' not in s, nom + ' : syntaxe Liquid dans la source'
    return s

def ecrire(rel, contenu):
    chemin = os.path.join(THEME, rel)
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(contenu)
    print('  %-46s %6d octets' % (rel, len(contenu.encode('utf-8'))))

def entre(s, debut, fin, inclure_fin=False):
    a = s.index(debut)
    b = s.index(fin, a)
    return s[a:b + (len(fin) if inclure_fin else 0)]


# ---------------------------------------------------------------- reecritures
ASSET = re.compile(r'assets/([A-Za-z0-9_.\-]+\.(?:webp|png|svg|avif|jpe?g|gif|woff2|mp4))')

def _asset(m):
    nom = m.group(1)
    if nom in HORS_THEME:
        return HORS_THEME[nom]
    utilises.add(nom)
    return "{{ '%s' | asset_url }}" % nom

def _lien(m):
    cible, ancre = m.group(1), m.group(2) or ''
    return 'href="%s%s"' % (LIENS[cible], ancre)

def liquidifier(html):
    """Chemins d'images -> asset_url, liens entre pages -> adresses Shopify."""
    html = ASSET.sub(_asset, html)
    html = re.sub(r'href="(%s)(#[^"]*)?"' % '|'.join(re.escape(k) for k in LIENS), _lien, html)
    html = html.replace('href="https://rawstate.fr/blogs/', 'href="/blogs/')
    reste = re.findall(r'href="[^"]*\.html[^"]*"', html)
    assert not reste, 'liens non convertis : %r' % reste[:5]
    return html

def titre_desc(s):
    t = re.search(r'<title>(.*?)</title>', s, re.S).group(1).strip()
    d = re.search(r'<meta name="description" content="(.*?)" />', s, re.S).group(1).strip()
    return t, d


# ------------------------------------------------------------------- sources
base = page('index')
pied = entre(base, '  <!-- ============ FOOTER', '</footer>', True)
panier = entre(base, '<div class="cart-overlay"', '</aside>', True)

def decouper(nom):
    """(classe du body, avant le main + main + blocs propres a la page, titre, description)"""
    s = page(nom)
    assert entre(s, '  <!-- ============ FOOTER', '</footer>', True) == pied, nom + ' : pied de page different'
    assert entre(s, '<div class="cart-overlay"', '</aside>', True) == panier, nom + ' : panier different'
    tete_ref = re.sub(r'<title>.*?</title>|<meta name="description" content=".*?" />', '', base[:base.index('</head>')], flags=re.S)
    tete = re.sub(r'<title>.*?</title>|<meta name="description" content=".*?" />', '', s[:s.index('</head>')], flags=re.S)
    assert tete == tete_ref, nom + ' : <head> different de celui de index.html'
    classe = re.search(r'<body(?: class="([^"]*)")?>', s).group(1) or ''
    corps = s[re.search(r'<body[^>]*>', s).end():s.index('  <!-- ============ FOOTER')]
    propre = s[s.index('</footer>') + len('</footer>'):s.index('<!-- Cart drawer -->') if '<!-- Cart drawer -->' in s else s.index('<div class="cart-overlay"')]
    t, d = titre_desc(s)
    return classe, (corps.strip('\n') + '\n' + propre.rstrip() + '\n'), t, d

meta = {}        # cle de page -> (titre, description, classe du body)

# ------------------------------------------------------------------ accueil
print('theme ->', THEME)
classe, corps, t, d = decouper('index')
meta['index'] = (t, d, classe)

# Le Journal : les cartes en dur deviennent une boucle sur le blog Shopify
grille = entre(corps, '<div class="articles__grid">', '        <div class="section-cta')
assert grille.count('class="article-card') >= 1
boucle = """<div class="articles__grid">
          {%- comment -%} le theme n'embarque que la locale en : mois traduits a la main {%- endcomment -%}
          {%- assign mois_fr = 'janvier,février,mars,avril,mai,juin,juillet,août,septembre,octobre,novembre,décembre' | split: ',' -%}
          {%- for article in blogs.news.articles limit: 4 -%}
          {%- assign idx_mois = article.published_at | date: '%-m' | plus: 0 | minus: 1 -%}
          <a class="article-card reveal" href="{{ article.url }}">
            <span class="article-card__media">{% if article.image %}<img src="{{ article.image | image_url: width: 800 }}" alt="{{ article.image.alt | default: article.title | escape }}" loading="lazy" width="800" height="450" />{% endif %}</span>
            <span class="article-card__body">
              <time class="article-card__date" datetime="{{ article.published_at | date: '%Y-%m-%d' }}">{{ article.published_at | date: '%-d' }} {{ mois_fr[idx_mois] }} {{ article.published_at | date: '%Y' }}</time>
              <h3>{{ article.title | escape }}</h3>
              <p>{{ article.excerpt_or_content | strip_html | truncate: 130 }}</p>
              <span class="article-card__more">Lire l'article</span>
            </span>
          </a>
          {%- endfor -%}
        </div>
"""
ecrire('templates/index.liquid', liquidifier(corps.replace(grille, '\0')).replace('\0', boucle))

# ------------------------------------------------------- en-tete des autres gabarits
# (blog, article, pages legales, 404...) : celui de l'accueil, sans lien actif
entete = corps[:corps.index('  <main')]
assert entete.count(' class="is-on"') == 2
entete = entete.replace(' class="is-on"', '')
n = entete.count('#articles">Le Journal</a>')
assert n == 2
entete = entete.replace('#articles">Le Journal</a>',
                        "#articles\"{% if actif == 'journal' %} class=\"is-on\"{% endif %}>Le Journal</a>")
ecrire('snippets/entete.liquid', liquidifier(entete))

# ------------------------------------------------------------ fiches produit
cas = []
for nom, handle in PRODUITS:
    classe, corps, t, d = decouper(nom)
    meta['p:' + handle] = (t, d, classe)
    ecrire('snippets/fiche-%s.liquid' % nom, liquidifier(corps))
    cas.append("  {%%- when '%s' -%%}\n    {%% render 'fiche-%s' %%}" % (handle, nom))

generique = lire(os.path.join(THEME, 'templates', 'product.liquid'))
if '{%- case product.handle -%}' in generique:          # deja porte : on reprend le repli
    generique = entre(generique, '    <section class="container"', '    </section>', True) + '\n'
generique = generique.replace('padding: clamp(48px,7vw,90px) 0;', 'padding-block: clamp(48px,7vw,90px);')
ecrire('templates/product.liquid',
       "{%- comment -%} Genere par rawstate/tools/build-theme.py : une fiche par produit, repli generique sinon {%- endcomment -%}\n"
       "{%- case product.handle -%}\n" + '\n'.join(cas) + "\n  {%- else -%}\n"
       "    {% render 'entete' %}\n  <main id=\"top\">\n" + generique + "  </main>\n{%- endcase -%}\n")

# ------------------------------------------------------------------ rituels
classe, corps, t, d = decouper('rituels')
meta['g:rituels'] = (t, d, classe)
ecrire('templates/page.rituels.liquid', liquidifier(corps))

# ------------------------------------------------------------ pages legales
for nom in LEGALES:
    s = page(nom)
    t, d = titre_desc(s)
    meta['g:' + nom] = (t, d, '')
    contenu = entre(s, '  <!-- Hero -->', '</main>', True)
    ecrire('templates/page.%s.liquid' % nom, "{% render 'entete' %}\n" + liquidifier(contenu) + '\n')

# ----------------------------------------- gabarits generiques : en-tete + marges
# `padding: X 0` sur un .container ecrasait ses marges laterales (texte colle
# aux bords en mobile) : on ne regle que le padding vertical.
for nom, actif in [('404', ''), ('article', 'journal'), ('blog', 'journal'), ('cart', ''), ('collection', ''),
                   ('list-collections', ''), ('page', ''), ('search', '')]:
    s = lire(os.path.join(THEME, 'templates', nom + '.liquid'))
    if "{% render 'entete'" in s:                       # deja porte
        s = s[s.index('<main id="top">\n') + len('<main id="top">\n'):s.rindex('  </main>')]
    s = re.sub(r'padding: (clamp\([^)]*\)) 0;', r'padding-block: \1;', s)
    assert not re.search(r'class="container[^"]*" style="padding:', s), nom + ' : padding lateral ecrase'
    rendu = "{% render 'entete'" + (", actif: '%s'" % actif if actif else '') + " %}\n"
    ecrire('templates/%s.liquid' % nom, rendu + '  <main id="top">\n' + s.rstrip('\n') + '\n  </main>\n')

# ------------------------------------------------------------------- scripts
def porter_js(nom):
    s = lire(os.path.join(ROOT, nom))
    # 'assets/x.webp' -> RAW_ASSET('x.webp') ; src="assets/x.webp" dans une chaine -> concatenation
    def litteral(m):
        utilises.add(m.group(1)) if m.group(1) not in HORS_THEME else None
        return "RAW_ASSET('%s')" % m.group(1)
    def dans_chaine(m):
        utilises.add(m.group(1)) if m.group(1) not in HORS_THEME else None
        return "\"' + RAW_ASSET('%s') + '\"" % m.group(1)
    s, a = re.subn(r"'assets/([A-Za-z0-9_.\-]+)'", litteral, s)
    s, b = re.subn(r'"assets/([A-Za-z0-9_.\-]+)"', dans_chaine, s)
    assert 'assets/' not in re.sub(r'//[^\n]*|/\*.*?\*/', '', s, flags=re.S), nom + ' : chemin assets/ non converti'
    ecrire('assets/' + nom, s)
    return re.findall(r"RAW_ASSET\('([^']+)'\)", s)

noms_js = []
for f in ('cart.js', 'shop.js', 'script.js'):
    noms_js += porter_js(f)
noms_js = sorted(set(noms_js))

css = lire(os.path.join(ROOT, 'styles.css'))
css, n = re.subn(r"url\((['\"]?)assets/([A-Za-z0-9_.\-]+)\1\)", lambda m: (utilises.add(m.group(2)), "url('%s')" % m.group(2))[1], css)
assert 'assets/' not in css
ecrire('assets/styles.css', css)

# -------------------------------------------------------------------- layout
tete = base[:base.index('</head>')]
tete = tete.replace('<html lang="fr">', '<html lang="{{ request.locale.iso_code }}">')

def echappe(t):
    return t.replace('{', '&#123;')

lignes = ["  {%- liquid",
          "    assign cle = template.name",
          "    if template.name == 'product'",
          "      assign cle = 'p:' | append: product.handle",
          "    elsif template.name == 'page'",
          "      assign cle = 'g:' | append: page.handle",
          "    endif",
          "    assign classe = ''",
          "  -%}",
          "  {%- case cle -%}"]
for cle, (t, d, classe) in meta.items():
    lignes.append("  {%%- when '%s' -%%}" % cle)
    lignes.append("    {%%- assign classe = '%s' -%%}" % classe)
    lignes.append('    <title>%s</title>' % echappe(t))
    lignes.append('    <meta name="description" content="%s" />' % echappe(d))
lignes += ["  {%- else -%}",
           "    <title>{{ page_title }}{% unless page_title contains shop.name %} — {{ shop.name }}{% endunless %}</title>",
           "    {%- if page_description -%}<meta name=\"description\" content=\"{{ page_description | escape }}\" />{%- endif -%}",
           "  {%- endcase %}",
           '  <link rel="canonical" href="{{ canonical_url }}" />']
tete, n = re.subn(r'  <title>.*?</title>\n', '\0', tete, flags=re.S)
assert n == 1
tete, n = re.subn(r'  <meta name="description" content=".*?" />\n', '', tete, flags=re.S)
assert n == 1
tete = liquidifier(tete).replace('\0', '\n'.join(lignes) + '\n')
tete, n = re.subn(r'href="styles\.css"', "href=\"{{ 'styles.css' | asset_url }}\"", tete)
assert n == 2, 'styles.css : %d reference(s) dans le head' % n

handles = ','.join(h for _, h in PRODUITS)
carte_js = ',\n'.join('      %-36s "%s"' % ('"%s":' % nom, HORS_THEME[nom] if nom in HORS_THEME else "{{ '%s' | asset_url }}" % nom)
                      for nom in noms_js)
scripts_tete = """
  {%%- comment -%%} Images utilisees par les scripts (galerie The Fold, panier) {%%- endcomment -%%}
  <script>
    window.THEME_ASSETS = {
%s
    };
    window.RAW_ASSET = function (n) { return window.THEME_ASSETS[n] || ('assets/' + n); };
  </script>

  {%%- comment -%%} Variantes Shopify pour le paiement : cart.js retrouve chaque ligne par son SKU
     (tapis The Fold : par le nom du coloris). all_products : 20 handles au plus par page. {%%- endcomment -%%}
  {%%- assign handles_boutique = '%s' | split: ',' -%%}
  <script>
    window.RAW_SHOP = {
      root: {{ routes.root_url | json }},
      fold: { {%%- for v in all_products['rawstate-the-fold'].variants -%%}{{ v.option1 | json }}: {{ v.id }}{%%- unless forloop.last -%%},{%%- endunless -%%}{%%- endfor -%%} },
      sku: { {%%- for h in handles_boutique -%%}{%%- for v in all_products[h].variants -%%}{%%- if v.sku != blank -%%}{{ v.sku | json }}: {{ v.id }},{%%- endif -%%}{%%- endfor -%%}{%%- endfor -%%} }
    };
  </script>

  {{ content_for_header }}
""" % (carte_js, handles)

# pied de page : reseaux sociaux regles dans le theme, vraie inscription a la newsletter
pied_l = liquidifier(pied)
for reseau in ('Facebook', 'Instagram'):
    avant = '<a href="#" aria-label="%s">' % reseau
    assert pied_l.count(avant) == 1, reseau
    pied_l = pied_l.replace(avant, '<a href="{{ settings.social_%s_link | default: \'#\' }}" aria-label="%s" target="_blank" rel="noopener noreferrer">'
                            % (reseau.lower(), reseau))
news = entre(pied_l, '          <form class="news"', '</form>', True)
pied_l = pied_l.replace(news, """          {% form 'customer' %}
            <div class="news">
              <input type="hidden" name="contact[tags]" value="newsletter" />
              <input type="email" name="contact[email]" placeholder="Votre email" aria-label="Votre email" required />
              <button class="btn btn--dark btn--sm" type="submit">S'inscrire</button>
            </div>
            {% if form.posted_successfully? %}<p style="margin-top:10px;font-size:13px;">Merci, votre inscription est confirmée&nbsp;!</p>{% endif %}
          {% endform %}""")

layout = (tete + scripts_tete + "</head>\n\n<body{% if classe != '' %} class=\"{{ classe }}\"{% endif %}>\n\n"
          + "{{ content_for_layout }}\n\n" + pied_l + "\n\n  <!-- Cart drawer -->\n  " + liquidifier(panier) + "\n\n"
          + "  <script src=\"{{ 'cart.js' | asset_url }}\" defer></script>\n"
          + "  {%- if cle == 'p:rawstate-the-fold' %}\n  <script src=\"{{ 'script.js' | asset_url }}\" defer></script>\n"
          + "  {%- else %}\n  <script src=\"{{ 'shop.js' | asset_url }}\" defer></script>\n  {%- endif %}\n</body>\n</html>\n")
ecrire('layout/theme.liquid', layout)

# -------------------------------------------------------------------- assets
dest = os.path.join(THEME, 'assets')
src = os.path.join(ROOT, 'assets')
# les gabarits que ce script ne genere pas (page mot de passe...) ont aussi leurs images
for dossier in ('layout', 'templates', 'snippets'):
    for n in os.listdir(os.path.join(THEME, dossier)):
        for nom in re.findall(r"'([A-Za-z0-9_.\-]+)' \| asset_url", lire(os.path.join(THEME, dossier, n))):
            if not nom.endswith(('.js', '.css')):
                utilises.add(nom)
garder = set(utilises) | {'cart.js', 'shop.js', 'script.js', 'styles.css'}
manquants = [n for n in sorted(utilises) if not os.path.exists(os.path.join(src, n))]
assert not manquants, 'images introuvables dans assets/ : %r' % manquants
for n in sorted(utilises):
    shutil.copyfile(os.path.join(src, n), os.path.join(dest, n))
retires = []
for n in sorted(os.listdir(dest)):
    if n not in garder:
        # on ne retire qu'une copie : l'original doit exister dans rawstate/assets
        assert os.path.exists(os.path.join(src, n)), 'assets/%s du theme sans original : laisse en place' % n
        os.remove(os.path.join(dest, n))
        retires.append(n)
poids = sum(os.path.getsize(os.path.join(dest, n)) for n in os.listdir(dest))
print('%d fichiers dans assets/ (%.1f Mo), %d anciens retires' % (len(os.listdir(dest)), poids / 1e6, len(retires)))
print('%d pages decrites dans theme.liquid' % len(meta))
