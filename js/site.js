/* ============================================================
   BND Construction — shared site behaviour
   ============================================================ */
(function () {
  'use strict';

  var doc = document;
  var root = doc.documentElement;

  /* JS flag: reveal styles only apply when we can undo them, so a
     JS failure never leaves the page blank */
  root.classList.add('js');

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- header: transparent over a dark hero, solid after ---------- */
  var head = doc.querySelector('.head');
  var hero = doc.querySelector('.hero, .phead');

  if (head && !head.classList.contains('head--solid')) {
    var solidAfter = function () {
      var trigger = hero ? Math.min(hero.offsetHeight - 90, 220) : 40;
      if (window.scrollY > trigger) head.classList.add('is-solid');
      else head.classList.remove('is-solid');
    };
    solidAfter();
    window.addEventListener('scroll', solidAfter, { passive: true });
  }

  /* ---------- mobile drawer ---------- */
  var burger = doc.querySelector('.burger');
  var drawer = doc.getElementById('drawer');

  if (burger && drawer) {
    var setDrawer = function (open) {
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      drawer.classList.toggle('is-open', open);
      doc.body.style.overflow = open ? 'hidden' : '';
    };
    burger.addEventListener('click', function () {
      setDrawer(burger.getAttribute('aria-expanded') !== 'true');
    });
    drawer.addEventListener('click', function (e) {
      if (e.target.closest('a')) setDrawer(false);
    });
    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && burger.getAttribute('aria-expanded') === 'true') {
        setDrawer(false);
        burger.focus();
      }
    });
  }

  /* ---------- scroll reveals ---------- */
  var revealables = doc.querySelectorAll('[data-reveal]');

  /* Reveal one element. Grid/list siblings that share a parent and carry no
     authored data-delay get an automatic cascade so rows of cards fan in. */
  function revealEl(el) {
    if (!el.hasAttribute('data-delay') && el.parentNode) {
      var sibs = el.parentNode.children;
      var group = [];
      for (var s = 0; s < sibs.length; s++) {
        if (sibs[s].hasAttribute && sibs[s].hasAttribute('data-reveal')) group.push(sibs[s]);
      }
      if (group.length > 1) {
        var idx = group.indexOf(el);
        if (idx > 0) el.style.transitionDelay = Math.min(idx * 80, 480) + 'ms';
      }
    }
    el.classList.add('is-in');
  }

  function showAll() {
    for (var i = 0; i < revealables.length; i++) revealables[i].classList.add('is-in');
  }

  if (reduce || !('IntersectionObserver' in window)) {
    showAll();
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          revealEl(entry.target);
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.08 });

    for (var j = 0; j < revealables.length; j++) io.observe(revealables[j]);

    /* anything already on screen at load shows immediately (no travel delay) */
    requestAnimationFrame(function () {
      for (var k = 0; k < revealables.length; k++) {
        if (revealables[k].getBoundingClientRect().top < window.innerHeight * 0.9) {
          revealables[k].classList.add('is-in');
          io.unobserve(revealables[k]);
        }
      }
    });
  }

  /* last resort: never leave content hidden */
  window.addEventListener('load', function () { setTimeout(showAll, 1500); });

  /* ---------- scroll progress bar + directional header + media parallax ---------- */
  if (!reduce) {
    /* progress bar */
    var prog = doc.createElement('div');
    prog.className = 'scrollprog';
    doc.body.appendChild(prog);

    /* media to parallax (hero / page-head imagery) */
    var media = doc.querySelectorAll('.hero__media img, .phead__media img');

    var lastY = window.scrollY;
    var ticking = false;

    function onFrame() {
      var y = window.scrollY;
      var docH = doc.documentElement.scrollHeight - window.innerHeight;
      prog.style.width = (docH > 0 ? (y / docH) * 100 : 0) + '%';

      /* header: hide when scrolling down past the hero, reveal on scroll up */
      if (head && !(drawer && drawer.classList.contains('is-open'))) {
        if (y > 260 && y > lastY + 4) head.classList.add('is-hidden');
        else if (y < lastY - 4 || y < 260) head.classList.remove('is-hidden');
      }

      /* subtle parallax — image drifts slower than the page */
      for (var m = 0; m < media.length; m++) {
        var el = media[m];
        var rect = el.getBoundingClientRect();
        if (rect.bottom > 0 && rect.top < window.innerHeight) {
          var mid = rect.top + rect.height / 2 - window.innerHeight / 2;
          el.style.transform = 'translate3d(0,' + (mid * -0.06).toFixed(1) + 'px,0) scale(1.06)';
        }
      }

      lastY = y;
      ticking = false;
    }

    window.addEventListener('scroll', function () {
      if (!ticking) { window.requestAnimationFrame(onFrame); ticking = true; }
    }, { passive: true });
    onFrame();
  }

  /* ---------- current year ---------- */
  var y = doc.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();

/* ============================================================
   Hero background video

   Loaded only when it is actually going to be watched: never on
   small screens, never under reduced-motion, never on a metered
   connection. Sources carry data-src so nothing is fetched until
   we opt in. Falls back to the poster image in every other case.
   ============================================================ */
(function () {
  'use strict';

  var video = document.querySelector('[data-hero-video]');
  if (!video) return;

  /* stays off until a file is actually in place — an enabled-but-missing
     video would fire two 404s on every page load */
  if (video.getAttribute('data-hero-video') !== 'on') return;

  var mqReduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var mqSmall = window.matchMedia('(max-width: 760px)');
  var conn = navigator.connection || {};

  function shouldPlay() {
    return !mqReduce.matches && !mqSmall.matches && !conn.saveData;
  }

  var loaded = false;
  function load() {
    if (loaded || !shouldPlay()) return;
    loaded = true;
    var sources = video.querySelectorAll('source[data-src]');
    for (var i = 0; i < sources.length; i++) {
      sources[i].src = sources[i].getAttribute('data-src');
    }
    video.load();
    var p = video.play();
    if (p && p.catch) p.catch(function () { /* autoplay blocked — poster stays */ });
  }

  video.addEventListener('playing', function () {
    video.classList.add('is-playing');
  });
  /* a missing or unplayable file must never show a broken element */
  video.addEventListener('error', function () {
    video.classList.remove('is-playing');
  }, true);

  if (shouldPlay()) {
    if (document.readyState === 'complete') load();
    else window.addEventListener('load', load);
  }

  /* don't burn cycles decoding video that is scrolled out of view */
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!loaded) return;
        if (e.isIntersecting) { var p = video.play(); if (p && p.catch) p.catch(function () {}); }
        else video.pause();
      });
    }, { threshold: 0.1 }).observe(video);
  }

  /* respond if the user changes their motion preference mid-session */
  if (mqReduce.addEventListener) {
    mqReduce.addEventListener('change', function () {
      if (mqReduce.matches) { video.pause(); video.classList.remove('is-playing'); }
    });
  }
})();
