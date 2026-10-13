/* =========================================================
   RAWSTATE — interactions
   ========================================================= */
(function () {
  'use strict';

  /* ---------- Variant data (strict grayscale palette) ---------- */
  /* `swatchImg` = miniature du tapis entier (detoure sur fond transparent) posee
     dans la pastille de selection, par-dessus l'aplat `color`. */
  var VARIANTS = [
    { id: 'anthracite', name: 'Fog',    color: '#383b3e', ink: '#ffffff',
      swatchImg: RAW_ASSET('swatch-grey.webp') },
    { id: 'sky',        name: 'Lagoon', color: '#a9cfe3', ink: '#111111',
      swatchImg: RAW_ASSET('swatch-blue.webp') },
    { id: 'rose',       name: 'Dusk',   color: '#ebc7d2', ink: '#111111',
      swatchImg: RAW_ASSET('swatch-pink.webp') }
  ];
  var current = 0;

  /* ---------- Gallery (9 photos + 1 vidéo, 1:1, ordre fixe) ----------
     Une entrée est soit une string (image), soit { video, poster }. La vignette
     n'affiche jamais que le poster : la vidéo n'est téléchargée qu'au moment où
     l'on ouvre sa vue. Les index 0-2 restent les 3 coloris (utilisés par le
     sélecteur de couleur et par les lignes du panier). */
  var GALLERY = [
    RAW_ASSET('mat-grey.webp'),   // 1 — tapis gris déplié
    RAW_ASSET('mat-blue.webp'),   // 2 — tapis bleu déplié
    RAW_ASSET('mat-pink.webp'),   // 3 — tapis rose déplié
    RAW_ASSET('colors.webp'),     // 4 — les 3 coloris pliés + badge garantie 30 jours
    RAW_ASSET('carousel-sofa.webp'),    // 5 — rangé sous le canapé (« Le tapis facile à ranger chez soi »)
    RAW_ASSET('carousel-yoga.webp'),    // 6 — pile de tapis rose plié (+ tapis bleu)
    RAW_ASSET('carousel-stack.webp'),   // 7 — comparatif « Tapis plié » / « Tapis déplié » au sol
    RAW_ASSET('carousel-texture.webp'), // 8 — tableau comparatif The Fold vs tapis roulés
    RAW_ASSET('dimensions.webp'), // 9 — dimensions
    { video: RAW_ASSET('programme-21jours.mp4'),        // 10 — le programme 21 jours feuilleté
      poster: RAW_ASSET('programme-21jours-poster.webp') }
  ];

  var mainEl = document.querySelector('[data-gallery-main]');
  var stageEl = document.querySelector('[data-gallery-stage]');
  var thumbsEl = document.querySelector('[data-gallery-thumbs]');
  var activeThumb = 0;

  function imgTag(src) {
    return '<img src="' + src + '" alt="Tapis pliable The Fold" loading="lazy" />';
  }
  function isVideo(item) { return typeof item !== 'string'; }
  function posterOf(item) { return isVideo(item) ? item.poster : item; }
  function mainTag(item) {
    if (!isVideo(item)) return imgTag(item);
    // muted + playsinline sont indispensables : sans eux les navigateurs
    // refusent la lecture automatique.
    return '<video src="' + item.video + '" poster="' + item.poster + '"' +
      ' autoplay muted loop playsinline preload="metadata"' +
      ' aria-label="Aperçu du programme 21 jours pour reprendre le yoga"></video>';
  }
  function renderGallery() {
    thumbsEl.innerHTML = GALLERY.map(function (item, i) {
      return '<button class="gallery__thumb' + (i === activeThumb ? ' is-active' : '') +
        (isVideo(item) ? ' is-video' : '') +
        '" data-thumb="' + i + '" aria-label="Vue ' + (i + 1) +
        (isVideo(item) ? ' (vidéo)' : '') + '">' + imgTag(posterOf(item)) + '</button>';
    }).join('');
    setMain(activeThumb);
  }
  function setMain(i) {
    activeThumb = i;
    stageEl.innerHTML = '<div class="fade" style="width:100%;height:100%">' + mainTag(GALLERY[i]) + '</div>';
    Array.prototype.forEach.call(thumbsEl.children, function (btn, idx) {
      btn.classList.toggle('is-active', idx === i);
    });
  }
  function step(dir) {
    setMain((activeThumb + dir + GALLERY.length) % GALLERY.length);
  }

  thumbsEl.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-thumb]');
    if (btn) setMain(parseInt(btn.getAttribute('data-thumb'), 10));
  });
  mainEl.addEventListener('click', function (e) {
    var nav = e.target.closest('[data-nav]');
    if (nav) step(parseInt(nav.getAttribute('data-nav'), 10));
  });

  /* Swipe tactile (mobile) : glisser sur l'image principale change de vue.
     On agit au touchend pour ne pas bloquer le scroll vertical de la page. */
  (function () {
    var startX = 0, startY = 0, tracking = false;
    mainEl.addEventListener('touchstart', function (e) {
      if (e.touches.length !== 1) { tracking = false; return; }
      startX = e.touches[0].clientX;
      startY = e.touches[0].clientY;
      tracking = true;
    }, { passive: true });
    mainEl.addEventListener('touchend', function (e) {
      if (!tracking) return;
      tracking = false;
      var t = e.changedTouches[0];
      var dx = t.clientX - startX;
      var dy = t.clientY - startY;
      if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy) * 1.5) {
        step(dx < 0 ? 1 : -1);
      }
    }, { passive: true });
  })();

  /* ---------- Offers + colour selection ---------- */
  var offersEl = document.querySelector('[data-offers]');
  var stickyVariant = document.querySelector('[data-sticky-variant]');
  var buyPriceEls = document.querySelectorAll('[data-buy] .btn__price');

  var PRICES = {
    1: { now: '69,90 €' },
    2: { now: '118,80 €', old: '139,80 €' },
    3: { now: '99 €', old: '114,70 €' }
  };

  /* Coloris du bloc et des chaussettes, pour l'offre « Rituel L'Essentiel ».
     ATTENTION : recopies de tools/products.py. Cette fiche n'est pas generee
     depuis le catalogue, il faut les resynchroniser a la main si ca change. */
  var BLOC = [
    { name: 'Rose', color: '#f3bfd0', swatchImg: RAW_ASSET('bloc-sw-rose.webp') },
    { name: 'Vert', color: '#cfe39a', swatchImg: RAW_ASSET('bloc-sw-vert.webp') },
    { name: 'Noir', color: '#6f6a66', swatchImg: RAW_ASSET('bloc-sw-noir.webp') },
    { name: 'Bleu', color: '#b7dcf5', swatchImg: RAW_ASSET('bloc-sw-bleu.webp') }
  ];
  var SOCKS = [
    { name: 'Noir', color: '#6f6a66', swatchImg: RAW_ASSET('chaussettes-sw-noir.webp') },
    { name: 'Bleu', color: '#b5d3f3', swatchImg: RAW_ASSET('chaussettes-sw-bleu.webp') },
    { name: 'Rose', color: '#f7cfcf', swatchImg: RAW_ASSET('chaussettes-sw-rose.webp') }
  ];

  var state = { offer: 1, single: 0, duo: [0, 1], rit: { fold: 0, bloc: 0, socks: 0 } };

  function swatchBtns(liste, selected) {
    return liste.map(function (v, i) {
      return '<button type="button" class="swatch' + (i === selected ? ' is-active' : '') +
        '" aria-label="' + v.name + '" data-idx="' + i + '" style="background:' + v.color +
        ';border-color:' + v.color + '">' +
        '<img class="swatch__img" src="' + v.swatchImg + '" alt="" aria-hidden="true" />' +
        '</button>';
    }).join('');
  }
  // mention : texte ajoute apres le coloris (la taille des chaussettes), hors du <span>
  function pickRow(group, label, liste, selected, mention) {
    return '<div class="pick-row" data-group="' + group + '">' +
      '<div class="pick-row__label">' + label + ' — <span>' + liste[selected].name + '</span>' +
      (mention ? ' ' + mention : '') + '</div>' +
      '<div class="pick-row__swatches">' + swatchBtns(liste, selected) + '</div></div>';
  }

  function renderOffers() {
    offersEl.querySelector('[data-pick="single"]').innerHTML =
      pickRow('single', 'Couleur', VARIANTS, state.single);
    offersEl.querySelector('[data-pick="duo"]').innerHTML =
      pickRow('duo0', 'Tapis 1', VARIANTS, state.duo[0]) + pickRow('duo1', 'Tapis 2', VARIANTS, state.duo[1]);
    var pickRit = offersEl.querySelector('[data-pick="rituel"]');
    if (pickRit) {
      pickRit.innerHTML = pickRow('rit-fold', 'Tapis The Fold', VARIANTS, state.rit.fold)
        + pickRow('rit-bloc', 'Bloc The Block', BLOC, state.rit.bloc)
        + pickRow('rit-socks', 'Chaussettes The Socks', SOCKS, state.rit.socks, '(Taille : 37-43)');
    }
    // le sac offert suit le nombre de tapis de l'offre choisie
    var sacEl = document.querySelector('[data-offerts-sac]');
    if (sacEl) sacEl.textContent = state.offer === 2 ? '2 sacs de rangement' : '1 sac de rangement';

    offersEl.querySelectorAll('.offer').forEach(function (card) {
      var on = parseInt(card.getAttribute('data-offer'), 10) === state.offer;
      card.classList.toggle('is-active', on);
      card.setAttribute('aria-checked', on);
      var body = card.querySelector('.offer__body');
      if (!body) return;
      clearTimeout(body._ovfTimer);
      if (on) {
        body.style.maxHeight = body.scrollHeight + 'px';
        // once expanded, allow overflow so the selection ring isn't clipped by the panel edges
        body._ovfTimer = setTimeout(function () { body.style.overflow = 'visible'; }, 380);
      } else {
        body.style.overflow = 'hidden';
        body.style.maxHeight = null;
      }
    });

    var p = PRICES[state.offer];
    buyPriceEls.forEach(function (el) { el.textContent = '— ' + p.now; });
    if (stickyVariant) {
      stickyVariant.textContent =
        (state.offer === 1 ? '1 tapis · ' : state.offer === 3 ? "Rituel L'Essentiel · " : '2 tapis · ') + p.now;
    }
  }

  offersEl.addEventListener('click', function (e) {
    var sw = e.target.closest('.swatch');
    if (sw) {
      var idx = parseInt(sw.getAttribute('data-idx'), 10);
      var group = sw.closest('.pick-row').getAttribute('data-group');
      state.offer = parseInt(sw.closest('.offer').getAttribute('data-offer'), 10);
      var tapis = true;   // seuls les coloris de TAPIS font bouger la galerie
      if (group === 'single') state.single = idx;
      else if (group === 'duo0') state.duo[0] = idx;
      else if (group === 'duo1') state.duo[1] = idx;
      else if (group === 'rit-fold') state.rit.fold = idx;
      else if (group === 'rit-bloc') { state.rit.bloc = idx; tapis = false; }
      else if (group === 'rit-socks') { state.rit.socks = idx; tapis = false; }
      renderOffers();
      if (tapis) setMain(idx); // galerie sur le coloris choisi (0/1/2)
      return;
    }
    var card = e.target.closest('.offer');
    if (card) {
      state.offer = parseInt(card.getAttribute('data-offer'), 10);
      renderOffers();
    }
  });

  /* ---------- Icons ---------- */
  var ICONS = {
    check: '<path d="M4 12l5 5L20 6"/>',
    cart: '<circle cx="9" cy="21" r="1.2"/><circle cx="19" cy="21" r="1.2"/><path d="M2 3h3l2.4 12.2a1.6 1.6 0 0 0 1.6 1.3h9a1.6 1.6 0 0 0 1.6-1.3L23 7H6"/>',
    lock: '<rect x="3.5" y="11" width="17" height="10.5" rx="2.2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/><circle cx="12" cy="15.6" r="1.1"/><path d="M12 16.7v1.7"/>',
    truck: '<path d="M2 7h11v8H2zM13 10h4l3 3v2h-7zM7 18a2 2 0 1 0 0-.01M17 18a2 2 0 1 0 0-.01"/>',
    return: '<polyline points="2 5 2 11 8 11"/><path d="M4.6 15.5a9 9 0 1 0 1.9-9.2L2 11"/>',
    shield: '<path d="M12 21.5c4.5-2 7-5.2 7-9.5V5.2l-7-2.6-7 2.6V12c0 4.3 2.5 7.5 7 9.5z"/><path d="M9.1 11.8l2 2 3.7-3.9"/>',
    globe: '<circle cx="12" cy="12" r="8"/><path d="M4 12h16M12 4c2.5 2.5 2.5 13 0 16M12 4c-2.5 2.5-2.5 13 0 16"/>',
    heart: '<path d="M12 20s-7-4.4-9-8.5C1.5 8 3.5 5 6.5 5 9 5 12 8 12 8s3-3 5.5-3C20.5 5 22.5 8 21 11.5 19 15.6 12 20 12 20z"/>',
    bolt: '<path d="M13 3L5 13h6l-1 8 8-10h-6z"/>',
    fold: '<path d="M4 8l8-4 8 4-8 4zM4 8v8l8 4 8-4V8M12 12v8"/>',
    bag: '<path d="M6 8h12l-1 12H7zM9 8V6a3 3 0 0 1 6 0v2"/>',
    grip: '<path d="M5 5h4v4H5zM10 5h4v4h-4zM15 5h4v4h-4zM5 10h4v4H5zM10 10h4v4h-4zM15 10h4v4h-4zM5 15h4v4H5zM10 15h4v4h-4zM15 15h4v4h-4z"/>',
    leaf: '<path d="M4 20C4 10 12 4 20 4c0 10-7 16-16 16zM4 20c4-8 8-11 12-13"/>',
    plane: '<path d="M10 4l2 6 8 3-8 2-2 6-2-6-4-2 4-2z"/>',
    sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/>',
    balance: '<path d="M12 3v18M5 21h14M6 7h12M6 7l-3 6a3 3 0 0 0 6 0zM18 7l-3 6a3 3 0 0 0 6 0z"/>',
    drop: '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>',
    instagram: '<rect x="4" y="4" width="16" height="16" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17" cy="7" r="1" fill="currentColor" stroke="none"/>',
    tiktok: '<path d="M15 4c.5 3 2.5 4.5 5 4.5v3c-2 0-3.7-.6-5-1.6V15a5.5 5.5 0 1 1-5.5-5.5c.3 0 .7 0 1 .1v3.1a2.5 2.5 0 1 0 1.5 2.3V4z"/>',
    youtube: '<rect x="3" y="6" width="18" height="12" rx="4"/><path d="M10 9.5l5 2.5-5 2.5z" fill="currentColor" stroke="none"/>',
    pinterest: '<circle cx="12" cy="12" r="9"/><path d="M9.5 20c-.5-2 .5-5 1-7 .3-1.2-.5-2.5.3-3.7C11.8 7.5 15 8 15 11c0 2-1 4-3 4-1 0-1.7-.8-1.5-1.8"/>'
  };

  function icoSvg(name) {
    if (!ICONS[name]) return '';
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">' + ICONS[name] + '</svg>';
  }
  // Version balise complete, pour le contenu injecte apres coup (le balayage
  // [data-ico] ci-dessous ne tourne qu'une fois, au chargement).
  function icoHtml(name, cls) {
    return '<span class="' + (cls || 'ico') + '">' + icoSvg(name) + '</span>';
  }

  document.querySelectorAll('[data-ico]').forEach(function (el) {
    el.innerHTML = icoSvg(el.getAttribute('data-ico'));
  });

  /* ---------- Délai de livraison estimé (temps réel : +6 à +8 jours ouvrés) ---------- */
  var FOLD_LIVR = [6, 8, 'o'];   // repris tel quel par la ligne de panier
  (function () {
    var els = document.querySelectorAll('[data-delivery]');
    if (!els.length) return;
    function addBusinessDays(from, n) {
      var d = new Date(from.getTime());
      var added = 0;
      while (added < n) {
        d.setDate(d.getDate() + 1);
        var day = d.getDay();
        if (day !== 0 && day !== 6) added++; // saute samedi (6) et dimanche (0)
      }
      return d;
    }
    var today = new Date();
    var d1 = addBusinessDays(today, FOLD_LIVR[0]);
    var d2 = addBusinessDays(today, FOLD_LIVR[1]);
    function day(d) { return d.toLocaleDateString('fr-FR', { day: 'numeric' }); }
    function dayMonth(d) { return d.toLocaleDateString('fr-FR', { day: 'numeric', month: 'long' }); }
    var sameMonth = d1.getMonth() === d2.getMonth() && d1.getFullYear() === d2.getFullYear();
    var txt = sameMonth
      ? 'Livré entre le ' + day(d1) + ' et le ' + dayMonth(d2)
      : 'Livré entre le ' + dayMonth(d1) + ' et le ' + dayMonth(d2);
    Array.prototype.forEach.call(els, function (el) { el.textContent = txt; });
  })();

  /* ---------- Formulaire d'avis (jeune marque) ----------
     Démo statique : validation + confirmation côté client. Pour collecter
     réellement les avis, brancher le submit sur une app d'avis / un endpoint. */
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

  /* ---------- Instagram marquee ---------- */
  var INSTA_IMGS = [
    RAW_ASSET('insta-home.webp'), RAW_ASSET('insta-suitcase.webp'), RAW_ASSET('insta-studio.webp'),
    RAW_ASSET('insta-shelf.webp'), RAW_ASSET('insta-rooftop.webp'), RAW_ASSET('insta-gift.webp')
  ];
  function instaUnit() {
    return INSTA_IMGS.map(function (src, i) {
      return '<a class="insta__cell" href="#" aria-label="Post Instagram ' + (i + 1) + '">' +
        '<img src="' + src + '" alt="Rawstate lifestyle" loading="lazy" /></a>';
    }).join('');
  }

  /* ---------- Complementary products ---------- */
  var ADDON_ICON = {
    strap: '<svg viewBox="0 0 100 100" fill="none" stroke="#111" stroke-width="2.5" stroke-linecap="round"><rect x="30" y="20" width="40" height="60" rx="6"/><path d="M30 35h40M30 65h40"/><path d="M20 30c-6 8-6 32 0 40M80 30c6 8 6 32 0 40"/></svg>',
    spray: '<svg viewBox="0 0 100 100" fill="none" stroke="#111" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="36" y="38" width="28" height="42" rx="4"/><path d="M42 38v-8h16v8M58 22h10M58 26h8M58 30h6"/></svg>',
    block: '<svg viewBox="0 0 100 100" fill="none" stroke="#111" stroke-width="2.5" stroke-linejoin="round"><path d="M28 42l22-12 22 12-22 12z"/><path d="M28 42v22l22 12 22-12V42M50 54v22"/></svg>',
    towel: '<svg viewBox="0 0 100 100" fill="none" stroke="#111" stroke-width="2.5" stroke-linecap="round"><rect x="26" y="26" width="48" height="48" rx="4"/><path d="M36 26v48M64 26v48" opacity=".5"/></svg>'
  };
  var ADDONS = [
    { name: 'Sangle de transport', icon: 'strap', rating: '4.8', reviews: '312', price: '24€' },
    { name: 'Spray nettoyant', icon: 'spray', rating: '4.9', reviews: '540', price: '18€' },
    { name: 'Brique de yoga', icon: 'block', rating: '4.7', reviews: '208', price: '22€' },
    { name: 'Serviette de yoga', icon: 'towel', rating: '4.9', reviews: '176', price: '29€' }
  ];
  var addonsEl = document.querySelector('[data-addons]');
  if (addonsEl) {
    addonsEl.innerHTML = ADDONS.map(function (a) {
      return '<article class="addon reveal">' +
        '<div class="addon__media">' + ADDON_ICON[a.icon] + '</div>' +
        '<div class="addon__body">' +
        '<h3>' + a.name + '</h3>' +
        '<div class="addon__rating"><span class="stars stars--sm"><span class="stars__fill" style="--rating:100%"></span></span> ' + a.rating + ' · ' + a.reviews + ' avis</div>' +
        '<div class="addon__foot"><span class="addon__price">' + a.price + '</span><button class="addon__add">Ajouter</button></div>' +
        '</div></article>';
    }).join('');
  }

  /* ---------- Accordion ---------- */
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

  /* ---------- Reveal on scroll + histogram ---------- */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) {
        en.target.classList.add('is-in');
        io.unobserve(en.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });

  var histoIO = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { en.target.classList.add('is-in'); histoIO.unobserve(en.target); }
    });
  }, { threshold: 0.4 });
  document.querySelectorAll('.histo__bar').forEach(function (el) { histoIO.observe(el); });

  /* ---------- Mobile menu toggle ---------- */
  var menuToggle = document.querySelector('[data-menu-toggle]');
  var hdr = document.querySelector('[data-header]');
  if (menuToggle && hdr) {
    menuToggle.addEventListener('click', function () {
      var open = hdr.classList.toggle('is-menu-open');
      menuToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      menuToggle.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
    });
    document.querySelectorAll('[data-mobile-menu] a').forEach(function (a) {
      a.addEventListener('click', function () {
        hdr.classList.remove('is-menu-open');
        menuToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ---------- Header scroll state ---------- */
  var header = document.querySelector('[data-header]');
  var stickyCart = document.querySelector('[data-sticky-cart]');
  var productSection = document.getElementById('product');

  function onScroll() {
    var y = window.scrollY;
    header.classList.toggle('is-scrolled', y > 8);
    if (stickyCart && productSection) {
      var pastProduct = y > productSection.offsetTop + 200;
      var nearFooter = (window.innerHeight + y) > document.body.offsetHeight - 400;
      stickyCart.classList.toggle('is-visible', pastProduct && !nearFooter);
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---------- Hero parallax ---------- */
  var parallax = document.querySelector('[data-parallax]');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var ticking = false;
  function parallaxTick() {
    if (parallax) {
      var offset = Math.min(window.scrollY * 0.12, 80);
      parallax.style.transform = 'translateY(' + offset + 'px)';
    }
    ticking = false;
  }
  if (parallax && !reduce) {
    window.addEventListener('scroll', function () {
      if (!ticking) { window.requestAnimationFrame(parallaxTick); ticking = true; }
    }, { passive: true });
  }

  /* ---------- Panier : commun a toute la boutique (cart.js) ----------
     Cette fiche fabrique l'article ; le rendu, les quantites, l'upsell duo et
     le changement du 2e coloris vivent dans cart.js, donc sur toutes les pages. */
  function eur(n) { return n.toFixed(2).replace('.', ',') + ' €'; }

  // ce dont le panier a besoin pour proposer un duo, hors de cette page
  function foldMeta(cols) {
    return { c: cols,
             v: VARIANTS.map(function (v, i) { return { n: v.name, color: v.color, img: GALLERY[i] }; }),
             duo: { nom: 'Tapis pliable The Fold · Duo', prix: 118.80 } };
  }
  function cle(t) { return t.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/\s+/g, '-'); }

  function currentItem() {
    if (state.offer === 3) {
      // meme cle, meme libelle et meme delai que la fiche du rituel : les deux
      // pages alimentent la meme ligne de panier
      var r = state.rit;
      var f = VARIANTS[r.fold].name, bl = BLOC[r.bloc].name, so = SOCKS[r.socks].name;
      return { id: 'rituel-essentiel-' + [f, bl, so].map(cle).join('-'), nom: "Rituel L'Essentiel",
        detail: 'Tapis pliable The Fold ' + f + ' · Bloc de yoga The Block ' + bl + ' · Chaussettes The Socks ' + so,
        prix: 99, imgs: [RAW_ASSET('rituel-essentiel-1.webp')],
        sacs: 1, programme: true, livr: [6, 12, 'c'],
        // memes proprietes de ligne que la fiche du rituel (shop.js)
        shop: { sku: window.RawCart.sku('rituel-essentiel'),
                p: { 'Tapis pliable The Fold': f, 'Bloc de yoga The Block': bl, 'Chaussettes The Socks': so } } };
    }
    if (state.offer === 1) {
      var v = VARIANTS[state.single];
      return { id: 'o1-' + state.single, nom: 'Tapis pliable The Fold', detail: 'Coloris : ' + v.name,
        prix: 69.90, imgs: [GALLERY[state.single]], sw: [v.color],
        sacs: 1, programme: true, livr: FOLD_LIVR, fold: foldMeta([state.single]) };
    }
    return window.RawCart.foldDuo(foldMeta([]), state.duo[0], state.duo[1], FOLD_LIVR);
  }

  function addToCart() { window.RawCart.add(currentItem(), 1); }

  // un duo cree ou modifie depuis le panier se reflete sur la fiche
  window.RawCart.onFold = function (cols) {
    state.offer = 2; state.duo = cols;
    if (offersEl) renderOffers();
  };

  document.querySelectorAll('[data-buy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      addToCart();
      var labelSpan = btn.querySelector('span:not(.btn__price)');
      if (labelSpan) {
        var prev = labelSpan.textContent;
        labelSpan.textContent = 'Ajouté ✓';
        setTimeout(function () { labelSpan.textContent = prev; }, 1400);
      }
    });
  });

  /* ---------- Video placeholder ---------- */
  var video = document.querySelector('[data-video]');
  if (video) {
    video.addEventListener('click', function () {
      video.style.transition = 'opacity .3s';
      video.style.opacity = '.85';
      setTimeout(function () { video.style.opacity = '1'; }, 300);
    });
  }

  /* ---------- Seamless marquees (cities + announcement bar) ---------- */
  // Repeat the content until one group is wider than the screen, then clone it:
  // the -50% translate then loops with no empty gap on any screen size.
  function seamlessMarquee(track, unit, groupClass, speed) {
    if (!track) return;
    var viewport = track.parentElement.offsetWidth;
    var group = document.createElement('div');
    group.className = groupClass;
    group.innerHTML = unit;
    track.innerHTML = '';
    track.appendChild(group);

    var guard = 0;
    while (group.offsetWidth < viewport && guard < 40) { group.innerHTML += unit; guard++; }

    track.appendChild(group.cloneNode(true)); // second identical group -> seamless -50%
    track.style.animationDuration = Math.round(group.offsetWidth / speed) + 's'; // constant visual speed
  }

  function itemsUnit(list) {
    return list.map(function (t) { return '<span>' + t + '</span><i>·</i>'; }).join('');
  }

  /* Bandeau d'annonce : un message a la fois, change toutes les 5 s. Le sortant
     glisse vers le bas, l'entrant arrive par le haut. Meme rendu que shop.js. */
  function rotationAnnonce(track, messages) {
    if (!track) return;
    track.innerHTML = '';
    var items = messages.map(function (t, i) {
      var el = document.createElement('span');
      el.className = 'announce__item' + (i === 0 ? ' is-in' : '');
      el.textContent = t;
      el.setAttribute('aria-hidden', i === 0 ? 'false' : 'true');
      track.appendChild(el);
      return el;
    });
    if (items.length < 2) return;
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
      setTimeout(function () {
        sortant.style.transition = 'none';
        sortant.classList.remove('is-out');
        void sortant.offsetHeight;
        sortant.style.transition = '';
      }, 600);
    }, 5000);
  }
  var citiesTrack = document.querySelector('[data-marquee]');
  var announceTrack = document.querySelector('[data-announce-track]');
  var reviewsTrack = document.querySelector('[data-reviews-track]');
  var reviewsUnit = reviewsTrack ? reviewsTrack.innerHTML : ''; // capture cards once
  var instaTrack = document.querySelector('[data-insta-track]');
  rotationAnnonce(announceTrack,
    ['Livraison offerte', 'Garantie 30 jours', 'Programme yoga offert avec chaque tapis']);

  function buildMarquees() {
    seamlessMarquee(citiesTrack,
      itemsUnit(['Bali', 'Lisbonne', 'Tulum', 'Canggu', 'Tokyo', 'Medellín', 'Chiang Mai', 'Cape Town']),
      'marquee__group', 55);
    // le bandeau d'annonce ne defile plus : il change de message toutes les 5 s
    seamlessMarquee(reviewsTrack, reviewsUnit, 'reviews__group', 55);
    seamlessMarquee(instaTrack, instaUnit(), 'insta__group', 45);
  }

  var mqTimer;
  window.addEventListener('resize', function () {
    clearTimeout(mqTimer);
    mqTimer = setTimeout(buildMarquees, 200);
  });
  if (document.fonts && document.fonts.ready) { document.fonts.ready.then(buildMarquees); }

  /* ---------- Live "watching" counter (random 40–80) ---------- */
  (function () {
    var el = document.querySelector('[data-watching-count]');
    if (!el) return;
    function rand() { return Math.floor(Math.random() * 41) + 40; } // 40–80
    function tick() {
      el.textContent = rand();
      setTimeout(tick, 2500 + Math.random() * 3000); // every 2.5–5.5s
    }
    el.textContent = rand();
    setTimeout(tick, 2500 + Math.random() * 3000);
  })();

  /* ---------- Init ---------- */
  renderGallery();
  renderOffers();
  buildMarquees();
  onScroll();
})();
