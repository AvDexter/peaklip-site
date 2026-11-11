// peaklip.com/account.html — sign in with your Peaklip account to see credits and usage, buy a plan,
// manage or cancel the subscription, or delete the account. Talks only to Peaklip's server; the sign-in
// key lives in this tab's sessionStorage (gone when the tab closes). No cookies, no trackers.
(function () {
  "use strict";
  var API = "https://clipfactory-production-e466.up.railway.app";
  var KEY = "peaklip.token";
  var AR = document.documentElement.lang === "ar";
  var T = AR ? {
    signin: "تسجيل الدخول", signingIn: "لحظة…", email: "البريد الإلكتروني", password: "كلمة المرور",
    needBoth: "أدخل بريدك وكلمة المرور.", offline: "تعذّر الوصول إلى خادم Peaklip. حاول بعد قليل.",
    generic: "حدث خطأ. حاول مرة أخرى.", credits: "رصيد", unlimited: "رصيد غير محدود",
    noPlan: "لا توجد خطة بعد", trial: "تجربة مجانية", active: "فعّالة", past_due: "مشكلة في الدفع — حدّث بطاقتك",
    paused: "متوقفة", canceled: "ملغاة", renews: "تتجدد في ", trialEnds: "تنتهي التجربة في ",
    cancels: "تُلغى في ", clips: "مقطع صُنع", buy: "اشترِ ", perMonth: "/شهرياً", creditsMonth: " رصيد شهرياً",
    trialNote: "التجربة المجانية (3 أيام، 10 مقاطع) تبدأ من تطبيق Peaklip فقط. الشراء من هنا يبدأ الخطة المدفوعة مباشرة.",
    manage: "إدارة الاشتراك", cancel: "إلغاء الاشتراك",
    cancelAsk: "إلغاء اشتراكك؟ تحتفظ بخطتك ورصيدك حتى نهاية الفترة المدفوعة، ولن تُحاسَب بعدها.",
    cancelled: "أُلغي اشتراكك. يبقى فعّالاً حتى ", history: "سجل الرصيد", noHistory: "لا يوجد سجل بعد.",
    when: "التاريخ", change: "التغيير", balance: "الرصيد", what: "التفاصيل",
    del: "حذف الحساب نهائياً", delType: "اكتب DELETE للتأكيد.", delPass: "أدخل كلمة مرورك.",
    deleted: "حُذف حسابك. شكراً لتجربتك Peaklip.", signout: "تسجيل الخروج", hello: "مرحباً، ",
    opening: "جارٍ فتح صفحة الدفع…", perYear: "/سنوياً", monthly: "شهري", yearly: "سنوي", save: "وفّر 15%",
    popular: "الأكثر شيوعاً", aboutMonth: function (m) { return "حوالي $" + m + " شهرياً · وفّر 15%"; },
    billedMonthly: "تُدفع شهرياً", yearlyNote: "تُدفع الخطط السنوية مرة في السنة وتتجدد أرصدتك كل شهر كالمعتاد.",
    notes: {"Free trial started": "بدأت التجربة المجانية", "Plan renewed": "تجددت الخطة",
            "Subscription ended": "انتهى الاشتراك", "Clip made": "صُنع مقطع",
            "Clip failed — credit returned": "فشل مقطع — أُعيد الرصيد", "Credits from Peaklip": "رصيد من Peaklip",
            "Monthly credits (yearly plan)": "رصيد الشهر (خطة سنوية)"}
  } : {
    signin: "Sign in", signingIn: "One moment…", email: "Email", password: "Password",
    needBoth: "Enter your email and password.", offline: "Couldn't reach the Peaklip server. Try again in a minute.",
    generic: "Something went wrong. Try again.", credits: "credits", unlimited: "Unlimited credits",
    noPlan: "No plan yet", trial: "Free trial", active: "Active", past_due: "Payment problem — update your card",
    paused: "Paused", canceled: "Cancelled", renews: "Renews ", trialEnds: "Trial ends ",
    cancels: "Cancels on ", clips: "clips made", buy: "Buy ", perMonth: "/month", creditsMonth: " credits a month",
    trialNote: "The free trial (3 days, 10 clips) starts in the Peaklip app only. Buying here starts the paid plan straight away.",
    manage: "Manage subscription", cancel: "Cancel subscription",
    cancelAsk: "Cancel your subscription? You keep your plan and credits until the end of the period you paid for, and you won't be charged again.",
    cancelled: "Your subscription is cancelled. It stays active until ", history: "Credit history", noHistory: "No history yet.",
    when: "Date", change: "Change", balance: "Balance", what: "Details",
    del: "Delete my account for good", delType: "Type DELETE to confirm.", delPass: "Enter your password.",
    deleted: "Your account has been deleted. Thanks for trying Peaklip.", signout: "Sign out", hello: "Hi, ",
    opening: "Opening the payment page…", perYear: "/year", monthly: "Monthly", yearly: "Yearly",
    save: "Save 15%", popular: "Most popular", aboutMonth: function (m) { return "About $" + m + " a month · save 15%"; },
    billedMonthly: "Billed monthly", yearlyNote: "Yearly plans are paid once a year and still refill your credits every month.",
    notes: {}
  };
  // [id, name, $ a month, credits a month, $ a year, about $ a month when paid yearly]
  var PLANS = [["starter", "Starter", 19, 120, 194, "16.17"], ["creator", "Creator", 39, 300, 398, "33.17"],
               ["pro", "Pro", 69, 750, 704, "58.67"]];
  var bill = "month";
  var LIVE = ["trialing", "active", "past_due"];

  function $(id) { return document.getElementById(id); }
  function token() { try { return sessionStorage.getItem(KEY); } catch (e) { return null; } }
  function setToken(t) { try { if (t) { sessionStorage.setItem(KEY, t); } else { sessionStorage.removeItem(KEY); } } catch (e) { /* private mode */ } }
  function date(iso) {
    if (!iso) { return ""; }
    return new Date(iso).toLocaleDateString(AR ? "ar" : undefined, { year: "numeric", month: "short", day: "numeric" });
  }
  function el(tag, text, cls) { var n = document.createElement(tag); if (text != null) { n.textContent = text; } if (cls) { n.className = cls; } return n; }
  function say(box, text, ok) { box.textContent = text || ""; box.hidden = !text; box.style.color = ok ? "var(--ok)" : "#FF7A7A"; }

  function call(method, path, body) {
    var headers = { "Accept": "application/json" };
    if (body) { headers["Content-Type"] = "application/json"; }
    var t = token();
    if (t) { headers.Authorization = "Bearer " + t; }
    return fetch(API + path, { method: method, headers: headers, body: body ? JSON.stringify(body) : undefined, credentials: "omit" })
      .catch(function () { throw new Error(T.offline); })
      .then(function (r) {
        return r.text().then(function (txt) {
          var data = null;
          try { data = txt ? JSON.parse(txt) : null; } catch (e) { data = null; }
          if (r.ok) { return data; }
          if (r.status === 401 && path !== "/auth/login") { setToken(null); show(); }
          var err = new Error((data && data.message) || (r.status >= 500 ? T.offline : T.generic));
          err.code = data && data.error;
          throw err;
        });
      });
  }

  // ------------------------------------------------------------------ sign in

  function signIn(ev) {
    ev.preventDefault();
    var email = $("email").value.trim(), pass = $("password").value, msg = $("signin-msg"), btn = $("signin-btn");
    if (!email || !pass) { say(msg, T.needBoth); return; }
    btn.disabled = true; btn.textContent = T.signingIn; say(msg, "");
    call("POST", "/auth/login", { email: email, password: pass, remember: false })
      .then(function (data) { setToken(data.token); $("password").value = ""; show(); })
      .catch(function (e) { say(msg, e.message); })
      .then(function () { btn.disabled = false; btn.textContent = T.signin; });
  }

  function signOut() {
    call("POST", "/auth/logout").catch(function () { /* signed out here regardless */ })
      .then(function () { setToken(null); show(); });
  }

  // ------------------------------------------------------------------ account

  function show() {
    var signedIn = !!token();
    $("signin").hidden = signedIn;
    $("account").hidden = !signedIn;
    if (signedIn) { load(); }
  }

  function load() {
    say($("acct-msg"), "");
    call("GET", "/me/usage?limit=100").then(render).catch(function (e) { say($("acct-msg"), e.message); });
  }

  function render(u) {
    $("hello").textContent = T.hello + (u.name || u.email);
    $("who").textContent = u.email;
    $("credits").textContent = u.unlimited ? T.unlimited : (u.credits + " " + T.credits);
    $("clips").textContent = u.clips_made + " " + T.clips;
    var live = LIVE.indexOf(u.status) >= 0;
    var parts = [];
    if (live || u.status === "canceled") { parts.push((u.plan_name || "") + " · " + (T[u.status] || u.status)); } else { parts.push(T.noPlan); }
    if (live && u.cancels_at) { parts.push(T.cancels + date(u.cancels_at)); }
    else if (live && u.period_ends_at) { parts.push((u.status === "trialing" ? T.trialEnds : T.renews) + date(u.period_ends_at)); }
    $("plan-line").textContent = parts.join(" · ");

    var actions = $("sub-actions");
    actions.innerHTML = "";
    if (u.has_subscription && !u.unlimited) {
      var manage = el("button", T.manage, "btn btn-quiet btn-sm");
      manage.type = "button";
      manage.onclick = function () { openUrl("/billing/portal", null, manage); };
      actions.appendChild(manage);
    }
    if (live && u.has_subscription && !u.cancels_at && !u.unlimited) {
      var cancel = el("button", T.cancel, "btn btn-quiet btn-sm");
      cancel.type = "button";
      cancel.onclick = function () {
        if (!window.confirm(T.cancelAsk)) { return; }
        cancel.disabled = true;
        call("POST", "/me/cancel-subscription").then(function (nu) {
          render(nu);
          say($("acct-msg"), T.cancelled + date(nu.cancels_at || nu.period_ends_at) + ".", true);
        }).catch(function (e) { cancel.disabled = false; say($("acct-msg"), e.message); });
      };
      actions.appendChild(cancel);
    }

    var buy = $("buy");
    buy.hidden = live || u.unlimited;
    if (!buy.hidden) {
      var grid = $("plans");
      var yearly = !!u.yearly_ready;
      if (!yearly) { bill = "month"; }
      var old = $("bill-switch");
      if (old) { old.parentNode.removeChild(old); }
      if (yearly) {
        var wrap = el("div", null, "billing");
        wrap.id = "bill-switch";
        var tg = el("div", null, "bill-toggle");
        tg.setAttribute("role", "group");
        [["month", T.monthly], ["year", T.yearly]].forEach(function (o) {
          var btn = el("button", o[1], "bill-opt");
          btn.type = "button";
          btn.setAttribute("aria-pressed", String(bill === o[0]));
          if (o[0] === "year") { btn.appendChild(el("span", T.save, "save-chip")); }
          btn.onclick = function () { bill = o[0]; render(u); };
          tg.appendChild(btn);
        });
        wrap.appendChild(tg);
        grid.parentNode.insertBefore(wrap, grid);
      }
      grid.innerHTML = "";
      PLANS.forEach(function (p) {
        var featured = p[0] === "creator";
        var card = el("article", null, "plan panel" + (featured ? " plan-featured" : ""));
        if (featured) { card.appendChild(el("span", T.popular, "plan-badge")); }
        card.appendChild(el("h3", p[1]));
        var price = el("p", null, "price");
        price.appendChild(el("span", "$" + (bill === "year" ? p[4] : p[2]), "amt"));
        price.appendChild(el("span", bill === "year" ? T.perYear : T.perMonth, "per"));
        card.appendChild(price);
        var sub = el("p", bill === "year" ? T.aboutMonth(p[5]) : T.billedMonthly, "price-sub");
        if (bill === "year") { sub.style.color = "#3DD68C"; }
        card.appendChild(sub);
        card.appendChild(el("p", p[3] + T.creditsMonth, "plan-credits"));
        var b = el("button", T.buy + p[1], "btn " + (featured ? "btn-primary" : "btn-quiet") + " plan-btn");
        b.type = "button";
        b.style.marginTop = "var(--space-4)";
        var chosen = bill;
        b.onclick = function () {
          openUrl("/billing/checkout", chosen === "year" ? { plan: p[0], interval: "year" } : { plan: p[0] }, b);
        };
        card.appendChild(b);
        grid.appendChild(card);
      });
    }

    var body = $("history-rows");
    body.innerHTML = "";
    $("no-history").hidden = (u.history || []).length > 0;
    (u.history || []).forEach(function (h) {
      var tr = el("tr");
      tr.appendChild(el("td", date(h.at)));
      tr.appendChild(el("td", (h.delta > 0 ? "+" : "") + h.delta));
      tr.appendChild(el("td", String(h.balance)));
      tr.appendChild(el("td", T.notes[h.note] || h.note || ""));
      body.appendChild(tr);
    });
  }

  function openUrl(path, body, btn) {
    btn.disabled = true;
    say($("acct-msg"), T.opening, true);
    call("POST", path, body || {}).then(function (data) {
      if (data && /^https:\/\//.test(data.url)) { window.location.href = data.url; }
    }).catch(function (e) { btn.disabled = false; say($("acct-msg"), e.message); });
  }

  function deleteAccount(ev) {
    ev.preventDefault();
    var msg = $("del-msg"), btn = $("del-btn");
    if ($("del-confirm").value.trim().toUpperCase() !== "DELETE") { say(msg, T.delType); return; }
    if (!$("del-password").value) { say(msg, T.delPass); return; }
    btn.disabled = true;
    call("POST", "/me/delete", { password: $("del-password").value }).then(function () {
      setToken(null);
      show();
      say($("signin-msg"), T.deleted, true);
    }).catch(function (e) { btn.disabled = false; say(msg, e.message); });
  }

  // Never work inside another site's frame (someone could overlay it to trick clicks or typing).
  if (window.top !== window.self) {
    document.documentElement.style.display = "none";
    try { window.top.location = window.self.location.href; } catch (e) { /* blocked: stays hidden */ }
    return;
  }

  document.addEventListener("DOMContentLoaded", function () {
    $("signin-form").addEventListener("submit", signIn);
    $("signout").addEventListener("click", signOut);
    $("del-form").addEventListener("submit", deleteAccount);
    show();
  });
})();
