#!/usr/bin/env python3
import os, re, subprocess, sys

BASE = "https://futbol.eurohack.shop"
ROOT = "/Users/braiannavarrete/Downloads/Opencode/sitio-referencia"
HTML = os.path.join(ROOT, "index.html")

with open(HTML, "r", encoding="utf-8") as f:
    html = f.read()

urls = set()
# href/src simples
for m in re.finditer(r'(?:href|src)="([^"]+)"', html):
    urls.add(m.group(1))
# srcset (múltiples URLs con descriptores)
for m in re.finditer(r'srcset="([^"]+)"', html):
    for part in m.group(1).split(","):
        part = part.strip()
        if part:
            urls.add(part.split()[0])

downloaded, failed = [], []
for u in sorted(urls):
    if not u.startswith("/"):
        continue  # externos (stripe, facebook, mailto, #anclas)
    path = os.path.normpath(os.path.join(ROOT, u.lstrip("/")))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path) and os.path.getsize(path) > 0:
        continue
    r = subprocess.run(["curl", "-sL", "--fail", "-o", path, BASE + u],
                       capture_output=True)
    if r.returncode == 0 and os.path.exists(path) and os.path.getsize(path) > 0:
        downloaded.append(u)
    else:
        failed.append(u)

# Reescribir rutas absolutas -> relativas
new_html = re.sub(r'="(/[^"]+)"', lambda m: '=".' + m.group(1) + '"', html)
with open(HTML, "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"Descargados: {len(downloaded)}")
if failed:
    print("Fallidos:", *failed, sep="\n  ")