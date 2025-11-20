# Smart Screenshot Sorter

[![Status](https://img.shields.io/badge/status-in_development-blue?style=flat-square)](#)
[![Tests](https://img.shields.io/badge/tests-pytest-blueviolet?style=flat-square)](https://docs.pytest.org/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square)](https://www.python.org/)
[![Type](https://img.shields.io/badge/project-CLI_tool-lightgrey?style=flat-square)](#)

------------------------------------------------------------------------

## Inhalt

1.  [Überblick](#überblick)
2.  [Funktionen](#funktionen)
3.  [Installation](#installation)
4.  [CLI-Nutzung](#cli-nutzung)
    -   [scan](#scan)
    -   [dedupe](#dedupe)
5.  [Tests](#tests)
6.  [Architektur](#architektur)
7.  [Roadmap](#roadmap)

------------------------------------------------------------------------

## Überblick

Smart Screenshot Sorter (SSS) ist ein modular aufgebautes
Python-CLI-Werkzeug zur Analyse, Sortierung und Bereinigung von
Bilddateien, insbesondere Screenshots.

Ziel des Projekts ist es: - eine klare Softwarearchitektur zu üben, -
testgetrieben zu entwickeln (TDD), - CLI-Tools professionell
aufzubauen, - wiederholbare, stabile Dateioperationen sicherzustellen.

SSS trennt die CLI-Schicht klar von der Logik und ist vollständig
testbar.

------------------------------------------------------------------------

## Funktionen

### 1. Scan

Analysiert ein Eingabeverzeichnis, erkennt gängige Screenshot-Dateien
und erzeugt eine Zielstruktur nach Jahr und Monat.

-   Standard: Dry-Run (keine Änderungen)
-   Verschieben nur mit `--no-dry-run`
-   Konfigurierbares Zielverzeichnis

### 2. Duplicate Detection (dedupe)

Erkennt doppelte Dateien (über Hashvergleich) und generiert definierte
Aktionen für deren Bereinigung.

-   Standard: Dry-Run
-   Mit `--execute`: Aktionen wirklich ausführen
-   Klare und nachvollziehbare Ausgabe
-   Alle Operationen testbar

### 3. Sichere Operationen

Alle Dateiaktionen sind gekapselt und reproduzierbar.\
Tests stellen sicher, dass: - Dry-Runs nie Dateien verändern -
Execute-Modi zuverlässig verschieben - Fehlerfälle abgefangen werden

------------------------------------------------------------------------

## Installation

Das Paket kann einfach über PyPI installiert werden:

pip install smart-screenshot-sorter


Überprüfe anschließend, ob der CLI-Befehl verfügbar ist:

sss --help
------------------------------------------------------------------------

## CLI-Nutzung

Die CLI basiert auf Typer und ist bewusst minimalistisch und konsistent
gehalten.

------------------------------------------------------------------------

### scan

Analysiert ein Verzeichnis, erkennt Screenshots und plant
Sortieraktionen.

**Dry-Run (Standard):**

``` bash
python -m src.sss.cli scan "C:/Users/<Name>/Downloads"
```

**Zielverzeichnis angeben:**

``` bash
python -m src.sss.cli scan "C:/Downloads" --out-dir "D:/Screenshots"
```

**Operationen ausführen (kein Dry-Run):**

``` bash
python -m src.sss.cli scan "C:/Downloads" --no-dry-run --out-dir "D:/Screenshots"
```

------------------------------------------------------------------------

### dedupe

Erkennt doppelte Dateien und plant Move-Aktionen.

**Dry-Run (Standard):**

``` bash
python -m src.sss.cli dedupe "C:/Users/<Name>/Downloads"
```

Beispielausgabe:

    Dry-Run: 3 geplante Aktionen
    MOVE C:/Downloads/a.jpg -> C:/Downloads/duplicates/a.jpg
    MOVE C:/Downloads/b.jpg -> C:/Downloads/duplicates/b.jpg

**Moves ausführen:**

``` bash
python -m src.sss.cli dedupe --execute "C:/Downloads"
```

Beispiel:

    Ausführung abgeschlossen.
    Verschoben: 3 Dateien

------------------------------------------------------------------------

## Tests

SSS wurde vollständig testgetrieben entwickelt.

Tests starten:

``` bash
pytest
```

Coverage:

``` bash
pytest --cov=src/sss
```

Abgedeckte Szenarien:

-   Dry-Run ohne Auswirkungen
-   Execute verschiebt Dateien korrekt
-   Keine Duplikate → informative Ausgabe
-   Fehlerhafte Pfade → stabile Reaktion
-   Konsistentes Verhalten über `CliRunner`

------------------------------------------------------------------------

## Architektur

Verzeichnisstruktur:

    src/sss/
    │
    ├── cli.py            # CLI (Typer), ruft Pipeline-Schritte auf
    ├── dedupe.py         # Duplicate Detection, DedupAction, execute_actions
    ├── mover.py          # Sichere Dateioperationen
    ├── summary.py        # Ausführungsstatistiken
    ├── metadata.py       # (in Planung)
    └── utils.py          # Hilfsfunktionen

Designprinzipien:

-   Trennung von CLI und Logik
-   Keine versteckten I/O-Operationen
-   Reproduzierbares Verhalten
-   Vollständige Testbarkeit
-   Kleine, klar verantwortliche Module

------------------------------------------------------------------------

MIT License

Copyright (c) 2025 Johannes Stolley

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

------------------------------------------------------------------------

## Roadmap

### Geplant

-   Bessere Formatierung der CLI-Ausgabe
-   Erweiterte Fehlerbehandlung
-   EXIF-/Metadatenunterstützung
-   Automatisches Umbenennen von Dateien
-   Verzeichnisüberwachung (Watcher)
-   Packaging als `pip`-Modul

### Mittelfristig

-   Konsolidierte CLI mit Subcommands
-   Konfigurierbare Pipeline-Regeln
-   Plugin-basierte Actions

### Langfristig

-   ML-basierte Screenshot-Kategorisierung
-   GUI-Frontend
-   Cross-Plattform-Support
