from pathlib import Path
import re
from datetime import datetime

FILE = Path("index.html")

# بکاپ
backup = FILE.with_name(
    f"index.before-floating-fix-{datetime.now().strftime('%Y%m%d-%H%M%S')}.html"
)
backup.write_text(FILE.read_text(encoding="utf-8"), encoding="utf-8")

html = FILE.read_text(encoding="utf-8")

# ---------------------------------------------------------
# 1. حذف تمام نسخه‌های قبلی دکمه شناور جوکستان
# ---------------------------------------------------------
html = re.sub(
    r'<!-- JOKESTAN FLOATING WHATSAPP BUTTON -->.*?<!-- END JOKESTAN FLOATING WHATSAPP BUTTON -->',
    '',
    html,
    flags=re.DOTALL
)

# ---------------------------------------------------------
# 2. اگر cp-sticky چند بار در HTML آمده، فقط اولین دکمه را نگه دار
# ---------------------------------------------------------
pattern = re.compile(
    r'<a\b[^>]*class=["\'][^"\']*\bcp-sticky\b[^"\']*["\'][^>]*>.*?</a>',
    re.IGNORECASE | re.DOTALL
)

matches = list(pattern.finditer(html))

if len(matches) > 1:
    # همه نسخه‌های تکراری به جز اولین نسخه حذف شوند
    for match in reversed(matches[1:]):
        html = html[:match.start()] + html[match.end():]

# ---------------------------------------------------------
# 3. دکمه شناور جوکستان
# ---------------------------------------------------------
jokestan = r'''
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
/* جلوگیری از تداخل دکمه‌ها */
.cp-sticky {
  z-index: 99998 !important;
}

.jokestan-floating {
  position: fixed;
  right: 18px;
  bottom: 22px;
  z-index: 99999;

  display: flex;
  align-items: center;
  gap: 9px;

  padding: 9px 14px 9px 10px;
  border-radius: 50px;

  background: linear-gradient(135deg, #25D366, #128C7E);
  color: white !important;
  text-decoration: none !important;

  box-shadow: 0 7px 24px rgba(0,0,0,.25);

  font-family: inherit;

  transition:
    transform .2s ease,
    box-shadow .2s ease;
}

.jokestan-floating:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 28px rgba(0,0,0,.32);
}

.jokestan-floating-icon {
  width: 42px;
  height: 42px;
  min-width: 42px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 50%;
  background: rgba(255,255,255,.18);

  font-size: 24px;
}

.jokestan-floating-text {
  display: flex;
  flex-direction: column;
  line-height: 1.15;
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
    right: 10px;
    bottom: 15px;
    padding: 7px 11px 7px 8px;
  }

  .jokestan-floating-icon {
    width: 38px;
    height: 38px;
    min-width: 38px;
    font-size: 22px;
  }

  .jokestan-floating-text strong {
    font-size: 13px;
  }

  .jokestan-floating-text small {
    font-size: 9px;
  }
}
</style>
<!-- END JOKESTAN FLOATING WHATSAPP BUTTON -->
'''

# ---------------------------------------------------------
# 4. اضافه کردن قبل از </body>
# ---------------------------------------------------------
pos = html.lower().rfind("</body>")

if pos == -1:
    raise SystemExit("ERROR: </body> پیدا نشد.")

html = html[:pos] + jokestan + "\n" + html[pos:]

FILE.write_text(html, encoding="utf-8")

# ---------------------------------------------------------
# گزارش
# ---------------------------------------------------------
remaining = len(
    re.findall(
        r'class=["\'][^"\']*\bcp-sticky\b',
        html,
        re.IGNORECASE
    )
)

jokestan_count = html.count("jokestan-floating")

print()
print("======================================")
print("اصلاح دکمه‌های شناور انجام شد")
print("======================================")
print(f"دکمه‌های CapCut Academy: {remaining}")
print(f"دکمه‌های Jokestan: {jokestan_count}")
print(f"Backup: {backup.name}")
print("======================================")
