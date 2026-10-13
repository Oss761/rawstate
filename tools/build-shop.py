# -*- coding: utf-8 -*-
"""Genere la boutique multiproduit a partir de tools/products.py.

  python tools/build-shop.py

Produit : index.html (page de garde), the-fold.html (contenu d'origine, intact)
et une page par produit. Les blocs communs figes sont dans tools/parts/ :
head.html (dont le CSS critique inline), main-the-fold.html, footer.html,
cart.html, announce.html.
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import products as P

def lire(nom):
    return io.open(os.path.join(HERE, 'parts', nom), encoding='utf-8').read()

HEAD_SRC = lire('head.html')
MAIN_FOLD = lire('main-the-fold.html')
FOOTER = lire('footer.html')
CART = lire('cart.html')
ANNONCE = lire('announce.html')

# Logos de paiement : repris tels quels de la fiche The Fold (source unique)
_m = re.search(r'<div class="pay-badges".*?</div>', MAIN_FOLD, re.S)
assert _m, "bloc pay-badges introuvable dans main-the-fold.html"
PAY_BADGES = _m.group(0)

def eur(v):
    return ('%.2f' % v).replace('.', ',') + ' €'


# ---------------------------------------------------------------- head
def head(titre, description, extra_css='', hero_preload=False):
    """Reprend le head d'origine (CSS critique inline) en changeant titre et
    description. Le preload du hero ne sert qu'a the-fold.html : ailleurs il
    telechargerait une image jamais affichee."""
    h = HEAD_SRC
    h = re.sub(r'<title>.*?</title>', '<title>%s</title>' % titre, h, flags=re.S)
    h = re.sub(r'<meta name="description" content=".*?" />',
               '<meta name="description" content="%s" />' % description, h, flags=re.S)
    if not hero_preload:
        h = re.sub(r'\n\s*<link rel="preload" as="image".*?/>', '', h, flags=re.S)
    if extra_css:
        h = h.replace('</style>', extra_css + '\n  </style>', 1)
    return h


# -------------------------------------------------------------- header
def header(actif=''):
    def lien(href, label, cle):
        on = ' class="is-on"' if cle == actif else ''
        return '<a href="%s"%s>%s</a>' % (href, on, label)
    nav = [lien('index.html', 'Boutique', 'boutique'),
           lien('rituels.html', 'Rituels', 'rituels'),
           lien('index.html#tapis', 'Tapis', 'tapis'),
           lien('index.html#accessoires', 'Accessoires', 'accessoires'),
           lien('index.html#articles', 'Le Journal', 'articles')]
    return """  <!-- Header -->
  <header class="header" data-header>
    <div class="container header__inner">
      <button class="header__burger" aria-label="Ouvrir le menu" aria-expanded="false" data-menu-toggle>
        <span></span><span></span>
      </button>
      <a href="index.html" class="logo" aria-label="Rawstate — accueil"><img src="assets/logo-light.png" alt="Rawstate" /></a>
      <nav class="nav" aria-label="Navigation principale">
        %s
      </nav>
      <div class="header__actions">
        <button class="header__cart" aria-label="Panier" data-cart-toggle>
          <span class="ico" data-ico="cart"></span>
          <span class="header__cart-count" data-cart-count hidden>0</span>
        </button>
      </div>
    </div>

    <nav class="header__mobile" data-mobile-menu aria-label="Menu mobile">
      %s
      <a href="index.html#tapis" class="btn btn--dark btn--block">Voir les tapis</a>
    </nav>
  </header>
""" % ('\n        '.join(nav), '\n      '.join(nav))


# ------------------------------------------------------- cartes produit
def carte(p):
    prix = '<span class="pcard__price">%s</span>' % eur(p['prix'])
    return """          <a class="pcard reveal" href="{page}">
            <span class="pcard__media"><img src="{img}" alt="{alt}" loading="lazy" /></span>
            <span class="pcard__body">
              <span class="pcard__cat">{cat}</span>
              <h3>{nom}</h3>
              <p>{resume}</p>
              <span class="pcard__foot">{prix}<span class="pcard__more">Découvrir</span></span>
            </span>
          </a>""".format(page=p['page'], img=p['img'], alt=p['alt'],
                         cat='Tapis' if p['cat'] == 'tapis' else 'Accessoire',
                         nom=p['nom'], resume=p['resume'], prix=prix)


def bloc_articles(titre_h2='Nos articles'):
    cartes = []
    for a in P.ARTICLES:
        cartes.append("""          <a class="article-card reveal" href="{url}">
            <span class="article-card__media"><img src="{img}" alt="{alt}" loading="lazy" /></span>
            <span class="article-card__body">
              <time class="article-card__date" datetime="{date_iso}">{date}</time>
              <h3>{titre}</h3>
              <p>{resume}</p>
              <span class="article-card__more">Lire l'article</span>
            </span>
          </a>""".format(**a))
    return """
    <!-- ============ ARTICLES ============ -->
    <section class="articles" id="articles">
      <div class="container">
        <div class="articles__head reveal">
          <span class="eyebrow">Le journal</span>
          <h2>%s</h2>
          <p>Nos guides pour choisir, entretenir et pratiquer, sans jargon.</p>
        </div>
        <div class="articles__grid">
%s
        </div>
        <div class="section-cta reveal">
          <a href="https://rawstate.fr/blogs/news" class="btn btn--dark btn--lg">Voir tous les articles</a>
        </div>
      </div>
    </section>
""" % (titre_h2, '\n'.join(cartes))


def bloc_avis(p):
    """Formulaire d'avis de la fiche The Fold, repris tel quel, avec le nom du produit
    dans le texte d'exemple (le JS vit dans shop.js)."""
    etoiles = '\n'.join(
        '              <button type="button" class="review-form__star" data-star="%d" '
        'aria-label="%d étoile%s sur 5">★</button>' % (n, n, 's' if n > 1 else '')
        for n in range(1, 6))
    return """
    <!-- ============ AVIS ============ -->
    <section class="reviews" id="reviews">
      <div class="container">
        <div class="reviews__intro reveal">
          <span class="eyebrow">Premiers retours clients</span>
          <h2>Rawstate est une jeune marque</h2>
          <p>Laissez-nous un avis sur le produit — votre retour aide les prochaines et prochains à se lancer.</p>
        </div>

        <form class="review-form reveal" data-review-form novalidate>
          <div class="review-form__field">
            <label class="review-form__label">Votre note</label>
            <div class="review-form__stars" data-rating role="radiogroup" aria-label="Note sur 5">
{etoiles}
            </div>
          </div>
          <div class="review-form__field">
            <label class="review-form__label" for="review-name">Votre prénom</label>
            <input type="text" id="review-name" class="review-form__input" name="name" placeholder="Ex. Camille" required />
          </div>
          <div class="review-form__field">
            <label class="review-form__label" for="review-text">Votre avis</label>
            <textarea id="review-text" class="review-form__textarea" name="review" rows="4" placeholder="Partagez votre expérience avec {court}…" required></textarea>
          </div>
          <button type="submit" class="btn btn--white btn--lg btn--block review-form__submit">Publier mon avis</button>
          <p class="review-form__error" data-review-error hidden>Merci d'ajouter une note et votre avis avant d'envoyer.</p>
          <p class="review-form__done" data-review-done hidden>Merci pour votre retour&nbsp;! Votre avis a bien été envoyé, il sera publié après validation.</p>
        </form>
      </div>
    </section>
""".format(etoiles=etoiles, court=P.nom_court(p))


def _sceau(i, anneau, legende, ico=None, centre=None):
    """Un sceau rond : le texte court autour du cercle (SVG textPath, centre en
    haut du cercle), et au milieu soit une icone, soit un disque terracotta avec
    deux lignes de texte. L'id du chemin est unique par sceau."""
    nl = chr(10)
    coeur = ('        <circle class="sceau__coeur sceau__coeur--plein" cx="80" cy="80" r="42" />' + nl
             + '        <text class="sceau__jours" x="80" y="76" text-anchor="middle">%s</text>' % centre[0] + nl
             + '        <text class="sceau__jours-sous" x="80" y="92" text-anchor="middle">%s</text>' % centre[1] + nl
             ) if centre else (
             '        <circle class="sceau__coeur" cx="80" cy="80" r="42" />' + nl)
    icone = ('      <span class="sceau__ico ico" data-ico="%s"></span>' % ico + nl) if ico else ''
    return ('    <div class="sceau reveal">' + nl
            + '      <div class="sceau__disque">' + nl
            + '        <svg class="sceau__svg" viewBox="0 0 160 160" role="img" aria-label="%s">'
              % anneau.replace(' · ', ', ').capitalize() + nl
            # le cercle demarre EN BAS et tourne dans le sens horaire : le milieu
            # du trace (50 %) tombe donc en haut, avec autant de place de chaque
            # cote. En partant de la gauche, un texte long etait coupe au debut.
            + '          <defs><path id="sceau-%d" fill="none"'
              ' d="M80 80 m 0 61 a 61 61 0 1 1 0 -122 a 61 61 0 1 1 0 122" /></defs>' % i + nl
            + '          <circle class="sceau__anneau" cx="80" cy="80" r="78" />' + nl
            + coeur
            + '          <text class="sceau__texte"><textPath href="#sceau-%d" startOffset="50%%"'
              ' text-anchor="middle">%s</textPath></text>' % (i, anneau) + nl
            + '        </svg>' + nl
            + icone
            + '      </div>' + nl
            + '      <p class="sceau__legende">%s</p>' % legende + nl
            + '    </div>')


REASSURANCE = """
    <!-- ============ REASSURANCE ============ -->
    <section class="sceaux">
      <div class="container sceaux__grid">
%s
      </div>
    </section>
""" % '\n'.join([
    _sceau(1, "LIVRAISON OFFERTE · SANS MINIMUM D'ACHAT",
           "Sur toute la boutique, même pour une paire de chaussettes.", ico="truck"),
    _sceau(2, "SATISFAIT OU REMBOURSÉ · RETOUR OFFERT",
           "Pour essayer chez vous, à votre rythme.", centre=("30", "JOURS")),
    _sceau(3, "LIÈGE · TPE · COTON · CHOISIS POUR DURER",
           "Des matières choisies une à une, pour durer.", ico="grain"),
    _sceau(4, "PAIEMENT SÉCURISÉ · VISA · MASTERCARD · APPLE PAY",
           "Visa, Mastercard et Apple&nbsp;Pay.", ico="lock"),
])


# ------------------------------------------------------ page de garde
def page_index():
    tapis = [p for p in P.PRODUITS if p['cat'] == 'tapis']
    acc = [p for p in P.PRODUITS if p['cat'] == 'accessoires']
    vedette = P.par_slug('the-fold')

    hero = """
    <!-- ============ HERO BOUTIQUE ============ -->
    <section class="shop-hero">
      <div class="container shop-hero__inner">
        <div class="shop-hero__txt reveal">
          <h1>Votre studio de yoga. Chez vous.</h1>
          <p>Tapis, blocs, chaussettes, acupression : des rituels complets pensés ensemble,
             du premier salut au soleil à la récupération du soir.</p>
          <div class="shop-hero__actions">
            <div class="shop-hero__cta">
              <a href="rituels.html" class="btn btn--dark btn--lg">Composer votre rituel</a>
            </div>
            <ul class="shop-hero__pills">
              <li>Livraison offerte</li><li>Garantie 30 jours</li><li>Programme yoga offert</li>
            </ul>
          </div>
        </div>
        <a class="shop-hero__feature reveal" href="rituels.html">
          <img src="assets/hero-studio.webp" width="1168" height="880" alt="Deux pratiquants en posture, tapis en liege, blocs et gourdes, dans leur salon" fetchpriority="high" />
        </a>
      </div>
    </section>
"""

    def section(id_, eyebrow, titre, chapo, items):
        # avec 2 produits seulement, la rangee de 3 laisse un vide a droite :
        # le modificateur recentre la paire sans changer la largeur des cartes
        duo = ' pgrid__grid--duo' if len(items) == 2 else ''
        return """
    <!-- ============ %s ============ -->
    <section class="pgrid" id="%s">
      <div class="container">
        <div class="pgrid__head reveal">
          <span class="eyebrow">%s</span>
          <h2>%s</h2>
          <p>%s</p>
        </div>
        <div class="pgrid__grid%s">
%s
        </div>
      </div>
    </section>
""" % (id_.upper(), id_, eyebrow, titre, chapo, duo, '\n'.join(carte(p) for p in items))

    # bandeau de logos qui defile (droite -> gauche). Le groupe est duplique :
    # la piste se decale de 50 % puis revient, la boucle est invisible.
    def bandeau_logos(n=8):
        groupe = ('          <div class="logoband__group" aria-hidden="true">'
                  + ''.join('<img src="assets/logo-dark.png" alt="" loading="lazy" />'
                            for _ in range(n))
                  + '</div>')
        return """
    <!-- ============ BANDEAU LOGOS ============ -->
    <div class="logoband" role="presentation">
      <div class="logoband__track">
%s
%s
      </div>
    </div>
""" % (groupe, groupe)

    # Les 3 rituels sur l'accueil. Memes cartes que rituels.html.
    # Desktop : les 3 cote a cote. Mobile : carrousel centre sur Le Studio
    # (scroll-snap pour le glissement au doigt, fleches pilotees par shop.js).
    rituels_accueil = """
    <!-- ============ RITUELS ============ -->
    <section class="pgrid rhome" id="rituels">
      <div class="container">
        <div class="pgrid__head reveal">
          <span class="eyebrow">Les rituels</span>
          <h2>Les Rituels Rawstate</h2>
          <p>Chaque rituel réunit ce qu'il faut pour commencer, sans qu'il y ait à deviner quoi
            associer et coûte toujours moins cher que les mêmes objets achetés un par un.</p>
        </div>
        <div class="rhome__zone">
          <button class="rhome__nav rhome__nav--prev" type="button" data-rhome="-1"
                  aria-label="Rituel précédent"><span class="ico" data-ico="chevron"></span></button>
          <div class="rhome__piste" data-rhome-piste>
%s
          </div>
          <button class="rhome__nav rhome__nav--next" type="button" data-rhome="1"
                  aria-label="Rituel suivant"><span class="ico" data-ico="chevron"></span></button>
        </div>
      </div>
    </section>
""" % '\n'.join(carte_rituel(r) for r in P.RITUELS)

    main = ('  <main id="top">\n' + hero + bandeau_logos() + rituels_accueil
            + section('tapis', 'Les tapis', 'Un tapis pour chaque pratique.',
                      "The Fold se glisse dans un sac pour la pratique en voyage ou en studio. "
                      "The Grip reste au sol à la maison, et accroche même quand les mains "
                      "commencent à transpirer.", tapis)
            + bandeau_logos()
            + section('accessoires', 'Les accessoires', "Ce qui change une séance",
                      "Pas une collection d'accessoires. Six objets qu'on utilise vraiment, "
                      "à chaque séance.", acc)
            + REASSURANCE + bloc_articles() + '\n  </main>\n')

    return '\n'.join([
        head("Rawstate — Tapis de yoga pliables et accessoires",
             "La boutique Rawstate : The Fold, le tapis de yoga pliable, le tapis en liège The Grip et les accessoires. Livraison offerte, 30 jours pour essayer."),
        '<body class="page-shop">', '', ANNONCE, header('boutique'), main,
        FOOTER, CART, '  <script src="cart.js"></script>', '  <script src="shop.js"></script>', '</body>', '</html>', ''])


# --------------------------------------------------------- page rituels
def prix_rond(v):
    """99.0 -> "99 €" ; 114.70 -> "114,70 €" (les packs sont a prix rond)."""
    return ('%d €' % v) if float(v).is_integer() else eur(v)


def carte_rituel(r):
    plein = P.prix_plein(r)
    eco = round(plein - r['prix'], 2)
    # inventaire du pack : texte seul, volontairement non cliquable (seuls le
    # visuel et le bouton menent a la fiche du rituel)
    lignes = '\n'.join(
        '            <li>%s<span>%s</span></li>' % (q['nom'], eur(q['prix']))
        for q in (P.par_slug(s) for s in r['produits']))
    return """        <article class="rite reveal{vedette}">
          <a class="rite__visuel" href="#{slug}" aria-hidden="true" tabindex="-1">
            <img src="{img}" alt="{alt}" loading="lazy" />
            <span class="rite__badge">{badge}</span>
          </a>
          <div class="rite__corps">
            <h2 class="rite__nom" id="{slug}">{nom}</h2>
            <p class="rite__sous">{sous}</p>
            <ul class="rite__liste">
{lignes}
            </ul>
            <div class="rite__prix">
              <strong>{prix}</strong>
              <span class="rite__plein">{plein}</span>
              <i class="rite__eco">−{eco}</i>
            </div>
            <a class="btn {bouton} btn--block" href="rituel-{slug}.html">Découvrir le rituel</a>
          </div>
        </article>""".format(
        vedette=' rite--vedette' if r.get('vedette') else '',
        slug=r['slug'], img=r['img'], alt=r['alt'], badge=r['badge'],
        nom=r['nom'], sous=r['sous'], lignes=lignes,
        prix=prix_rond(r['prix']), plein=eur(plein), eco=eur(eco),
        bouton='btn--white' if r.get('vedette') else 'btn--dark')


def produit_rituel(r):
    """Fiche produit d'un pack, construite depuis RITUELS : meme gabarit que les
    autres fiches (galerie, buy box, barre collante) mais un seul article au panier,
    au prix du lot. Visuels provisoires en attendant les photos."""
    items = [P.par_slug(s) for s in r['produits']]
    plein = P.prix_plein(r)
    eco = round(plein - r['prix'], 2)
    liens = '<ul>' + ''.join(
        '<li><a href="%s"><strong>%s</strong></a> — %s</li>' % (q['page'], q['nom'], eur(q['prix']))
        for q in items) + '</ul>'
    return dict(
        slug='rituel-' + r['slug'], page='rituel-%s.html' % r['slug'], cat='rituels',
        nom='Rituel %s' % r['nom'], accroche=r['sous'], prix=r['prix'],
        libelle_bouton='Choisir ce rituel',
        sans_quantite=True,          # un rituel s'ajoute a l'unite
        cadeau_offert=r.get('cadeau'),
        # (slug, nom, coloris, mention facultative affichee apres le coloris)
        composer=[(q['slug'], q['nom'],
                   [(n, h, v) for n, h, v, _ in q['coloris']] if q.get('coloris') else [q['pastille']],
                   q.get('composer_mention') or '')
                  for q in items if q.get('coloris') or q.get('pastille')],
        imgs=r.get('imgs'),                        # galerie si les photos sont fournies
        etapes=r.get('etapes'),                    # section "Comment proceder a ce rituel ?"
        livraison=r.get('livraison'),              # (mini, maxi) jours -> date estimee sous le titre
        img=(r['imgs'][0][0] if r.get('imgs') else 'assets/rituel-a-venir.webp'),
        alt=(r['imgs'][0][1] if r.get('imgs') else 'Visuel a venir pour le rituel %s' % r['nom']),
        resume="%s %s" % (r['sous'], 'Le pack complet à prix rond, moins cher qu’à l’unité.'),
        pdp_resume=r.get('pdp_resume') or (
            "%s Les %d produits du rituel réunis pour %s au lieu de %s, soit %s d'économie."
            % (r['sous'], len(items), prix_rond(r['prix']), eur(plein), eur(eco))),
        prix_barre=eur(plein),
        mention_prix="Économisez %s" % eur(eco),
        mention_badge=True,
        prix_sur_bouton=True,
        bullets=[q['nom'] for q in items],
        # le tableau se lit comme un calcul : prix plein barre, livraison offerte,
        # economie, puis le prix du lot sur une ligne appuyee
        specs=[(q['nom'], eur(q['prix'])) for q in items]
              + [('Acheté séparément', eur(plein), 'spec--barre'),
                 ('Livraison', 'Offerte', 'spec--offerte'),
                 ('Votre économie', '−' + eur(eco), 'spec--eco'),
                 ('Prix du rituel', prix_rond(r['prix']), 'spec--total')],
        # titre, texte et "Bon a savoir" de la section "En detail" : calcules par
        # defaut, mais un rituel peut fournir les siens (ecrits a la main).
        titre_detail=r.get('titre_detail'),      # sinon l'accroche sert de h2
        usage_ico=r.get('usage_ico'),            # icone a gauche de "Bon a savoir"
        desc=r.get('desc') or (
            "Les produits de ce rituel sont pensés pour aller ensemble : %s "
            "Vous les recevez en une seule commande, au prix du lot."
            % r['sous'].lower()),
        usage=r.get('usage') or (
            "Un rituel complet, livré d'un coup — et %s d'économie par rapport aux achats séparés."
            % eur(eco)),
        # un rituel peut fournir ses propres accordeons (texte ecrit a la main) ;
        # sinon la liste des produits et le delai generique sont generes.
        accordeons=r.get('accordeons') or [
            ("Ce que contient le rituel", liens),
            ("Livraison",
             "<p>Votre commande est préparée sous 1 à 2 jours ouvrés. "
             "Les produits du rituel sont expédiés ensemble.</p>")])


def page_rituels():
    cartes = '\n'.join(carte_rituel(r) for r in P.RITUELS)
    main = """  <main id="top">

    <!-- ============ RITUELS ============ -->
    <section class="rituels">
      <div class="container">
        <div class="rituels__head reveal">
          <span class="eyebrow">Offres — rituels</span>
          <h1>Les Rituels Rawstate</h1>
          <p>Chaque rituel réunit ce qu'il faut pour commencer, sans qu'il y ait à deviner quoi
            associer et coûte toujours moins cher que les mêmes objets achetés un par un.</p>
        </div>

        <div class="rituels__grid">
{cartes}
        </div>

        <ul class="rituels__notes reveal">
          <li><span class="ico" data-ico="truck"></span> Livraison offerte</li>
          <li><span class="ico" data-ico="shield"></span> Garantie 30 jours — satisfait ou remboursé</li>
          <li><span class="ico" data-ico="leaf"></span> Programme 21 jours offert</li>
        </ul>
      </div>
    </section>
  </main>
""".format(cartes=cartes)

    return '\n'.join([
        head("Les Rituels Rawstate — packs yoga complets",
             "Trois rituels Rawstate : L'Essentiel, Le Studio et La Récup'. Des packs complets "
             "(tapis, bloc, chaussettes, roue, acupression, gourde) à prix rond, livraison offerte."),
        '<body class="page-rituels">', '', ANNONCE, header('rituels'), main,
        FOOTER, CART, '  <script src="cart.js"></script>', '  <script src="shop.js"></script>', '</body>', '</html>', ''])


# ------------------------------------------------------- page produit
def attrs_panier(p):
    """Attributs lus par shop.js a l'ajout au panier : delai de livraison et cadeaux
    de la fiche. Le panier n'annonce un sac ou le programme que s'ils sont ici."""
    assert p.get('livraison'), 'pas de delai de livraison : %s' % p['slug']
    out = ' data-livr="%d,%d"' % tuple(p['livraison'])
    cad = p.get('cadeau_offert') or []
    if cad and isinstance(cad[0], str):
        cad = [cad]
    for titre, _mention, _img in cad:
        if 'sac' in titre.lower():
            out += ' data-sacs="%d"' % int(titre.split()[0])
        elif 'programme' in titre.lower():
            out += ' data-programme="1"'
        else:
            raise AssertionError('cadeau inconnu du panier : %s' % titre)
    return out


def page_produit(p):
    # une ligne de specs = (libelle, valeur) ou (libelle, valeur, classe de la ligne)
    specs = '\n'.join(
        '              <div class="spec%s"><dt>%s</dt><dd>%s</dd></div>'
        % ((' ' + s[2]) if len(s) > 2 else '', s[0], s[1])
        for s in p['specs'])
    bullets = '\n'.join(
        '            <li><span class="ico" data-ico="check"></span> %s</li>' % b
        for b in p['bullets'])
    # cross-sell : pas sur les packs (qui reunissent deja plusieurs produits),
    # ni sur les fiches qui posent `sans_cross`
    autres = [q for q in P.PRODUITS if q['slug'] != p['slug'] and q['cat'] != 'rituels'][:3]
    cross = '' if (p['cat'] == 'rituels' or p.get('sans_cross')) else """    <!-- ============ CROSS-SELL ============ -->
    <section class="pgrid pgrid--tight">
      <div class="container">
        <div class="pgrid__head reveal">
          <span class="eyebrow">Compléter</span>
          <h2>Ça va bien ensemble</h2>
        </div>
        <div class="pgrid__grid">
%s
        </div>
      </div>
    </section>
""" % '\n'.join(carte(q) for q in autres)

    # selecteur de coloris (optionnel). Si la fiche choisit un coloris par
    # exemplaire du lot, le choix se fait dans les cartes : pas de selecteur ici.
    cols = [] if p.get('coloris_par_lot') else (p.get('coloris') or [])
    choix = ''
    if cols:
        nl2 = chr(10)
        gab = ('              <button type="button" class="swatch%s" data-color="%s"'
               ' data-color-img="%s" data-gal="%d" aria-label="%s"'
               ' style="background:%s;border-color:%s">'
               '<img class="swatch__img" src="%s" alt="" aria-hidden="true" /></button>')
        puces = nl2.join(
            gab % (' is-active' if i == 0 else '', nom, P.par_slug(p['slug'])['imgs'][gal][0],
                   gal, nom, hexa, hexa, vign)
            for i, (nom, hexa, vign, gal) in enumerate(cols))
        choix = ('            <div class="variants" data-colors>' + nl2
                 + '              <div class="variants__label">Coloris — <span data-color-name>'
                 + cols[0][0] + '</span></div>' + nl2
                 + '              <div class="variants__list">' + nl2 + puces + nl2
                 + '              </div>' + nl2 + '            </div>' + nl2)
    # offres par lot (optionnel) : remplacent le selecteur de quantite.
    # La remise porte sur le prix plein du lot ; le lot part au panier comme une seule ligne.
    offres = p.get('offres') or []
    bloc_offres = ''
    qty_box = ('              <div class="qty" data-qty>\n'
               '                <button type="button" data-qty-dec aria-label="Diminuer la quantité">−</button>\n'
               '                <span data-qty-val>1</span>\n'
               '                <button type="button" data-qty-inc aria-label="Augmenter la quantité">+</button>\n'
               '              </div>\n')
    if p.get('sans_quantite'):        # packs : on ajoute un rituel a la fois
        qty_box = ''
    if offres:
        qty_box = ''
        nl6 = chr(10)
        unite = p.get('unite_lot') or 'article'
        # un coloris par exemplaire du lot : seulement si la fiche le demande
        cols_lot = (p.get('coloris') or []) if p.get('coloris_par_lot') else []
        # Un lot s'ecrit soit en tuple -- (n, remise %, sous-titre) ou
        # (n, remise, sous-titre, prix impose) -- soit en dict pour un lot qui
        # melange plusieurs produits : dict(titre=, sous=, prix=, produits=[slug...]).
        def _norm(o):
            if isinstance(o, dict):
                prods = [P.par_slug(s) for s in o['produits']]
                return dict(n=len(prods), remise=0, sous=o['sous'], titre=o['titre'],
                            prix=round(o['prix'], 2), prods=prods,
                            plein=round(sum(q['prix'] for q in prods), 2))
            n, remise, sous = o[0], o[1], o[2]
            return dict(n=n, remise=remise, sous=sous, titre=None, prods=None,
                        plein=round(p['prix'] * n, 2),
                        prix=round(o[3], 2) if len(o) > 3 else
                             round(p['prix'] * n * (100 - remise) / 100.0, 2))
        lots = [_norm(o) for o in offres]
        economies = [round(L['plein'] - L['prix'], 2) for L in lots]
        meilleure = max(economies)
        cartes = []
        for i, L in enumerate(lots):
            n, remise, sous = L['n'], L['remise'], L['sous']
            plein, total, eco = L['plein'], L['prix'], economies[i]
            actif = (i == 0)
            titre = L['titre'] or '%d %s%s' % (n, unite, 's' if n > 1 else '')
            pills = ''
            if eco > 0:
                # avec un prix impose, le pourcentage serait faux : on annonce l'economie en euros
                pct = ('<i>−%d&nbsp;%%</i>' % remise) if remise else ''
                pills = ('                    <span class="offer__pills">%s'
                         '<i class="offer__pill--eco">Économisez %s</i></span>'
                         % (pct, eur(eco).replace(' ', '&nbsp;')) + nl6)
            vieux = ''
            unitaire = ''
            if eco > 0:
                vieux = ('                      <span class="offer__old">%s</span>'
                         % eur(plein).replace(' ', '&nbsp;')) + nl6
            if n > 1 and not L['prods']:     # sans objet pour un lot de produits differents
                unitaire = ('                      <span class="offer__unit">soit %s %s</span>'
                            % (eur(round(total / n, 2)).replace(' ', '&nbsp;'),
                               ('le ' if unite in ('bloc', 'tapis') else 'la ') + unite)) + nl6
            badge = ''
            if eco == meilleure and eco > 0:
                badge = '                <span class="offer__badge">Meilleure offre</span>' + nl6
            # coloris du lot : soit n exemplaires de ce produit, soit un par produit
            corps = ''
            # (produit dont on prend les coloris, etiquette de la ligne, nom pour le panier)
            if L['prods']:
                # libelle affiche = type + nom commercial ("Gants The Gloves") ; le panier garde le nom court
                rangees = [(q, q['nom'].split()[0] + ' ' + P.nom_court(q), P.nom_court(q))
                           for q in L['prods'] if q.get('coloris')]
            elif cols_lot:
                rangees = [(p, ('%s %d' % (unite.capitalize(), k + 1)) if n > 1 else 'Coloris', None)
                           for k in range(n)]
            else:
                rangees = []
            if rangees:
                gab_l = ('                      <button type="button" class="swatch%s" data-color="%s"'
                         ' data-color-img="%s" data-gal="%d" aria-label="%s"'
                         ' style="background:%s;border-color:%s">'
                         '<img class="swatch__img" src="%s" alt="" aria-hidden="true" /></button>')
                rangs = []
                for k, (src_p, etiq, nom_panier) in enumerate(rangees):
                    cols_r = src_p['coloris']
                    puces_l = nl6.join(
                        gab_l % (' is-active' if j == 0 else '', nomc,
                                 src_p['imgs'][gal][0], gal, nomc, hexa, hexa, vign)
                        for j, (nomc, hexa, vign, gal) in enumerate(cols_r))
                    attr_nom = (' data-lot-produit="%s"' % nom_panier) if nom_panier else ''
                    # lot de produits differents : la mention du produit (taille) suit son coloris,
                    # en texte nu car le <span> ne porte que le nom du coloris, remplace par shop.js
                    mention_r = (' ' + src_p['composer_mention']) if (L['prods'] and src_p.get('composer_mention')) else ''
                    rangs.append(
                        '                  <div class="pick-row" data-lot-pick="%d"%s>' % (k, attr_nom) + nl6
                        + '                    <div class="pick-row__label">%s — <span data-lot-nom>%s</span>%s</div>'
                          % (etiq, cols_r[0][0], mention_r) + nl6
                        + '                    <div class="pick-row__swatches">' + nl6 + puces_l + nl6
                        + '                    </div>' + nl6
                        + '                  </div>')
                corps = ('                <div class="offer__body">' + nl6
                         + '                  <div class="offer__pick">' + nl6
                         + nl6.join(rangs) + nl6
                         + '                  </div>' + nl6
                         + '                </div>' + nl6)
            cartes.append(
                '              <div class="offer%s" data-offer-lot="%d" data-prix="%.2f" data-remise="%d"'
                '%s role="radio" aria-checked="%s" tabindex="0">'
                % (' is-active' if actif else '', n, total, remise,
                   (' data-lot-titre="%s" data-livr="%d,%d"'
                    % (titre, max(q['livraison'][0] for q in L['prods']),
                       max(q['livraison'][1] for q in L['prods']))) if L['prods'] else '',
                   'true' if actif else 'false') + nl6
                + badge
                + '                <div class="offer__main">' + nl6
                + '                  <span class="offer__radio"></span>' + nl6
                + '                  <div class="offer__info">' + nl6
                + '                    <span class="offer__title">%s</span>' % titre + nl6
                + '                    <span class="offer__sub">%s</span>' % sous + nl6
                + pills
                + '                  </div>' + nl6
                + '                  <div class="offer__price">' + nl6
                + vieux
                + '                      <span class="offer__now">%s</span>' % eur(total).replace(' ', '&nbsp;') + nl6
                + unitaire
                + '                  </div>' + nl6
                + '                </div>' + nl6
                + corps
                + '              </div>')
        bloc_offres = ('            <div class="offers" data-offers-lots data-unite="%s" role="radiogroup"'
                       ' aria-label="Choisissez votre lot">' % unite + nl6
                       + nl6.join(cartes) + nl6
                       + '            </div>' + nl6)

    # photos en situation : les 4 visuels 9:16 sur une ligne, sous les moyens de paiement
    ugc = p.get('ugc') or []
    bande = ''
    if ugc:
        nl = chr(10)   # pas d'antislash ici : l'echappement saute a l'ecriture
        bande = (nl + '            <div class="ugc-strip">' + nl
                 + nl.join('              <img src="%s" alt="%s" loading="lazy" />' % (src, alt)
                           for src, alt in ugc) + nl
                 + '            </div>' + nl)

    # renvoi vers le rituel qui contient ce produit (optionnel), entre la bande
    # de photos et les accordeons. Tous les montants sont CALCULES depuis le
    # catalogue : surcout du pack, prix des autres a l'unite, economie.
    vers_rituel = ''
    vr = p.get('rituel_lie')
    if vr:
        slug_r, compo_r, enum_r = vr[:3]
        eyebrow_r = vr[3] if len(vr) > 3 else 'Ce produit existe en rituel'
        rit = next(x for x in P.RITUELS if x['slug'] == slug_r)
        plein_r = P.prix_plein(rit)
        eco_r = round(plein_r - rit['prix'], 2)
        sup_r = round(rit['prix'] - p['prix'], 2)      # ce que coutent les autres dans le pack
        seuls_r = round(plein_r - p['prix'], 2)        # les memes, achetes a l'unite
        nl5 = chr(10)
        vers_rituel = (
            nl5
            + '            <a class="vrit" href="rituel-%s.html">' % slug_r + nl5
            + '              <span class="vrit__eyebrow">%s</span>' % eyebrow_r + nl5
            + '              <span class="vrit__tete">' + nl5
            + '                <span class="vrit__img"><img src="%s" alt="" loading="lazy" /></span>' % rit['img'] + nl5
            + '                <span class="vrit__id">' + nl5
            + '                  <strong class="vrit__nom">Rituel %s</strong>' % rit['nom'] + nl5
            + '                  <span class="vrit__compo">%s</span>' % compo_r + nl5
            + '                </span>' + nl5
            + '              </span>' + nl5
            + '              <span class="vrit__arg">Ajoutez %s pour <b>%s</b> au lieu de <s>%s</s>.</span>'
              % (enum_r, eur(sup_r), eur(seuls_r)) + nl5
            + '              <span class="vrit__prix"><strong>%s</strong>'
              '<span class="vrit__plein">%s</span>'
              '<i class="vrit__eco">Économisez %s</i></span>'
              % (prix_rond(rit['prix']), eur(plein_r), eur(eco_r)) + nl5
            + '              <span class="btn btn--ghost btn--block">Passer au Rituel %s</span>' % rit['nom'] + nl5
            + '              <span class="vrit__note">Vous choisirez les coloris sur la page du rituel.</span>' + nl5
            + '            </a>' + nl5)

    # accordeons optionnels, sous les moyens de paiement
    accs = p.get('accordeons') or []
    accordeons = ''
    if accs:
        gabarit = ('                <div class="acc">\n'
                   '                  <button class="acc__q">%s<span class="acc__ico"></span></button>\n'
                   '                  <div class="acc__a"><div class="acc__body">%s</div></div>\n'
                   '                </div>')
        items = '\n'.join(gabarit % (titre, corps) for titre, corps in accs)
        accordeons = ('\n            <div class="accordion pdp__accordion" data-accordion>\n'
                      + items + '\n            </div>\n')

    # "Comment proceder a ce rituel ?" : section optionnelle entre la buy box et
    # "En detail". Reutilise le gabarit .howto / .step de la fiche The Fold ;
    # le modificateur .howto--etapes passe juste les indices en terracotta.
    pas = p.get('etapes') or []
    etapes = ''
    if pas:
        cartes_pas = '\n'.join(
            """          <article class="step reveal">
            <div class="step__media">
              <img src="%s" alt="%s" loading="lazy" />
              <span class="step__num">%d</span>
            </div>
            <h3>%s</h3>
            <p>%s</p>
          </article>""" % (src_e, alt_e, i, titre_e, sous_e)
            for i, (titre_e, sous_e, src_e, alt_e) in enumerate(pas, 1))
        etapes = """
    <!-- ============ ETAPES DU RITUEL ============ -->
    <section class="howto howto--etapes">
      <div class="container">
        <div class="howto__head reveal">
          <h2>Comment procéder à ce rituel&nbsp;?</h2>
        </div>
        <div class="howto__grid">
%s
        </div>
      </div>
    </section>
""" % cartes_pas

    # "Composez votre rituel" : un choix de coloris par produit du pack (optionnel).
    # Les pastilles reutilisent le style .swatch des fiches produit.
    comp = p.get('composer') or []
    composer = ''
    if comp:
        nl8 = chr(10)
        lignes = []
        for ligne_c in comp:
            slug_c, nom_c, cols = ligne_c[:3]
            # texte nu (pas de <span>) : .composer__label span est en gras fonce,
            # et shop.js ne remplace que le contenu de [data-composer-nom]
            mention_c = (' ' + ligne_c[3]) if len(ligne_c) > 3 and ligne_c[3] else ''
            puces = nl8.join(
                '                  <button type="button" class="swatch%s" data-color="%s" data-vignette="%s"'
                ' aria-label="%s : %s" style="background:%s;border-color:%s">'
                '<img class="swatch__img" src="%s" alt="" aria-hidden="true" /></button>'
                % (' is-active' if i == 0 else '', nom, vign, nom_c, nom, hexa, hexa, vign)
                for i, (nom, hexa, vign) in enumerate(cols))
            lignes.append(
                '              <div class="composer__ligne" data-composer-item="%s" data-produit="%s">' % (slug_c, nom_c) + nl8
                + '                <div class="composer__label">%s — <span data-composer-nom>%s</span>%s</div>' % (nom_c, cols[0][0], mention_c) + nl8
                + '                <div class="variants__list">' + nl8 + puces + nl8
                + '                </div>' + nl8
                + '              </div>')
        composer = ('            <div class="composer" data-composer>' + nl8
                    + '              <span class="composer__badge">Livraison offerte</span>' + nl8
                    + '              <div class="composer__titre">Composez votre rituel</div>' + nl8
                    + nl8.join(lignes) + nl8
                    + '            </div>' + nl8)

    # cadeau offert, juste au-dessus du bouton d'ajout (optionnel) : carte claire,
    # bordure pointillee terracotta, case prechochee et icone cadeau. Utilise par
    # les packs et par The Grip.
    cad_r = p.get('cadeau_offert')
    cadeau_rituel = ''
    if cad_r:
        # une seule ligne (3 chaines) ou une liste de lignes
        lignes_c = [cad_r] if isinstance(cad_r[0], str) else list(cad_r)
        nl9 = chr(10)
        rangs = nl9.join(
            '              <div class="cadeau__ligne">' + nl9
            + '                <input type="checkbox" class="cadeau__case" checked'
              ' aria-label="%s : inclus" />' % titre_c + nl9
            + '                <span class="cadeau__img"><img src="%s" alt="" loading="lazy" /></span>' % vignette_c + nl9
            + '                <span class="cadeau__txt">%s</span>' % titre_c + nl9
            + '                <span class="cadeau__free">%s</span>' % mention_c + nl9
            + '              </div>'
            for titre_c, mention_c, vignette_c in lignes_c)
        cadeau_rituel = (
            '            <div class="cadeau cadeau--offert">' + nl9
            + '              <img class="cadeau__ico" src="assets/ico-cadeau-rouge.png" alt="" aria-hidden="true" />' + nl9
            + rangs + nl9
            + '            </div>' + nl9)

    # a cote du prix : "Livraison offerte", ou le prix plein barre pour les packs
    prix_annexe = ('<span class="pdp__barre">%s</span>' % p['prix_barre']) if p.get('prix_barre') \
        else '<span>Livraison offerte</span>'
    # mention complementaire (taille, economie...) : simple texte, ou badge terracotta
    mention = ('<span class="pdp__note%s">%s</span>'
               % (' pdp__note--badge' if p.get('mention_badge') else '', p['mention_prix'])) \
        if p.get('mention_prix') else ''

    # cadeau mis en avant sous les bullet points (optionnel)
    cad = p.get('cadeau')
    cadeau = ''
    if cad:
        titre, libelle, vignette = cad
        nl7 = chr(10)
        cadeau = ('            <div class="cadeau">' + nl7
                  + '              <span class="cadeau__img"><img src="%s" alt="" loading="lazy" /></span>' % vignette + nl7
                  + '              <span class="cadeau__txt">%s</span>' % titre + nl7
                  + '              <span class="cadeau__free">%s</span>' % libelle + nl7
                  + '            </div>' + nl7)

    # delai de livraison estime sous le titre (optionnel) : rempli par shop.js au chargement
    livr = p.get('livraison')
    delai = ''
    if livr:
        nl4 = chr(10)
        delai = ('            <p class="pinfo__delivery">' + nl4
                 + '              <span class="ico" data-ico="truck"></span>' + nl4
                 + '              <span data-ship-eta data-min="%d" data-max="%d">'
                   'Estimation du délai de livraison…</span>' % livr + nl4
                 + '            </p>' + nl4)

    # prix a payer sur le bouton d'ajout (optionnel) : suit la quantite choisie
    libelle = p.get('libelle_bouton') or 'Ajouter au panier'
    total_btn = ('\n                %s — <span data-add-total>%s</span>\n              '
                 % (libelle, prix_rond(p['prix']))) if p.get('prix_sur_bouton') else '\n                %s\n              ' % libelle

    # section "A completer avec", sous les badges de reassurance (optionnelle) :
    # un coloris impose par produit, bouton d'ajout immediat (1 exemplaire, sans passer par la fiche)
    comps = p.get('complements') or []
    complements = ''
    if comps:
        nl3 = chr(10)
        lignes = []
        for slug_c, coul in comps:
            q = P.par_slug(slug_c)
            trouve = [c for c in (q.get('coloris') or []) if c[0] == coul]
            if not trouve:
                raise SystemExit('complement %s : coloris "%s" absent du catalogue' % (slug_c, coul))
            vue = q['imgs'][trouve[0][3]]      # la photo de ce coloris
            lignes.append(
                '                <div class="complement">' + nl3
                + '                  <a class="complement__media" href="%s" tabindex="-1" aria-hidden="true">'
                  '<img src="%s" alt="" loading="lazy" /></a>' % (q['page'], vue[0]) + nl3
                + '                  <div class="complement__txt">' + nl3
                + '                    <a class="complement__nom" href="%s">%s</a>' % (q['page'], q['nom']) + nl3
                + '                    <span class="complement__meta">%s · %s</span>' % (coul, eur(q['prix'])) + nl3
                + '                  </div>' + nl3
                + '                  <button type="button" class="btn btn--dark btn--sm complement__add"'
                  ' data-add-now="%s-%s" data-nom="%s · %s" data-prix="%.2f" data-img="%s"%s>'
                  'Ajouter au panier</button>'
                  % (q['slug'], coul.lower(), q['nom'], coul, q['prix'], vue[0], attrs_panier(q)) + nl3
                + '                </div>')
        complements = (nl3 + '            <div class="complements">' + nl3
                       + '              <h2 class="complements__title">À compléter avec</h2>' + nl3
                       + '              <div class="complements__list">' + nl3
                       + nl3.join(lignes) + nl3
                       + '              </div>' + nl3
                       + '            </div>' + nl3)

    # Galerie : une seule image -> visuel simple ; plusieurs -> stage + vignettes
    vues = p.get('imgs') or [(p['img'], p['alt'])]
    if len(vues) == 1:
        galerie = ('            <div class="pdp__media">\n'
                   '              <img src="%s" alt="%s" fetchpriority="high" />\n'
                   '            </div>' % (vues[0][0], vues[0][1]))
    else:
        thumbs = '\n'.join(
            '                <button type="button" class="pgal__thumb%s" data-pgal-go="%d" '
            'aria-label="Vue %d">'
            '<img src="%s" alt="" loading="lazy" /></button>'
            % (' is-active' if i == 0 else '', i, i + 1, src)
            for i, (src, _) in enumerate(vues))
        srcs = '|'.join(s for s, _ in vues)
        alts = '|'.join(a for _, a in vues)
        galerie = ("""            <div class="pgal" data-pgal data-pgal-srcs="{srcs}" data-pgal-alts="{alts}">
              <div class="pdp__media" data-pgal-stage>
                <img src="{first}" alt="{firstalt}" fetchpriority="high" />
                <button type="button" class="pgal__nav pgal__nav--prev" data-pgal-prev aria-label="Vue précédente"><span class="ico" data-ico="chevron"></span></button>
                <button type="button" class="pgal__nav pgal__nav--next" data-pgal-next aria-label="Vue suivante"><span class="ico" data-ico="chevron"></span></button>
              </div>
              <div class="pgal__thumbs" style="--thumbs:{cols}">
{thumbs}
              </div>
            </div>""").format(srcs=srcs, alts=alts, first=vues[0][0],
                              firstalt=vues[0][1], thumbs=thumbs,
                              cols=len(vues))   # toutes les vues sur une seule ligne

    main = """  <main id="top">

    <!-- ============ FICHE PRODUIT ============ -->
    <section class="pdp">
      <div class="container">
        <nav class="crumbs" aria-label="Fil d'Ariane">
          <a href="index.html">Boutique</a><span>/</span>
          <a href="{cat_href}">{cat_label}</a><span>/</span>
          <span aria-current="page">{nom}</span>
        </nav>

        <div class="pdp__grid">
          <div class="pdp__gal reveal">
{galerie}
          </div>

          <div class="pdp__info reveal">
            <span class="eyebrow">{cat_label}</span>
            <h1>{nom}</h1>
{delai}            <p class="pdp__accroche">{accroche}</p>
            <div class="pdp__price"><strong>{prix}</strong>{prix_annexe}{mention}</div>
            <p class="pdp__resume">{resume}</p>
            <ul class="pinfo__bullets">
{bullets}
            </ul>

{cadeau}{choix}{composer}{cadeau_rituel}{bloc_offres}            <div class="pdp__buy">
{qty_box}              <button class="btn btn--dark btn--block btn--buy"
                      data-add="{slug}" data-nom="{nom}" data-prix="{prix_num}" data-img="{img}"{panier}>{total_btn}</button>
            </div>
            <p class="buy-guarantee"><span class="ico" data-ico="shield"></span> Garantie 30 jours — satisfait ou remboursé</p>

            {paybadges}
{bande}{vers_rituel}{accordeons}

            <div class="pinfo__reassure">
              <div><span class="ico" data-ico="truck"></span> Livraison offerte</div>
              <div><span class="ico" data-ico="return"></span> Retour 30 jours</div>
              <div><span class="ico" data-ico="leaf"></span> Matières choisies</div>
            </div>
{complements}          </div>
        </div>
      </div>
    </section>
{etapes}
    <!-- ============ DETAIL ============ -->
    <section class="pdetail">
      <div class="container pdetail__inner">
        <div class="pdetail__txt reveal">
          <span class="eyebrow">En détail</span>
          <h2>{titre_detail}</h2>
          <p>{desc}</p>
          <p class="pdetail__usage">{usage_ico}<strong>Bon à savoir —</strong> {usage}</p>
        </div>
        <dl class="specs reveal">
{specs}
        </dl>
      </div>
    </section>

{cross}
  </main>
""".format(cat=p['cat'],
           cat_label={'tapis': 'Tapis', 'rituels': 'Rituels'}.get(p['cat'], 'Accessoires'),
           cat_href='rituels.html' if p['cat'] == 'rituels' else ('index.html#' + p['cat']),
           nom=p['nom'], galerie=galerie, accroche=p['accroche'],
           img=p['img'],   # visuel repris dans la ligne de panier
           paybadges=PAY_BADGES,
           accordeons=accordeons,
           bande=bande,
           vers_rituel=vers_rituel,
           etapes=etapes,
           choix=choix,
           complements=complements,
           prix=prix_rond(p['prix']), prix_num=('%.2f' % p['prix']),
           resume=p.get('pdp_resume') or p['resume'],
           delai=delai, total_btn=total_btn,
           bloc_offres=bloc_offres, qty_box=qty_box, cadeau=cadeau, mention=mention,
           prix_annexe=prix_annexe,
           composer=composer, cadeau_rituel=cadeau_rituel,
           bullets=bullets, slug=p['slug'], desc=p['desc'], usage=p['usage'],
           titre_detail=p.get('titre_detail') or p['accroche'],
           usage_ico=('<span class="ico" data-ico="%s"></span>' % p['usage_ico']) if p.get('usage_ico') else '',
           specs=specs, cross=cross, panier=attrs_panier(p))

    # barre d'achat collante en mobile (le CSS .sticky-cart ne s'affiche que sous 640 px),
    # affichee quand la buy box est sortie de l'ecran. Le bouton porte les memes
    # donnees que celui de la fiche : coloris, lot et quantite suivent.
    sticky = """  <!-- Sticky mobile add to cart -->
  <div class="sticky-cart" data-sticky-cart>
    <div class="sticky-cart__info">
      <strong>{nom}</strong>
      <span data-sticky-detail>{prix}</span>
    </div>
    <button class="btn btn--dark btn--sm" data-add="{slug}" data-nom="{nom}"
            data-prix="{prix_num}" data-img="{img}"{panier}>Ajouter</button>
  </div>
""".format(nom=p['nom'], prix=prix_rond(p['prix']), slug=p['slug'],
           prix_num=('%.2f' % p['prix']), img=p['img'], panier=attrs_panier(p))

    return '\n'.join([
        head('%s — Rawstate' % p['nom'], p['resume'].replace('"', '&quot;')),
        '<body class="page-pdp">', '', ANNONCE, header(p['cat']), main,
        FOOTER, sticky, CART, '  <script src="cart.js"></script>', '  <script src="shop.js"></script>', '</body>', '</html>', ''])


# ----------------------------------------------------- page the-fold
def page_the_fold():
    """Contenu d'origine, hero retire (2026-09-22) : la page commence sur la fiche.
    Plus de preload d'image hero, elle n'existe plus sur cette page."""
    return '\n'.join([
        head("Tapis pliable The Fold — Le tapis de yoga pliable qui se range partout",
             "Tapis pliable The Fold — le tapis de yoga pliable premium. Ultra léger, compact, stable. Pensé pour ceux qui pratiquent partout."),
        '<body>', '', ANNONCE, header('tapis'), MAIN_FOLD, FOOTER,
        """  <!-- Sticky mobile add to cart -->
  <div class="sticky-cart" data-sticky-cart>
    <div class="sticky-cart__info">
      <strong>Tapis pliable The Fold</strong>
      <span data-sticky-variant>Fog · 128€</span>
    </div>
    <button class="btn btn--dark btn--sm" data-buy>Ajouter</button>
  </div>
""", CART, '  <script src="cart.js"></script>', '  <script src="script.js"></script>', '</body>', '</html>', ''])


if __name__ == '__main__':
    pages = [('index.html', page_index()), ('rituels.html', page_rituels()),
             ('the-fold.html', page_the_fold())]
    for p in P.PRODUITS:
        if p['slug'] != 'the-fold':
            pages.append((p['page'], page_produit(p)))
    for r in P.RITUELS:                       # une fiche produit par pack
        pr = produit_rituel(r)
        pages.append((pr['page'], page_produit(pr)))
    for nom, html in pages:
        io.open(os.path.join(ROOT, nom), 'w', encoding='utf-8').write(html)
        print('  %-34s %7d octets' % (nom, len(html.encode('utf-8'))))
    print('%d pages generees' % len(pages))
