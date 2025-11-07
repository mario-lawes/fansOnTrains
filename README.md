# Fan-Travel Analyzer

## Projektziel
Dieses Projekt visualisiert Fanbewegungen rund um Bundesliga-Spiele auf einer interaktiven Karte.
- Wann und wo Züge voller Fans sein könnten
- Potenzielle Treffpunkte rivalisierender Fangruppen an Bahnhöfen oder in Zügen
Ziel ist es, ein übersichtliches Lagebild der Fanströme zu erhalten – für Fans, Vereine und Sicherheitsbehörden.

Dieses Projekt analysiert die Reisedaten von Fußballfans in Deutschland, um Einblicke in Zugauslastungen rund um Bundesliga-Spiele zu gewinnen. Es soll herausgefunden werden:
Welche Züge voraussichtlich voll sein könnten, basierend auf den Spielterminen und -orten.
Wo sich Fangruppen treffen könnten, insbesondere potenziell rivalisierende Gruppen, an Bahnhöfen oder in Zügen.
Damit können Fans, Vereine oder Sicherheitsbehörden besser planen und Risiken reduzieren.

## Funktionsweise
1. Spielpläne einlesen
  - Alle Spieltage der 1. bis 3. Bundesliga inklusive Datum, Uhrzeit, Heim- und Auswärtsteam.
2. Team-Städte auf Bahnhöfe mappen
  - Jeder Mannschaft wird die entsprechende Stadt zugeordnet und der nächstgelegene Bahnhof identifiziert.
3. EVA-Nummern abrufen
  - Mittels Deutsche Bahn Timetables API werden EVA-Nummern für die Bahnhöfe ermittelt, um Fahrpläne abzufragen.
4. Zugverbindungen analysieren
  - Relevante Zugverbindungen für jedes Spiel werden abgerufen.
5. Fan-Auslastung simulieren
  - Prognose von überfüllten Zügen und möglichen Treffpunkten rivalisierender Fangruppen.
6. Visualisierung auf Karte
  - Alle relevanten Bewegungen und Hotspots werden interaktiv auf einer Karte dargestellt:
  - Start- und Zielbahnhöfe
  - Zugverbindungen als Linien
  - Bahnhöfe mit hoher Fanaufkommen als Heatmap
## Technologien
- Python 3.12+
  - Pandas – für Datenmanagement der Spielpläne und Zugverbindungen
  - Requests – zur Abfrage der DB-API
  - xml.etree.ElementTree – zum Parsen der XML-Antworten der DB-API
  - Plotly – interaktive Kartenvisualisierung
