/* Ad measurement (Meta Pixel), only with the visitor's yes.
   Nothing from Meta loads and no cookie is set until "Accept" is clicked. The choice is kept in this
   browser's local storage ("peaklip-consent" = yes | no) and can be changed with "Cookie settings" in the footer.
   Used on the marketing pages only, never on account.html (its CSP allows peaklip.com scripts only). */
(function () {
  "use strict";
  var PIXEL_ID = "4513794125554263";                // Meta Events Manager → the Peaklip dataset's ID (numbers only)
  if (!/^\d{6,20}$/.test(PIXEL_ID)) return;

  var KEY = "peaklip-consent";
  var ar = document.documentElement.lang === "ar";
  var T = ar ? {
    text: "نستخدم ملف تعريف ارتباط من Meta لنعرف أي إعلاناتنا أوصلتك إلى هنا. لا يُحمَّل شيء ما لم توافق.",
    more: "التفاصيل", yes: "موافق", no: "رفض", settings: "إعدادات ملفات تعريف الارتباط", privacy: "privacy.html"
  } : {
    text: "We use a Meta cookie to see which of our ads brought you here. Nothing loads unless you accept.",
    more: "Details", yes: "Accept", no: "Decline", settings: "Cookie settings", privacy: "privacy.html"
  };

  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) { /* private mode: ask again next visit */ } }

  var loaded = false;
  function load() {
    if (loaded) return;
    loaded = true;
    /* Meta's standard base code */
    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = "2.0"; n.queue = [];
      t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
    }(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");
    window.fbq("init", PIXEL_ID);
    window.fbq("track", "PageView");
  }

  /* A click on any installer link = the conversion the ads are judged by */
  document.addEventListener("click", function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href*="PeaklipSetup.exe"]') : null;
    // On phones the link opens the email form instead (assets/sendlink.js), which counts its own Lead when sent
    if (a && loaded && window.fbq && !document.documentElement.classList.contains("is-phone"))
      window.fbq("track", "Lead", { content_name: "Download for Windows" });
  }, true);

  var bar = null;
  function hide() { if (bar) { bar.remove(); bar = null; } }
  function show() {
    if (bar) return;
    bar = document.createElement("div");
    bar.className = "cookie-bar";
    bar.setAttribute("role", "dialog");
    bar.setAttribute("aria-label", T.settings);
    var p = document.createElement("p");
    p.textContent = T.text + " ";
    var link = document.createElement("a");
    link.href = T.privacy + "#cookies";
    link.textContent = T.more;
    p.appendChild(link);
    var row = document.createElement("div");
    row.className = "cookie-actions";
    [[T.no, "btn btn-quiet btn-sm", "no"], [T.yes, "btn btn-primary btn-sm", "yes"]].forEach(function (b) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = b[1];
      btn.textContent = b[0];
      btn.addEventListener("click", function () {
        set(b[2]);
        hide();
        if (b[2] === "yes") load();
        else if (loaded) location.reload();     // withdrawing consent: reload without the pixel
      });
      row.appendChild(btn);
    });
    bar.appendChild(p);
    bar.appendChild(row);
    document.body.appendChild(bar);
  }

  function footerLink() {
    var nav = document.querySelector(".site-footer nav");
    if (!nav) return;
    var a = document.createElement("a");
    a.href = "#";
    a.textContent = T.settings;
    a.addEventListener("click", function (e) { e.preventDefault(); show(); });
    nav.appendChild(a);
  }

  var choice = get();
  if (choice === "yes") load();
  else if (choice !== "no") show();
  footerLink();
})();
