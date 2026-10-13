/* =========================================================
   RAWSTATE — boutique multiproduit
   Utilise sur index.html et les pages produit (the-fold.html garde
   script.js). Le panier, lui, est commun : il vit dans cart.js.
   ========================================================= */
(function () {
  'use strict';

  /* ---------- Icons (memes glyphes que script.js, plus calendar et info) ---------- */
  var ICONS = {
    check: '<path d="M4 12l5 5L20 6"/>',
    cart: '<circle cx="9" cy="21" r="1.2"/><circle cx="19" cy="21" r="1.2"/><path d="M2 3h3l2.4 12.2a1.6 1.6 0 0 0 1.6 1.3h9a1.6 1.6 0 0 0 1.6-1.3L23 7H6"/>',
    lock: '<rect x="3.5" y="11" width="17" height="10.5" rx="2.2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/><circle cx="12" cy="15.6" r="1.1"/><path d="M12 16.7v1.7"/>',
    truck: '<path d="M2 7h11v8H2zM13 10h4l3 3v2h-7zM7 18a2 2 0 1 0 0-.01M17 18a2 2 0 1 0 0-.01"/>',
    return: '<polyline points="2 5 2 11 8 11"/><path d="M4.6 15.5a9 9 0 1 0 1.9-9.2L2 11"/>',
    shield: '<path d="M12 21.5c4.5-2 7-5.2 7-9.5V5.2l-7-2.6-7 2.6V12c0 4.3 2.5 7.5 7 9.5z"/><path d="M9.1 11.8l2 2 3.7-3.9"/>',
    leaf: '<path d="M20 4C10 4 4 9 4 16v4"/><path d="M20 4c0 9-5 14-12 14H4"/>',
    calendar: '<rect x="3.5" y="5" width="17" height="15.5" rx="2.2"/><path d="M8 2.8v4M16 2.8v4M3.5 10h17"/>',
    info: '<circle cx="12" cy="12" r="9"/><path d="M12 11.3v5.2"/><circle cx="12" cy="7.9" r=".55"/>',
    // grain de matiere (liege) : un cercle parseme de points
    grain: '<circle cx="12" cy="12" r="9"/><circle cx="9" cy="9.4" r=".9"/><circle cx="14.8" cy="10" r=".7"/>'
         + '<circle cx="11.6" cy="13.2" r=".8"/><circle cx="15.4" cy="14.6" r=".9"/><circle cx="8.6" cy="15.2" r=".7"/>',
    chevron: '<polyline points="15 5 8 12 15 19"/>'
  };
  function icoSvg(n) {
    return ICONS[n] ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">' + ICONS[n] + '</svg>' : '';
  }
  function paintIcons(root) {
    (root || document).querySelectorAll('[data-ico]').forEach(function (el) {
      if (!el.firstChild) el.innerHTML = icoSvg(el.getAttribute('data-ico'));
    });
  }
  paintIcons();

  // "24,90 €" mais "99 €" : les packs sont a prix rond
  function eur(v) { return (v % 1 ? v.toFixed(2).replace('.', ',') : String(v)) + ' €'; }

  /* ---------- Panier : commun a toute la boutique (cart.js) ----------
     Le bouton d'ajout porte ce que la fiche annonce : cadeaux et delai. */
  function infosPanier(btn, carte) {
    var l = ((carte && carte.getAttribute('data-livr')) || btn.getAttribute('data-livr') || '').split(',');
    return { sacs: parseInt(btn.getAttribute('data-sacs'), 10) || 0,
             programme: btn.getAttribute('data-programme') === '1',
             livr: l.length === 2 ? [parseInt(l[0], 10), parseInt(l[1], 10), 'c'] : null };
  }

  /* ---------- Accordeons (meme comportement que sur The Fold) ---------- */
  document.querySelectorAll('[data-accordion]').forEach(function (accordion) {
    accordion.addEventListener('click', function (e) {
      var q = e.target.closest('.acc__q');
      if (!q) return;
      var item = q.parentElement;
      var answer = item.querySelector('.acc__a');
      var open = item.classList.contains('is-open');
      accordion.querySelectorAll('.acc.is-open').forEach(function (it) {
        it.classList.remove('is-open');
        it.querySelector('.acc__a').style.maxHeight = null;
      });
      if (!open) {
        item.classList.add('is-open');
        answer.style.maxHeight = answer.scrollHeight + 'px';
      }
    });
  });

  /* ---------- Galerie de la fiche produit ---------- */
  var showGal = null;
  var gal = document.querySelector('[data-pgal]');
  if (gal) {
    var srcs = (gal.getAttribute('data-pgal-srcs') || '').split('|');
    var alts = (gal.getAttribute('data-pgal-alts') || '').split('|');
    var stageImg = gal.querySelector('[data-pgal-stage] img');
    var thumbs = gal.querySelectorAll('[data-pgal-go]');
    var shown = 0;
    // precharge les autres vues : le changement de vignette est alors instantane
    srcs.slice(1).forEach(function (s) { var i = new Image(); i.src = s; });

    showGal = function (i) {
      if (i < 0) i = srcs.length - 1;
      if (i >= srcs.length) i = 0;
      shown = i;
      stageImg.src = srcs[i];
      stageImg.alt = alts[i] || '';
      thumbs.forEach(function (t, k) { t.classList.toggle('is-active', k === i); });
    };
    gal.addEventListener('click', function (e) {
      var b = e.target.closest('[data-pgal-go]');
      if (b) { showGal(parseInt(b.getAttribute('data-pgal-go'), 10)); return; }
      // fleches de navigation : la galerie boucle (showGal gere le debordement)
      if (e.target.closest('[data-pgal-prev]')) showGal(shown - 1);
      else if (e.target.closest('[data-pgal-next]')) showGal(shown + 1);
    });
    // balayage tactile sur l'image principale
    var x0 = null;
    var stage = gal.querySelector('[data-pgal-stage]');
    stage.addEventListener('touchstart', function (e) {
      x0 = e.touches.length === 1 ? e.touches[0].clientX : null;
    }, { passive: true });
    stage.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 40) showGal(shown + (dx < 0 ? 1 : -1));
      x0 = null;
    }, { passive: true });
  }

  /* ---------- Coloris ---------- */
  var colorBox = document.querySelector('[data-colors]');
  var couleur = null, couleurImg = null;
  if (colorBox) {
    var premier = colorBox.querySelector('.swatch');
    couleur = premier.getAttribute('data-color');
    couleurImg = premier.getAttribute('data-color-img');
    var nomEl = colorBox.querySelector('[data-color-name]');
    colorBox.addEventListener('click', function (e) {
      var sw = e.target.closest('.swatch');
      if (!sw) return;
      colorBox.querySelectorAll('.swatch').forEach(function (b) { b.classList.remove('is-active'); });
      sw.classList.add('is-active');
      couleur = sw.getAttribute('data-color');
      couleurImg = sw.getAttribute('data-color-img');
      if (nomEl) nomEl.textContent = couleur;
      // la galerie suit le coloris choisi
      var i = sw.getAttribute('data-gal');
      if (i !== null && typeof showGal === 'function') showGal(parseInt(i, 10));
      majTotalBouton();   // le coloris apparait aussi dans la barre collante
    });
  }

  /* ---------- Delai de livraison estime (sous le titre) ----------
     jours calendaires ajoutes a la date du jour, recalcule a chaque chargement. */
  document.querySelectorAll('[data-ship-eta]').forEach(function (el) {
    var min = parseInt(el.getAttribute('data-min'), 10) || 8;
    var max = parseInt(el.getAttribute('data-max'), 10) || 14;
    var jour = function (d) { return d.getDate() === 1 ? '1er' : String(d.getDate()); };
    var jourMois = function (d) {
      return jour(d) + ' ' + d.toLocaleDateString('fr-FR', { month: 'long' });
    };
    var a = new Date(); a.setDate(a.getDate() + min);
    var b = new Date(); b.setDate(b.getDate() + max);
    var memeMois = a.getMonth() === b.getMonth() && a.getFullYear() === b.getFullYear();
    el.textContent = 'Livré entre le ' + (memeMois ? jour(a) : jourMois(a)) + ' et le ' + jourMois(b);
  });

  /* ---------- Quantite sur la fiche produit ---------- */
  var qtyBox = document.querySelector('[data-qty]');
  var qty = 1;
  var totalBtn = document.querySelector('[data-add-total]');
  var addBtn = document.querySelector('[data-add]');
  var stickyDetail = document.querySelector('[data-sticky-detail]');
  var lot = null;   // offre par lot choisie, si la fiche en propose
  function prixCourant() {
    if (!addBtn) return 0;
    return lot ? lot.prix : parseFloat(addBtn.getAttribute('data-prix')) * qty;
  }
  function majTotalBouton() {
    var t = prixCourant();
    if (totalBtn && addBtn) totalBtn.textContent = eur(Math.round(t * 100) / 100);
    // la barre collante rappelle ce qu'on s'apprete a ajouter
    if (stickyDetail) {
      var bouts = [];
      if (couleur) bouts.push(couleur);
      else if (composerBox) bouts.push(coloris().map(function (c) { return c.couleur; }).join(' · '));
      if (lot && lot.n > 1) bouts.push('lot de ' + lot.n);
      else if (qty > 1) bouts.push(qty + ' articles');
      bouts.push(eur(t));
      stickyDetail.textContent = bouts.join(' · ');
    }
  }
  if (qtyBox) {
    var val = qtyBox.querySelector('[data-qty-val]');
    qtyBox.addEventListener('click', function (e) {
      if (e.target.closest('[data-qty-inc]')) qty = Math.min(qty + 1, 20);
      else if (e.target.closest('[data-qty-dec]')) qty = Math.max(qty - 1, 1);
      else return;
      val.textContent = qty;
      majTotalBouton();
    });
  }

  /* ---------- "Composez votre rituel" : un coloris par produit du pack ---------- */
  var composerBox = document.querySelector('[data-composer]');
  function coloris() {
    // [{produit, couleur}] dans l'ordre d'affichage
    if (!composerBox) return [];
    return Array.prototype.map.call(composerBox.querySelectorAll('[data-composer-item]'), function (l) {
      var sw = l.querySelector('.swatch.is-active') || l.querySelector('.swatch');
      return { produit: l.getAttribute('data-produit'), couleur: sw.getAttribute('data-color') };
    });
  }
  if (composerBox) {
    composerBox.addEventListener('click', function (e) {
      var sw = e.target.closest('.swatch');
      if (!sw) return;
      var ligne = sw.closest('[data-composer-item]');
      ligne.querySelectorAll('.swatch').forEach(function (b) { b.classList.remove('is-active'); });
      sw.classList.add('is-active');
      var nomEl = ligne.querySelector('[data-composer-nom]');
      if (nomEl) nomEl.textContent = sw.getAttribute('data-color');
      majTotalBouton();
    });
  }

  /* ---------- Offres par lot (remplacent le selecteur de quantite) ---------- */
  var lotsBox = document.querySelector('[data-offers-lots]');
  if (lotsBox) {
    var cartes = lotsBox.querySelectorAll('[data-offer-lot]');
    var unite = lotsBox.getAttribute('data-unite') || 'article';
    var choisirLot = function (el) {
      Array.prototype.forEach.call(cartes, function (c) {
        var on = c === el;
        c.classList.toggle('is-active', on);
        c.setAttribute('aria-checked', on ? 'true' : 'false');
        // le corps (coloris du lot) ne s'ouvre que sur la carte choisie
        var corps = c.querySelector('.offer__body');
        if (corps) {
          clearTimeout(corps._ovf);
          if (on) {
            corps.style.maxHeight = corps.scrollHeight + 'px';
            // une fois ouvert, on libere l'overflow : sinon l'anneau de selection
            // de la 1re pastille est rogne par le bord du panneau
            corps._ovf = setTimeout(function () { corps.style.overflow = 'visible'; }, 380);
          } else {
            corps.style.overflow = 'hidden';
            corps.style.maxHeight = null;
          }
        }
      });
      lot = { n: parseInt(el.getAttribute('data-offer-lot'), 10),
              prix: parseFloat(el.getAttribute('data-prix')),
              remise: parseInt(el.getAttribute('data-remise'), 10),
              carte: el };
      majTotalBouton();
    };

    /* coloris choisis dans la carte active, un par exemplaire du lot */
    lotsBox.coloris = function () {
      if (!lot || !lot.carte) return [];
      return Array.prototype.map.call(
        lot.carte.querySelectorAll('[data-lot-pick]'), function (r) {
          var a = r.querySelector('.swatch.is-active');
          return a ? { couleur: a.getAttribute('data-color'),
                       produit: r.getAttribute('data-lot-produit') } : null;
        }).filter(Boolean);
    };

    // clic sur une pastille d'un lot : pastille active, libelle, galerie, bouton
    lotsBox.addEventListener('click', function (e) {
      var sw = e.target.closest('.swatch');
      if (!sw) return;
      e.stopPropagation();                       // ne pas rebasculer la carte
      var rang = sw.closest('[data-lot-pick]');
      var carte = sw.closest('[data-offer-lot]');
      if (carte && carte !== (lot && lot.carte)) choisirLot(carte);
      rang.querySelectorAll('.swatch').forEach(function (b) { b.classList.remove('is-active'); });
      sw.classList.add('is-active');
      var nomEl = rang.querySelector('[data-lot-nom]');
      if (nomEl) nomEl.textContent = sw.getAttribute('data-color');
      // la galerie suit le 1er exemplaire du lot
      if (rang.getAttribute('data-lot-pick') === '0') {
        couleurImg = sw.getAttribute('data-color-img');
        var ig = sw.getAttribute('data-gal');
        if (ig !== null && typeof showGal === 'function') showGal(parseInt(ig, 10));
      }
      majTotalBouton();
    });
    lotsBox.addEventListener('click', function (e) {
      if (e.target.closest('.swatch')) return;   // gere par le handler des pastilles
      var c = e.target.closest('[data-offer-lot]');
      if (c) choisirLot(c);
    });
    lotsBox.addEventListener('keydown', function (e) {
      if (e.key !== 'Enter' && e.key !== ' ') return;
      var c = e.target.closest('[data-offer-lot]');
      if (c) { e.preventDefault(); choisirLot(c); }
    });
    choisirLot(lotsBox.querySelector('.offer.is-active') || cartes[0]);
  }
  majTotalBouton();   // etat initial du bouton et de la barre collante

  /* ---------- Ajout au panier ---------- */
  document.querySelectorAll('[data-add]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var slug = btn.getAttribute('data-add') + (couleur ? '-' + couleur.toLowerCase() : '');
      var nom = btn.getAttribute('data-nom') + (couleur ? ' · ' + couleur : '');
      var prix = parseFloat(btn.getAttribute('data-prix'));
      var n = qty, unite2 = null;
      // reference Shopify de la ligne (cart.js s'en sert au moment de payer) :
      // la variante se retrouve par son SKU, les coloris d'un lot ou d'un pack
      // partent en proprietes de ligne
      var ref = btn.getAttribute('data-add') + (couleur ? '-' + couleur : '');
      var props = {};
      // pack compose : le detail des coloris distingue les lignes de panier
      var choix = coloris();
      if (choix.length) {
        slug += '-' + choix.map(function (c) {
          return c.couleur.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/\s+/g, '-');
        }).join('-');
        unite2 = choix.map(function (c) { return c.produit + ' ' + c.couleur; }).join(' · ');
        choix.forEach(function (c) { props[c.produit] = c.couleur; });
      }
      if (lot) {
        // un lot = une ligne de panier : prix du lot, quantite = nombre de lots
        n = 1;
        prix = lot.prix;
        var cl = lotsBox.coloris ? lotsBox.coloris() : [];
        var titreLot = lot.carte.getAttribute('data-lot-titre');   // lot multi-produits
        ref += titreLot ? '-duo' : '-lot' + lot.n;
        cl.forEach(function (c, k) {
          props[c.produit || (cl.length > 1 ? 'Coloris ' + (k + 1) : 'Coloris')] = c.couleur;
        });
        if (cl.length) {
          slug += '-' + cl.map(function (c) {
            return c.couleur.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/\s+/g, '-');
          }).join('-');
          var premiere = lot.carte.querySelector('[data-lot-pick="0"] .swatch.is-active');
          if (premiere) couleurImg = premiere.getAttribute('data-color-img');
        }
        if (titreLot) {
          // duo de produits differents : on nomme chaque produit avec son coloris
          slug += '-' + titreLot.toLowerCase().normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, '-');
          nom += ' · ' + titreLot;
          unite2 = cl.map(function (c) {
            return (c.produit ? c.produit + ' ' : '') + c.couleur;
          }).join(' · ');
        } else if (lot.n > 1) {
          slug += '-lot' + lot.n;
          nom += ' · Lot de ' + lot.n;
          unite2 = (cl.length ? cl.map(function (c) { return c.couleur; }).join(' + ') + ' · ' : '')
            + eur(lot.prix) + ' le lot · ' + eur(lot.prix / lot.n) + ' l’unité';
        } else if (cl.length) {
          nom += ' · ' + cl[0].couleur;
          unite2 = null;
        }
      }
      var infos = infosPanier(btn, lot && lot.carte);
      window.RawCart.add({ id: slug, nom: nom, detail: unite2, prix: prix,
                           imgs: [couleurImg || btn.getAttribute('data-img')],
                           sacs: infos.sacs, programme: infos.programme, livr: infos.livr,
                           shop: { sku: window.RawCart.sku(ref), p: props } }, n);
    });
  });

  /* ---------- Ajout immediat ("A completer avec") ----------
     coloris impose par le bouton, toujours 1 exemplaire : ni le coloris
     ni la quantite choisis sur la fiche ne s'appliquent ici. */
  document.querySelectorAll('[data-add-now]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var infos = infosPanier(btn);
      window.RawCart.add({ id: btn.getAttribute('data-add-now'), nom: btn.getAttribute('data-nom'),
                           prix: parseFloat(btn.getAttribute('data-prix')),
                           imgs: [btn.getAttribute('data-img')],
                           sacs: infos.sacs, programme: infos.programme, livr: infos.livr }, 1);
    });
  });

  /* ---------- Formulaire d'avis (repris de script.js) ----------
     Demo statique : validation + confirmation cote client. Pour collecter
     reellement les avis, brancher le submit sur une app d'avis / un endpoint. */
  (function () {
    var form = document.querySelector('[data-review-form]');
    if (!form) return;
    var starsWrap = form.querySelector('[data-rating]');
    var stars = starsWrap ? Array.prototype.slice.call(starsWrap.querySelectorAll('.review-form__star')) : [];
    var rating = 0;
    function paint(n) { stars.forEach(function (s, i) { s.classList.toggle('is-on', i < n); }); }
    stars.forEach(function (s) {
      var val = parseInt(s.getAttribute('data-star'), 10);
      s.addEventListener('click', function () { rating = val; paint(rating); s.setAttribute('aria-pressed', 'true'); });
      s.addEventListener('mouseenter', function () { paint(val); });
    });
    if (starsWrap) starsWrap.addEventListener('mouseleave', function () { paint(rating); });

    var errEl = form.querySelector('[data-review-error]');
    var doneEl = form.querySelector('[data-review-done]');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = (form.querySelector('[name="name"]') || {}).value || '';
      var review = (form.querySelector('[name="review"]') || {}).value || '';
      if (!rating || !name.trim() || !review.trim()) {
        if (errEl) errEl.hidden = false;
        return;
      }
      if (errEl) errEl.hidden = true;
      Array.prototype.forEach.call(form.querySelectorAll('.review-form__field, .review-form__submit'), function (el) {
        el.style.display = 'none';
      });
      if (doneEl) doneEl.hidden = false;
    });
  })();

  /* ---------- Story a la une (photos en situation) ----------
     Lecture facon story : 5 s par photo, barres de progression, navigation
     gauche/droite (clic, fleches, balayage), fermeture a la derniere photo. */
  (function () {
    var vue = document.querySelector('[data-storyview]');
    var bulle = document.querySelector('[data-story]');
    if (!vue || !bulle) return;
    var DUREE = 5000;
    var srcs = (vue.getAttribute('data-srcs') || '').split('|');
    var alts = (vue.getAttribute('data-alts') || '').split('|');
    var img = vue.querySelector('[data-story-img]');
    var barres = vue.querySelectorAll('.sv__barre');
    var i = 0, minuteur = null;

    srcs.forEach(function (s) { var p = new Image(); p.src = s; });   // precharge

    function montrer(n) {
      if (n < 0) n = 0;
      if (n >= srcs.length) { fermer(); return; }
      i = n;
      img.src = srcs[i];
      img.alt = alts[i] || '';
      Array.prototype.forEach.call(barres, function (b, k) {
        b.classList.remove('is-active', 'is-passee');
        if (k < i) b.classList.add('is-passee');
      });
      // on relance l'animation de la barre courante
      var barre = barres[i];
      if (barre) {
        var i2 = barre.querySelector('i');
        i2.style.animation = 'none';
        void i2.offsetWidth;
        i2.style.animation = '';
        barre.classList.add('is-active');
      }
      clearTimeout(minuteur);
      minuteur = setTimeout(function () { montrer(i + 1); }, DUREE);
    }

    function ouvrir() {
      vue.hidden = false;
      document.body.classList.add('sv-ouverte');
      vue.style.setProperty('--sv-duree', (DUREE / 1000) + 's');
      montrer(0);
      var f = vue.querySelector('[data-story-close]');
      if (f) f.focus();
    }
    function fermer() {
      clearTimeout(minuteur);
      vue.hidden = true;
      document.body.classList.remove('sv-ouverte');
      Array.prototype.forEach.call(barres, function (b) { b.classList.remove('is-active', 'is-passee'); });
      bulle.focus();
    }

    bulle.addEventListener('click', ouvrir);
    vue.querySelector('[data-story-close]').addEventListener('click', fermer);
    vue.querySelector('[data-story-prev]').addEventListener('click', function () { montrer(i - 1); });
    vue.querySelector('[data-story-next]').addEventListener('click', function () { montrer(i + 1); });
    document.addEventListener('keydown', function (e) {
      if (vue.hidden) return;
      if (e.key === 'Escape') fermer();
      else if (e.key === 'ArrowLeft') montrer(i - 1);
      else if (e.key === 'ArrowRight') montrer(i + 1);
    });
    // balayage tactile
    var x0 = null;
    vue.addEventListener('touchstart', function (e) {
      x0 = e.touches.length === 1 ? e.touches[0].clientX : null;
    }, { passive: true });
    vue.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 40) montrer(i + (dx < 0 ? 1 : -1));
      x0 = null;
    }, { passive: true });
  })();

  /* ---------- Barre d'achat collante (mobile) ----------
     visible quand la buy box est sortie de l'ecran, masquee pres du pied de page.
     Le CSS ne l'affiche que sous 640 px. */
  var sticky = document.querySelector('[data-sticky-cart]');
  var buyBox = document.querySelector('.pdp__buy');
  function majSticky() {
    if (!sticky || !buyBox) return;
    var passee = buyBox.getBoundingClientRect().bottom < 0;
    var pied = (window.innerHeight + window.scrollY) > document.body.offsetHeight - 320;
    sticky.classList.toggle('is-visible', passee && !pied);
  }
  window.addEventListener('resize', majSticky);
  majSticky();

  /* ---------- Header : scroll + menu mobile ---------- */
  var header = document.querySelector('[data-header]');
  var burger = document.querySelector('[data-menu-toggle]');
  var mobile = document.querySelector('[data-mobile-menu]');
  window.addEventListener('scroll', function () {
    if (header) header.classList.toggle('is-scrolled', window.scrollY > 8);
    majSticky();
  }, { passive: true });
  // le CSS ouvre le panneau sur .header.is-menu-open (comme script.js)
  function menu(on) {
    header.classList.toggle('is-menu-open', on);
    burger.setAttribute('aria-expanded', on ? 'true' : 'false');
    burger.setAttribute('aria-label', on ? 'Fermer le menu' : 'Ouvrir le menu');
  }
  if (header && burger && mobile) {
    burger.addEventListener('click', function () { menu(!header.classList.contains('is-menu-open')); });
    mobile.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { menu(false); });
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') menu(false); });
  }

  /* ---------- Les 3 rituels de l'accueil ----------
     Desktop : les 3 cote a cote, rien a faire. Mobile : la piste deborde et
     defile ; on centre Le Studio au chargement, les fleches avancent d'une
     carte, le glissement au doigt est natif (scroll-snap). */
  var rPiste = document.querySelector('[data-rhome-piste]');
  if (rPiste) {
    var rCartes = rPiste.querySelectorAll('.rite');
    var rFleches = document.querySelectorAll('[data-rhome]');
    var rCentre = false;
    var rLargeur = 0;

    function rPas() {
      return rCartes.length > 1
        ? rCartes[1].getBoundingClientRect().left - rCartes[0].getBoundingClientRect().left
        : rPiste.clientWidth;
    }
    function rMajFleches() {
      var max = rPiste.scrollWidth - rPiste.clientWidth;
      rFleches.forEach(function (b) {
        var sens = parseInt(b.getAttribute('data-rhome'), 10);
        b.disabled = max <= 0 || (sens < 0 ? rPiste.scrollLeft <= 4
                                           : rPiste.scrollLeft >= max - 4);
      });
    }
    function rCentrer() {
      var max = rPiste.scrollWidth - rPiste.clientWidth;
      if (max > 0) { rPiste.scrollLeft = max / 2; rCentre = true; }
      rLargeur = rPiste.clientWidth;
      rMajFleches();
    }

    rFleches.forEach(function (b) {
      b.addEventListener('click', function () {
        rPiste.scrollBy({ left: parseInt(b.getAttribute('data-rhome'), 10) * rPas(),
                          behavior: 'smooth' });
      });
    });
    rPiste.addEventListener('scroll', rMajFleches, { passive: true });
    rCentrer();
    // le CSS complet est charge en asynchrone : tant qu'il n'est pas applique la
    // piste ne deborde pas et le centrage ne peut pas avoir lieu.
    window.addEventListener('load', function () { if (!rCentre) rCentrer(); });
    // on ne recentre au redimensionnement que si la largeur a vraiment change
    // (sinon la barre d'adresse mobile relancerait le centrage pendant le scroll)
    window.addEventListener('resize', function () {
      if (rPiste.clientWidth !== rLargeur) rCentrer();
    });
  }

  /* ---------- Apparition au scroll ---------- */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* ---------- Bandeau d'annonce ----------
     Un message a la fois, change toutes les 5 s : le sortant glisse vers le bas,
     l'entrant arrive par le haut. Les messages hors ecran sont masques aux
     lecteurs d'ecran, qui ne doivent entendre que celui affiche. */
  var track = document.querySelector('[data-announce-track]');
  if (track) {
    var messages = ['Livraison offerte', 'Garantie 30 jours',
                    'Programme yoga offert avec chaque tapis'];
    track.innerHTML = '';
    var items = messages.map(function (t, i) {
      var el = document.createElement('span');
      el.className = 'announce__item' + (i === 0 ? ' is-in' : '');
      el.textContent = t;
      el.setAttribute('aria-hidden', i === 0 ? 'false' : 'true');
      track.appendChild(el);
      return el;
    });
    if (items.length > 1) {
      var courant = 0;
      setInterval(function () {
        var sortant = items[courant];
        courant = (courant + 1) % items.length;
        var entrant = items[courant];
        sortant.classList.remove('is-in');
        sortant.classList.add('is-out');
        sortant.setAttribute('aria-hidden', 'true');
        entrant.classList.add('is-in');
        entrant.setAttribute('aria-hidden', 'false');
        // une fois sorti, on le replace en haut sans animation, pret a revenir
        setTimeout(function () {
          sortant.style.transition = 'none';
          sortant.classList.remove('is-out');
          void sortant.offsetHeight;          // force le recalcul avant de rendre la main
          sortant.style.transition = '';
        }, 600);
      }, 5000);
    }
  }
})();
