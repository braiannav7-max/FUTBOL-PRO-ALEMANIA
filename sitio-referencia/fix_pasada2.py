#!/usr/bin/env python3
p = "/Users/braiannavarrete/Downloads/Opencode/sitio-referencia/index.html"
html = open(p, encoding="utf-8").read()

repl = [
    # HERO párrafo largo
    ("160 entrenamientos listos, 300 ejercicios, 52 semanas de planificación y más de 950 páginas listas para usar",
     "160 fertige Trainingseinheiten, 300 Übungen, 52 Wochen Planung und über 950 Seiten einsatzbereit"),
    # PRICING párrafo (quedó a medio traducir)
    ("160 fertige Trainingseinheiten, 300 ejercicios, 52 semanas y más de 950 páginas listas para usar",
     "160 fertige Trainingseinheiten, 300 Übungen, 52 Wochen und über 950 Seiten einsatzbereit"),
    # FAQ 6 respuesta completa
    ("FußballPro Masterpack es la biblioteca completa para ahorrar tiempo en la preparación: 160 entrenamientos listos, 300 ejercicios, 52 semanas, 6 bonus y más de 950 páginas listas para usar. Trainer Marketing Pro añade el sistema para promocionar tus servicios, encontrar nuevos jugadores y generar más ingresos como entrenador.",
     "Das FußballPro Masterpack ist die komplette Bibliothek, um Zeit bei der Vorbereitung zu sparen: 160 fertige Trainingseinheiten, 300 Übungen, 52 Wochen, 6 Boni und über 950 Seiten einsatzbereit. Trainer Marketing Pro ergänzt das System, um deine Leistungen zu bewerben, neue Spieler zu gewinnen und als Trainer mehr zu verdienen."),
    # Título de sección marketing (rotto por "incluidos"->"inklusive")
    ("Los volúmenes inklusive en el sistema", "Die im System enthaltenen Bände"),
    # CTA upsell
    ("SÍ, QUIERO EL FußballPro Masterpack + Trainer Marketing Pro",
     "JA, ICH WILL DAS FUßBALLPRO MASTERPACK + TRAINER MARKETING PRO"),
    # Badge de garantías (quedó "Pago seguro" suelto)
    ("• Pago seguro", "• Sichere Zahlung"),
    # Labels Bonus01..06
    ("Bonus01", "Bonus 1"), ("Bonus02", "Bonus 2"), ("Bonus03", "Bonus 3"),
    ("Bonus04", "Bonus 4"), ("Bonus05", "Bonus 5"), ("Bonus06", "Bonus 6"),
    # Upsell title en config de checkout
    ("&#34;upsellTitle&#34;:[0,&#34;Entrenador Marketing Pro&#34;]",
     "&#34;upsellTitle&#34;:[0,&#34;Trainer Marketing Pro&#34;]"),
]

for old, new in repl:
    n = html.count(old)
    html = html.replace(old, new)
    print(f"{n}x  {old[:70]}")

# JSON social proof — estado actual completo
json_old = '[{&#34;name&#34;:&#34;David M. desde Madrid&#34;,&#34;action&#34;:&#34;ha desbloqueado FußballPro Masterpack&#34;},{&#34;name&#34;:&#34;L. Kaiser desde Valencia&#34;,&#34;action&#34;:&#34;está preparando la próxima sesión en pocos minutos&#34;},{&#34;name&#34;:&#34;Andrés F. desde Sevilla&#34;,&#34;action&#34;:&#34;acaba de descargar los entrenamientos Alevín&#34;},{&#34;name&#34;:&#34;Marcos P. desde Bilbao&#34;,&#34;action&#34;:&#34;ha añadido Entrenador Marketing Pro&#34;},{&#34;name&#34;:&#34;L. Kaiser desde Madrid&#34;,&#34;action&#34;:&#34;acaba de completar la compra&#34;}]'
json_new = '[{&#34;name&#34;:&#34;D. Weber aus München&#34;,&#34;action&#34;:&#34;hat das FußballPro Masterpack freigeschaltet&#34;},{&#34;name&#34;:&#34;L. Schneider aus Hamburg&#34;,&#34;action&#34;:&#34;bereitet seine nächste Einheit in wenigen Minuten vor&#34;},{&#34;name&#34;:&#34;A. Brandt aus Köln&#34;,&#34;action&#34;:&#34;hat gerade die E-Jugend-Einheiten heruntergeladen&#34;},{&#34;name&#34;:&#34;M. Schulz aus Berlin&#34;,&#34;action&#34;:&#34;hat Trainer Marketing Pro hinzugefügt&#34;},{&#34;name&#34;:&#34;L. Kaiser aus Stuttgart&#34;,&#34;action&#34;:&#34;hat gerade den Kauf abgeschlossen&#34;}]'
n = html.count(json_old)
html = html.replace(json_old, json_new)
print(f"{n}x  JSON social proof")

open(p, "w", encoding="utf-8").write(html)
print("OK")