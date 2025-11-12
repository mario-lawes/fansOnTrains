# 🧳 Fan-Travel Analyzer

## Projektziel

In diesem Übungsprojekt möchte ich die potenziellen Reisebewegungen von Fußballfans in Deutschlan untersuchen, um **Zugauslastungen rund um Bundesliga-Spiele** besser einschätzen zu können.  
Ziel ist es, **mögliche Engpässe und Fan-Hotspots** frühzeitig zu erkennen und dadurch eine **bessere Planung für Fans, Vereine und Sicherheitsbehörden** zu ermöglichen.

Konkret soll analysiert werden:
- Welche **Züge voraussichtlich stark ausgelastet** sein könnten – basierend auf Spielterminen und -orten.  
- Wo sich **Fangruppen treffen könnten**, insbesondere rivalisierende Gruppen an Bahnhöfen oder in Zügen.  

---

## Funktionsweise

1. **Spielpläne einlesen**  
   - Import aller Spieltage der 1. bis 3. Bundesliga inklusive Datum, Uhrzeit, Heim- und Auswärtsteam.  

2. **Team-Städte auf Bahnhöfe mappen**  
   - Zuordnung jeder Mannschaft zu ihrer Heimstadt und Identifikation des nächstgelegenen Bahnhofs.  

3. **Fernverkehr-Verbindungen abrufen**  
   - Nutzung der Daten von [DELFI e.V.](http://gtfs.de,de,latest-fv-free,info@gtfs.de,https://gtfs.de)

4. **Zugverbindungen analysieren** *(in Entwicklung)*  
   - Abfrage und Filterung relevanter Zugverbindungen zwischen den Städten der Spielbegegnungen.  

5. **Fan-Auslastung simulieren** *(in Entwicklung)*  
   - Simulation voraussichtlicher Fanbewegungen zur Ermittlung potenziell überfüllter Züge und Treffpunkte rivalisierender Gruppen.  

6. **Visualisierung auf Karte** *(in Entwicklung)*  
   - Interaktive Darstellung der Fanbewegungen auf einer Karte, inklusive:
     - Start- und Zielbahnhöfen  
     - Zugverbindungen als Linien  
     - Heatmap mit Bahnhöfen hoher Fanfrequenz  

---

## Lernziele

Das Projekt dient als praktische Übung zur Kombination von **Datenanalyse, API-Integration und Geovisualisierung**:

- **Datenintegration:** Einlesen, Bereinigen und Strukturieren von Spielplänen und Bahndaten.  
- **API-Nutzung:** Abrufen und Verarbeiten von XML-Daten über die **Deutsche Bahn Timetables API**.  
- **Feature Engineering:** Herstellen semantischer Beziehungen zwischen Vereinen, Städten und Bahnhöfen.  
- **Visual Analytics:** Erstellung interaktiver Karten mit Plotly zur Exploration von Mobilitätsmustern.  

---

## Technologien

- **Python**
  - `pandas` – Datenmanagement und Transformation der Spiel- und Fahrplandaten  
  - `requests` – Abfrage der Deutschen Bahn API  
  - `xml.etree.ElementTree` – Parsing der XML-Antworten der DB-API  
  - `plotly` – Interaktive Karten- und Heatmap-Visualisierung  
