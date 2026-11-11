/* Peaklip site motion. Everything here is decoration: the page reads the same without it,
   and visitors who ask for reduced motion get the final, still state. */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = window.matchMedia("(pointer: fine)").matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* Sticky header hairline once scrolled */
  var header = $(".site-header");
  if (header) {
    var onScrollHeader = function () { header.classList.toggle("scrolled", window.scrollY > 8); };
    window.addEventListener("scroll", onScrollHeader, { passive: true }); onScrollHeader();
  }

  /* Staggered reveals */
  var groups = {};
  $$(".reveal").forEach(function (el) {
    var key = el.parentElement ? el.parentElement : document.body;
    var list = groups[key.dataset.revealId || (key.dataset.revealId = String(Math.random()))] = groups[key.dataset.revealId] || [];
    el.style.setProperty("--i", list.length);
    list.push(el);
  });
  if (reduce || !("IntersectionObserver" in window)) {
    $$(".reveal").forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    $$(".reveal").forEach(function (el) { io.observe(el); });
  }

  /* Hero: light follows the cursor, phone tilts toward it */
  var hero = $(".hero"), phone = $(".phone");
  if (hero && !reduce && finePointer) {
    var raf = 0, last = null;
    hero.addEventListener("pointermove", function (e) {
      last = e;
      if (raf) return;
      raf = requestAnimationFrame(function () {
        raf = 0;
        var r = hero.getBoundingClientRect();
        hero.style.setProperty("--mx", ((last.clientX - r.left) / r.width * 100) + "%");
        hero.style.setProperty("--my", ((last.clientY - r.top) / r.height * 100) + "%");
        if (phone) {
          var p = phone.getBoundingClientRect();
          var dx = (last.clientX - (p.left + p.width / 2)) / r.width;
          var dy = (last.clientY - (p.top + p.height / 2)) / r.height;
          phone.style.setProperty("--ry", (dx * 16).toFixed(2) + "deg");
          phone.style.setProperty("--rx", (-dy * 12).toFixed(2) + "deg");
        }
      });
    });
    hero.addEventListener("pointerleave", function () {
      if (phone) { phone.style.setProperty("--rx", "0deg"); phone.style.setProperty("--ry", "0deg"); }
    });
  }

  /* Cards: glow follows the cursor */
  if (!reduce && finePointer) {
    $$(".glow-card").forEach(function (card) {
      card.addEventListener("pointermove", function (e) {
        var r = card.getBoundingClientRect();
        card.style.setProperty("--gx", (e.clientX - r.left) + "px");
        card.style.setProperty("--gy", (e.clientY - r.top) + "px");
      });
    });
  }

  /* Caption demo: highlight the spoken word, like Peaklip's captions */
  var words = $$("#cap span");
  if (words.length) {
    if (reduce) { words[1].classList.add("on"); }
    else {
      var lines = document.documentElement.lang === "ar"
        ? [["لا", "يمكن", "أنه"], ["قفز", "من", "فوق"], ["الجسر!", "يلا", "بينا"]]
        : [["No", "way", "he"], ["actually", "landed", "it"], ["let's", "go!", ""]];
      var line = 0, i = 0;
      setInterval(function () {
        if (document.hidden) return;
        words.forEach(function (w, n) { w.classList.toggle("on", n === i); });
        i += 1;
        if (i >= words.length || !words[i].textContent) {
          i = 0; line = (line + 1) % lines.length;
          setTimeout(function () { words.forEach(function (w, n) { w.textContent = lines[line][n]; }); }, 380);
        }
      }, 420);
    }
  }

  /* Scroll story: a waveform is "played"; the peak lights up and becomes a clip */
  var wave = $("#wave");
  if (wave) {
    var N = window.innerWidth < 700 ? 56 : 96;
    var peakAt = Math.round(N * 0.66), peakW = Math.max(4, Math.round(N * 0.07));
    var seed = 7;
    var rnd = function () { seed = (seed * 9301 + 49297) % 233280; return seed / 233280; };
    var bars = [];
    var frag = document.createDocumentFragment();
    for (var k = 0; k < N; k++) {
      var base = 0.16 + rnd() * 0.32 + Math.sin(k / 5) * 0.06;
      var d = Math.abs(k - peakAt);
      var hot = d <= peakW / 2;
      var h = hot ? 0.72 + (1 - d / (peakW / 2 + 0.01)) * 0.28 : base;
      var bar = document.createElement("div");
      bar.className = "bar" + (hot ? " hot" : "");
      bar.style.setProperty("--h", Math.round(Math.min(1, h) * 100) + "%");
      frag.appendChild(bar);
      bars.push(bar);
    }
    wave.insertBefore(frag, wave.firstChild);
    var clip = $("#clipbox"), head = $("#playhead"), steps = $$("#peaksteps span");
    var start = (peakAt - peakW * 1.6) / N, width = (peakW * 3.2) / N;
    clip.style.setProperty("--c0", (start * 100) + "%");
    clip.style.setProperty("--cw", (width * 100) + "%");

    var paint = function (p) {
      var played = Math.round(p * N);
      bars.forEach(function (b, n) { b.classList.toggle("played", n < played); });
      head.style.setProperty("--p", (Math.min(1, p) * 100) + "%");
      clip.classList.toggle("on", p > (peakAt + peakW) / N + 0.04);
      var stage = p < 0.2 ? 0 : p < 0.45 ? 1 : p < (peakAt + peakW) / N + 0.04 ? 2 : 3;
      steps.forEach(function (s, n) { s.classList.toggle("on", n <= stage); });
    };
    if (reduce) { paint(1); }
    else {
      var section = $("#peak"), ticking = false;
      var update = function () {
        ticking = false;
        var r = section.getBoundingClientRect();
        var total = section.offsetHeight - window.innerHeight;
        var p = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 1;
        paint(p * 1.08);   // finish slightly before the end so the result rests on screen
      };
      window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
      window.addEventListener("resize", update);
      update();
    }
  }

  /* Credit numbers tick up when they come into view */
  var nums = $$(".plan-credits .n");
  if (nums.length && !reduce && "IntersectionObserver" in window) {
    var io2 = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        io2.unobserve(e.target);
        var el = e.target, to = parseFloat(el.dataset.to), t0 = performance.now(), dur = 700;
        var step = function (t) {
          var q = Math.min(1, (t - t0) / dur), v = to * (1 - Math.pow(1 - q, 3));
          el.textContent = to % 1 ? v.toFixed(1) : String(Math.round(v));
          if (q < 1) requestAnimationFrame(step);
        };
        el.textContent = "0";
        requestAnimationFrame(step);
      });
    }, { threshold: 0.6 });
    nums.forEach(function (n) { io2.observe(n); });
  }

  /* Plans: Monthly / Yearly */
  var plansEl = $(".plans"), billBtns = $$(".bill-opt");
  if (plansEl && billBtns.length) {
    billBtns.forEach(function (b) {
      b.addEventListener("click", function () {
        var bill = b.getAttribute("data-bill");
        if (plansEl.getAttribute("data-bill") === bill) return;
        billBtns.forEach(function (o) { o.setAttribute("aria-pressed", String(o === b)); });
        plansEl.setAttribute("data-bill", bill);
        plansEl.classList.remove("switching"); void plansEl.offsetWidth; plansEl.classList.add("switching");
      });
    });
  }
})();
