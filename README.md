
# Trading Simulation Anwendung

Dies ist eine Trading Simulation Anwendung, die es ermöglicht, Handelsstrategien mit Kryptowährungen zu simulieren und zu analysieren. Die Anwendung nutzt die CoinGecko API, um historische Preisdaten von Bitcoin und ausgewählten Altcoins abzurufen und führt eine einfache Handelsstrategie basierend auf festgelegten Kauf- und Verkaufsprozentsätzen durch.

## Installation

1. **Python installieren**: Stellen Sie sicher, dass Python 3.7 oder höher installiert ist.

2. **Repository klonen oder herunterladen**:

   ```bash
   git clone https://github.com/IhrBenutzername/trading-simulation.git
   cd trading-simulation
   ```

3. **Abhängigkeiten installieren**:

   Installieren Sie die erforderlichen Python-Pakete mit `pip`:

   ```bash
   pip install -r requirements.txt
   ```

   **Hinweis:** Stellen Sie sicher, dass Sie eine virtuelle Umgebung verwenden, um Abhängigkeitskonflikte zu vermeiden.

## Startprozess

Um die Anwendung zu starten, führen Sie das `main.py` Skript aus:

```bash
python main.py
```

Dies öffnet die grafische Benutzeroberfläche der Anwendung.

## Funktionsumfang

### Trading-Simulation Tab

- **Altcoin-Auswahl**: Wählen Sie einen Altcoin aus einer Liste verfügbarer Coins aus.
- **Parameter einstellen**: Legen Sie die Kauf- und Verkaufsprozentsätze fest, die die Handelsstrategie steuern.
- **Zeitraum auswählen**: Wählen Sie den Zeitraum für die Simulation (z.B. 90, 180, 365 Tage).
- **Startkapital eingeben**: Geben Sie das Startkapital in USD ein, das in BTC umgerechnet wird.
- **Simulation starten**: Führen Sie die Simulation durch und analysieren Sie die Ergebnisse, einschließlich des Endkapitals, der durchschnittlichen täglichen Fluktuation und der durchgeführten Trades.
- **Visualisierung**: Betrachten Sie Diagramme der Preisentwicklung von Bitcoin und dem ausgewählten Altcoin sowie die Handelsaktivitäten.

### Gainers & Losers Tab

- **Marktübersicht**: Sehen Sie die Top 10 Gewinner und Verlierer des Marktes in den letzten 24 Stunden.
- **Schnellauswahl**: Wählen Sie einen Coin aus der Liste, um ihn direkt für die Simulation auszuwählen.

### Parameteranalyse Tab

- **Batch-Simulationen**: Führen Sie Simulationen über einen Bereich von Kauf- und Verkaufsprozentsätzen durch, um optimale Einstellungen zu finden.
- **Ergebnisse anzeigen**: Betrachten Sie die Ergebnisse in einer Tabelle, die Gewinn/Verlust, Anzahl der Transaktionen und den Zeitraum der Handelsaktivitäten für jede Kombination anzeigt.
- **Analysebericht**: Erhalten Sie einen Bericht mit den Einstellungen, die den höchsten Gewinn erzielt haben.

## Verwendung

1. **Anwendung starten**: Führen Sie `python main.py` aus.

2. **Simulation durchführen**:

   - Gehen Sie zum **Trading-Simulation** Tab.
   - Wählen Sie den gewünschten Altcoin aus.
   - Stellen Sie die Kauf- und Verkaufsprozentsätze sowie das Startkapital ein.
   - Klicken Sie auf **Simulation starten**.
   - Analysieren Sie die Ergebnisse und betrachten Sie die Diagramme.

3. **Markttrends erkunden**:

   - Wechseln Sie zum **Gainers & Losers** Tab.
   - Sehen Sie sich die aktuellen Markttrends an.
   - Klicken Sie auf einen Coin, um ihn für die Simulation auszuwählen.

4. **Parameteranalyse durchführen**:

   - Gehen Sie zum **Parameteranalyse** Tab.
   - Legen Sie die Bereiche für die Kauf- und Verkaufsprozentsätze fest.
   - Klicken Sie auf **Analyse starten**.
   - Betrachten Sie die Ergebnisse in der Tabelle und lesen Sie den Analysebericht.

## Anforderungen

- Python 3.7 oder höher
- Abhängigkeiten aus `requirements.txt` (z.B. pandas, matplotlib, tkinter, requests)

## Hinweise

- **API-Limits**: Beachten Sie, dass die Verwendung der CoinGecko API gewissen Limits unterliegt. Bei intensiver Nutzung kann es zu Einschränkungen kommen.
- **Datenverfügbarkeit**: Die Genauigkeit der Simulation hängt von der Verfügbarkeit und Qualität der historischen Preisdaten ab.

## Weiterentwicklung

- **Erweiterte Strategien**: Integration weiterer Handelsstrategien und Indikatoren.
- **Live-Daten**: Echtzeit-Analyse und Monitoring der Märkte.
- **Benutzererfahrung**: Verbesserung der Benutzeroberfläche und der Interaktivität.

## Lizenz

Dieses Projekt steht unter der [MIT Lizenz](LICENSE).

## Kontakt

Bei Fragen oder Anregungen wenden Sie sich bitte an [Ihre E-Mail-Adresse] oder erstellen Sie ein Issue im Repository.
```
