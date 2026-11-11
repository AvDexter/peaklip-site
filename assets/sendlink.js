/* Phones and tablets: Peaklip only runs on Windows, so instead of downloading an installer the visitor can't open,
   they get the link by email for later, on their PC. Computers keep the normal "Download for Windows" button.
   The email is sent by the Peaklip server (Resend) and the address isn't stored. */
(function () {
  "use strict";
  var root = document.documentElement;
  if (!root.classList.contains("is-phone")) return;
  var API = "https://clipfactory-production-e466.up.railway.app/site/send-link";
  var ar = root.lang === "ar";
  var T = ar ? {
    sending: "جارٍ الإرسال…", sent: "أُرسل! افتح البريد على حاسوبك لتثبيت Peaklip.",
    bad: "اكتب بريداً إلكترونياً صحيحاً.", fail: "تعذّر الإرسال. حاول مرة أخرى بعد قليل."
  } : {
    sending: "Sending…", sent: "Sent! Open the email on your PC to install Peaklip.",
    bad: "Enter a valid email address.", fail: "We couldn't send it. Try again in a minute."
  };
  var form = document.getElementById("send-link");
  if (!form) return;
  var input = form.querySelector("input"), button = form.querySelector("button"), msg = form.querySelector(".send-link-msg");

  /* Every other "Download" link on the page leads here instead of to the .exe */
  document.addEventListener("click", function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href*="PeaklipSetup.exe"]') : null;
    if (!a) return;
    e.preventDefault();
    form.scrollIntoView({ behavior: "smooth", block: "center" });
    setTimeout(function () { input.focus(); }, 400);
  }, true);

  function say(text, kind) { msg.textContent = text; msg.className = "send-link-msg" + (kind ? " " + kind : ""); }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var email = (input.value || "").trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { say(T.bad, "err"); input.focus(); return; }
    button.disabled = true; say(T.sending);
    fetch(API, { method: "POST", headers: { "Content-Type": "application/json" },
                 body: JSON.stringify({ email: email, lang: ar ? "ar" : "en" }) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (res) {
        if (res.ok) {
          say(T.sent, "ok"); form.reset();
          if (window.fbq) window.fbq("track", "Lead", { content_name: "Email download link" });
        } else {
          say(ar ? T.fail : (res.j.message || T.fail), "err");
        }
      })
      .catch(function () { say(T.fail, "err"); })
      .then(function () { button.disabled = false; });
  });
})();
