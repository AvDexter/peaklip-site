"""Builds account.html and ar/account.html (the same page in English and Arabic).

Run after changing the page:  python tools/build_account.py
The page's behaviour (and its few runtime texts in both languages) lives in assets/account.js.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EN = {
    "lang": 'lang="en"', "base": "", "self": "account.html", "other": "ar/account.html", "other_lang": "ar",
    "other_name": "العربية", "skip": "Skip to content", "home": "Peaklip home", "main": "Main", "footer": "Footer",
    "nav": '<a href="./#how">How it works</a><a href="./#features">Features</a><a href="./#faq">FAQ</a>',
    "title": "Your account · Peaklip",
    "desc": "Sign in to see your Peaklip credits and usage, buy or cancel a plan, or delete your account.",
    "h1": "Your account",
    "intro": "Sign in with the email and password you use in the Peaklip app.",
    "email": "Email", "password": "Password", "signin": "Sign in",
    "noacct": 'No account yet? <a href="./">Download Peaklip</a> and create one in the app (that\'s also where the free trial starts). Forgot your password? Use “Forgot password?” in the app.',
    "privacy": "Signing in here keeps a sign-in key in this browser tab only, until you close it or sign out. No cookies.",
    "signout": "Sign out", "plan": "Plan", "buy_h": "Choose a plan",
    "buy_note": "The free trial (3 days, 10 clips) starts in the Peaklip app only. Buying here starts the paid plan straight away. Prices in US dollars; taxes are added where required. Payments are handled by Creem — Peaklip never sees your card.",
    "history": "Credit history", "when": "Date", "change": "Change", "balance": "Balance", "what": "Details",
    "nohistory": "No history yet.",
    "del_h": "Delete my account",
    "del_p": "This cancels your subscription straight away (no further charges) and erases your account, credits and history from Peaklip's server. It can't be undone. Videos and clips on your PC aren't touched.",
    "del_pass": "Your password", "del_confirm": "Type DELETE to confirm", "del_btn": "Delete my account for good",
    "foot": '<a href="privacy.html">Privacy</a><a href="terms.html">Terms</a><a href="refunds.html">Refunds</a><a href="acceptable-use.html">Acceptable use</a><a href="account.html">Account</a><a href="mailto:hello@peaklip.com">hello@peaklip.com</a>',
}
AR = {
    "lang": 'lang="ar" dir="rtl"', "base": "../", "self": "ar/account.html", "other": "../account.html",
    "other_lang": "en", "other_name": "English", "skip": "تخطَّ إلى المحتوى", "home": "الصفحة الرئيسية لـ Peaklip",
    "main": "الرئيسية", "footer": "التذييل",
    "nav": '<a href="./#how">كيف يعمل</a><a href="./#features">المزايا</a><a href="./#faq">الأسئلة</a>',
    "title": "حسابك · Peaklip",
    "desc": "سجّل الدخول لترى رصيدك واستخدامك في Peaklip، أو لشراء خطة أو إلغائها، أو لحذف حسابك.",
    "h1": "حسابك",
    "intro": "سجّل الدخول بالبريد وكلمة المرور اللذين تستخدمهما في تطبيق Peaklip.",
    "email": "البريد الإلكتروني", "password": "كلمة المرور", "signin": "تسجيل الدخول",
    "noacct": 'ليس لديك حساب؟ <a href="./">نزّل Peaklip</a> وأنشئ حساباً من التطبيق (ومن هناك تبدأ التجربة المجانية أيضاً). نسيت كلمة المرور؟ استخدم «نسيت كلمة المرور؟» في التطبيق.',
    "privacy": "تسجيل الدخول هنا يحفظ مفتاح الدخول في علامة التبويب هذه فقط، حتى تغلقها أو تسجّل الخروج. بلا ملفات تعريف ارتباط.",
    "signout": "تسجيل الخروج", "plan": "الخطة", "buy_h": "اختر خطة",
    "buy_note": "التجربة المجانية (3 أيام، 10 مقاطع) تبدأ من تطبيق Peaklip فقط. الشراء من هنا يبدأ الخطة المدفوعة مباشرة. الأسعار بالدولار الأمريكي، وتُضاف الضرائب حيث يلزم. يتولى Creem المدفوعات — ولا يرى Peaklip بطاقتك أبداً.",
    "history": "سجل الرصيد", "when": "التاريخ", "change": "التغيير", "balance": "الرصيد", "what": "التفاصيل",
    "nohistory": "لا يوجد سجل بعد.",
    "del_h": "حذف حسابي",
    "del_p": "يلغي هذا اشتراكك فوراً (بلا أي رسوم أخرى) ويمحو حسابك ورصيدك وسجلك من خادم Peaklip. لا يمكن التراجع عنه. لا تُمسّ الفيديوهات والمقاطع على حاسوبك.",
    "del_pass": "كلمة مرورك", "del_confirm": "اكتب DELETE للتأكيد", "del_btn": "احذف حسابي نهائياً",
    "foot": '<a href="privacy.html">الخصوصية</a><a href="terms.html">الشروط</a><a href="refunds.html">الاسترداد</a><a href="acceptable-use.html">الاستخدام المقبول</a><a href="account.html">حسابي</a><a href="mailto:hello@peaklip.com">hello@peaklip.com</a>',
}

PAGE = """<!doctype html>
<html {lang}>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#0E0E12">
  <meta name="robots" content="noindex">
  <link rel="icon" href="{base}favicon.svg" type="image/svg+xml">
  <link rel="canonical" href="https://peaklip.com/{self}">
  <link rel="alternate" hreflang="en" href="https://peaklip.com/account.html">
  <link rel="alternate" hreflang="ar" href="https://peaklip.com/ar/account.html">
  <link rel="stylesheet" href="{base}assets/style.css?v=6">
  <style>
    .acct-form {{ display: grid; gap: 12px; max-width: 420px; margin-top: var(--space-4); }}
    .acct-form input {{ min-height: 46px; padding: 0 14px; border-radius: 12px; border: 1px solid var(--border);
      background: var(--surface-2); color: var(--text); font: inherit; }}
    .acct-form input:focus {{ outline: 2px solid var(--accent); outline-offset: 1px; }}
    .acct-msg {{ font-size: 14px; margin-top: var(--space-2); }}
    .acct-top {{ display: flex; justify-content: space-between; align-items: center; gap: 16px; flex-wrap: wrap; }}
    .acct-stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: var(--space-3); margin-top: var(--space-4); }}
    .acct-stats .big {{ font-size: 30px; font-weight: 700; color: var(--text); line-height: 1.2; }}
    .acct-actions {{ display: flex; gap: 10px; flex-wrap: wrap; margin-top: var(--space-3); }}
    .acct-table {{ width: 100%; border-collapse: collapse; margin-top: var(--space-3); font-size: 14px; }}
    .acct-table th, .acct-table td {{ text-align: start; padding: 10px 8px; border-bottom: 1px solid var(--border); color: var(--text-2); }}
    .acct-table th {{ color: var(--text-3); font-weight: 500; }}
    .table-wrap {{ overflow-x: auto; }}
    .legal.account {{ max-width: 980px; }}
    .account .plans {{ margin-top: var(--space-3); }}
    @media (max-width: 760px) {{ .account .plans {{ grid-template-columns: 1fr; }} }}
    details.danger summary {{ cursor: pointer; color: #FF7A7A; font-weight: 600; }}
  </style>
  <script src="{base}assets/account.js?v=1" defer></script>
</head>
<body>
<a class="skip" href="#main">{skip}</a>
<header class="site-header scrolled">
  <div class="wrap nav">
    <a class="brand" href="./" aria-label="{home}"><img src="{base}assets/logo.svg" alt="" width="30" height="30">Peaklip</a>
    <nav class="nav-links" aria-label="{main}">{nav}</nav>
    <a class="lang" href="{other}" hreflang="{other_lang}" lang="{other_lang}">{other_name}</a>
  </div>
</header>

<main id="main" class="wrap">
  <article class="legal account" aria-live="polite">
    <section id="signin">
      <h1>{h1}</h1>
      <p>{intro}</p>
      <form id="signin-form" class="acct-form" novalidate>
        <input id="email" type="email" autocomplete="email" placeholder="{email}" aria-label="{email}" required>
        <input id="password" type="password" autocomplete="current-password" placeholder="{password}" aria-label="{password}" required>
        <button id="signin-btn" class="btn btn-primary" type="submit">{signin}</button>
        <p id="signin-msg" class="acct-msg" hidden></p>
      </form>
      <p style="margin-top: var(--space-4)">{noacct}</p>
      <p class="updated" style="margin-top: var(--space-3)">{privacy}</p>
    </section>

    <section id="account" hidden>
      <div class="acct-top">
        <div><h1 id="hello">{h1}</h1><p id="who"></p></div>
        <button id="signout" class="btn btn-quiet btn-sm" type="button">{signout}</button>
      </div>
      <div class="acct-stats">
        <div class="panel"><p class="big" id="credits">…</p><p id="clips"></p></div>
        <div class="panel"><p>{plan}</p><p class="big" id="plan-line" style="font-size: 20px">…</p>
          <div id="sub-actions" class="acct-actions"></div></div>
      </div>
      <p id="acct-msg" class="acct-msg" hidden></p>

      <div id="buy" hidden>
        <h2>{buy_h}</h2>
        <div id="plans" class="plans"></div>
        <p class="updated" style="margin-top: var(--space-3)">{buy_note}</p>
      </div>

      <h2>{history}</h2>
      <div class="table-wrap">
        <table class="acct-table">
          <thead><tr><th>{when}</th><th>{change}</th><th>{balance}</th><th>{what}</th></tr></thead>
          <tbody id="history-rows"></tbody>
        </table>
      </div>
      <p id="no-history" hidden>{nohistory}</p>

      <h2>{del_h}</h2>
      <details class="danger">
        <summary>{del_h}</summary>
        <p style="margin-top: var(--space-3)">{del_p}</p>
        <form id="del-form" class="acct-form" novalidate>
          <input id="del-password" type="password" autocomplete="current-password" placeholder="{del_pass}" aria-label="{del_pass}">
          <input id="del-confirm" type="text" autocomplete="off" placeholder="{del_confirm}" aria-label="{del_confirm}">
          <button id="del-btn" class="btn btn-quiet" type="submit" style="color: #FF7A7A">{del_btn}</button>
          <p id="del-msg" class="acct-msg" hidden></p>
        </form>
      </details>
    </section>
  </article>
</main>

<footer class="site-footer">
  <div class="wrap foot">
    <a class="brand" href="./" aria-label="{home}"><img src="{base}assets/logo.svg" alt="" width="24" height="24">Peaklip</a>
    <span>© 2026 Peaklip</span>
    <nav aria-label="{footer}">{foot}</nav>
  </div>
</footer>
</body>
</html>
"""

for words in (EN, AR):
    (ROOT / words["self"]).write_text(PAGE.format(**words), encoding="utf-8")
    print("wrote", words["self"])
