/* ============================================================
   BND Construction — forms

   Both the bid enquiry and the subcontractor prequalification
   post here. FormSubmit answers HTTP 200 even when it rejects a
   submission, and activation is tied to (inbox + DOMAIN) — so a
   form proven on one host is NOT proven on another. Always
   re-test from the live domain after any DNS change.
   ============================================================ */
(function () {
  'use strict';

  var INBOX = 'vcgcbids@gmail.com';
  var CC = 'daniel@bnd-co.com';
  var ENDPOINT = 'https://formsubmit.co/ajax/' + INBOX;


  /* ---- native multipart forms (they carry a file, so they cannot go over
     AJAX as JSON). Validate client-side, then let the browser submit. ---- */
  var MAX_FILE = 5 * 1024 * 1024;

  Array.prototype.forEach.call(document.querySelectorAll('[data-validate]'), function (form) {
    var msg = form.parentNode.querySelector('[data-form-msg]');
    function say(text, state) {
      if (!msg) return;
      msg.textContent = text;
      if (state) msg.setAttribute('data-state', state); else msg.removeAttribute('data-state');
    }

    form.addEventListener('submit', function (e) {
      var required = form.querySelectorAll('[required]');
      for (var i = 0; i < required.length; i++) {
        var f = required[i], v = (f.value || '').trim();
        var label = (f.getAttribute('data-label') || f.name).toLowerCase();
        if (!v) { e.preventDefault(); say('Add your ' + label + '.', 'error'); f.focus(); return; }
        if (f.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) {
          e.preventDefault(); say('That email doesn\u2019t look right. Check it and try again.', 'error'); f.focus(); return;
        }
        if (f.type === 'tel' && v.replace(/[^\d]/g, '').length < 7) {
          e.preventDefault(); say('That phone number looks too short.', 'error'); f.focus(); return;
        }
      }

      var file = form.querySelector('input[type="file"]');
      if (file && file.files && file.files.length && file.files[0].size > MAX_FILE) {
        e.preventDefault();
        var what = (file.getAttribute('data-label') || 'file').toLowerCase();
        say('That ' + what + ' file is over 5 MB. Attach a smaller one, or send it to ' + INBOX + '.', 'error');
        file.focus();
        return;
      }

      say('Sending\u2026');
    });
  });

  var forms = document.querySelectorAll('[data-form]');
  if (!forms.length) return;

  Array.prototype.forEach.call(forms, function (form) {
    var msg = form.parentNode.querySelector('[data-form-msg]');
    var button = form.querySelector('button[type="submit"]');

    function say(text, state) {
      if (!msg) return;
      msg.textContent = text;
      if (state) msg.setAttribute('data-state', state);
      else msg.removeAttribute('data-state');
    }

    function fail(text, field) {
      say(text, 'error');
      if (field) field.focus();
      return false;
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var data = {};
      var required = form.querySelectorAll('[required]');

      /* validate in document order so the message always matches
         the first field the person still has to fix */
      for (var i = 0; i < required.length; i++) {
        var f = required[i];
        var v = (f.value || '').trim();
        var label = f.getAttribute('data-label') || f.name;

        if (!v) return fail('Add your ' + label.toLowerCase() + '.', f);

        if (f.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) {
          return fail('That email doesn’t look right. Check it and try again.', f);
        }
        if (f.type === 'tel' && v.replace(/[^\d]/g, '').length < 7) {
          return fail('That phone number looks too short.', f);
        }
      }

      /* collect everything, required or not */
      var fields = form.querySelectorAll('input,select,textarea');
      for (var j = 0; j < fields.length; j++) {
        var el = fields[j];
        if (!el.name) continue;
        var label = el.getAttribute('data-label') || el.name;
        data[label] = (el.value || '').trim();
      }

      data._subject = (form.getAttribute('data-subject') || 'BND website enquiry')
        + ' — ' + (data.Name || data.Company || 'new');
      data._template = 'table';
      data._captcha = 'false';
      if (CC) data._cc = CC;

      button.disabled = true;
      say('Sending…');

      fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(data)
      })
        .then(function (res) {
          if (!res.ok) throw new Error('HTTP ' + res.status);
          return res.json();
        })
        .then(function (d) {
          /* trust the body, not the status code */
          var ok = d && (d.success === true || d.success === 'true');
          if (!ok) throw new Error((d && d.message) || 'rejected');
          form.reset();
          say(form.getAttribute('data-success')
              || 'Thanks — that’s with us. We’ll be in touch shortly.', 'ok');
        })
        .catch(function () {
          say('That didn’t send. Please email ' + INBOX + ' directly.', 'error');
        })
        .then(function () {
          button.disabled = false;
        });
    });
  });
})();
