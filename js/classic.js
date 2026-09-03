/* ============================================================
   BND Construction — "Classic" direction
   ============================================================ */
(function () {
  'use strict';

  var doc = document;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  doc.documentElement.classList.add('js');

  /* ---------- page load ----------
     Gates the hero entrance only. There is no preloader and nothing waits
     on this: the page is interactive from first paint, this just lets the
     photograph settle rather than snapping in. */
  function markLoaded() {
    /* On a warm reload readyState is already 'complete', so adding the
       class here would land in the SAME frame as first paint - the start
       state never gets painted and the browser has nothing to transition
       from, which makes the hero look static on every refresh. Two frames
       guarantees the opacity:0 / scale(1.05) state is on screen first. */
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { doc.documentElement.classList.add('is-loaded'); });
    });
  }
  if (doc.readyState === 'complete') markLoaded();
  else window.addEventListener('load', markLoaded);
  /* a slow hero image must never hold the headline hostage */
  setTimeout(markLoaded, 1200);

  /* ---------- stagger card groups ----------
     Delay is carried by data-i in CSS. Rather than hand-tagging every
     card, walk the known groups and number their children. Grids longer
     than eight cycle 1-4, so each ROW steps instead of the last card
     waiting on the whole first row. */
  (function stagger() {
    var groups = doc.querySelectorAll('.cards,.pods,.grid4,.hilite');
    for (var g = 0; g < groups.length; g++) {
      var kids = groups[g].children, n = 0, wide = kids.length > 8;
      for (var i = 0; i < kids.length; i++) {
        if (!kids[i].hasAttribute('data-up')) continue;
        /* position in the group wins over any hand-authored data-i: those
           were an ad-hoc 0,1,2 that collides with a clean sequence */
        kids[i].setAttribute('data-i', String(wide ? (n % 4) + 1 : Math.min(n + 1, 8)));
        n++;
      }
    }
  })();

  /* ---------- scroll reveals ---------- */
  var ups = doc.querySelectorAll('[data-up]');
  function showAll() { for (var i = 0; i < ups.length; i++) ups[i].classList.add('on'); }

  if (!('IntersectionObserver' in window) || reduce) {
    showAll();
  } else {
    var io = new IntersectionObserver(function (es) {
      for (var i = 0; i < es.length; i++) {
        if (!es[i].isIntersecting) continue;
        es[i].target.classList.add('on');
        io.unobserve(es[i].target);
      }
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });

    /* Observation starts two frames late, on purpose. Anything already in
       view intersects immediately, and on a warm reload that callback can
       land in the same frame as first paint - the start state is never
       painted, so there is nothing to transition from and the hero looks
       static. Two frames costs ~32ms and guarantees the motion is seen. */
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        for (var j = 0; j < ups.length; j++) io.observe(ups[j]);
        queueSweep();
      });
    });

    /* Safety net, not a bypass.
       This used to be a blanket showAll() on a 2.8s timer, which revealed
       the WHOLE page two seconds after load - so everything below the fold
       was already on screen before the reader ever scrolled to it, and no
       scroll reveal was ever actually seen. The net now only ever reveals
       what is genuinely in view, so a failed observer still cannot leave
       content invisible, but nothing is revealed ahead of the reader. */
    var sweeping = false;
    function sweep() {
      sweeping = false;
      var vh = window.innerHeight;
      for (var k = 0; k < ups.length; k++) {
        var el = ups[k];
        if (el.classList.contains('on')) continue;
        var r = el.getBoundingClientRect();
        if (r.top < vh * 0.92 && r.bottom > 0) { el.classList.add('on'); io.unobserve(el); }
      }
    }
    function queueSweep() {
      if (!sweeping) { sweeping = true; requestAnimationFrame(sweep); }
    }
    window.addEventListener('scroll', queueSweep, { passive: true });
    window.addEventListener('resize', queueSweep, { passive: true });
  }

  /* ---------- statistics ----------
     Counts the digits up once, the first time the block is seen. Values
     are read from the markup and never invented: anything without a
     number in it (OSHA) is skipped, and whatever surrounds the digits -
     a "+", a comma - is put back exactly as authored. */
  (function counters() {
    if (reduce || !('IntersectionObserver' in window)) return;
    var els = doc.querySelectorAll('.figs__k');
    var live = [];
    for (var i = 0; i < els.length; i++) {
      var m = /^(\D*)(\d[\d,]*)(\D*)$/.exec(els[i].textContent.trim());
      if (!m) continue;
      live.push({
        el: els[i], pre: m[1], post: m[3],
        to: parseInt(m[2].replace(/,/g, ''), 10),
        grouped: m[2].indexOf(',') > -1
      });
    }
    if (!live.length) return;

    function paint(s, v) {
      s.el.textContent = s.pre + (s.grouped ? v.toLocaleString('en-US') : v) + s.post;
    }
    function run(s) {
      var dur = 1300, t0 = 0;
      function frame(t) {
        if (!t0) t0 = t;
        var p = Math.min((t - t0) / dur, 1);
        paint(s, Math.round(s.to * (1 - Math.pow(1 - p, 3))));
        if (p < 1) requestAnimationFrame(frame);
        else paint(s, s.to);            /* land exactly on the authored value */
      }
      requestAnimationFrame(frame);
    }

    var cio = new IntersectionObserver(function (es) {
      for (var i = 0; i < es.length; i++) {
        if (!es[i].isIntersecting) continue;
        cio.unobserve(es[i].target);
        for (var k = 0; k < live.length; k++) {
          if (live[k].el === es[i].target && !live[k].done) { live[k].done = true; run(live[k]); }
        }
      }
    }, { threshold: 0.5 });

    for (var j = 0; j < live.length; j++) {
      /* already on screen at load: leave the real number alone rather than
         blanking it to zero in front of the reader */
      if (live[j].el.getBoundingClientRect().top < window.innerHeight) { live[j].done = true; continue; }
      paint(live[j], 0);
      cio.observe(live[j].el);
    }
    /* if the observer never fires, the number must not be left at zero */
    setTimeout(function () {
      for (var q = 0; q < live.length; q++) if (!live[q].done) { live[q].done = true; paint(live[q], live[q].to); }
    }, 4000);
  })();

  /* ---------- parallax ----------
     Two images only. Both sit in an overflow:hidden parent and are scaled
     up in CSS by more than the travel, so the shift cannot expose an edge.
     Fine pointers and wide viewports only; the handler is rAF-throttled
     and only measures elements currently in view. */
  (function parallax() {
    if (reduce || !('IntersectionObserver' in window)) return;
    if (!(window.matchMedia && window.matchMedia('(pointer:fine)').matches)) return;
    if (window.innerWidth < 761) return;

    var imgs = doc.querySelectorAll('.band__media img,.shot__main img');
    if (!imgs.length) return;
    for (var i = 0; i < imgs.length; i++) imgs[i].setAttribute('data-par', '');

    var vis = [], ticking = false, MAX = 8;
    function queue() { if (!ticking) { ticking = true; requestAnimationFrame(apply); } }
    function apply() {
      ticking = false;
      var h = window.innerHeight;
      for (var i = 0; i < vis.length; i++) {
        var r = vis[i].getBoundingClientRect();
        var mid = (r.top + r.height / 2 - h / 2) / h;
        vis[i].style.setProperty('--par', (Math.max(-1, Math.min(1, mid)) * MAX).toFixed(1) + 'px');
      }
    }
    var pio = new IntersectionObserver(function (es) {
      for (var i = 0; i < es.length; i++) {
        var at = vis.indexOf(es[i].target);
        if (es[i].isIntersecting) { if (at < 0) vis.push(es[i].target); }
        else if (at > -1) vis.splice(at, 1);
      }
      if (vis.length) queue();
    }, { rootMargin: '12% 0px' });
    for (var k = 0; k < imgs.length; k++) pio.observe(imgs[k]);

    window.addEventListener('scroll', queue, { passive: true });
    window.addEventListener('resize', queue, { passive: true });
    apply();
  })();

  /* ---------- sticky nav shadow ---------- */
  var bar = doc.getElementById('bar');
  if (bar) {
    var stuck = false;
    var onScroll = function () {
      var should = window.scrollY > 50;
      if (should !== stuck) { stuck = should; bar.classList.toggle('is-stuck', stuck); }
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- mobile sheet ---------- */
  var sheet = doc.getElementById('sheet');
  var openBtn = doc.querySelector('[data-open]');

  if (sheet && openBtn) {
    var last = null;

    function setSheet(open) {
      if (open) {
        last = doc.activeElement;
        /* removing [hidden] makes the panel displayed and focusable in the
           same tick, so focus is deterministic rather than a frame race */
        sheet.hidden = false;
        var first = sheet.querySelector('a');
        if (first) first.focus();
        requestAnimationFrame(function () { sheet.classList.add('is-open'); });
      } else {
        sheet.classList.remove('is-open');
        setTimeout(function () { sheet.hidden = true; }, 320);
        if (last) last.focus();
      }
      openBtn.setAttribute('aria-expanded', String(open));
      doc.body.classList.toggle('is-locked', open);
    }

    openBtn.addEventListener('click', function () { setSheet(true); });

    var closers = sheet.querySelectorAll('[data-close], a');
    for (var c = 0; c < closers.length; c++) {
      closers[c].addEventListener('click', function () { setSheet(false); });
    }

    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && sheet.classList.contains('is-open')) setSheet(false);
    });

    /* keep Tab inside the panel while it is open */
    sheet.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab' || !sheet.classList.contains('is-open')) return;
      var f = sheet.querySelectorAll('a[href], button');
      if (!f.length) return;
      var first = f[0], lastEl = f[f.length - 1];
      if (e.shiftKey && doc.activeElement === first) { e.preventDefault(); lastEl.focus(); }
      else if (!e.shiftKey && doc.activeElement === lastEl) { e.preventDefault(); first.focus(); }
    });
  }

  /* ---------- hero footage ----------
     The still carries first paint. Footage loads once the page has
     settled, never on reduced motion or a metered connection. */
  var video = doc.querySelector('[data-hero]');
  if (video) {
    var conn = navigator.connection || {};
    if (!reduce && !conn.saveData && !/2g/.test(conn.effectiveType || '')) {
      window.addEventListener('load', function () {
        setTimeout(function () {
          var src = video.querySelector('source[data-src]');
          if (!src) return;
          src.src = src.getAttribute('data-src');
          video.load();
          var pr = video.play();
          if (pr && pr.catch) pr.catch(function () { /* blocked — the still stands */ });
        }, 700);
      });
    }
  }

  /* ---------- enquiry form ----------
     FormSubmit answers HTTP 200 even when it REJECTS a submission — an
     unactivated inbox returns {success:"false"} and the enquiry is
     dropped. Trust the body, never the status code. */
  var form = doc.querySelector('[data-form]');
  if (!form) return;

  var msg = form.querySelector('[data-form-msg]');
  var button = form.querySelector('button[type="submit"]');
  /* take the destination from the form's own action so routing lives in one
     place — a hardcoded copy here silently outlives the markup */
  var INBOX = (form.getAttribute('action') || '').split('/').pop();

  function say(text, state) {
    if (!msg) return;
    msg.textContent = text;
    if (state) msg.setAttribute('data-state', state); else msg.removeAttribute('data-state');
  }
  function fail(text, id) {
    say(text, 'err');
    var el = doc.getElementById(id);
    if (el) el.focus();
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var v = function (id) { var el = doc.getElementById(id); return el ? (el.value || '').trim() : ''; };

    if (!v('q-name')) return fail('Add your name.', 'q-name');
    var email = v('q-email');
    if (!email) return fail('Add an email address.', 'q-email');
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
      return fail('That email doesn’t look right. Check it and try again.', 'q-email');
    }
    /* the form carries novalidate for the AJAX path, so the topic and the
       message are checked here rather than by the browser */
    if (!form.querySelector('input[name="About"]:checked')) {
      say('Pick what your message is about.', 'err');
      var chip = form.querySelector('input[name="About"]');
      if (chip) chip.focus();
      return;
    }
    if (!v('q-msg')) return fail('Add a message.', 'q-msg');

    if (button) button.disabled = true;
    say('Sending…');

    var payload = {};
    new FormData(form).forEach(function (val, key) {
      if (key === '_honey') return;
      if (val) payload[key] = val;
    });

    fetch('https://formsubmit.co/ajax/' + INBOX, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(payload)
    })
      .then(function (res) { return res.json(); })
      .then(function (d) {
        var ok = d && (d.success === true || d.success === 'true');
        if (!ok) throw new Error((d && d.message) || 'rejected');
        form.reset();
        say('Thanks — your enquiry is with estimating. We’ll come back to you shortly.', 'ok');
      })
      .catch(function () {
        say('That didn’t send. Please email ' + INBOX + ' directly.', 'err');
      })
      .then(function () { if (button) button.disabled = false; });
  });
})();

/* ============================================================
   Portfolio filter — appended so it runs on the portfolio page
   only; every other page simply has no [data-filter-group].
   ============================================================ */
(function () {
  'use strict';

  var group = document.querySelector('[data-filter-group]');
  if (!group) return;

  var buttons = group.querySelectorAll('[data-filter]');
  var cards = document.querySelectorAll('#pgrid [data-market]');
  var list = document.getElementById('plist');
  var rows = list ? list.querySelectorAll('[data-market]') : [];

  function apply(market) {
    var shownInList = 0;

    for (var i = 0; i < cards.length; i++) {
      var show = market === 'all' || cards[i].getAttribute('data-market') === market;
      cards[i].hidden = !show;
    }
    for (var j = 0; j < rows.length; j++) {
      /* the text list only makes sense inside one market — showing every
         un-photographed project under "All work" reads as missing images */
      var showRow = market !== 'all' && rows[j].getAttribute('data-market') === market;
      rows[j].hidden = !showRow;
      if (showRow) shownInList++;
    }
    if (list) list.hidden = shownInList === 0;

    for (var k = 0; k < buttons.length; k++) {
      buttons[k].setAttribute('aria-pressed',
        String(buttons[k].getAttribute('data-filter') === market));
    }
  }

  for (var b = 0; b < buttons.length; b++) {
    (function (btn) {
      btn.addEventListener('click', function () { apply(btn.getAttribute('data-filter')); });
    })(buttons[b]);
  }

  /* deep link: portfolio.html?market=Retail */
  var q = new URLSearchParams(window.location.search).get('market');
  if (q) {
    for (var m = 0; m < buttons.length; m++) {
      if (buttons[m].getAttribute('data-filter') === q) { apply(q); break; }
    }
  }
})();

/* ============================================================
   Services accordion. Every panel ships open so the page reads
   fully without JS; this collapses all but one and takes over.
   ============================================================ */
(function () {
  'use strict';

  var acc = document.querySelector('[data-acc]');
  if (!acc) return;

  var items = [].slice.call(acc.querySelectorAll('.acc__i'));
  var shots = acc.querySelectorAll('.acc__shot');
  if (!items.length) return;

  function setOpen(item, open) {
    var btn = item.querySelector('.acc__hd');
    var panel = item.querySelector('.acc__p');
    item.classList.toggle('is-open', open);
    btn.setAttribute('aria-expanded', String(open));
    /* inert keeps a collapsed panel out of the tab order and the
       accessibility tree — grid-rows:0fr only hides it visually */
    if (open) panel.removeAttribute('inert');
    else panel.setAttribute('inert', '');

    if (open) {
      var n = parseInt(item.getAttribute('data-shot'), 10);
      for (var s = 0; s < shots.length; s++) shots[s].classList.toggle('is-on', s === n);
    }
  }

  function openOnly(item) {
    for (var i = 0; i < items.length; i++) setOpen(items[i], items[i] === item);
  }

  items.forEach(function (item) {
    item.querySelector('.acc__hd').addEventListener('click', function () {
      /* keep one open: clicking the open row leaves it open rather than
         collapsing to nothing, which would empty the image panel */
      if (!item.classList.contains('is-open')) openOnly(item);
    });
  });

  /* deep links from the homepage service cards land on #tenant-finish-out etc. */
  function fromHash() {
    var id = window.location.hash.replace('#', '');
    if (!id) return null;
    for (var i = 0; i < items.length; i++) if (items[i].id === id) return items[i];
    return null;
  }

  openOnly(fromHash() || items[0]);

  window.addEventListener('hashchange', function () {
    var target = fromHash();
    if (target) openOnly(target);
  });
})();

/* ============================================================
   Estimate dialog. The trigger links point at the estimate page,
   so with no JS — or no <dialog> support — they simply navigate.
   ============================================================ */
(function () {
  'use strict';

  var modal = document.getElementById('estimate-modal');
  if (!modal || typeof modal.showModal !== 'function') return;

  var triggers = document.querySelectorAll('a[href$="request-an-estimate.html"]');
  if (!triggers.length) return;

  for (var i = 0; i < triggers.length; i++) {
    triggers[i].addEventListener('click', function (e) {
      /* let modified clicks open the page in a new tab as usual */
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
      e.preventDefault();
      modal.showModal();
      var first = modal.querySelector('input, select, textarea');
      if (first) first.focus();
    });
  }

  /* click the backdrop to dismiss — the dialog itself fills only part of it */
  modal.addEventListener('click', function (e) {
    if (e.target === modal) modal.close();
  });
})();

/* ============================================================
   Native forms that stay in place.
   A required file cannot go over FormSubmit's AJAX endpoint, so
   these post for real — into a hidden iframe, so the page never
   navigates. Success is confirmed by the iframe reaching our own
   redirect target: if it is still on formsubmit.co the read
   throws, and FormSubmit answers 200 even when it rejects, so a
   blind "thank you" would lie about discarded submissions.
   ============================================================ */
(function () {
  'use strict';

  var forms = document.querySelectorAll('form[data-native]');
  var sink = document.querySelector('iframe[name="bnd-sink"]');
  if (!forms.length || !sink) return;

  var pending = null;

  function say(form, text, state) {
    var msg = form.querySelector('[data-form-msg]');
    if (!msg) return;
    msg.textContent = text;
    if (state) msg.setAttribute('data-state', state);
    else msg.removeAttribute('data-state');
  }

  for (var i = 0; i < forms.length; i++) {
    (function (form) {
      form.addEventListener('submit', function () {
        /* the browser has already run native validation by this point */
        pending = form;
        var btn = form.querySelector('button[type="submit"]');
        if (btn) btn.disabled = true;
        say(form, 'Sending…');
      });
    })(forms[i]);
  }

  sink.addEventListener('load', function () {
    if (!pending) return;                     /* the initial about:blank load */
    var form = pending;
    pending = null;

    var btn = form.querySelector('button[type="submit"]');
    if (btn) btn.disabled = false;

    var landed = false;
    try {
      /* readable only once the iframe is back on our own origin */
      landed = /form-ok\.html/.test(sink.contentWindow.location.pathname);
    } catch (err) {
      landed = false;                          /* still cross-origin */
    }

    if (landed) {
      form.reset();
      say(form, 'Thank you — your request is in. Estimating will come back to you shortly.', 'ok');
    } else {
      say(form, 'That didn’t send. Please email estimating@bnd-co.com directly.', 'err');
    }
  });
})();

/* ============================================================
   Pre-qualification wizard.
   `required` is held as data-req and only promoted to the real
   attribute on the visible step — a required control inside a
   hidden fieldset makes the browser refuse to submit and log
   "not focusable", with nothing shown to the person filling it.
   ============================================================ */
(function () {
  'use strict';

  var wiz = document.querySelector('[data-wiz]');
  if (!wiz) return;

  var steps = [].slice.call(wiz.querySelectorAll('.wiz__step'));
  var bar = wiz.querySelector('[data-wiz-bar]');
  var now = wiz.querySelector('[data-wiz-now]');
  var back = wiz.querySelector('[data-wiz-back]');
  var next = wiz.querySelector('[data-wiz-next]');
  var send = wiz.querySelector('[data-wiz-send]');
  var msg = wiz.querySelector('[data-form-msg]');
  var at = 0;

  function setRequired(step, on) {
    var fields = step.querySelectorAll('[data-req]');
    for (var i = 0; i < fields.length; i++) {
      if (on) fields[i].setAttribute('required', '');
      else fields[i].removeAttribute('required');
    }
  }

  function show(i) {
    setRequired(steps[at], false);
    at = i;
    for (var s = 0; s < steps.length; s++) steps[s].hidden = s !== at;
    setRequired(steps[at], true);

    bar.style.width = ((at + 1) / steps.length * 100) + '%';
    now.textContent = String(at + 1);
    back.disabled = at === 0;
    next.hidden = at === steps.length - 1;
    send.hidden = at !== steps.length - 1;
    if (msg) { msg.textContent = ''; msg.removeAttribute('data-state'); }
  }

  function valid(step) {
    var fields = step.querySelectorAll('input, select, textarea');
    for (var i = 0; i < fields.length; i++) {
      if (!fields[i].checkValidity()) { fields[i].reportValidity(); return false; }
    }
    /* radio groups carry their requirement on the wrapper */
    var groups = step.querySelectorAll('.chips[data-required]');
    for (var g = 0; g < groups.length; g++) {
      if (!groups[g].querySelector('input:checked')) {
        var label = document.getElementById(groups[g].getAttribute('aria-labelledby'));
        if (msg) {
          msg.textContent = 'Choose an option for “' +
            (label ? label.textContent.replace('*', '').trim() : 'this question') + '”.';
          msg.setAttribute('data-state', 'err');
        }
        var first = groups[g].querySelector('input');
        if (first) first.focus();
        return false;
      }
    }
    return true;
  }

  next.addEventListener('click', function () {
    if (!valid(steps[at])) return;
    show(at + 1);
    wiz.scrollIntoView({ block: 'start', behavior: 'smooth' });
  });

  back.addEventListener('click', function () {
    show(at - 1);
    wiz.scrollIntoView({ block: 'start', behavior: 'smooth' });
  });

  wiz.addEventListener('submit', function (e) {
    if (!valid(steps[at])) { e.preventDefault(); return; }
  });

  show(0);
})();

/* ============================================================
   Hero slideshow. Crossfades four projects; holds on the first
   under reduced motion, and pauses while the tab is hidden so
   it is not decoding images nobody is looking at.
   ============================================================ */
(function () {
  'use strict';

  var stage = document.querySelector('[data-slides]');
  if (!stage) return;

  var slides = stage.querySelectorAll('[data-slide]');
  if (slides.length < 2) return;

  /* Slides 2-n ship without a src: at opacity 0 they are invisible, but
     loading them eagerly put ~1.3MB on the wire in front of the hero image
     and pushed LCP past six seconds. Hydrate once the page has loaded, long
     before the first rotation at 6s. If this never runs, slide one still
     shows and the hero is simply static. */
  function hydrate() {
    for (var i = 0; i < slides.length; i++) {
      var el = slides[i];
      if (el.dataset.srcset && !el.srcset) el.srcset = el.dataset.srcset;
      if (el.dataset.src && !el.getAttribute('src')) el.src = el.dataset.src;
    }
  }
  if (document.readyState === 'complete') hydrate();
  else window.addEventListener('load', hydrate);


  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var timer = null;

  function step() {
    /* read the live index rather than trusting a counter — if anything else
       touches the classes, a stale counter leaves two slides visible at once */
    var at = 0;
    for (var i = 0; i < slides.length; i++) {
      if (slides[i].classList.contains('is-on')) { at = i; break; }
    }
    for (var j = 0; j < slides.length; j++) slides[j].classList.remove('is-on');
    slides[(at + 1) % slides.length].classList.add('is-on');
  }

  function start() { if (!timer) timer = setInterval(step, 6000); }
  function stop() { clearInterval(timer); timer = null; }

  document.addEventListener('visibilitychange', function () {
    if (document.hidden) stop(); else start();
  });

  start();
})();
