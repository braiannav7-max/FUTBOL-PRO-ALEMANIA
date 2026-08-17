#!/usr/bin/env python3
"""Generador de PDFs FußballPro Masterpaket.
Cada ficha = 1 página A4 premium. Pipeline: HTML -> Chrome headless --print-to-pdf."""
import html as H
import os, re, subprocess, json

SRC = os.path.dirname(os.path.abspath(__file__))
PROD = os.path.dirname(SRC)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LOGO = os.path.join(SRC, "logo.png")

GREEN = "#7ED957"; INK = "#0B1210"; GOLD = "#C9A84C"; PAPER = "#F4F0E6"

DIAGRAMS = {}
DIAGRAMS["slalom"] = """
<svg viewBox="0 0 700 300" class="diag">
 <rect x="2" y="2" width="696" height="296" rx="8" fill="#7FB06B"/>
 <rect x="2" y="2" width="696" height="296" rx="8" fill="none" stroke="#fff" stroke-width="3"/>
 <path d="M 60 250 L 210 250" stroke="#2A2A26" stroke-width="6" marker-end="url(#a)"/>
 <path d="M 230 250 C 270 250 270 200 320 200 S 370 250 410 250 S 460 200 510 200 S 560 250 600 250" fill="none" stroke="#2A2A26" stroke-width="6" marker-end="url(#a)"/>
 <g fill="#E8873C"><polygon points="240,70 228,102 252,102"/><polygon points="300,70 288,102 312,102"/><polygon points="360,70 348,102 372,102"/><polygon points="420,70 408,102 432,102"/><polygon points="480,70 468,102 492,102"/></g>
 <g font-family="Arial" font-weight="800" font-size="24" text-anchor="middle">
  <circle cx="90" cy="60" r="24" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="90" y="69">1</text>
  <circle cx="280" cy="240" r="24" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="280" y="249">2</text>
  <circle cx="600" cy="130" r="24" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="600" y="139">3</text>
 </g>
 <circle cx="620" cy="250" r="18" fill="#fff" stroke="#0B1210" stroke-width="4"/>
 <defs><marker id="a" markerWidth="12" markerHeight="12" refX="8" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#2A2A26"/></marker></defs>
</svg>"""

DIAGRAMS["rondo"] = """
<svg viewBox="0 0 700 300" class="diag">
 <rect x="2" y="2" width="696" height="296" rx="8" fill="#7FB06B"/>
 <rect x="2" y="2" width="696" height="296" rx="8" fill="none" stroke="#fff" stroke-width="3"/>
 <circle cx="350" cy="150" r="100" fill="none" stroke="#2A2A26" stroke-width="5" stroke-dasharray="14 10"/>
 <g font-family="Arial" font-weight="800" font-size="23" text-anchor="middle">
  <circle cx="350" cy="52" r="23" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="350" y="61">1</text>
  <circle cx="446" cy="100" r="23" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="446" y="109">2</text>
  <circle cx="254" cy="100" r="23" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="254" y="109">3</text>
  <circle cx="446" cy="200" r="23" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="446" y="209">4</text>
  <circle cx="254" cy="200" r="23" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="254" y="209">5</text>
  <circle cx="350" cy="150" r="20" fill="#F2B84B" stroke="#0B1210" stroke-width="4"/><text x="350" y="158">P</text>
  <circle cx="350" cy="248" r="20" fill="#F2B84B" stroke="#0B1210" stroke-width="4"/><text x="350" y="256">P</text>
 </g>
</svg>"""

DIAGRAMS["gates"] = """
<svg viewBox="0 0 700 300" class="diag">
 <rect x="2" y="2" width="696" height="296" rx="8" fill="#7FB06B"/>
 <rect x="2" y="2" width="696" height="296" rx="8" fill="none" stroke="#fff" stroke-width="3"/>
 <g stroke="#2A2A26" stroke-width="5" marker-end="url(#a)">
  <path d="M 80 250 L 180 250"/><path d="M 200 250 L 300 250"/>
  <path d="M 320 250 L 420 250"/><path d="M 440 250 L 540 250"/>
  <path d="M 560 250 L 620 250"/>
 </g>
 <g fill="#E8873C">
  <polygon points="95,270 82,235 108,235"/><polygon points="215,270 202,235 228,235"/><polygon points="335,270 322,235 348,235"/><polygon points="455,270 442,235 468,235"/><polygon points="575,270 562,235 588,235"/>
  <polygon points="150,235 138,200 162,200"/><polygon points="270,235 258,200 282,200"/><polygon points="390,235 378,200 402,200"/><polygon points="510,235 498,200 522,200"/>
 </g>
 <g font-family="Arial" font-weight="800" font-size="24" text-anchor="middle">
  <circle cx="100" cy="70" r="24" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="100" y="79">1</text>
  <circle cx="350" cy="120" r="24" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="350" y="129">2</text>
  <circle cx="600" cy="70" r="24" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="600" y="79">3</text>
 </g>
 <defs><marker id="a" markerWidth="12" markerHeight="12" refX="8" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#2A2A26"/></marker></defs>
</svg>"""

DIAGRAMS["field"] = """
<svg viewBox="0 0 700 300" class="diag">
 <rect x="2" y="2" width="696" height="296" rx="8" fill="#7FB06B"/>
 <rect x="2" y="2" width="696" height="296" rx="8" fill="none" stroke="#fff" stroke-width="3"/>
 <line x1="350" y1="2" x2="350" y2="298" stroke="#fff" stroke-width="3"/>
 <circle cx="350" cy="150" r="38" fill="none" stroke="#fff" stroke-width="3"/>
 <rect x="2" y="62" width="150" height="176" fill="none" stroke="#fff" stroke-width="3"/>
 <rect x="548" y="62" width="150" height="176" fill="none" stroke="#fff" stroke-width="3"/>
 <g stroke="#2A2A26" stroke-width="5" marker-end="url(#a)">
  <path d="M 160 100 L 330 100"/><path d="M 370 100 L 540 100"/>
 </g>
 <g font-family="Arial" font-weight="800" font-size="24" text-anchor="middle">
  <circle cx="80" cy="80" r="24" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="80" y="89">1</text>
  <circle cx="350" cy="45" r="24" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="350" y="54">2</text>
  <circle cx="620" cy="220" r="24" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="620" y="229">3</text>
 </g>
 <defs><marker id="a" markerWidth="12" markerHeight="12" refX="8" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#2A2A26"/></marker></defs>
</svg>"""

DIAGRAMS["grid"] = """
<svg viewBox="0 0 700 300" class="diag">
 <rect x="2" y="2" width="696" height="296" rx="8" fill="#7FB06B"/>
 <rect x="2" y="2" width="696" height="296" rx="8" fill="none" stroke="#fff" stroke-width="3"/>
 <line x1="235" y1="2" x2="235" y2="298" stroke="#fff" stroke-width="3"/>
 <line x1="468" y1="2" x2="468" y2="298" stroke="#fff" stroke-width="3"/>
 <line x1="2" y1="150" x2="698" y2="150" stroke="#fff" stroke-width="3"/>
 <g font-family="Arial" font-weight="800" font-size="22" text-anchor="middle">
  <circle cx="118" cy="75" r="23" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="118" y="84">1</text>
  <circle cx="351" cy="75" r="23" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="351" y="84">2</text>
  <circle cx="584" cy="75" r="23" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="584" y="84">3</text>
  <circle cx="118" cy="225" r="23" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="118" y="234">4</text>
  <circle cx="351" cy="225" r="23" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="351" y="234">5</text>
  <circle cx="584" cy="225" r="23" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="584" y="234">6</text>
 </g>
 <circle cx="600" cy="80" r="16" fill="#fff" stroke="#0B1210" stroke-width="4"/>
</svg>"""

DIAGRAMS["goals"] = """
<svg viewBox="0 0 700 300" class="diag">
 <rect x="2" y="2" width="696" height="296" rx="8" fill="#7FB06B"/>
 <rect x="2" y="2" width="696" height="296" rx="8" fill="none" stroke="#fff" stroke-width="3"/>
 <line x1="350" y1="2" x2="350" y2="298" stroke="#fff" stroke-width="3"/>
 <circle cx="350" cy="150" r="38" fill="none" stroke="#fff" stroke-width="3"/>
 <rect x="2" y="62" width="150" height="176" fill="none" stroke="#fff" stroke-width="3"/>
 <rect x="548" y="62" width="150" height="176" fill="none" stroke="#fff" stroke-width="3"/>
 <g stroke="#2A2A26" stroke-width="5" marker-end="url(#a)">
  <path d="M 150 240 C 200 240 220 180 280 180"/><path d="M 550 60 C 500 60 480 120 420 120"/>
 </g>
 <g font-family="Arial" font-weight="800" font-size="24" text-anchor="middle">
  <circle cx="200" cy="200" r="24" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="200" y="209">1</text>
  <circle cx="350" cy="60" r="24" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="350" y="69">2</text>
  <circle cx="500" cy="240" r="24" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="500" y="249">3</text>
 </g>
 <defs><marker id="a" markerWidth="12" markerHeight="12" refX="8" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#2A2A26"/></marker></defs>
</svg>"""

DIAGRAMS["stations"] = """
<svg viewBox="0 0 700 300" class="diag">
 <rect x="2" y="2" width="696" height="296" rx="8" fill="#7FB06B"/>
 <rect x="2" y="2" width="696" height="296" rx="8" fill="none" stroke="#fff" stroke-width="3"/>
 <g stroke="#fff" stroke-width="3">
  <line x1="180" y1="2" x2="180" y2="298"/><line x1="520" y1="2" x2="520" y2="298"/>
 </g>
 <g font-family="Arial" font-weight="800" font-size="22" text-anchor="middle">
  <circle cx="90" cy="120" r="23" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="90" y="129">A</text>
  <circle cx="90" cy="200" r="23" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="90" y="209">1</text>
  <circle cx="350" cy="80" r="23" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="350" y="89">B</text>
  <circle cx="350" cy="160" r="23" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="350" y="169">2</text>
  <circle cx="350" cy="240" r="23" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="350" y="249">3</text>
  <circle cx="610" cy="120" r="23" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="610" y="129">C</text>
  <circle cx="610" cy="200" r="23" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="610" y="209">4</text>
 </g>
 <g stroke="#2A2A26" stroke-width="5" marker-end="url(#a)">
  <path d="M 140 200 L 300 200"/><path d="M 420 160 L 560 160"/>
 </g>
 <defs><marker id="a" markerWidth="12" markerHeight="12" refX="8" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#2A2A26"/></marker></defs>
</svg>"""

DIAGRAMS["channel"] = """
<svg viewBox="0 0 700 300" class="diag">
 <rect x="2" y="2" width="696" height="296" rx="8" fill="#7FB06B"/>
 <rect x="2" y="2" width="696" height="296" rx="8" fill="none" stroke="#fff" stroke-width="3"/>
 <g stroke="#fff" stroke-width="3">
  <line x1="235" y1="2" x2="235" y2="298"/><line x1="468" y1="2" x2="468" y2="298"/>
 </g>
 <g stroke="#2A2A26" stroke-width="5" marker-end="url(#a)">
  <path d="M 70 250 C 70 170 110 160 110 110 C 110 60 170 50 170 30"/>
  <path d="M 300 250 C 300 170 260 160 260 110 C 260 60 320 50 350 30"/>
  <path d="M 500 250 C 500 170 540 160 540 110 C 540 60 600 50 630 30"/>
 </g>
 <g font-family="Arial" font-weight="800" font-size="24" text-anchor="middle">
  <circle cx="70" cy="270" r="24" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="70" y="279">1</text>
  <circle cx="300" cy="270" r="24" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="300" y="279">2</text>
  <circle cx="500" cy="270" r="24" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="500" y="279">3</text>
 </g>
 <defs><marker id="a" markerWidth="12" markerHeight="12" refX="8" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#2A2A26"/></marker></defs>
</svg>"""

DIAGRAMS["pressing"] = """
<svg viewBox="0 0 700 300" class="diag">
 <rect x="2" y="2" width="696" height="296" rx="8" fill="#7FB06B"/>
 <rect x="2" y="2" width="696" height="296" rx="8" fill="none" stroke="#fff" stroke-width="3"/>
 <line x1="350" y1="2" x2="350" y2="298" stroke="#fff" stroke-width="3"/>
 <circle cx="350" cy="150" r="38" fill="none" stroke="#fff" stroke-width="3"/>
 <rect x="2" y="62" width="150" height="176" fill="none" stroke="#fff" stroke-width="3"/>
 <rect x="548" y="62" width="150" height="176" fill="none" stroke="#fff" stroke-width="3"/>
 <line x1="2" y1="205" x2="698" y2="205" stroke="#E8873C" stroke-width="6" stroke-dasharray="16 12"/>
 <g stroke="#2A2A26" stroke-width="5" marker-end="url(#a)">
  <path d="M 300 225 L 250 175"/><path d="M 400 225 L 450 175"/>
 </g>
 <g font-family="Arial" font-weight="800" font-size="24" text-anchor="middle">
  <circle cx="350" cy="235" r="24" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="350" y="244">1</text>
  <circle cx="300" cy="140" r="24" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="300" y="149">2</text>
  <circle cx="400" cy="140" r="24" fill="#fff" stroke="#0B1210" stroke-width="4"/><text x="400" y="149">3</text>
 </g>
 <defs><marker id="a" markerWidth="12" markerHeight="12" refX="8" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#2A2A26"/></marker></defs>
</svg>"""

CSS = """
@page { size: A4; margin: 0; }
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; color:#0B1210; background:#fff; }
.page { width:210mm; height:297mm; page-break-after: always; position:relative; background:#F4F0E6; overflow:hidden; }
.page:last-child { page-break-after: auto; }
.goldline { height:5px; background:linear-gradient(90deg,#C9A84C,#8a6f2a); }
header.pd { background:#0B1210; padding:16px 22mm 14px; display:flex; justify-content:space-between; align-items:center; }
header.pd .brand { font-weight:800; font-size:11pt; letter-spacing:4px; color:#fff; }
header.pd .brand span { color:#7ED957; }
header.pd .band { font-weight:700; font-size:9pt; letter-spacing:2px; color:#7ED957; background:rgba(126,217,87,.12); border:1px solid rgba(126,217,87,.4); padding:4px 12px; border-radius:999px; }
.pad { padding: 10mm 16mm 0; }
.eyebrow { font-size:8.5pt; font-weight:700; letter-spacing:3px; color:#3E8F3C; text-transform:uppercase; }
h1.t { font-size:23pt; font-weight:800; line-height:1.1; margin:5px 0 6px; letter-spacing:-.5px; }
.rule { width:34mm; height:6px; border-radius:3px; background:linear-gradient(90deg,#7ED957,#C9A84C); margin:8px 0 12px; }
.chips { display:flex; gap:6px; flex-wrap:wrap; margin-bottom:10px; }
.chip { background:#fff; border:1px solid #E0D9C6; border-radius:999px; padding:4px 12px; font-size:8.5pt; font-weight:600; box-shadow:0 1px 3px rgba(11,18,16,.06); }
.chip b { color:#3E8F3C; }
.card { background:#fff; border:1px solid #E0D9C6; border-radius:4mm; padding:7mm 8mm; margin-bottom:5mm; box-shadow:0 2px 8px rgba(11,18,16,.05); }
.label { font-size:8pt; font-weight:800; letter-spacing:2.5px; color:#3E8F3C; text-transform:uppercase; margin-bottom:4px; display:flex; align-items:center; gap:8px; }
.label::after { content:''; flex:1; height:1.5px; background:linear-gradient(90deg,#D8D0BC,transparent); }
.card p { font-size:9.5pt; line-height:1.5; color:#2A2A26; }
.step { display:flex; gap:6px; align-items:flex-start; margin-bottom:5px; }
.num { min-width:7mm; height:7mm; border-radius:50%; background:#0B1210; color:#7ED957; font-weight:800; font-size:9pt; display:flex; align-items:center; justify-content:center; }
.step b { font-size:9pt; color:#0B1210; }
.step span { font-size:9pt; color:#2A2A26; line-height:1.45; }
.tick { color:#3E8F3C; font-weight:800; font-size:9pt; }
.fieldwrap { background:#fff; border:1px solid #E0D9C6; border-radius:4mm; padding:6mm 8mm; box-shadow:0 2px 8px rgba(11,18,16,.05); }
.diag { width:100%; display:block; }
footer.pd { position:absolute; bottom:8mm; left:16mm; right:16mm; display:flex; justify-content:space-between; align-items:center; border-top:1.5px solid #D8D0BC; padding-top:4mm; }
footer.pd .l { display:flex; align-items:center; gap:4mm; }
footer.pd .l img { height:7mm; width:7mm; object-fit:contain; }
footer.pd span { font-size:7.5pt; font-weight:600; color:#7A7464; letter-spacing:1.5px; }
.pageno { font-size:9pt; font-weight:800; color:#0B1210; background:#F4F0E6; border:1px solid #D8D0BC; border-radius:50%; width:9mm; height:9mm; display:flex; align-items:center; justify-content:center; }
/* portada */
.cover { background:#0B1210; color:#fff; }
.cover .goldline { position:absolute; top:0; left:0; right:0; }
.cover img.portada { position:absolute; left:0; right:0; top:32mm; bottom:70mm; width:100%; height:auto; object-fit:contain; }
.cover h1.big { position:absolute; top:18mm; left:0; right:0; text-align:center; font-size:21pt; font-weight:800; letter-spacing:5px; }
.cover h1.big span { color:#7ED957; }
.cover .coverfoot { position:absolute; bottom:16mm; left:20mm; right:20mm; text-align:center; }
.cover .coverfoot .t1 { font-size:16pt; font-weight:800; letter-spacing:2px; }
.cover .coverfoot .t2 { font-size:9.5pt; color:#9FB4A3; margin-top:4mm; line-height:1.6; }
table.tab { width:100%; border-collapse:collapse; font-size:8.5pt; }
table.tab th { background:#0B1210; color:#fff; font-weight:800; text-align:left; padding:2.2mm 3mm; letter-spacing:1px; }
table.tab td { padding:2mm 3mm; border-bottom:1px solid #EDE7D8; color:#2A2A26; }
table.tab tr:nth-child(even) td { background:#FAF8F1; }
"""

def wrap(text, font_px, maxchars):
    """wrap simple por caracteres para párrafos largos"""
    return text

def esc(s): return H.escape(s)

def render_ficha(band, band_label, age_label, i, f, total):
    n = f.get("n", i)
    t = f["titel"]
    ziel = f["ziel"]
    dauer = f.get("dauer", "60 Min")
    spieler = f.get("spieler", "12")
    material = f.get("material", "Bälle, Hütchen, Leibchen")
    ablauf = f["ablauf"]
    varianten = f.get("varianten", [])
    abschluss = f.get("abschluss", "")
    diagram = f.get("diagram", "field")
    dauer_num = re.sub(r"\D", "", dauer) or "60"
    step_html = ""
    for s_ in ablauf:
        m = re.match(r"^([\w äöüßÄÖÜ-]+?)\s*\((.*?)\)\s*:\s*(.*)$", s_)
        if m:
            step_html += f'<div class="step"><div class="num">{n}</div><div><b>{esc(m.group(1))} ({esc(m.group(2))}):</b> <span>{esc(m.group(3))}</span></div></div>'
        else:
            step_html += f'<div class="step"><div class="num">{n}</div><div><span>{esc(s_)}</span></div></div>'
    var_html = "".join(f'<p><span class="tick">✓</span> {esc(v)}</p>' for v in varianten)
    pg = 1 + i  # fichas empiezan en página 1 (portada es página aparte sin número)
    return f"""
<div class="page">
 <div class="goldline"></div>
 <header class="pd"><div class="brand">FUßBALLPRO <span>MASTERPAKET</span></div><div class="band">{esc(band_label)}</div></header>
 <div class="pad">
  <div class="eyebrow">{esc(f.get("kategorie", "Trainingseinheit"))} · Einheit {n}</div>
  <h1 class="t">{esc(t)}</h1>
  <div class="rule"></div>
  <div class="chips">
    <div class="chip"><b>{dauer_num}</b> Minuten</div>
    <div class="chip"><b>{esc(spieler)}</b> Spieler</div>
    <div class="chip"><b>{esc(material.split(',')[0])}</b></div>
    <div class="chip"><b>{esc(age_label)}</b></div>
  </div>
  <div class="card"><div class="label">Ziel</div><p>{esc(ziel)}</p></div>
  <div class="card"><div class="label">Ablauf</div>{step_html}</div>
  <div style="display:flex;gap:5mm;">
    <div class="card" style="flex:1;"><div class="label">Varianten</div>{var_html}</div>
    <div class="card" style="flex:1.3;"><div class="label">Abschlussspiel</div><p>{esc(abschluss)}</p></div>
  </div>
  <div class="fieldwrap" style="margin-top:5mm;">
    <div class="label">Platzskizze</div>
    {DIAGRAMS[diagram]}
  </div>
 </div>
 <footer class="pd">
  <div class="l"><img src="file://{LOGO}" alt=""><span>FUßBALLPRO MASTERPAKET · {esc(band_label)}</span></div>
  <div class="pageno">{n}</div>
 </footer>
</div>"""

def render_portada(band_num, band_label, age_label, titulo, subtitulo, portada_img, indice_items, img_has_text=False):
    rows = "".join(
        f'<tr><td style="width:12%">{i+1:02d}</td><td>{esc(t)}</td><td style="width:18%">{esc(k)}</td></tr>'
        for i, (t, k) in enumerate(indice_items))
    img = f'<img class="portada" src="file://{portada_img}">' if portada_img else ""
    h1 = "" if img_has_text else f'<h1 class="big">FUßBALLPRO <span>MASTERPAKET</span></h1>'
    t1 = "" if img_has_text else f'<div class="t1">{esc(titulo)}</div>'
    return f"""
<div class="page cover">
 <div class="goldline"></div>
 {h1}
 {img}
 <div class="coverfoot">
  {t1}
  <div class="t2">{esc(subtitulo)}</div>
 </div>
 <footer class="pd" style="bottom:6mm;">
  <div class="l"><img src="file://{LOGO}" alt=""><span>FUßBALLPRO MASTERPAKET · {esc(band_label)}</span></div>
  <div class="pageno">{band_num}</div>
 </footer>
</div>
<div class="page">
 <div class="goldline"></div>
 <header class="pd"><div class="brand">FUßBALLPRO <span>MASTERPAKET</span></div><div class="band">{esc(band_label)}</div></header>
 <div class="pad">
  <div class="eyebrow">Inhalt</div>
  <h1 class="t">Übersicht</h1>
  <div class="rule"></div>
  <table class="tab" style="margin-top:4mm;">
   <tr><th>Einheit</th><th>Thema</th><th>Schwerpunkt</th></tr>
   {rows}
  </table>
 </div>
 <footer class="pd"><div class="l"><img src="file://{LOGO}" alt=""><span>FUßBALLPRO MASTERPAKET · {esc(band_label)}</span></div><div class="pageno">01</div></footer>
</div>"""

def build_doc(band_num, band_label, age_label, titulo, subtitulo, portada_img, fichas, extra_pages=""):
    indice = [(f["titel"], f.get("kategorie", "Training")) for f in fichas]
    parts = [render_portada(band_num, band_label, age_label, titulo, subtitulo, portada_img, indice)]
    for i, f in enumerate(fichas, start=1):
        parts.append(render_ficha(band_num, band_label, age_label, i, f, len(fichas)))
    return f"""<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8"><style>{CSS}</style></head><body>{''.join(parts)}{extra_pages}</body></html>"""

def to_pdf(html_path, pdf_path):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                    "--print-to-pdf-no-header",
                    "--print-to-pdf=" + pdf_path,
                    "file://" + html_path],
                   check=True, capture_output=True)

def make_pdf(band_num, band_label, age_label, titulo, subtitulo, portada_img, fichas, out_name, extra_pages=""):
    src_dir = os.path.join(SRC, "html")
    os.makedirs(src_dir, exist_ok=True)
    html_path = os.path.join(src_dir, f"band-{band_num}.html")
    pdf_path = os.path.join(PROD, out_name)
    html = build_doc(band_num, band_label, age_label, titulo, subtitulo, portada_img, fichas, extra_pages)
    open(html_path, "w", encoding="utf-8").write(html)
    to_pdf(html_path, pdf_path)
    kb = os.path.getsize(pdf_path) // 1024
    print(f"OK {out_name} | {kb}KB | {len(fichas)} fichas")

if __name__ == "__main__":
    import sys
    # test rápido: render 1 ficha
    test = [{"titel": "Test", "ziel": "Testziel", "dauer": "45 Min", "spieler": "10",
             "material": "8 Hütchen", "ablauf": ["Aufwärmen (10 Min): frei dribbeln im Quadrat."],
             "varianten": ["Feld verkleinern"], "abschluss": "Freies Spiel.",
             "kategorie": "Technik", "diagram": "slalom"}]
    html = build_doc(1, "BAND 01 · F-JUGEND", "U8–U10", "Test Band", "Subtítulo", None, test)
    open(os.path.join(SRC, "html", "test.html"), "w", encoding="utf-8").write(html)
    to_pdf(os.path.join(SRC, "html", "test.html"), os.path.join(PROD, "_test.pdf"))
    print("test OK:", os.path.getsize(os.path.join(PROD, "_test.pdf")) // 1024, "KB")