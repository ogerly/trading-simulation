### **README_Gedankengänge_und_Erklärung.md**

```markdown
# Erklärung der Trading Simulation Anwendung

Diese Anwendung wurde entwickelt, um Handelsstrategien mit Kryptowährungen zu simulieren und zu analysieren. Sie soll Benutzern helfen, die Auswirkungen verschiedener Parameter auf ihre Handelsstrategien zu verstehen und optimale Einstellungen zu finden.

## Idee und Motivation

Der Kryptowährungsmarkt ist bekannt für seine Volatilität. Händler suchen nach Möglichkeiten, von den Schwankungen zu profitieren. Diese Anwendung ermöglicht es, eine einfache Strategie zu simulieren, bei der ein Altcoin gekauft wird, wenn sein Preis gegenüber Bitcoin um einen bestimmten Prozentsatz fällt, und verkauft wird, wenn er um einen bestimmten Prozentsatz steigt.

Durch die Simulation können Benutzer sehen, wie sich ihre Strategie über einen bestimmten Zeitraum entwickelt hätte, ohne echtes Kapital zu riskieren.

## Hauptkomponenten

### 1. Datenabruf (`data.py`)

- **Preisgeschichte**: Historische Preisdaten von Bitcoin und ausgewählten Altcoins werden von der CoinGecko API abgerufen und zwischengespeichert, um API-Anfragen zu minimieren.
- **Top Gainers & Losers**: Aktuelle Daten zu den größten Gewinnern und Verlierern des Marktes werden abgerufen, um interessante Coins für die Analyse zu identifizieren.

### 2. Simulation (`simulation.py`)

- **Handelslogik**: Die Funktion `simulate_trading` implementiert die Handelsstrategie. Sie kauft den Altcoin, wenn der Preis um einen bestimmten Prozentsatz vom letzten Hoch gefallen ist, und verkauft ihn, wenn der Preis um einen bestimmten Prozentsatz vom Kaufpreis gestiegen ist.
- **Trade Log**: Alle Handelsaktivitäten werden protokolliert, um sie später analysieren zu können.

### 3. Benutzeroberfläche (`gui.py`)

- **Trading-Simulation Tab**: Ermöglicht es dem Benutzer, die Parameter für die Simulation einzustellen und die Ergebnisse zu sehen. Ein Diagramm zeigt die Preisentwicklung und die Handelsaktivitäten.
- **Gainers & Losers Tab**: Zeigt die Top Gewinner und Verlierer des Marktes an. Mit einem Klick auf einen Coin kann dieser für die Simulation ausgewählt werden.
- **Parameteranalyse Tab**: Führt Simulationen für verschiedene Kombinationen von Kauf- und Verkaufsprozentsätzen durch. Die Ergebnisse werden in einer Tabelle angezeigt, um optimale Parameter zu identifizieren. Neu hinzugefügt sind Informationen über das Startkapital, die Anzahl der Transaktionen und den Zeitraum, in dem die Transaktionen stattgefunden haben.

## Nutzung der Anwendung

1. **Simulation durchführen**: Wählen Sie einen Altcoin, legen Sie die Kauf- und Verkaufsprozentsätze fest und starten Sie die Simulation. Analysieren Sie die Ergebnisse und passen Sie die Parameter nach Bedarf an.

2. **Gainers & Losers erkunden**: Finden Sie interessante Coins basierend auf aktuellen Marktbewegungen und führen Sie Simulationen für diese durch.

3. **Parameteranalyse**: Untersuchen Sie, welche Kombinationen von Kauf- und Verkaufsprozentsätzen die besten Ergebnisse liefern, um Ihre Strategie zu optimieren. Die Analyse zeigt das potenzielle Endkapital, die Anzahl der Trades und den Zeitraum der Handelsaktivitäten.

## Weiterentwicklung

- **Erweiterte Handelsstrategien**: Implementierung komplexerer Strategien und Indikatoren.
- **Benutzerfreundlichkeit**: Verbesserung der GUI für eine intuitivere Bedienung.
- **Performance**: Optimierung des Codes für schnellere Berechnungen und effizientere Ressourcennutzung.

## Schlusswort

Diese Anwendung dient als Werkzeug für diejenigen, die den Kryptowährungsmarkt besser verstehen und ihre Handelsstrategien verbessern möchten. Sie bietet eine Plattform zum Experimentieren und Lernen, ohne finanzielles Risiko einzugehen.
```