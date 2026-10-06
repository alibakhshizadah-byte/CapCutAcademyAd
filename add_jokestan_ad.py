from pathlib import Path

site = Path("index.html")

html = site.read_text(encoding="utf-8")

ad = r'''
<!-- JOKESTAN WHATSAPP CHANNEL AD -->
<section id="jokestan-ad" class="jokestan-ad" dir="rtl">
  <div class="jokestan-content">
    <div class="jokestan-icon">🤣</div>

    <div class="jokestan-text">
      <div class="jokestan-badge">پیشنهاد ویژه</div>
      <h2>🤣 جوکستان</h2>
      <p>هر روز جوک‌های خنده‌دار و سرگرم‌کننده را در کانال واتساپ دنبال کن!</p>
    </div>

    <a
      class="jokestan-button"
      href="https://whatsapp.com/channel/0029Vb7HtHYHbFVDt9xBfi2N"
      target="_blank"
      rel="noopener noreferrer"
    >
      ورود به کانال
    </a>
  </div>
</section>

<style>
.jokestan-ad {
  width: min(92%, 900px);
  margin: 30px auto;
  padding: 0;
  border-radius: 24px;
  overflow: hidden;
  background: linear-gradient(135deg, #111827, #1f2937);
  box-shadow: 0 12px 35px rgba(0,0,0,.18);
  color: #fff;
  font-family: inherit;
}

.jokestan-content {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px;
}

.jokestan-icon {
  width: 70px;
  height: 70px;
  min-width: 70px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 20px;
  background: rgba(255,255,255,.12);
  font-size: 38px;
}

.jokestan-text {
  flex: 1;
}

.jokestan-badge {
  display: inline-block;
  margin-bottom: 5px;
  padding: 4px 10px;
  border-radius: 20px;
  background: rgba(255,255,255,.12);
  font-size: 12px;
}

.jokestan-text h2 {
  margin: 2px 0 6px;
  font-size: 25px;
}

.jokestan-text p {
  margin: 0;
  opacity: .85;
  line-height: 1.7;
}

.jokestan-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 20px;
  border-radius: 14px;
  background: #25D366;
  color: #fff !important;
  text-decoration: none !important;
  font-weight: 700;
  white-space: nowrap;
  transition: transform .2s, opacity .2s;
}

.jokestan-button:hover {
  transform: translateY(-2px);
  opacity: .9;
}

@media (max-width: 650px) {
  .jokestan-content {
    flex-direction: column;
    text-align: center;
  }

  .jokestan-button {
    width: 100%;
  }
}
</style>
<!-- END JOKESTAN WHATSAPP CHANNEL AD -->
'''

# Insert before </body> so the existing site remains intact.
if "</body>" not in html.lower():
    raise SystemExit("خطا: تگ </body> در index.html پیدا نشد.")

if "id=\"jokestan-ad\"" in html:
    raise SystemExit("تبلیغ جوکستان قبلاً به سایت اضافه شده است.")

pos = html.lower().rfind("</body>")
html = html[:pos] + ad + "\n" + html[pos:]

site.write_text(html, encoding="utf-8")

print("تبلیغ کانال 🤣 جوکستان با موفقیت به index.html اضافه شد.")
