\# 📸 Smart Screenshot Sorter



Ein Python-Tool, das automatisch Screenshots (z. B. PNG, JPG) in einem angegebenen Ordner findet, 

sortiert und optional nach Datum in Unterordner verschiebt.  

Das Projekt dient als Lernübung für \*\*Python\*\*, \*\*CLI-Entwicklung\*\* und \*\*GitHub-Projektstruktur\*\*.



---



\## 🎯 Ziel des Projekts

\- Python in einem echten Projektkontext anwenden  

\- Ein eigenes CLI-Tool mit \*\*Typer\*\* entwickeln  

\- Den Umgang mit \*\*virtuellen Umgebungen (venv)\*\*, \*\*Git\*\* und \*\*VS Code\*\* trainieren  

\- Projekt als Referenz im GitHub-Portfolio nutzen  



---



\## ⚙️ Installation



1\. Repository klonen oder herunterladen  

2\. Virtuelle Umgebung erstellen:

&nbsp;  ```bash

&nbsp;  python -m venv .venv

Aktivieren:



bash

Code kopieren

.\\.venv\\Scripts\\Activate.ps1

Abhängigkeiten installieren:



bash

Code kopieren

pip install -r requirements.txt

🧩 Aktuell implementierte Funktionen

Funktion	Beschreibung	Beispielausgabe

Scan-Funktion (scan <Pfad>)	Durchsucht den angegebenen Ordner nach Screenshots (.png, .jpg, .jpeg). Erkennt alle Dateien, sortiert sie nach Änderungsdatum und gibt Dateigröße sowie Änderungszeit aus.	```bash

python -m src.sss.cli scan C:\\Users<USER>\\Downloads		



Gefundene Screenshots:



IMG\_0846.jpg – 0.33 MB – 10.02.2022 16:27:00



|

Code kopieren

| \*\*Sortiermodus\*\* | Sortiert Screenshots automatisch nach Änderungsdatum (neueste zuerst). | ```bash

Sortierreihenfolge: Neueste zuerst

``` |

| \*\*Dry-Run-Feature\*\* (`--dry-run`) | Simuliert das Verschieben in nach Datum geordnete Unterordner (`/by\_date/Jahr/Monat`). Keine Dateien werden verändert, nur der geplante Zielort angezeigt. | ```bash

PLAN: IMG\_0854.jpg → by\_date/2022/02

Nur Simulation (dry-run aktiv)

``` |

| \*\*Tatsächliches Verschieben\*\* | Wenn `--dry-run` \*\*nicht\*\* gesetzt ist, werden Dateien wirklich verschoben und nach Jahr/Monat einsortiert. | ```bash

✅ Verschoben: IMG\_0854.jpg → by\_date/2022/02

``` |



---



\## 💻 Verwendung

### Hilfe anzeigen
```bash
python -m src.sss.cli --help

\### Simulation (keine Dateien werden verändert)

```bash

python -m src.sss.cli scan "C:\Users\<DEINNAME>\Downloads"

Zielbasis selbst wählen (--out-dir)

python -m src.sss.cli scan "C:\Users\<DEINNAME>\Downloads" --out-dir "D:\Screenshots"


Tatsächliches Verschieben

bash

python -m src.sss.cli scan "C:\Users\<DEINNAME>\Downloads" --no-dry-run --out-dir "D:\Screenshots"

🧠 Beispielausgaben

📁 Zielbasis: D:\Screenshots
Gefundene Screenshots:
🟡 Simulation: IMG_0853.jpg → D:\Screenshots\2022\02
…
✅ Zusammenfassung: gesamt=12 | verschoben=0 | simuliert=12 | zielbasis=D:\Screenshots


📁 Projektstruktur



📸 Scan-Ausgabe



🧰 Verwendete Technologien

Python 3.10+



Typer (CLI-Framework)



OS (Modul für Dateiverwaltung)



Datetime (Zeitstempel-Umwandlung)



VS Code \& GitHub



📅 Geplante Erweiterungen

🧠 Duplicate Detector – erkennt doppelte Screenshots (dedupe.py)



🗂️ Metadata Extractor – liest EXIF- oder Dateimetadaten aus (metadata.py)



🚚 Mover – verschiebt Dateien automatisch nach Regeln (mover.py)



🏷️ Renamer – vergibt automatisch sprechende Dateinamen (renamer.py)



🔄 Watcher – beobachtet Ordner in Echtzeit (watcher.py)


---

## 📚 Über dieses Projekt

Dieses Tool ist Teil meines Lernprozesses in Python.  
Ich habe es mit Unterstützung von ChatGPT Schritt für Schritt aufgebaut, um zu verstehen,  
wie man eine eigene CLI-Anwendung strukturiert und mit Dateien arbeitet.

Der Fokus liegt nicht auf perfektem Code, sondern auf dem **Lernfortschritt** –  
insbesondere beim Verständnis und Anwenden von:

- 🧩 `pathlib` → Dateipfade und Ordnerverwaltung  
- ⏰ `datetime` → Arbeit mit Zeitstempeln  
- ⚙️ `typer` → Aufbau einer Kommandozeilen-App  
- 📁 Projektstruktur, CLI-Optionen und Modullogik

Ich verstehe die zentralen Abläufe und kann den Code erklären,  
weil jeder Teil bewusst mit Unterstützung entwickelt und nachvollzogen wurde.

> 💡 Ziel war nicht, ein Produkt zu veröffentlichen, sondern **praktisch zu lernen**,  
> wie Python-Code in realen Projekten organisiert und umgesetzt wird.



🧾 Lizenz



Dieses Projekt dient Lernzwecken.

(c) 2025 Johannes Stolley

