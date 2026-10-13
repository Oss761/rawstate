/* =========================================================
   RAWSTATE — panier commun a toute la boutique
   Charge avant shop.js (accueil, fiches, rituels) et avant script.js
   (fiche The Fold) : les deux y ajoutent leurs articles via RawCart.add().
   Un seul panier, garde dans localStorage, donc identique d'une page a l'autre.

   Un article :
     id         cle de la ligne (deux ajouts de meme id fusionnent)
     nom        titre de la ligne
     detail     sous-titre (coloris, composition) ; sinon le prix a l'unite
     prix       prix d'un exemplaire de la ligne
     imgs       1 ou 2 vignettes
     sw         pastilles de couleur devant le detail (facultatif)
     sacs       sacs de rangement offerts PAR exemplaire (0 si la fiche n'en annonce pas)
     programme  true si la fiche offre le programme 21 jours
     livr       [mini, maxi, 'c' | 'o'] : delai en jours calendaires ou ouvres
     fold       { c: [coloris], v: [{n, color, img}], duo: {nom, prix} } pour un
                tapis The Fold seul ou en duo : permet l'upsell et le changement
                du 2e coloris depuis le panier, sur n'importe quelle page
     shop       { sku, p: {libelle: valeur} } : variante Shopify de la ligne et
                proprietes de ligne (coloris d'un lot, composition d'un rituel).
                Les tapis The Fold n'en ont pas : leur variante est le coloris.
   ========================================================= */
(function () {
  'use strict';

  var KEY = 'rawstate-cart-v2';
  try { localStorage.removeItem('rawstate-cart-v1'); } catch (e) {}   // ancien format

  function lire() {
    try {
      var c = JSON.parse(localStorage.getItem(KEY));
      return Array.isArray(c) ? c.filter(function (i) {
        return i && typeof i.id === 'string' && typeof i.prix === 'number' && i.qty > 0;
      }) : [];
    } catch (e) { return []; }
  }
  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(cart)); } catch (e) {}
  }
  var cart = lire();

  var cartEl = document.querySelector('[data-cart]');
  var overlay = document.querySelector('[data-cart-overlay]');
  var itemsEl = document.querySelector('[data-cart-items]');
  var emptyEl = document.querySelector('[data-cart-empty]');
  var countEl = document.querySelector('[data-cart-count]');
  var countLabel = document.querySelector('[data-cart-count-label]');
  var subtotalEl = document.querySelector('[data-cart-subtotal]');
  var shippingEl = document.querySelector('[data-cart-shipping]');
  var totalEl = document.querySelector('[data-cart-total]');
  var giftsEl = document.querySelector('[data-cart-gifts]');
  var giftsList = document.querySelector('[data-cart-gifts-list]');
  var upsellEl = document.querySelector('[data-upsell]');
  var upsellSw = document.querySelector('[data-upsell-swatches]');
  var etaLine = document.querySelector('[data-cart-eta-line]');
  var etaEl = document.querySelector('[data-cart-eta]');
  var checkoutBtn = document.querySelector('.cart__checkout');

  var SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">';
  var ICO_SHIELD = SVG + '<path d="M12 21.5c4.5-2 7-5.2 7-9.5V5.2l-7-2.6-7 2.6V12c0 4.3 2.5 7.5 7 9.5z"/><path d="M9.1 11.8l2 2 3.7-3.9"/></svg>';
  var ICO_CADEAU = SVG + '<rect x="3.5" y="8" width="17" height="4.5" rx="1"/><path d="M5 12.5V21h14v-8.5M12 8v13"/>'
    + '<path d="M12 8C10.5 5 8.6 3.6 7.4 4.6 6 5.8 7.6 8 12 8zM12 8c1.5-3 3.4-4.4 4.6-3.4C18 5.8 16.4 8 12 8z"/></svg>';

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }
  // "24,90 €" mais "99 €" : les packs sont a prix rond
  function eur(v) {
    v = Math.round(v * 100) / 100;
    return (v % 1 ? v.toFixed(2).replace('.', ',') : String(v)) + ' €';
  }
  function trouver(id) {
    for (var k = 0; k < cart.length; k++) if (cart[k].id === id) return cart[k];
    return null;
  }

  /* ---------- Cadeaux : uniquement ceux que la fiche de l'article annonce ---------- */
  function sacsTxt(n) { return n > 1 ? n + ' sacs de rangement' : '1 sac de rangement'; }
  function cadeauxLigne(i) {
    var t = [];
    if (i.sacs) t.push(sacsTxt(i.sacs * i.qty));
    if (i.programme) t.push('programme 21 jours');
    return t;
  }

  /* ---------- Date de livraison estimee ----------
     Chaque article a son delai. La commande est complete quand le plus lent
     est arrive : on retient donc la plus tardive des dates "au plus tot" et
     la plus tardive des dates "au plus tard". */
  function dans(n, ouvres) {
    var d = new Date();
    if (!ouvres) { d.setDate(d.getDate() + n); return d; }
    var k = 0;
    while (k < n) {
      d.setDate(d.getDate() + 1);
      if (d.getDay() !== 0 && d.getDay() !== 6) k++;   // saute samedi et dimanche
    }
    return d;
  }
  function estimation() {
    var a = null, b = null;
    for (var k = 0; k < cart.length; k++) {
      var l = cart[k].livr;
      if (!l) return null;                 // un delai inconnu : pas de date plutot qu'une date fausse
      var d1 = dans(l[0], l[2] === 'o'), d2 = dans(l[1], l[2] === 'o');
      if (!a || d1 > a) a = d1;
      if (!b || d2 > b) b = d2;
    }
    return a ? [a, b] : null;
  }
  function jour(d) { return d.getDate() === 1 ? '1er' : String(d.getDate()); }
  function jourMois(d) { return jour(d) + ' ' + d.toLocaleDateString('fr-FR', { month: 'long' }); }
  function texteLivraison(e) {
    var a = e[0], b = e[1];
    if (a.toDateString() === b.toDateString()) return 'Livraison estimée le ' + jourMois(a);
    var memeMois = a.getMonth() === b.getMonth() && a.getFullYear() === b.getFullYear();
    return 'Livraison estimée entre le ' + (memeMois ? jour(a) : jourMois(a)) + ' et le ' + jourMois(b);
  }

  /* ---------- Tapis The Fold : duo fabrique a partir des infos de l'article ---------- */
  function foldDuo(meta, c1, c2, livr) {
    var v = meta.v;
    return { id: 'o2-' + c1 + '-' + c2, nom: meta.duo.nom, detail: v[c1].n + ' + ' + v[c2].n,
             prix: meta.duo.prix, imgs: [v[c1].img, v[c2].img], sw: [v[c1].color, v[c2].color],
             sacs: 2, programme: true, livr: livr,
             fold: { c: [c1, c2], v: v, duo: meta.duo } };
  }
  function estSeul(i) { return i.fold && i.fold.c.length === 1 && i.fold.duo; }
  function prevenirFold(cols) {
    if (typeof api.onFold === 'function') api.onFold(cols);
  }

  /* ---------- Rendu ---------- */
  function ligne(i) {
    var medias = (i.imgs || []).map(function (src) {
      return '<img src="' + esc(src) + '" alt="" loading="lazy" />';
    }).join('');
    var pastilles = (i.sw || []).map(function (c) {
      return '<span class="cart-swatch" style="background:' + esc(c) + '"></span>';
    }).join('');
    var second = '';
    if (i.fold && i.fold.c.length === 2) {
      second = '<div class="cart-item__switch"><span class="cart-item__switch-lbl">2ᵉ&nbsp;tapis&nbsp;:</span>' +
        i.fold.v.map(function (v, k) {
          return '<button type="button" class="cart-item__sw' + (k === i.fold.c[1] ? ' is-on' : '') +
            '" data-set-second="' + k + '" style="background:' + esc(v.color) +
            '" aria-label="2e tapis : ' + esc(v.n) + '" title="' + esc(v.n) + '"></button>';
        }).join('') + '</div>';
    }
    var offerts = cadeauxLigne(i);
    return '<div class="cart-item" data-id="' + esc(i.id) + '">' +
      '<div class="cart-item__media">' + medias + '</div>' +
      '<div class="cart-item__info"><strong>' + esc(i.nom) + '</strong>' +
      '<span class="cart-item__colors">' + pastilles + esc(i.detail || eur(i.prix) + ' l’unité') + '</span>' +
      second +
      (offerts.length ? '<span class="cart-item__offert">' + ICO_CADEAU + 'Offert : ' + esc(offerts.join(' + ')) + '</span>' : '') +
      '<div class="cart-item__qty"><button data-dec aria-label="Moins">−</button><span>' + i.qty +
      '</span><button data-inc aria-label="Plus">+</button></div></div>' +
      '<div class="cart-item__right"><span class="cart-item__price">' + eur(i.prix * i.qty) + '</span>' +
      '<button class="cart-item__remove" data-remove>Retirer</button></div></div>';
  }
  function cadeau(visuel, label, offert) {
    return '<li>' + visuel + '<span class="perk__name">' + label + '</span>' +
      (offert ? '<i class="perk__free">Offert</i>' : '') + '</li>';
  }

  function render() {
    var count = 0, subtotal = 0, sacs = 0, programme = false, tapisFold = 0, seul = null;
    cart.forEach(function (i) {
      count += i.qty;
      subtotal += i.prix * i.qty;
      sacs += (i.sacs || 0) * i.qty;
      if (i.programme) programme = true;
      if (i.fold) tapisFold += i.fold.c.length * i.qty;
      if (!seul && estSeul(i)) seul = i;
    });

    if (countEl) { countEl.textContent = count; countEl.hidden = count === 0; }
    if (countLabel) countLabel.textContent = count + ' article' + (count > 1 ? 's' : '');
    if (emptyEl) emptyEl.style.display = count ? 'none' : 'block';
    if (itemsEl) itemsEl.innerHTML = cart.map(ligne).join('');

    // recapitulatif des cadeaux : affiche seulement si un article du panier en apporte
    var aCadeaux = sacs > 0 || programme;
    if (giftsEl) giftsEl.hidden = !aCadeaux;
    if (giftsList) {
      giftsList.innerHTML = !aCadeaux ? '' :
        (sacs ? cadeau('<img class="perk__img" src="' + RAW_ASSET('perk-bag.webp') + '" alt="" loading="lazy" />', sacsTxt(sacs), true) : '') +
        (programme ? cadeau('<img class="perk__img" src="' + RAW_ASSET('perk-guide.webp') + '" alt="" loading="lazy" />',
                            'Programme 21 jours pour reprendre le yoga', true) : '') +
        cadeau('<span class="perk__ico ico">' + ICO_SHIELD + '</span>',
               'Garantie ' + (tapisFold > 1 ? 90 : 30) + ' jours', false);
    }

    // upsell duo : seulement si un tapis The Fold seul est au panier
    if (upsellEl) upsellEl.hidden = !seul;
    if (upsellSw) {
      upsellSw.innerHTML = !seul ? '' : seul.fold.v.map(function (v, k) {
        return '<button type="button" class="cart-upsell__sw" data-color="' + k + '" style="background:' + esc(v.color) +
          '" aria-label="Coloris ' + esc(v.n) + '" title="' + esc(v.n) + '"></button>';
      }).join('');
    }

    if (subtotalEl) subtotalEl.textContent = eur(subtotal);
    if (shippingEl) {
      shippingEl.textContent = count ? 'Offerte' : '—';
      shippingEl.classList.toggle('is-free', count > 0);
    }
    if (totalEl) totalEl.textContent = eur(subtotal);

    var e = count ? estimation() : null;
    if (etaLine) etaLine.hidden = !e;
    if (etaEl) etaEl.textContent = e ? texteLivraison(e) : '';
    if (checkoutBtn) checkoutBtn.disabled = count === 0;
  }
  function maj() { save(); render(); }

  function openCart() {
    if (!cartEl) return;
    cartEl.classList.add('is-open'); cartEl.setAttribute('aria-hidden', 'false');
    if (overlay) overlay.classList.add('is-open');
  }
  function closeCart() {
    if (!cartEl) return;
    cartEl.classList.remove('is-open'); cartEl.setAttribute('aria-hidden', 'true');
    if (overlay) overlay.classList.remove('is-open');
  }

  /* ---------- Actions ---------- */
  function add(article, n) {
    n = n > 0 ? n : 1;
    var deja = trouver(article.id);
    if (deja) deja.qty += n;
    else { article.qty = n; cart.push(article); }
    maj(); openCart();
  }

  /* Upsell : convertit un "1 tapis" en duo. Le 1er garde son coloris, le
     client choisit celui du 2e. */
  function versDuo(c2) {
    var seul = null;
    for (var k = 0; k < cart.length && !seul; k++) if (estSeul(cart[k])) seul = cart[k];
    if (!seul) return;
    var c1 = seul.fold.c[0];
    var duo = foldDuo(seul.fold, c1, c2, seul.livr);
    seul.qty -= 1;
    if (seul.qty <= 0) cart = cart.filter(function (i) { return i !== seul; });
    var deja = trouver(duo.id);
    if (deja) deja.qty += 1;
    else { duo.qty = 1; cart.push(duo); }
    maj(); prevenirFold([c1, c2]);
  }
  /* Change le coloris du 2e tapis d'une ligne duo, depuis le panier. */
  function changerSecond(it, c2) {
    var c1 = it.fold.c[0];
    var neuf = foldDuo(it.fold, c1, c2, it.livr);
    if (neuf.id === it.id) return;
    var cible = trouver(neuf.id);
    if (cible) {                              // ce duo existe deja : on fusionne
      cible.qty += it.qty;
      cart = cart.filter(function (i) { return i !== it; });
    } else {
      neuf.qty = it.qty;
      cart[cart.indexOf(it)] = neuf;
    }
    maj(); prevenirFold([c1, c2]);
  }

  if (itemsEl) {
    itemsEl.addEventListener('click', function (e) {
      var rowEl = e.target.closest('[data-id]');
      if (!rowEl) return;
      var it = trouver(rowEl.getAttribute('data-id'));
      if (!it) return;
      var sw = e.target.closest('[data-set-second]');
      if (sw) { changerSecond(it, parseInt(sw.getAttribute('data-set-second'), 10)); return; }
      if (e.target.closest('[data-inc]')) it.qty += 1;
      else if (e.target.closest('[data-dec]')) it.qty -= 1;
      else if (e.target.closest('[data-remove]')) it.qty = 0;
      else return;
      if (it.qty <= 0) cart = cart.filter(function (i) { return i !== it; });
      maj();
    });
  }
  if (upsellSw) {
    upsellSw.addEventListener('click', function (e) {
      var b = e.target.closest('[data-color]');
      if (b) versDuo(parseInt(b.getAttribute('data-color'), 10));
    });
  }

  document.querySelectorAll('[data-cart-toggle]').forEach(function (b) { b.addEventListener('click', openCart); });
  document.querySelectorAll('[data-cart-close]').forEach(function (b) { b.addEventListener('click', closeCart); });
  if (overlay) overlay.addEventListener('click', closeCart);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeCart(); });

  /* ---------- Checkout ----------
     Sur le theme Shopify, theme.liquid injecte window.RAW_SHOP :
       { root, fold: {nom du coloris: id de variante}, sku: {SKU: id de variante} }
     Le panier local est alors recopie dans le panier Shopify, puis on part au
     paiement. Sans RAW_SHOP (site statique), la boutique reste une vitrine. */
  var SHOP = window.RAW_SHOP || null;
  var ATTENTE = 'rawstate-checkout';   // pose au depart vers le paiement

  // "bloc-lot2" -> "RAW-BLOC-LOT2", "gourde-Bleu" -> "RAW-GOURDE-BLEU"
  function sku(ref) {
    return 'RAW-' + String(ref).normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/[^A-Za-z0-9]+/g, '-').replace(/^-+|-+$/g, '').toUpperCase();
  }

  /* Lignes Shopify du panier, ou { manque: nom } si un article n'a pas de variante. */
  function lignesShopify() {
    var items = [];
    for (var k = 0; k < cart.length; k++) {
      var i = cart[k];
      if (i.fold) {
        // 1 ou 2 tapis : une ligne par coloris (la remise duo est appliquee par Shopify)
        for (var c = 0; c < i.fold.c.length; c++) {
          var idF = SHOP.fold && SHOP.fold[i.fold.v[i.fold.c[c]].n];
          if (!idF) return { manque: i.nom };
          items.push({ id: idF, quantity: i.qty });
        }
        continue;
      }
      if (!i.shop || !SHOP.sku) return { manque: i.nom };
      var p = i.shop.p || {}, cles = Object.keys(p);
      // un seul exemplaire d'un seul coloris : s'il existe une variante de ce
      // coloris (RAW-BLOC-LOT1-ROSE), on la prend, et le coloris n'a plus a
      // etre repete en propriete. Sinon variante generique + proprietes.
      var idC = cles.length === 1 && cles[0] === 'Coloris' && SHOP.sku[sku(i.shop.sku.replace(/^RAW-/, '') + '-' + p.Coloris)];
      var idV = idC || SHOP.sku[i.shop.sku];
      if (!idV) return { manque: i.nom };
      var l = { id: idV, quantity: i.qty };
      if (!idC && cles.length) l.properties = p;
      items.push(l);
    }
    return { items: items };
  }
  function poster(url, corps) {
    return fetch(SHOP.root + url, {
      method: 'POST', credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(corps || {})
    }).then(function (r) {
      if (!r.ok) throw new Error(url + ' ' + r.status);
      return r.json();
    });
  }
  function erreurCheckout(msg) {
    checkoutBtn.disabled = false;
    checkoutBtn.textContent = 'Passer commande';
    var el = document.querySelector('[data-cart-erreur]');
    if (!el) {
      el = document.createElement('p');
      el.setAttribute('data-cart-erreur', '');
      el.setAttribute('role', 'alert');
      el.style.cssText = 'font-size:13px;line-height:1.45;color:#C21531;text-align:center;';
      checkoutBtn.parentNode.insertBefore(el, checkoutBtn.nextSibling);
    }
    el.textContent = msg;
  }

  if (checkoutBtn) {
    checkoutBtn.addEventListener('click', function () {
      if (!cart.length) return;
      checkoutBtn.disabled = true;
      checkoutBtn.textContent = 'Redirection…';
      if (!SHOP) { window.location.href = 'https://rawstate.fr/cart'; return; }
      var res = lignesShopify();
      if (res.manque) {
        erreurCheckout('« ' + res.manque + ' » n’est plus disponible à la commande. Retirez-le du panier pour continuer.');
        return;
      }
      // le panier Shopify est remplace par le panier affiche : pas de doublon
      // si le client revient en arriere puis repasse commande
      poster('cart/clear.js').then(function () {
        return poster('cart/add.js', { items: res.items });
      }).then(function () {
        try { localStorage.setItem(ATTENTE, '1'); } catch (e) {}
        window.location.href = SHOP.root + 'checkout';
      }).catch(function () {
        erreurCheckout('La commande n’a pas pu être préparée. Réessayez dans un instant ou écrivez-nous à info@rawstate.fr.');
      });
    });
  }

  /* Retour sur la boutique apres un depart au paiement : Shopify vide son panier
     quand la commande est payee. S'il est vide, la commande est passee : on vide
     aussi le panier local. Sinon (abandon, retour arriere) on le garde. */
  function apresCheckout() {
    var parti = null;
    try { parti = localStorage.getItem(ATTENTE); } catch (e) {}
    if (!SHOP || !parti) return;
    fetch(SHOP.root + 'cart.js', { credentials: 'same-origin', headers: { 'Accept': 'application/json' } })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (c) {
        if (!c || c.item_count !== 0) return;
        try { localStorage.removeItem(ATTENTE); } catch (e) {}
        cart = []; maj();
      }).catch(function () {});
  }

  // le panier a pu changer ailleurs : autre onglet, ou retour arriere du navigateur
  window.addEventListener('storage', function (e) { if (e.key === KEY) { cart = lire(); render(); } });
  window.addEventListener('pageshow', function (e) {
    if (e.persisted) { cart = lire(); render(); apresCheckout(); }
  });

  var api = { add: add, open: openCart, close: closeCart, foldDuo: foldDuo, onFold: null, sku: sku };
  window.RawCart = api;
  render();
  apresCheckout();
})();
