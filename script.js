/* =========================================================
   RAWSTATE — interactions
   ========================================================= */
(function () {
  'use strict';

  /* ---------- Variant data (strict grayscale palette) ---------- */
  var VARIANTS = [
    { id: 'anthracite', name: 'Fog',    color: '#383b3e', ink: '#ffffff' },
    { id: 'sky',        name: 'Lagoon', color: '#a9cfe3', ink: '#111111' },
    { id: 'rose',       name: 'Dusk',   color: '#ebc7d2', ink: '#111111' }
  ];
  var current = 0;

  /* ---------- Gallery (9 product photos, 1:1, fixed order) ---------- */
  var GALLERY = [
    'assets/mat-grey.webp',   // 1 — tapis gris déplié
    'assets/mat-blue.webp',   // 2 — tapis bleu déplié
    'assets/mat-pink.webp',   // 3 — tapis rose déplié
    'assets/colors.webp',     // 4 — les 3 coloris pliés
    'assets/carousel-sofa.webp',    // 5 — rangé sous le canapé
    'assets/carousel-yoga.webp',    // 6 — pile de tapis rose plié (+ tapis bleu)
    'assets/carousel-stack.webp',   // 7 — pile de tapis pliés (à offrir)
    'assets/carousel-texture.webp', // 8 — texture & avantages
    'assets/dimensions.webp'  // 9 — dimensions
  ];

  var mainEl = document.querySelector('[data-gallery-main]');
  var stageEl = document.querySelector('[data-gallery-stage]');
  var thumbsEl = document.querySelector('[data-gallery-thumbs]');
  var activeThumb = 0;

  function imgTag(src) {
    return '<img src="' + src + '" alt="Rawstate The Fold" loading="lazy" />';
  }
  function renderGallery() {
    thumbsEl.innerHTML = GALLERY.map(function (src, i) {
      return '<button class="gallery__thumb' + (i === activeThumb ? ' is-active' : '') +
        '" data-thumb="' + i + '" aria-label="Vue ' + (i + 1) + '">' + imgTag(src) + '</button>';
    }).join('');
    setMain(activeThumb);
  }
  function setMain(i) {
    activeThumb = i;
    stageEl.innerHTML = '<div class="fade" style="width:100%;height:100%">' + imgTag(GALLERY[i]) + '</div>';
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
    2: { now: '118,80 €', old: '139,80 €' }
  };

  var state = { offer: 2, single: 0, duo: [0, 1] };

  function swatchBtns(selected) {
    return VARIANTS.map(function (v, i) {
      return '<button type="button" class="swatch' + (i === selected ? ' is-active' : '') +
        '" aria-label="' + v.name + '" data-idx="' + i + '" style="background:' + v.color +
        ';border-color:' + v.color + '"></button>';
    }).join('');
  }
  function pickRow(group, label, selected) {
    return '<div class="pick-row" data-group="' + group + '">' +
      '<div class="pick-row__label">' + label + ' — <span>' + VARIANTS[selected].name + '</span></div>' +
      '<div class="pick-row__swatches">' + swatchBtns(selected) + '</div></div>';
  }

  function renderOffers() {
    offersEl.querySelector('[data-pick="single"]').innerHTML =
      pickRow('single', 'Couleur', state.single);
    offersEl.querySelector('[data-pick="duo"]').innerHTML =
      pickRow('duo0', 'Tapis 1', state.duo[0]) + pickRow('duo1', 'Tapis 2', state.duo[1]);

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
      stickyVariant.textContent = (state.offer === 1 ? '1 tapis · ' : '2 tapis · ') + p.now;
    }
  }

  offersEl.addEventListener('click', function (e) {
    var sw = e.target.closest('.swatch');
    if (sw) {
      var idx = parseInt(sw.getAttribute('data-idx'), 10);
      var group = sw.closest('.pick-row').getAttribute('data-group');
      state.offer = parseInt(sw.closest('.offer').getAttribute('data-offer'), 10);
      if (group === 'single') state.single = idx;
      else if (group === 'duo0') state.duo[0] = idx;
      else if (group === 'duo1') state.duo[1] = idx;
      renderOffers();
      setMain(idx); // jump gallery to the chosen colour (grey/blue/pink = index 0/1/2)
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

  document.querySelectorAll('[data-ico]').forEach(function (el) {
    var name = el.getAttribute('data-ico');
    if (ICONS[name]) {
      el.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">' + ICONS[name] + '</svg>';
    }
  });

  /* ---------- Délai de livraison estimé (temps réel : +6 à +8 jours ouvrés) ---------- */
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
    var d1 = addBusinessDays(today, 6);
    var d2 = addBusinessDays(today, 8);
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
    'assets/insta-home.webp', 'assets/insta-suitcase.webp', 'assets/insta-studio.webp',
    'assets/insta-shelf.webp', 'assets/insta-rooftop.webp', 'assets/insta-gift.webp'
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

  /* ---------- Cart ---------- */
  var cart = [];
  var cartEl = document.querySelector('[data-cart]');
  var cartOverlay = document.querySelector('[data-cart-overlay]');
  var cartItemsEl = document.querySelector('[data-cart-items]');
  var cartEmptyEl = document.querySelector('[data-cart-empty]');
  var cartTotalEl = document.querySelector('[data-cart-total]');
  var cartSubtotalEl = document.querySelector('[data-cart-subtotal]');
  var cartShippingEl = document.querySelector('[data-cart-shipping]');
  var cartCountEl = document.querySelector('[data-cart-count]');
  var cartCountLabelEl = document.querySelector('[data-cart-count-label]');
  var cartToggle = document.querySelector('[data-cart-toggle]');
  var cartClose = document.querySelector('[data-cart-close]');
  var upsellEl = document.querySelector('[data-upsell]');

  function eur(n) { return n.toFixed(2).replace('.', ',') + ' €'; }

  function currentItem() {
    if (state.offer === 1) {
      return { id: 'o1-' + state.single, name: 'Rawstate The Fold',
        detail: 'Coloris : ' + VARIANTS[state.single].name, price: 69.90, colors: [state.single] };
    }
    return { id: 'o2-' + state.duo[0] + '-' + state.duo[1], name: 'Rawstate The Fold · Duo',
      detail: VARIANTS[state.duo[0]].name + ' + ' + VARIANTS[state.duo[1]].name, price: 118.80,
      colors: [state.duo[0], state.duo[1]] };
  }

  function renderCart() {
    var count = cart.reduce(function (s, i) { return s + i.qty; }, 0);
    var subtotal = cart.reduce(function (s, i) { return s + i.price * i.qty; }, 0);
    var shipping = 0; // livraison toujours offerte
    var total = subtotal + shipping;

    if (cartCountEl) { cartCountEl.textContent = count; cartCountEl.hidden = count === 0; }
    if (cartCountLabelEl) cartCountLabelEl.textContent = count + ' article' + (count > 1 ? 's' : '');
    if (cartEmptyEl) cartEmptyEl.style.display = count ? 'none' : 'block';
    if (cartItemsEl) {
      cartItemsEl.innerHTML = cart.map(function (i) {
        var cols = i.colors || [];
        var media = cols.map(function (ci) {
          return '<img src="' + GALLERY[ci] + '" alt="Tapis Rawstate ' + VARIANTS[ci].name + '" loading="lazy" />';
        }).join('');
        var swatches = cols.map(function (ci) {
          return '<span class="cart-swatch" style="background:' + VARIANTS[ci].color + '"></span>';
        }).join('');
        // Ligne duo : sélecteur de coloris pour le 2e tapis
        var secondSwitch = '';
        if (cols.length === 2) {
          var opts = VARIANTS.map(function (v, ci) {
            return '<button type="button" class="cart-item__sw' + (ci === cols[1] ? ' is-on' : '') +
              '" data-set-second="' + ci + '" style="background:' + v.color +
              '" aria-label="2e tapis : ' + v.name + '" title="' + v.name + '"></button>';
          }).join('');
          secondSwitch = '<div class="cart-item__switch"><span class="cart-item__switch-lbl">2ᵉ&nbsp;tapis&nbsp;:</span>' + opts + '</div>';
        }
        return '<div class="cart-item" data-id="' + i.id + '">' +
          '<div class="cart-item__media">' + media + '</div>' +
          '<div class="cart-item__info"><strong>' + i.name + '</strong>' +
          '<span class="cart-item__colors">' + swatches + i.detail + '</span>' +
          secondSwitch +
          '<div class="cart-item__qty"><button data-dec aria-label="Moins">−</button><span>' + i.qty + '</span><button data-inc aria-label="Plus">+</button></div>' +
          '</div>' +
          '<div class="cart-item__right"><span class="cart-item__price">' + eur(i.price * i.qty) + '</span>' +
          '<button class="cart-item__remove" data-remove>Retirer</button></div></div>';
      }).join('');
    }

    // Upsell duo : visible seulement si un "1 tapis" est présent
    var hasSingle = cart.some(function (i) { return i.id.indexOf('o1-') === 0; });
    if (upsellEl) upsellEl.hidden = !hasSingle;

    if (cartSubtotalEl) cartSubtotalEl.textContent = eur(subtotal);
    if (cartShippingEl) {
      if (shipping === 0) {
        cartShippingEl.textContent = subtotal > 0 ? 'Offerte' : '—';
        cartShippingEl.classList.toggle('is-free', subtotal > 0);
      } else {
        cartShippingEl.textContent = eur(shipping);
        cartShippingEl.classList.remove('is-free');
      }
    }
    if (cartTotalEl) cartTotalEl.textContent = eur(total);
  }

  function openCart() {
    if (!cartEl) return;
    cartEl.classList.add('is-open'); cartEl.setAttribute('aria-hidden', 'false');
    if (cartOverlay) cartOverlay.classList.add('is-open');
  }
  function closeCart() {
    if (!cartEl) return;
    cartEl.classList.remove('is-open'); cartEl.setAttribute('aria-hidden', 'true');
    if (cartOverlay) cartOverlay.classList.remove('is-open');
  }

  function addToCart() {
    var it = currentItem();
    var found = null;
    for (var k = 0; k < cart.length; k++) { if (cart[k].id === it.id) { found = cart[k]; break; } }
    if (found) found.qty += 1;
    else cart.push({ id: it.id, name: it.name, detail: it.detail, price: it.price, qty: 1, colors: it.colors });
    renderCart();
    openCart();
  }

  /* Upsell : convertit un "1 tapis" en pack duo (-21 €). Le client choisit
     le coloris du 2e tapis ; le 1er garde celui du tapis déjà au panier. */
  function upsellToDuo(secondColor) {
    var idx = -1;
    for (var k = 0; k < cart.length; k++) { if (cart[k].id.indexOf('o1-') === 0) { idx = k; break; } }
    if (idx < 0) return;
    var single = cart[idx];
    var c = parseInt(single.id.slice(3), 10);          // coloris du 1er tapis
    if (secondColor == null) secondColor = c;          // sécurité
    single.qty -= 1;                                    // retire une unité du single
    if (single.qty <= 0) cart.splice(idx, 1);
    var duoId = 'o2-' + c + '-' + secondColor;
    var existing = cart.filter(function (x) { return x.id === duoId; })[0];
    if (existing) existing.qty += 1;
    else cart.push({ id: duoId, name: 'Rawstate The Fold · Duo',
      detail: VARIANTS[c].name + ' + ' + VARIANTS[secondColor].name, price: 118.80, qty: 1, colors: [c, secondColor] });
    state.offer = 2; state.duo = [c, secondColor];      // reflète le choix sur la page
    renderCart();
    if (offersEl) renderOffers();
    openCart();
  }
  /* Change le coloris du 2e tapis d'une ligne duo, directement dans le panier. */
  function changeSecondColor(id, newColor) {
    var it = cart.filter(function (x) { return x.id === id; })[0];
    if (!it || !it.colors || it.colors.length < 2) return;
    var c1 = it.colors[0];
    var newId = 'o2-' + c1 + '-' + newColor;
    if (newId === id) return;
    var target = cart.filter(function (x) { return x.id === newId; })[0];
    if (target && target !== it) {           // même duo déjà présent → fusion des quantités
      target.qty += it.qty;
      cart = cart.filter(function (x) { return x !== it; });
    } else {
      it.id = newId; it.colors = [c1, newColor];
      it.detail = VARIANTS[c1].name + ' + ' + VARIANTS[newColor].name;
    }
    state.duo = [c1, newColor];              // reflète le choix sur la fiche produit
    renderCart();
    if (offersEl) renderOffers();
  }

  var upsellSwatchesEl = document.querySelector('[data-upsell-swatches]');
  if (upsellSwatchesEl) {
    upsellSwatchesEl.innerHTML = VARIANTS.map(function (v, i) {
      return '<button type="button" class="cart-upsell__sw" data-color="' + i + '" style="background:' + v.color +
        '" aria-label="Coloris ' + v.name + '" title="' + v.name + '"></button>';
    }).join('');
    upsellSwatchesEl.addEventListener('click', function (e) {
      var b = e.target.closest('[data-color]');
      if (b) upsellToDuo(parseInt(b.getAttribute('data-color'), 10));
    });
  }

  if (cartItemsEl) {
    cartItemsEl.addEventListener('click', function (e) {
      var row = e.target.closest('[data-id]');
      if (!row) return;
      var id = row.getAttribute('data-id');
      var item = cart.filter(function (i) { return i.id === id; })[0];
      if (!item) return;
      var sw = e.target.closest('[data-set-second]');
      if (sw) { changeSecondColor(id, parseInt(sw.getAttribute('data-set-second'), 10)); return; }
      if (e.target.closest('[data-inc]')) item.qty += 1;
      else if (e.target.closest('[data-dec]')) { item.qty -= 1; if (item.qty <= 0) cart = cart.filter(function (i) { return i.id !== id; }); }
      else if (e.target.closest('[data-remove]')) cart = cart.filter(function (i) { return i.id !== id; });
      else return;
      renderCart();
    });
  }

  if (cartToggle) cartToggle.addEventListener('click', openCart);
  if (cartClose) cartClose.addEventListener('click', closeCart);
  if (cartOverlay) cartOverlay.addEventListener('click', closeCart);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeCart(); });

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
  var citiesTrack = document.querySelector('[data-marquee]');
  var announceTrack = document.querySelector('[data-announce-track]');
  var reviewsTrack = document.querySelector('[data-reviews-track]');
  var reviewsUnit = reviewsTrack ? reviewsTrack.innerHTML : ''; // capture cards once
  var instaTrack = document.querySelector('[data-insta-track]');

  function buildMarquees() {
    seamlessMarquee(citiesTrack,
      itemsUnit(['Bali', 'Lisbonne', 'Tulum', 'Canggu', 'Tokyo', 'Medellín', 'Chiang Mai', 'Cape Town']),
      'marquee__group', 55);
    seamlessMarquee(announceTrack,
      itemsUnit(['30 cm plié', '700 g', 'Retour 30 jours']),
      'announce__group', 45);
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
  renderCart();
  buildMarquees();
  onScroll();
})();
