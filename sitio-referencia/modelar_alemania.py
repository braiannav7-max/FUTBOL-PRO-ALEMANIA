#!/usr/bin/env python3
import re

p = "/Users/braiannavarrete/Downloads/Opencode/sitio-referencia/index.html"
html = open(p, encoding="utf-8").read()

# (old, new) — ordenados de más largo a más corto para evitar colisiones
repl = [
    # === META / SEO ===
    ("Masterpack Entrenador de Fútbol Pro | 160 entrenamientos listos para entrenadores",
     "FußballPro Masterpack | 160 fertige Trainingseinheiten für Trainer"),
    ("160 entrenamientos listos, 300 ejercicios, 52 semanas de planificación y más de 950 páginas listas para usar para preparar tus sesiones en pocos minutos.",
     "160 fertige Trainingseinheiten, 300 Übungen, 52 Wochen Planung und über 950 Seiten – bereite deine Einheiten in wenigen Minuten vor."),

    # === NAV ===
    ("Masterpack Entrenador de Fútbol Pro", "FußballPro Masterpack"),
    ("MasterPack Entrenador de Fútbol Pro Completo", "FußballPro Masterpack"),
    ("MasterPack Entrenador de Fútbol Pro", "FußballPro Masterpack"),
    ("⚽ DESBLOQUEA POR 19,90 €", "⚽ JETZT FREISCHALTEN FÜR 19,90 €"),

    # === HERO ===
    ("Todo tu año de", "Dein komplettes Fußballjahr"),
    ("fútbol resuelto.", "– perfekt gelöst."),
    ("Basta de improvisar cada semana.", "Schluss mit dem Improvisieren vor jeder Einheit."),
    ("para preparar tus sesiones en pocos minutos y llegar al campo con más orden, más profesionalidad y menos estrés.",
     "bereite deine Einheiten in wenigen Minuten vor und komm besser organisiert, professioneller und entspannter auf den Platz."),
    ("PDF digitales", "Digitale PDFs"),
    ("Acceso inmediato", "Sofortiger Zugriff"),
    ("6 volúmenes + 6 bonus", "6 Bände + 6 Boni"),
    ("⚽ DESCARGA AHORA MASTERPACK ENTRENADOR DE FÚTBOL PRO",
     "⚽ JETZT DOWNLOADEN: FUßBALLPRO MASTERPACK TRAINER"),
    ("GARANTÍA 7 DÍAS", "7-TAGE-GARANTIE"),
    ("PAGO SEGURO", "SICHERE ZAHLUNG"),

    # === COACH QUOTE ===
    ("\"Cuando tienes sesiones listas, ejercicios ordenados y una planificación clara, dejas de perder horas cada semana y en el campo se nota la diferencia de inmediato.\"",
     "\"Wenn du fertige Einheiten, sortierte Übungen und eine klare Planung hast, hörst du auf, jede Woche Stunden zu verlieren – und auf dem Platz sieht man den Unterschied sofort.\""),
    ("FutbolPro • Equipo Técnico de Fútbol", "FußballPro • Technische Leitung Fußballschule"),

    # === DOLORES ===
    ("Si cada semana pierdes horas organizando las sesiones, esto te va a sonar demasiado familiar:",
     "Wenn du jede Woche Stunden mit der Vorbereitung verlierst, kommt dir das sicher bekannt vor:"),
    ("Pasas demasiado tiempo buscando o inventando ejercicios", "Du verbringst zu viel Zeit mit Suchen oder Erfinden von Übungen"),
    ("a última hora", "auf den letzten Drücker"),
    ("No tienes una progresión clara por edad, objetivos y nivel del grupo", "Dir fehlt eine klare Progression nach Alter, Zielen und Niveau der Gruppe"),
    ("y acabas repitiéndote", "und du wiederholst dich ständig"),
    ("Llegas al campo con sesiones poco fluidas, explicaciones largas y", "Du kommst mit wenig flüssigen Einheiten, langen Erklärungen und"),
    ("organización débil", "schwacher Organisation auf den Platz"),
    ("Te falta un archivo serio de ejercicios y variantes para usar sin", "Dir fehlt ein ernsthaftes Archiv aus Übungen und Varianten – ohne"),
    ("partir de cero", "bei null anfangen zu müssen"),
    ("Cuando la semana se complica, la planificación se va al traste e", "Wird die Woche chaotisch, fällt die Planung zusammen und"),
    ("improvisas demasiado", "du improvisierst zu viel"),
    ("Quieres parecer más preparado y profesional, pero sin un sistema listo", "Du willst vorbereiteter und professioneller wirken, aber ohne fertiges System"),
    ("pierdes horas innecesarias", "verlierst du unnötig Stunden"),

    # === QUÉ RECIBES ===
    ("Qué recibes hoy", "Das bekommst du heute"),
    ("Las 6 guías principales con una explicación clara de qué encuentras dentro y de cómo te ahorran tiempo cada semana. En total tienes más de 950 páginas listas para usar para usar y adaptar.",
     "Die 6 Hauptbände mit klarer Erklärung, was du darin findest und wie sie dir jede Woche Zeit sparen. Insgesamt über 950 Seiten – fertig zum Einsatz und Anpassen."),
    ("Contenido Incluido", "Enthalten"),
    ("Entrenamientos Listos", "Fertige Trainingseinheiten"),
    ("Prebenjamín/Benjamín (U8-U10)", "F-Jugend (U8–U10)"),
    ("Conducción, pase, control, coordinación, finalización y juegos técnicos.",
     "Dribbling, Passen, Ballkontrolle, Koordination, Abschluss und Technikspiele."),
    ("Una colección lista de sesiones para los más pequeños con actividades sencillas de explicar, rápidas de montar y fáciles de llevar al campo.",
     "Eine fertige Sammlung von Einheiten für die Kleinsten – mit einfachen Aktivitäten, die schnell aufgebaut und direkt auf den Platz zu bringen sind."),
    ("Cada sesión incluye objetivo, duración, material necesario, desarrollo paso a paso, variantes y partido final.",
     "Jede Einheit enthält Ziel, Dauer, benötigtes Material, Schritt-für-Schritt-Ablauf, Varianten und Abschlussspiel."),
    ("Alevín (U11-U12)", "E-Jugend (U11–U12)"),
    ("Posesión, construcción, apoyos, desmarques, superioridades numéricas y toma de decisiones.",
     "Ballbesitz, Spielaufbau, Anbieten, Freilaufen, Überzahlsituationen und Entscheidungsfindung."),
    ("Aquí encuentras sesiones ya estructuradas para trabajar de forma más ordenada la posesión, la construcción, los apoyos y los desmarques.",
     "Hier findest du strukturierte Einheiten, um Ballbesitz, Spielaufbau, Anbieten und Freilaufen geordnet zu trainieren."),
    ("Sirve para preparar entrenamientos más fluidos sin perder tiempo reconstruyendo la secuencia cada vez.",
     "So bereitest du flüssigere Einheiten vor, ohne die Abläufe jede Woche neu zusammenzusetzen."),
    ("Infantil (U13-U14)", "D-Jugend (U13–U14)"),
    ("Presión, transiciones, intensidad, organización táctica y ataque-defensa colectiva.",
     "Pressing, Umschaltspiel, Intensität, taktische Ordnung und kollektives Verteidigen."),
    ("Este volumen te da sesiones más avanzadas para categorías que requieren mayor estructura.",
     "Dieser Band liefert fortgeschrittenere Einheiten für Altersklassen, die mehr Struktur brauchen."),
    ("Trabajas presión, transiciones y momentos tácticos sin pasar horas montando bloques complejos desde cero.",
     "Trainiere Pressing, Umschaltspiel und taktische Momente, ohne komplexe Blöcke stundenlang selbst aufzubauen."),
    ("Cadete/Juvenil (U15-U18)", "C-/B-Jugend (U15–U18)"),
    ("Situaciones reales de partido, táctica aplicada, intensidad competitiva, velocidad de juego y principios del fútbol moderno.",
     "Realistische Spielsituationen, angewandte Taktik, Wettkampfintensität, Spieltempo und Prinzipien des modernen Fußballs."),
    ("Una biblioteca lista para categorías donde el nivel de atención, intensidad y organización debe subir.",
     "Eine einsatzbereite Bibliothek für Altersklassen, in denen Aufmerksamkeit, Intensität und Organisation steigen müssen."),
    ("Te ayuda a construir entrenamientos creíbles, exigentes y más cercanos a las necesidades del partido, sin quedarte bloqueado en la preparación.",
     "Damit baust du glaubwürdige, anspruchsvolle Einheiten, die näher am Spiel sind – ohne dich in der Vorbereitung festzufahren."),
    ("Archivo Profesional de", "Professionelles Archiv mit"),
    ("300 Ejercicios", "300 Übungen"),
    ("Una base de datos práctica para encontrar de inmediato el ejercicio adecuado y adaptarlo al grupo.",
     "Eine praktische Datenbank, um sofort die passende Übung zu finden und auf deine Gruppe anzupassen."),
    ("Este archivo te evita perder horas buscando ideas sueltas.",
     "Dieses Archiv erspart dir das stundenlange Suchen nach Einzelideen."),
    ("Tienes ejercicios listos, ordenados por objetivo y fáciles de combinar entre sí cuando necesitas montar una sesión en poco tiempo.",
     "Fertige Übungen, nach Zielen sortiert und leicht kombinierbar, wenn du in kurzer Zeit eine Einheit zusammenstellen musst."),
    ("52 Semanas de", "52 Wochen mit"),
    ("Planificación de temporada ya pensada para dar continuidad y orden a tu trabajo.",
     "Eine fertig durchdachte Saisonplanung für Kontinuität und Ordnung in deiner Arbeit."),
    ("El módulo que te ayuda a no vivir semana a semana.",
     "Das Modul, das dich von der Wochen-für-Wochen-Improvisation befreit."),
    ("Tienes una hoja de ruta anual ya lista para distribuir contenidos, progresiones y cargas con más lógica, así el trabajo se vuelve más ordenado y mucho menos estresante.",
     "Ein fertiger Jahresfahrplan, um Inhalte, Progressionen und Belastungen logisch zu verteilen – deine Arbeit wird strukturierter und deutlich entspannter."),

    # === MEJORAS ===
    ("Qué mejoras con el pack", "Was du mit dem Pack verbesserst"),
    ("160 entrenamientos listos divididos por edad y objetivos", "160 fertige Trainingseinheiten nach Alter und Zielen sortiert"),
    ("Más de 300 ejercicios ya ordenados para uso práctico", "Über 300 Übungen, sortiert für den praktischen Einsatz"),
    ("Más de 950 páginas listas para usar para consultar cuando las necesites", "Über 950 Seiten – einsatzbereit, wenn du sie brauchst"),
    ("Planificación semanal y de temporada más ordenada", "Strukturiertere Wochen- und Saisonplanung"),
    ("Más fluidez en la gestión del grupo y de los tiempos de campo", "Mehr Fluss bei Gruppenführung und Platzzeiten"),
    ("Menos improvisación, y se te ve mucho más profesional", "Weniger Improvisation, professionellerer Auftritt"),

    # === VISTA REAL ===
    ("VISTA REAL DEL CONTENIDO", "REALER EINBLICK INS MATERIAL"),
    ("Mira", "Schau"),
    ("por dentro", "hinein"),
    ("Páginas reales, listas para usar. Nada de promesas: esto es exactamente lo que descargas hoy.",
     "Echte, einsatzbereite Seiten. Keine Versprechen: Genau das lädst du heute herunter."),
    ("← Desliza para ver más →", "← Wische für mehr →"),
    ("950+ páginas listas para usar", "950+ Seiten einsatzbereit"),
    ("160 entrenamientos listos", "160 fertige Trainingseinheiten"),
    ("Formato PDF", "PDF-Format"),
    ("SÍ, QUIERO ESTE PACK", "JA, ICH WILL DIESEN PACK"),
    ("Acceso inmediato • Formato PDF • Pago seguro", "Sofortiger Zugriff • PDF-Format • Sichere Zahlung"),

    # === BONUS ===
    ("Además tienes los 6", "Zusätzlich bekommst du die 6"),
    ("BONUS OPERATIVOS", "PRAXIS-BONI"),
    ("incluidos", "inklusive"),
    ("Incluidos hoy en ambas ofertas", "Heute in beiden Angeboten enthalten"),
    ("🎁 BONUS 1: 100 Calentamientos Listos", "🎁 BONUS 1: 100 fertige Aufwärmprogramme"),
    ("100 calentamientos listos para usar antes de cualquier entrenamiento.",
     "100 fertige Aufwärmprogramme für jede Trainingseinheit."),
    ("🎁 BONUS 2: 50 Juegos Técnicos para Fútbol Base", "🎁 BONUS 2: 50 Technikspiele für den Jugendfußball"),
    ("Juegos prácticos para mejorar la técnica y mantener alta la participación de los jugadores.",
     "Praktische Spiele für bessere Technik und hohe Beteiligung der Spieler."),
    ("🎁 BONUS 3: 100 Ejercicios Sin Material", "🎁 BONUS 3: 100 Übungen ohne Material"),
    ("Entrenamientos adaptados para entrenadores con pocos recursos disponibles.",
     "Einheiten für Trainer mit wenig verfügbaren Mitteln."),
    ("🎁 BONUS 4: Entrenamientos Rápidos de 30 Minutos", "🎁 BONUS 4: 30-Minuten-Schnelleinheiten"),
    ("Sesiones cortas para situaciones con poco tiempo o pocos jugadores.",
     "Kurze Einheiten für wenig Zeit oder wenige Spieler."),
    ("🎁 BONUS 5: Fichas de Entrenamiento Imprimibles", "🎁 BONUS 5: Ausdruckbare Trainingskarten"),
    ("Plantillas profesionales listas para imprimir y llevar al campo.",
     "Professionelle Vorlagen zum Ausdrucken und Mitnehmen auf den Platz."),
    ("🎁 BONUS 6: Colección de 50 Rondos Profesionales", "🎁 BONUS 6: 50 Profi-Rondos"),
    ("50 variantes de rondos organizadas por nivel y objetivo técnico-táctico.",
     "50 Rondo-Varianten nach Niveau und technisch-taktischem Ziel sortiert."),
    ("Valor Total de los Bonus", "Gesamtwert der Boni"),
    ("Incluidos en el sistema sin costes adicionales", "Im System enthalten, ohne Zusatzkosten"),

    # === COUNTDOWN / URGENCIA ===
    ("⏰ EL PRECIO DE LANZAMIENTO TERMINA EN:", "⏰ DER EINFÜHRUNGSPREIS ENDET IN:"),
    ("Después sube", "Danach steigt der Preis"),
    ("y no vuelve a bajar.", "und sinkt nicht wieder."),
    ("🔴 Cupos al precio de lanzamiento", "🔴 Plätze zum Einführungspreis"),
    ("Quedan pocos", "Nur noch wenige"),
    ("% plazas ocupadas", "% der Plätze belegt"),

    # === PRICING ===
    ("Elige", "Wähle"),
    ("cómo quieres organizar tu trabajo como entrenador:", "wie du als Trainer arbeiten willst:"),
    ("Ambas opciones incluyen los 6 volúmenes principales, los 6 bonus listos para usar y más de 950 páginas en total",
     "Beide Optionen enthalten die 6 Hauptbände, die 6 einsatzbereiten Boni und insgesamt über 950 Seiten"),
    ("FußballPro Masterpack — 6 Guías + 6 Bonus Incluidos", "FußballPro Masterpack – 6 Bände + 6 Boni inklusive"),
    ("160 entrenamientos listos, 300 ejercicios, 52 semanas y más de 950 páginas listas para usar",
     "160 fertige Einheiten, 300 Übungen, 52 Wochen und über 950 Seiten einsatzbereit"),
    ("⭐ MÁS ELEGIDO", "⭐ MEISTGEWÄHLT"),
    ("AHORRÁS €35", "DU SPARST 35 €"),
    ("FußballPro Masterpack + Entrenador Marketing Pro", "FußballPro Masterpack + Trainer Marketing Pro"),
    ("Sistema completo + 4 volúmenes de marketing extra • LA MÁS ELEGIDA ⭐ AHORRAS 35,00 €",
     "Komplettes System + 4 Marketing-Bände extra • MEISTGEWÄHLT ⭐ DU SPARST 35,00 €"),
    ("El precio sube", "Der Preis steigt"),
    ("SÍ, QUIERO EL FußballPro Masterpack + Entrenador Marketing Pro",
     "JA, ICH WILL DAS FUßBALLPRO MASTERPACK + TRAINER MARKETING PRO"),
    ("Pago Seguro", "Sichere Zahlung"),
    ("Acceso Inmediato", "Sofortiger Zugriff"),
    ("Garantía 7 días", "7-Tage-Garantie"),
    ("Todos los métodos", "Alle Zahlungsmethoden"),

    # === MARKETING PRO ===
    ("ENTRENADOR MARKETING PRO", "TRAINER MARKETING PRO"),
    ("INCLUYE:", "ENTHÄLT:"),
    ("El bloque extra para quien quiere encontrar más jugadores, promocionar sus servicios y generar más ingresos como entrenador.",
     "Das Extra-Paket für alle, die mehr Spieler gewinnen, ihre Leistungen bewerben und als Trainer mehr verdienen wollen."),
    ("Si FußballPro Masterpack te da el sistema listo para usar para el campo,",
     "Während dir das FußballPro Masterpack das einsatzbereite System für den Platz liefert,"),
    ("te ayuda a promocionarte mejor, llenar campus y clases particulares y construir un negocio más sólido en el fútbol.",
     "hilft dir Trainer Marketing Pro, dich besser zu vermarkten, Camps und Einzeltrainings zu füllen und ein solideres Geschäft im Fußball aufzubauen."),
    ("Los volúmenes incluidos en el sistema", "Die im System enthaltenen Bände"),
    ("Meta Ads para Entrenadores de Fútbol", "Meta Ads für Fußballtrainer"),
    ("Cómo promocionar entrenamientos, campus y escuelas de tecnificación con presupuestos reducidos.",
     "So bewirbst du Trainingseinheiten, Camps und Fußballschulen mit kleinem Budget."),

    # === TESTIMONIOS ===
    ("Lo que dicen quienes ya usan", "Das sagen Trainer, die es bereits nutzen"),
    ("Menos tiempo delante del folio en blanco, más orden y más seguridad en el campo",
     "Weniger Zeit vor dem leeren Blatt, mehr Ordnung und mehr Sicherheit auf dem Platz"),
    ("\"La diferencia más grande es el tiempo: antes perdía dos tardes a la semana preparando, ahora abro el pack, adapto la sesión y en pocos minutos estoy listo.\"",
     "\"Der größte Unterschied ist die Zeit: Früher verlor ich zwei Abende pro Woche mit der Vorbereitung – jetzt öffne ich den Pack, passe die Einheit an und bin in wenigen Minuten fertig.\""),
    ("\"Me ha puesto orden. Ya no tengo que buscar ejercicios por todas partes ni improvisar bloques. Tengo material ya listo y una progresión mucho más clara.\"",
     "\"Er hat mir Ordnung gegeben. Ich muss nicht mehr überall Übungen suchen oder Blöcke improvisieren. Ich habe fertiges Material und eine viel klarere Progression.\""),
    ("\"El volumen Alevín y el archivo de ejercicios por sí solos ya valen el precio. Me ahorran una cantidad enorme de tiempo cada semana.\"",
     "\"Der E-Jugend-Band und das Übungsarchiv sind allein schon den Preis wert. Sie sparen mir jede Woche enorm viel Zeit.\""),
    ("\"Por fin un producto pensado para la realidad del campo: poco tiempo, muchos grupos y necesidad de llegar preparado. Nada de teoría, solo material listo para usar.\"",
     "\"Endlich ein Produkt für die Realität auf dem Platz: wenig Zeit, viele Gruppen und keine Zeit für unvorbereitetes Erscheinen. Keine Theorie, nur einsatzbereites Material.\""),
    ("\"Las 52 semanas listas me han quitado un peso enorme de encima. Ahora tengo una línea clara y ya no vivo todo a última hora.\"",
     "\"Die 52 fertigen Wochen haben mir eine enorme Last abgenommen. Jetzt habe ich eine klare Linie und mache nicht mehr alles auf den letzten Drücker.\""),
    ("\"Las listas de control, el planificador y las variantes rápidas me han ayudado muchísimo en la gestión práctica. Llego al campo más tranquila y mucho más organizada.\"",
     "\"Die Checklisten, der Planer und die schnellen Varianten helfen mir enorm bei der praktischen Organisation. Ich komme viel ruhiger und organisierter auf den Platz.\""),
    ("\"Cogí también el pack avanzado y la ventaja real es esta: recorta horas de preparación, no te vende humo. Te da herramientas que puedes usar ya mismo.\"",
     "\"Ich habe auch den erweiterten Pack genommen – der echte Vorteil: Er kürzt die Vorbereitungszeit, ohne heiße Luft zu verkaufen. Du bekommst Werkzeuge, die du sofort nutzen kannst.\""),
    ("Entrenador Prebenjamín", "F-Jugend-Trainer"),
    ("Entrenador Alevín", "E-Jugend-Trainer"),
    ("Escuela de fútbol privada", "Private Fußballschule"),
    ("Categoría Infantil", "D-Jugend-Trainer"),
    ("Cadete y Juvenil", "B-Jugend-Trainer"),
    ("Monitora de escuela de fútbol", "Jugendleiterin im Verein"),
    ("Responsable técnico", "Technischer Leiter"),

    # === FAQ ===
    ("Preguntas frecuentes", "Häufige Fragen"),
    ("Todo lo que necesitas saber antes de desbloquear FußballPro Masterpack",
     "Alles, was du vor dem Freischalten des FußballPro Masterpacks wissen musst"),
    ("¿Sirve también si entreno a niños o categorías base?", "Funktioniert das auch im Kinder- und Jugendbereich?"),
    ("Sí. El pack cubre distintas categorías de edad e incluye volúmenes específicos desde Prebenjamín hasta Juvenil, con ejercicios y sesiones pensados para contextos reales de escuela de fútbol.",
     "Ja. Der Pack deckt verschiedene Altersklassen ab und enthält eigene Bände von der F-Jugend bis zur B-Jugend – mit Übungen und Einheiten für den echten Vereinsalltag."),
    ("¿Recibo material físico?", "Bekomme ich physisches Material?"),
    ("No. Es un producto digital: recibes acceso inmediato a los PDF tras la compra.",
     "Nein. Es ist ein digitales Produkt: Du erhältst direkt nach dem Kauf Zugriff auf die PDFs."),
    ("¿Puedo leerlo desde el móvil?", "Kann ich es am Handy lesen?"),
    ("Sí. Puedes abrir los PDF desde el móvil, la tablet o el ordenador sin problemas.",
     "Ja. Du kannst die PDFs problemlos am Handy, Tablet oder Computer öffnen."),
    ("¿Es un curso teórico o federativo?", "Ist das ein Theoriekurs oder ein Verbandslehrgang?"),
    ("No. No es un curso académico ni un itinerario federativo. Es un archivo listo para usar pensado para ahorrarte tiempo en la preparación de los entrenamientos.",
     "Nein. Es ist weder ein akademischer Kurs noch ein Verbandslehrgang. Es ist ein einsatzbereites Archiv, das dir Zeit bei der Vorbereitung spart."),
    ("¿Realmente me ayuda a preparar más rápido?", "Hilft es wirklich, schneller vorzubereiten?"),
    ("Sí, y ese es precisamente el objetivo del pack: darte sesiones listas, ejercicios y planificación ya organizados para evitar empezar de cero cada semana.",
     "Ja, genau das ist das Ziel des Packs: fertige Einheiten, Übungen und Planung, damit du nicht jede Woche bei null anfangen musst."),
    ("¿Qué diferencia hay entre FußballPro Masterpack y Entrenador Marketing Pro?",
     "Was ist der Unterschied zwischen FußballPro Masterpack und Trainer Marketing Pro?"),
    ("FußballPro Masterpack es la biblioteca completa para ahorrar tiempo en la preparación: 160 entrenamientos listos, 300 ejercicios, 52 semanas, 6 bonus y más de 950 páginas listas para usar. Entrenador Marketing Pro añade el sistema para promocionar tus servicios, encontrar nuevos jugadores y generar más ingresos como entrenador.",
     "Das FußballPro Masterpack ist die komplette Bibliothek, um Zeit bei der Vorbereitung zu sparen: 160 fertige Trainingseinheiten, 300 Übungen, 52 Wochen, 6 Boni und über 950 Seiten einsatzbereit. Trainer Marketing Pro ergänzt das System, um deine Leistungen zu bewerben, neue Spieler zu gewinnen und als Trainer mehr zu verdienen."),
    ("FußballPro Masterpack te ayuda a preparar las sesiones en pocos minutos, llegar al campo más organizado y trabajar con más profesionalidad. Menos tiempo delante del folio en blanco. Más tiempo en el campo.",
     "Das FußballPro Masterpack hilft dir, Einheiten in wenigen Minuten vorzubereiten, organisierter auf den Platz zu kommen und professioneller zu arbeiten. Weniger Zeit vor dem leeren Blatt. Mehr Zeit auf dem Platz."),

    # === CTA FINAL / FOOTER / COOKIES ===
    ("⚽ SÍ, QUIERO MASTERPACK ENTRENADOR DE FÚTBOL PRO AHORA",
     "⚽ JA, JETZT DAS FUßBALLPRO MASTERPACK SICHERN"),
    ("© 2026 FutbolPro™. Todos los derechos reservados. Prohibida la reproducción y redistribución.",
     "© 2026 FußballPro™. Alle Rechte vorbehalten. Vervielfältigung und Weiterverbreitung untersagt."),
    ("Términos y Condiciones", "AGB"),
    ("Privacidad", "Datenschutz"),
    ("Usamos cookies de Meta para analizar el uso del sitio y mostrarte publicidad relevante. Puedes aceptar o rechazar su uso.",
     "Wir verwenden Meta-Cookies, um die Nutzung der Website zu analysieren und dir relevante Werbung zu zeigen. Du kannst sie akzeptieren oder ablehnen."),
    ("Rechazar", "Ablehnen"),
    ("Aceptar", "Akzeptieren"),
]

# Reemplazos regex adicionales (números de volumen, valores de bonus, nombres en alt)
regex_repl = [
    (r'Volumen (\d+)', r'Band \1'),
    (r'Valor (\d+,\d+) € — GRATIS', r'Wert \1 € – GRATIS'),
    (r'alt="(Javier L\.|Pablo F\.|Andrés P\.|David R\.|Mateo C\.|Marcos S\.|Lucas T\.)"', r'alt="Trainer"'),
]

# Social proof JSON completo
json_old = '[{"&#34;name&#34;:&#34;David M. desde Madrid&#34;,&#34;action&#34;:&#34;ha desbloqueado MasterPack Entrenador de Fútbol Pro Completo&#34;},{&#34;name&#34;:&#34;Lucas T. desde Valencia&#34;,&#34;action&#34;:&#34;está preparando la próxima sesión en pocos minutos&#34;},{&#34;name&#34;:&#34;Andrés F. desde Sevilla&#34;,&#34;action&#34;:&#34;acaba de descargar los entrenamientos Alevín&#34;},{&#34;name&#34;:&#34;Marcos P. desde Bilbao&#34;,&#34;action&#34;:&#34;ha añadido Entrenador Marketing Pro&#34;},{&#34;name&#34;:&#34;Lucas T. desde Madrid&#34;,&#34;action&#34;:&#34;acaba de completar la compra&#34;}]'
json_new = '[{"&#34;name&#34;:&#34;D. Weber aus München&#34;,&#34;action&#34;:&#34;hat das FußballPro Masterpack freigeschaltet&#34;},{&#34;name&#34;:&#34;L. Schneider aus Hamburg&#34;,&#34;action&#34;:&#34;bereitet seine nächste Einheit in wenigen Minuten vor&#34;},{&#34;name&#34;:&#34;A. Brandt aus Köln&#34;,&#34;action&#34;:&#34;hat gerade die E-Jugend-Einheiten heruntergeladen&#34;},{&#34;name&#34;:&#34;M. Schulz aus Berlin&#34;,&#34;action&#34;:&#34;hat Trainer Marketing Pro hinzugefügt&#34;},{&#34;name&#34;:&#34;L. Kaiser aus Stuttgart&#34;,&#34;action&#34;:&#34;hat gerade den Kauf abgeschlossen&#34;}]'

# Nombres de testimonios en texto visible
name_repl = [
    ("Javier L.", "J. Krüger"),
    ("Pablo F.", "P. Schneider"),
    ("Andrés P.", "A. Brandt"),
    ("David R.", "D. Hoffmann"),
    ("Mateo C.", "M. Wagner"),
    ("Marcos S.", "M. Scholz"),
    ("Lucas T.", "L. Kaiser"),
]

# Aplicar: primero los strings largos, luego regex, luego nombres cortos
for old, new in repl:
    html = html.replace(old, new)
for pat, rep in regex_repl:
    html = re.sub(pat, rep, html)
html = html.replace(json_old, json_new)
for old, new in name_repl:
    html = html.replace(old, new)

# Textos cortos con contexto (nodos de texto únicos)
html = html.replace(">hoy<", ">heute<")
html = html.replace(">en<", ">in<")
html = html.replace(">HS<", ">STD<")
html = html.replace(">MIN<", ">MIN<")
html = html.replace(">SEG<", ">SEK<")

open(p, "w", encoding="utf-8").write(html)
print("OK - texto reescrito")