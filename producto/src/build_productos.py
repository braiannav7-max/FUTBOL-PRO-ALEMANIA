#!/usr/bin/env python3
"""Construye los 6 PDFs del FußballPro Masterpaket."""
import os, importlib
import generador as G
from generador import esc, DIAGRAMS

SRC = os.path.dirname(os.path.abspath(__file__))
ASTRO = os.path.join(SRC, "..", "..", "sitio-referencia", "_astro")

VOL_IMG = {
    1: "volume-1.6rVcAecq_Z1yrJFe.webp",
    2: "volume-2.BYgAMZE__Z2tFfgT.webp",
    3: "volume-3.yFqzv0kr_Z1LB26D.webp",
    4: "volume-4.DTo6Ixib_pJysr.webp",
    5: "volume-5.BpHsGu6S_2i2nRx.webp",
    6: "volume-6.VqoICUNJ_Z1KbP4a.webp",
}

BANDS = {
    1: ("Band 01 · F-Jugend", "U8–U10", "F-JUGEND (U8–U10)", "20 komplette Trainingseinheiten für die Jüngsten – mit Platzskizzen, Varianten und Abschlussspielen."),
    2: ("Band 02 · E-Jugend", "U11–U12", "E-JUGEND (U11–U12)", "20 komplette Trainingseinheiten mit Passspiel, Ballbesitz und ersten taktischen Schritten."),
    3: ("Band 03 · D-Jugend", "U13–U14", "D-JUGEND (U13–U14)", "20 komplette Trainingseinheiten mit Spielaufbau, Pressing und Umschaltspiel."),
    4: ("Band 04 · C-/B-Jugend", "U15–U18", "C-/B-JUGEND (U15–U18)", "20 komplette Trainingseinheiten mit Systemtraining, Gegenpressing und Wettkampf."),
    5: ("Band 05 · Übungsarchiv", "U8–U18", "ÜBUNGSARCHIV · 60+ ÜBUNGEN", "Die komplette Übungssammlung nach Schwerpunkten sortiert – für jedes Alter und jedes Trainingsziel."),
    6: ("Band 06 · Saisonplanung", "U8–U18", "SAISONPLANUNG · 52 WOCHEN", "Die komplette Saisonplanung 2026/27: Phasen, Wochenpläne, Beispielwochen und Trainer-Checkliste."),
}


def band_pages(band_num, rows_per_page, headers, rows, start_page_label):
    pages = []
    for chunk_start in range(0, len(rows), rows_per_page):
        chunk = rows[chunk_start:chunk_start + rows_per_page]
        body = "".join(
            f'<tr>{"".join(f"<td>{esc(c)}</td>" for c in row)}</tr>'
            for row in chunk)
        num = int(start_page_label)
        pages.append(f"""
<div class="page">
 <div class="goldline"></div>
 <header class="pd"><div class="brand">FUßBALLPRO <span>MASTERPAKET</span></div><div class="band">{esc(BANDS[band_num][0])}</div></header>
 <div class="pad">
  <div class="eyebrow">Inhalt · Fortsetzung</div>
  <h1 class="t" style="font-size:16pt;">{esc(headers[0])}</h1>
  <div class="rule"></div>
  <table class="tab" style="margin-top:3mm;">
   <tr>{"".join(f"<th>{esc(h)}</th>" for h in headers[1:])}</tr>
   {body}
  </table>
 </div>
 <footer class="pd"><div class="l"><img src="file://{G.LOGO}" alt=""><span>FUßBALLPRO MASTERPAKET · {esc(BANDS[band_num][0])}</span></div><div class="pageno">{num:02d}</div></footer>
</div>""")
    return pages


def main():
    for num in (1, 2, 3, 4):
        label, age, title, sub = BANDS[num]
        mod = importlib.import_module(f"datos_band{num}")
        out = f"FußballPro-Masterpaket-Band-{num:02d}.pdf"
        G.make_pdf(num, label, age, title, sub,
                   os.path.join(ASTRO, VOL_IMG[num]),
                   mod.FICHAS, out)

    # ---- Band 5: Übungsarchiv ----
    b5 = importlib.import_module("datos_band5")
    rows = b5.ARCHIV[1:]
    headers = b5.ARCHIV[0]
    indice_cat = [(cat, f"{sum(1 for r in rows if r[0]==cat)} Übungen")
                  for cat in sorted(set(r[0] for r in rows))]
    portada = G.render_portada(5, BANDS[5][0], BANDS[5][1],
                               "PROFESSIONELLES ARCHIV · 300 ÜBUNGEN",
                               "Die komplette Übungssammlung nach Schwerpunkten sortiert – für jedes Alter und jedes Trainingsziel.",
                               os.path.join(ASTRO, VOL_IMG[5]), indice_cat, img_has_text=True)
    pages = band_pages(5, 34, headers, rows, "02")
    html = f"""<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8"><style>{G.CSS}</style></head><body>{portada}{''.join(pages)}</body></html>"""
    html_path = os.path.join(SRC, "html", "band-5.html")
    os.makedirs(os.path.dirname(html_path), exist_ok=True)
    open(html_path, "w", encoding="utf-8").write(html)
    out5 = os.path.join(os.path.dirname(SRC), "FußballPro-Masterpaket-Band-05.pdf")
    G.to_pdf(html_path, out5)
    print(f"OK FußballPro-Masterpaket-Band-05.pdf | {os.path.getsize(out5)//1024}KB | {len(rows)} Übungen")

    # ---- Band 6: 52-Wochen-Planung ----
    b6 = importlib.import_module("datos_band6")
    portada6 = G.render_portada(6, BANDS[6][0], BANDS[6][1],
                                "SAISONPLANUNG · 52 WOCHEN",
                                "Die komplette Saisonplanung 2026/27: Phasen, Wochenpläne, Beispielwochen und Trainer-Checkliste.",
                                os.path.join(ASTRO, VOL_IMG[6]),
                                [(p[0], p[3]) for p in b6.PHASEN],
                                img_has_text=True)
    # página de fases
    ph_body = "".join(
        f'<tr><td style="width:22%">{esc(p[0])}</td><td style="width:18%">{esc(p[1])}</td><td>{esc(p[2])}</td><td style="width:20%">{esc(p[3])}</td></tr>'
        for p in b6.PHASEN)
    page_phasen = f"""
<div class="page">
 <div class="goldline"></div>
 <header class="pd"><div class="brand">FUßBALLPRO <span>MASTERPAKET</span></div><div class="band">{esc(BANDS[6][0])}</div></header>
 <div class="pad">
  <div class="eyebrow">Saison 2026/27 · Deutschland</div>
  <h1 class="t" style="font-size:16pt;">Saisonphasen im Überblick</h1>
  <div class="rule"></div>
  <table class="tab" style="margin-top:3mm;">
   <tr><th>Phase</th><th>Zeitraum</th><th>Schwerpunkt</th><th>Umfang</th></tr>
   {ph_body}
  </table>
  <div class="card" style="margin-top:8mm;"><div class="label">Trainer-Notiz</div><p>Die Belastung steigt stufenweise an: In der Vorbereitung steht die Technik im Vordergrund, im Saisonverlauf gewinnen Taktik und Wettkampf an Bedeutung. Regenerationswochen sind fest eingeplant.</p></div>
 </div>
 <footer class="pd"><div class="l"><img src="file://{G.LOGO}" alt=""><span>FUßBALLPRO MASTERPAKET · {esc(BANDS[6][0])}</span></div><div class="pageno">02</div></footer>
</div>"""
    wk_headers = ("Woche", "Phase", "Fokus", "Belastung", "Einheiten")
    wk_rows = [r for r in b6.WOCHEN]
    wk_pages = band_pages(6, 26, wk_headers, wk_rows, "03")

    def beispiel_page(label, phase_title, einheiten, pageno):
        cards = ""
        for e in einheiten:
            cards += f"""<div class="card"><div class="label">{esc(e[0])} · {esc(e[1])}</div>
            <p><b>{esc(e[2])}</b></p>
            <div class="chips" style="margin-top:3mm;"><div class="chip"><b>{esc(e[3])}</b></div><div class="chip">{esc(e[4])}</div></div></div>"""
        return f"""
<div class="page">
 <div class="goldline"></div>
 <header class="pd"><div class="brand">FUßBALLPRO <span>MASTERPAKET</span></div><div class="band">{esc(BANDS[6][0])}</div></header>
 <div class="pad">
  <div class="eyebrow">Beispielwoche</div>
  <h1 class="t" style="font-size:16pt;">{esc(phase_title)}</h1>
  <div class="rule"></div>
  {cards}
 </div>
 <footer class="pd"><div class="l"><img src="file://{G.LOGO}" alt=""><span>FUßBALLPRO MASTERPAKET · {esc(BANDS[6][0])}</span></div><div class="pageno">{pageno}</div></footer>
</div>"""

    pg = [
        beispiel_page(6, "Beispielwoche 06 · Vorbereitung", b6.BEISPIEL_VORBEREITUNG, 7),
        beispiel_page(6, "Beispielwoche 12 · Saisonstart", b6.BEISPIEL_SAISON, 8),
        beispiel_page(6, "Beispielwoche 24 · Winterpause", b6.BEISPIEL_HALLE, 9),
        beispiel_page(6, "Beispielwoche 30 · Rückrunde", b6.BEISPIEL_RUECKRUNDE, 10),
    ]
    chk = "".join(f'<p style="margin-bottom:4px;"><span class="tick">✓</span> {esc(c)}</p>' for c in b6.CHECKLISTE)
    page_check = f"""
<div class="page">
 <div class="goldline"></div>
 <header class="pd"><div class="brand">FUßBALLPRO <span>MASTERPAKET</span></div><div class="band">{esc(BANDS[6][0])}</div></header>
 <div class="pad">
  <div class="eyebrow">Vor jeder Einheit</div>
  <h1 class="t" style="font-size:16pt;">Trainer-Checkliste</h1>
  <div class="rule"></div>
  <div class="card"><div class="label">Checkliste</div>{chk}</div>
  <div class="card"><div class="label">Rituale</div><p>Jede Einheit startet mit einem kurzen Aufwärmen und endet mit einer Abschlussrunde. So bleibt die Stimmung hoch und die Spieler kommen gerne wieder.</p></div>
 </div>
 <footer class="pd"><div class="l"><img src="file://{G.LOGO}" alt=""><span>FUßBALLPRO MASTERPAKET · {esc(BANDS[6][0])}</span></div><div class="pageno">11</div></footer>
</div>"""
    html6 = f"""<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8"><style>{G.CSS}</style></head><body>{portada6}{page_phasen}{''.join(wk_pages)}{''.join(pg)}{page_check}</body></html>"""
    html_path6 = os.path.join(SRC, "html", "band-6.html")
    open(html_path6, "w", encoding="utf-8").write(html6)
    out6 = os.path.join(os.path.dirname(SRC), "FußballPro-Masterpaket-Band-06.pdf")
    G.to_pdf(html_path6, out6)
    print(f"OK FußballPro-Masterpaket-Band-06.pdf | {os.path.getsize(out6)//1024}KB | 52 Wochen")


if __name__ == "__main__":
    main()
