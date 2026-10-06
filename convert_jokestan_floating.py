from pathlib import Path
import re

file = Path("index.html")
html = file.read_text(encoding="utf-8")

# حذف بخش تبلیغ قبلی
html = re.sub(
    r'<!-- JOKESTAN WHATSAPP CHANNEL AD -->.*?<!-- END JOKESTAN WHATSAPP CHANNEL AD -->',
    '',
    html,
    flags=re.DOTALL
)

floating = r'''
<!-- JOKESTAN FLOATING WHATSAPP BUTTON -->
<a
  href="https://whatsapp.com/channel/0029Vb7HtHYHbFVDt9xBfi2N"
  class="jokestan-floating"
  target="_blank"
  rel="noopener noreferrer"
  aria-label="ورود به کانال واتساپ جوکستان"
>
  <span class="jokestan-floating-icon">🤣</span>
  <span class="jokestan-floating-text">
    <strong>جوکستان</strong>
    <small>کانال واتساپ</small>
  </span>
</a>

<style>
.jokestan-floating {
  position: fixed;
  left: 18px;
  bottom: 22px;
  z-index: 99999;

  display: flex;
  align-items: center;
  gap: 10px;

  padding: 10px 15px 10px 11px;
  border-radius: 50px;

  background: linear-gradient(135deg, #25D366, #128C7E);
  color: #fff !important;
  text-decoration: none !important;

  box-shadow: 0 8px 25px rgba(0,0,0,.28);

  font-family: inherit;

  transition:
    transform .2s ease,
    box-shadow .2s ease;
}

.jokestan-floating:hover {
  transform: translateY(-4px) scale(1.03);
  box-shadow: 0 12px 30px rgba(0,0,0,.35);
}

.jokestan-floating-icon {
  width: 42px;
  height: 42px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 50%;
  background: rgba(255,255,255,.18);

  font-size: 25px;
}

.jokestan-floating-text {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}

.jokestan-floating-text strong {
  font-size: 15px;
}

.jokestan-floating-text small {
  margin-top: 3px;
  font-size: 10px;
  opacity: .85;
}

@media (max-width: 600px) {
  .jokestan-floating {
    left: 12px;
    bottom: 15px;
    padding: 8px 12px 8px 9px;
  }

  .jokestan-floating-icon {
    width: 38px;
    height: 38px;
    font-size: 22px;
  }

  .jokestan-floating-text strong {
    font-size: 14px;
  }
}
</style>
<!-- END JOKESTAN FLOATING WHATSAPP BUTTON -->
'''

# اضافه کردن قبل از body
pos = html.lower().rfind("</body>")
if pos == -1:
    raise SystemExit("تگ </body> پیدا نشد.")

html = html[:pos] + floating + "\n" + html[pos:]

file.write_text(html, encoding="utf-8")

print("دکمه شناور 🤣 جوکستان با موفقیت اضافه شد.")
