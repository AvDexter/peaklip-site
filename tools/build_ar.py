"""Builds the Arabic pages (ar/index.html, ar/privacy.html) from the English ones.

Run after changing the English pages:  python tools/build_ar.py
Every English text must have an Arabic entry below — the script stops and lists any it doesn't know.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

AR = {
 # head / chrome
 "Peaklip — Shorts, Reels and TikToks from your streams": "Peaklip — Shorts و Reels و TikTok من بثوثك",
 "Peaklip turns long streams and gaming videos into ready-to-post Shorts, Reels and TikToks. It finds the best moments, frames webcam and gameplay, adds animated captions and waits for your OK. Video editing software for Windows; your videos stay on your PC.":
   "يحوّل Peaklip البثوث الطويلة وفيديوهات الألعاب إلى Shorts و Reels و TikTok جاهزة للنشر. يجد أفضل اللحظات، ويؤطّر الكاميرا واللعب، ويضيف ترجمة متحركة، وينتظر موافقتك. برنامج تحرير فيديو لـ Windows، وفيديوهاتك تبقى على حاسوبك.",
 "Find the peak. Post the clip. Long videos in, ready-to-post Shorts, Reels and TikToks out.": "اعثر على الذروة. انشر المقطع. فيديوهات طويلة تدخل، و Shorts و Reels و TikTok جاهزة تخرج.",
 "Skip to content": "تخطَّ إلى المحتوى", "Peaklip home": "الصفحة الرئيسية لـ Peaklip", "Main": "الرئيسية", "Footer": "التذييل",
 "How it works": "كيف يعمل", "Features": "المزايا", "Plans": "الخطط", "FAQ": "الأسئلة", "Download ": "تنزيل ", "Soon": "قريباً",
 "Privacy": "الخصوصية", "Account": "حسابي", "Discord": "ديسكورد", "Acceptable use": "الاستخدام المقبول", "© 2026 Peaklip": "© 2026 Peaklip",
 # hero
 "For gaming creators &amp; clippers": "لصنّاع محتوى الألعاب ومحترفي القص",
 "Peaklip turns long streams and videos into ready-to-post Shorts, Reels and TikToks. It finds the best moments, frames the webcam and the gameplay, adds animated captions, and waits for your OK.":
   "يحوّل Peaklip البثوث والفيديوهات الطويلة إلى Shorts و Reels و TikTok جاهزة للنشر. يجد أفضل اللحظات، ويؤطّر الكاميرا واللعب، ويضيف ترجمة متحركة، وينتظر موافقتك.",
 "Download for Windows ": "تنزيل لـ Windows ", "Download for Windows": "تنزيل لـ Windows", "Download": "تنزيل", "Coming soon": "قريباً", "3-day free trial · 10 clips": "تجربة مجانية 3 أيام · 10 مقاطع", "Start free trial": "ابدأ التجربة المجانية", "Terms": "الشروط", "Refunds": "الاسترداد", "Start your free trial in the app: 3 days, 10 clips, card required — cancel before it ends and you pay nothing. Prices in US dollars; taxes are added where required. Payments are handled by Creem.": "ابدأ تجربتك المجانية من التطبيق: 3 أيام و10 مقاطع، وتلزم بطاقة دفع — ألغِ قبل انتهائها ولن تدفع شيئاً. الأسعار بالدولار الأمريكي، وتُضاف الضرائب حيث يلزم. يتولى Creem المدفوعات.", "See how it works": "شاهد كيف يعمل",
 "Windows 10 &amp; 11 · Your videos stay on your PC": "Windows 10 و 11 · فيديوهاتك تبقى على حاسوبك",
 "He jumped off the bridge": "قفز من فوق الجسر",
 # peak story
 "It listens for the moment.": "يُصغي إلى اللحظة.",
 "Peaklip reads the whole video — the words, the shouts, the sudden silence — and finds where it peaks. Then it cuts the clip around it.":
   "يقرأ Peaklip الفيديو كله — الكلمات، والصرخات، والصمت المفاجئ — ويجد أين يبلغ الذروة. ثم يقصّ المقطع حولها.",
 "A waveform of a long video with one loud peak; Peaklip marks it as a 30-second clip.": "موجة صوتية لفيديو طويل فيها ذروة واحدة عالية؛ يحدّدها Peaklip كمقطع من 30 ثانية.",
 "Clip found · 0:30": "وُجد مقطع · 0:30", "Transcribing speech": "تفريغ الكلام", "Measuring reactions": "قياس ردود الفعل",
 "Ranking moments": "ترتيب اللحظات", "Cutting the clip": "قص المقطع",
 # how
 "From a two-hour stream to clips in minutes": "من بث مدته ساعتان إلى مقاطع في دقائق",
 "Peaklip does the slow part. You keep the final say.": "Peaklip يقوم بالجزء البطيء. والكلمة الأخيرة لك.",
 "Bring a video": "أحضر فيديو",
 "Import video files from your PC — your own streams, recordings or uploads. Drag and drop, any length.":
   "استورد ملفات الفيديو من حاسوبك — بثوثك أو تسجيلاتك أو مقاطعك المرفوعة. اسحب وأفلت، بأي طول.",
 "Find the moments": "اعثر على اللحظات",
 "It transcribes the speech, measures reactions and loudness, and ranks the best moments automatically, on your PC.":
   "يفرّغ الكلام، ويقيس ردود الفعل وارتفاع الصوت، ويرتّب أفضل اللحظات تلقائياً على حاسوبك.",
 "Make them yours": "اجعلها بأسلوبك",
 "Pick a caption style, fix words, trim, reframe, add music or your watermark — with a live preview.":
   "اختر نمط الترجمة، صحّح الكلمات، قصّ، أعد التأطير، أضف موسيقى أو علامتك المائية — مع معاينة مباشرة.",
 "Approve and post": "وافق وانشر",
 "Post to YouTube Shorts and Instagram Reels from the app, or to TikTok with one paste. Nothing goes out without you.":
   "انشر على YouTube Shorts و Instagram Reels من التطبيق، أو على TikTok بلصقة واحدة. لا يُنشر شيء دونك.",
 # features
 "Everything a short clip needs": "كل ما يحتاجه المقطع القصير", "Vertical 1080 × 1920 clips that look made by hand.": "مقاطع عمودية 1080 × 1920 تبدو كأنها صُنعت يدوياً.",
 "Webcam + gameplay layout": "تخطيط الكاميرا + اللعب",
 "Finds your webcam and stacks it above the action automatically. You can change the framing for any clip.":
   "يجد كاميرتك ويضعها فوق اللعب تلقائياً. ويمكنك تغيير التأطير لأي مقطع.",
 "Animated captions": "ترجمة متحركة",
 "Ten caption styles with the spoken word highlighted, plus a hook title for the first seconds.":
   "عشرة أنماط للترجمة مع تمييز الكلمة المنطوقة، وعنوان جذب في الثواني الأولى.",
 "Titles, captions, hashtags": "عناوين ونصوص ووسوم",
 "Post text written for each platform from what's said in the clip, ready to check and edit.":
   "نص منشور مكتوب لكل منصة مما يُقال في المقطع، جاهز للمراجعة والتعديل — وبالعربية للمقاطع العربية.",
 "Edit any clip": "عدّل أي مقطع",
 "Trim, fix caption words, zoom in on big reactions, add your own music under the voice, and your logo or @handle.":
   "قصّ، صحّح كلمات الترجمة، كبّر عند ردود الفعل الكبيرة، أضف موسيقاك تحت الصوت، وشعارك أو @معرّفك.",
 "Private by design": "خصوصية من الأساس",
 "Your videos stay on your PC. Transcription and editing run locally — we never receive your footage. Smart picks only sends a few small still frames and the words of each candidate moment to be judged, and you can switch it off.":
   "فيديوهاتك تبقى على حاسوبك. التفريغ والتحرير يعملان محلياً — لا نستلم لقطاتك أبداً. يرسل الاختيار الذكي فقط بضع صور ثابتة صغيرة وكلمات كل لحظة مرشّحة لتقييمها، ويمكنك إيقافه.",
 "You approve every post": "أنت توافق على كل منشور",
 "Every clip and its text waits for your OK. Nothing is ever published automatically.": "كل مقطع ونصه ينتظران موافقتك. لا يُنشر شيء تلقائياً أبداً.",
 # plans
 "Simple plans. One credit per clip.": "خطط بسيطة. رصيد واحد لكل مقطع.",
 "Every clip costs one credit — 15, 30 or 60 seconds. Pick the plan that matches how much you post.":
   "كل مقطع يكلّف رصيداً واحداً — 15 أو 30 أو 60 ثانية. اختر الخطة التي تناسب كمية نشرك.",
 "Starter": "المبتدئ", "Creator": "صانع المحتوى", "Pro": "المحترف", "Recommended": "موصى بها",
 "For starters.": "للمبتدئين.", "For creators who post every day, across all their platforms.": "لصنّاع المحتوى الذين ينشرون كل يوم على كل منصاتهم.",
 "For clippers and teams turning out clips at volume.": "لمحترفي القص والفرق التي تصنع مقاطع بكميات كبيرة.",
 "/ month": "/ شهرياً", " credits a month": " رصيد شهرياً", "Every feature included": "كل المزايا مشمولة", "Free trial to start": "تجربة مجانية للبدء",
 "Up to 120 clips a month": "حتى 120 مقطعاً شهرياً", "Up to 300 clips a month": "حتى 300 مقطع شهرياً", "Up to 750 clips a month": "حتى 750 مقطعاً شهرياً",
 "Plans start when Peaklip launches. Prices in US dollars; local taxes may apply.": "تبدأ الخطط عند إطلاق Peaklip. الأسعار بالدولار الأمريكي؛ وقد تُضاف الضرائب المحلية.",
 # faq
 "Questions": "أسئلة شائعة", "Does it work on Mac?": "هل يعمل على Mac؟", "Not yet — Peaklip is a Windows 10 and 11 app for now.": "ليس بعد — Peaklip تطبيق لـ Windows 10 و 11 حالياً.",
 "Do I need a powerful PC?": "هل أحتاج حاسوباً قوياً؟",
 "It runs on most modern Windows PCs. An NVIDIA graphics card makes transcription and rendering much faster, but it isn't required.":
   "يعمل على معظم حواسيب Windows الحديثة. بطاقة رسوميات NVIDIA تجعل التفريغ والتصيير أسرع بكثير، لكنها ليست شرطاً.",
 "Can I clip anyone's videos?": "هل يمكنني قص فيديوهات أي شخص؟",
 "Only videos you own or have the creator's permission to clip and post. Peaklip works with video files on your PC and doesn't download anything from YouTube or other sites. To clip your own uploads, download them from YouTube Studio first.":
   "فقط الفيديوهات التي تملكها أو لديك إذن صاحبها بقصّها ونشرها. يعمل Peaklip على ملفات الفيديو الموجودة على حاسوبك ولا ينزّل أي شيء من YouTube أو مواقع أخرى. لقص مقاطعك المرفوعة، نزّلها أولاً من YouTube Studio.",
 "Does it post automatically?": "هل ينشر تلقائياً؟",
 "No. You approve every clip and its text first. YouTube Shorts and Instagram Reels can be posted from the app; for TikTok, Peaklip gets everything ready and you post it with one paste.":
   "لا. توافق أولاً على كل مقطع ونصه. يمكن النشر على YouTube Shorts و Instagram Reels من التطبيق؛ أما TikTok فيجهّز Peaklip كل شيء وتنشره أنت بلصقة واحدة.",
 "What does a credit buy?": "ماذا يشتري الرصيد؟", "One clip. A 15-, 30- or 60-second clip each costs one credit when it's made.": "مقطعاً واحداً. كل مقطع من 15 أو 30 أو 60 ثانية يكلّف رصيداً واحداً عند صنعه.",
 "Where do my videos go?": "أين تذهب فيديوهاتي؟", "Nowhere — they stay on your PC. With Smart picks on, a few small still frames and the words said in each candidate moment are sent to be judged; never the video, and nothing is kept. Your account stores your name, email and sign-in details.": "لا مكان — تبقى على حاسوبك. عند تشغيل الاختيار الذكي تُرسَل بضع صور ثابتة صغيرة والكلمات المنطوقة في كل لحظة مرشّحة لتقييمها؛ لا يُرسَل الفيديو أبداً ولا يُحفظ شيء. يحفظ حسابك اسمك وبريدك وبيانات الدخول.",
 "How do I install it?": "كيف أثبّته؟", "Download the installer and run it. Windows may show a SmartScreen warning because the installer isn't code-signed yet — click “More info”, then “Run anyway”. Peaklip needs 64-bit Windows 10 or 11.": "نزّل ملف التثبيت وشغّله. قد يعرض Windows تحذير SmartScreen لأن ملف التثبيت غير موقّع رقمياً بعد — اضغط «مزيد من المعلومات» ثم «التشغيل على أي حال». يحتاج Peaklip إلى Windows 10 أو 11 بنظام 64 بت.", "Get Peaklip for Windows 10 and 11.": "احصل على Peaklip لـ Windows 10 و 11.", "When can I download it?": "متى يمكنني تنزيله؟", "Soon. The app is in private testing; the download will appear right here when it's ready.": "قريباً. التطبيق في اختبار خاص؛ وسيظهر التنزيل هنا عندما يجهز.",
 "Your best moments, on every feed.": "أفضل لحظاتك، في كل منصة.", "Peaklip is in private testing. The Windows download is coming soon.": "Peaklip في اختبار خاص. تنزيل Windows قريباً.",
}

HERO_EN = re.compile(r"<h1>.*?</h1>", re.S)
HERO_AR = ('<h1><span class="rise" style="animation-delay:40ms">اعثر</span> <span class="rise" style="animation-delay:110ms">على</span> '
           '<span class="rise" style="animation-delay:180ms">الذروة.</span><br><span class="hl"><span class="rise" style="animation-delay:300ms">انشر</span> '
           '<span class="rise" style="animation-delay:370ms">المقطع.</span></span></h1>')


def translate_html(html: str, missing: set[str]) -> str:
    html = HERO_EN.sub(HERO_AR, html, count=1)
    html = re.sub(r'<div class="caption" id="cap">.*?</div>',
                  '<div class="caption" id="cap"><span>لا</span> <span>يمكن</span> <span>أنه</span></div>', html, count=1, flags=re.S)

    def text_node(m: re.Match[str]) -> str:
        raw = m.group(1)
        if not re.search(r"[A-Za-z]", raw) or raw.strip() in ("Peaklip", "hello@peaklip.com") or raw.strip().startswith("$"):
            return m.group(0)
        key = raw if raw in AR else raw.strip()
        if key in AR:
            return ">" + raw.replace(key, AR[key]) + "<"
        missing.add(raw)
        return m.group(0)

    def attr(m: re.Match[str]) -> str:
        name, val = m.group(1), m.group(2)
        if val in AR:
            return f'{name}="{AR[val]}"'
        if re.search(r"[A-Za-z]{3}", val) and name in ("aria-label", "content", "alt", "title"):
            if not val.startswith(("http", "#", "width=", "website")):
                missing.add(val)
        return m.group(0)

    body_start = html.index("<body>")
    head, body = html[:body_start], html[body_start:]
    head = re.sub(r"<title>(.*?)</title>", lambda m: f"<title>{AR.get(m.group(1), m.group(1))}</title>", head)
    head = re.sub(r'(content)="([^"]*)"', attr, head)
    body = re.sub(r"<script.*?</script>", lambda m: m.group(0).replace("<", "\x00"), body, flags=re.S)
    body = re.sub(r">([^<>]+)<", text_node, body)
    body = re.sub(r'(aria-label|alt|title)="([^"]*)"', attr, body)
    return (head + body).replace("\x00", "<")


def localize(html: str, page: str) -> str:
    html = html.replace('<html lang="en">', '<html lang="ar" dir="rtl">')
    html = html.replace('<div class="wave-box">', '<div class="wave-box" dir="ltr">')   # a timeline runs left to right
    html = re.sub(r'(href|src)="(?!https?:|mailto:|#|\.\./)(assets/[^"]*|favicon\.svg)"', r'\1="../\2"', html)
    html = html.replace('href="./"', 'href="./"').replace('href="./#', 'href="./#')
    for tag in (f'<link rel="canonical" href="https://peaklip.com/{page}">', f'<meta property="og:url" content="https://peaklip.com/{page}">'):
        html = html.replace(tag, tag.replace("peaklip.com/", "peaklip.com/ar/"))
    html = re.sub(r'<a class="lang"[^>]*>.*?</a>\n\s*', "", html)
    switch = f'<a class="lang" href="../{page}" hreflang="en" lang="en">English</a>'
    # Put "English" where the English page has "العربية": right after the main nav, before any header button.
    html, n = re.subn(r'(</nav>\n)(\s*)', lambda m: f"{m.group(1)}{m.group(2)}{switch}\n{m.group(2)}", html, count=1)
    if n != 1 or switch not in html:
        raise SystemExit(f"build_ar: could not place the English switch on {page}")
    return html


def english_switch(html: str, page: str) -> str:
    """Adds the 'العربية' link and hreflang alternates to an English page (idempotent)."""
    if 'class="lang"' not in html:
        link = f'<a class="lang" href="ar/{page}" hreflang="ar" lang="ar">العربية</a>'
        if 'btn-soon btn-sm' in html:
            html = html.replace('<a class="btn btn-soon btn-sm"', link + '\n    <a class="btn btn-soon btn-sm"', 1)
        else:
            html = html.replace('</nav>\n  </div>\n</header>', '</nav>\n    ' + link + '\n  </div>\n</header>', 1)
    if 'hreflang="ar"' not in html.split("</head>")[0]:
        alt = (f'  <link rel="alternate" hreflang="en" href="https://peaklip.com/{page}">\n'
               f'  <link rel="alternate" hreflang="ar" href="https://peaklip.com/ar/{page}">\n')
        html = html.replace("</head>", alt + "</head>", 1)
    return html


def main() -> None:
    from privacy_ar import PRIVACY_AR  # the privacy page is translated as a whole document
    (ROOT / "ar").mkdir(exist_ok=True)
    missing: set[str] = set()
    for page in ("index.html",):
        src = english_switch((ROOT / page).read_text(encoding="utf-8"), page if page != "index.html" else "")
        (ROOT / page).write_text(src, encoding="utf-8")
        out = localize(translate_html(src, missing), "")
        (ROOT / "ar" / page).write_text(out, encoding="utf-8")
    priv = english_switch((ROOT / "privacy.html").read_text(encoding="utf-8"), "privacy.html")
    (ROOT / "privacy.html").write_text(priv, encoding="utf-8")
    (ROOT / "ar" / "privacy.html").write_text(PRIVACY_AR, encoding="utf-8")
    # Terms and refunds: the English pages get the language switch; the Arabic ones reuse the Arabic privacy
    # page's frame (header, footer) around their own translated text.
    from legal_ar import (
        AUP_AR,
        AUP_AR_DESC,
        AUP_AR_TITLE,
        REFUNDS_AR,
        REFUNDS_AR_DESC,
        REFUNDS_AR_TITLE,
        TERMS_AR,
        TERMS_AR_DESC,
        TERMS_AR_TITLE,
    )
    frame_head, rest = PRIVACY_AR.split('<main id="main" class="wrap">', 1)
    frame_tail = rest.split("</main>", 1)[1]
    for page, title, desc, body in (("terms.html", TERMS_AR_TITLE, TERMS_AR_DESC, TERMS_AR),
                                    ("refunds.html", REFUNDS_AR_TITLE, REFUNDS_AR_DESC, REFUNDS_AR),
                                    ("acceptable-use.html", AUP_AR_TITLE, AUP_AR_DESC, AUP_AR)):
        en = english_switch((ROOT / page).read_text(encoding="utf-8"), page)
        (ROOT / page).write_text(en, encoding="utf-8")
        h = re.sub(r"<title>.*?</title>", f"<title>{title} · Peaklip</title>", frame_head, count=1)
        h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', h, count=1)
        h = h.replace("privacy.html", page)
        out = h + '<main id="main" class="wrap">\n  <article class="legal">\n' + body + "\n  </article>\n</main>" + frame_tail
        (ROOT / "ar" / page).write_text(out, encoding="utf-8")
    if missing:
        print("No Arabic for:", *sorted(missing), sep="\n  ")
        sys.exit(1)
    print("ar/ pages written")


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))
    main()
