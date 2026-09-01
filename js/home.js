/* ============================================================
   BND Construction — homepage behaviour
   Kept deliberately small: reveals, drawer, hero video, and the
   cursor-following service image. Everything degrades to a
   working page with JS disabled.
   ============================================================ */
(function () {
  'use strict';
  var doc = document;
  doc.documentElement.classList.add('js');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- mobile drawer ---- */
  var burger = doc.querySelector('.burger'), drawer = doc.getElementById('drawer');
  if (burger && drawer) {
    var set = function (open) {
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      drawer.classList.toggle('open', open);
      doc.body.style.overflow = open ? 'hidden' : '';
    };
    burger.addEventListener('click', function () { set(burger.getAttribute('aria-expanded') !== 'true'); });
    drawer.addEventListener('click', function (e) { if (e.target.closest('a')) set(false); });
    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && burger.getAttribute('aria-expanded') === 'true') { set(false); burger.focus(); }
    });
  }

  /* ---- reveals ---- */
  var targets = doc.querySelectorAll('[data-rise],[data-reveal-img]');
  function showAll() { for (var i = 0; i < targets.length; i++) targets[i].classList.add('seen'); }

  if (reduce || !('IntersectionObserver' in window)) {
    showAll();
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('seen'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.08 });
    for (var j = 0; j < targets.length; j++) io.observe(targets[j]);
    requestAnimationFrame(function () {
      for (var k = 0; k < targets.length; k++) {
        if (targets[k].getBoundingClientRect().top < window.innerHeight) targets[k].classList.add('seen');
      }
    });
  }
  /* never leave content hidden if anything above fails */
  window.addEventListener('load', function () { setTimeout(showAll, 1600); });

  /* ---- hero video: desktop + motion-allowed only ---- */
  var vid = doc.querySelector('[data-hero]');
  if (vid && !reduce && window.matchMedia('(min-width:761px)').matches) {
    var src = vid.querySelector('source[data-src]');
    if (src) {
      src.src = src.getAttribute('data-src');
      vid.load();
      vid.play().then(function () { vid.classList.add('on'); }).catch(function () { /* autoplay blocked: still shows */ });
    }
  }

  /* ---- hero parallax, subtle, rAF-throttled ---- */
  var heroImg = doc.querySelector('.hero__media');
  if (heroImg && !reduce && window.matchMedia('(min-width:900px)').matches) {
    var ticking = false;
    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var y = window.scrollY;
        if (y < window.innerHeight) heroImg.style.transform = 'translate3d(0,' + (y * 0.14) + 'px,0)';
        ticking = false;
      });
    }, { passive: true });
  }

})();
