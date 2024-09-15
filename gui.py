import tkinter as tk
from tkinter import ttk, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

from data import get_price_history, get_top_gainers_and_losers
from simulation import simulate_trading

DEFAULT_USD = 1000



def run_simulation(coin_var, buy_entry, sell_entry, days_var, initial_usd_entry, result_label, fluctuation_label, trades_textbox, frame_plot):
    try:
        buy_percentage = float(buy_entry.get()) / 100  # In Dezimal umwandeln
        sell_percentage = float(sell_entry.get()) / 100  # In Dezimal umwandeln
        selected_coin = coin_var.get()
        selected_days = int(days_var.get())
        initial_usd = float(initial_usd_entry.get())
    except ValueError:
        result_label.config(text="Fehler: Bitte gültige Eingaben machen.")
        return

    if buy_percentage <= 0 or sell_percentage <= 0 or initial_usd <= 0:
        result_label.config(text="Fehler: Werte müssen positiv sein.")
        return

    # Startkapital in BTC umrechnen
    btc_price_data = get_price_history('bitcoin', days=1)
    if btc_price_data is None:
        result_label.config(text="Fehler beim Abrufen des aktuellen BTC-Preises.")
        return
    current_btc_price = btc_price_data['bitcoin_price'].iloc[-1]
    initial_btc = initial_usd / current_btc_price

    # Daten abrufen
    btc_df = get_price_history('bitcoin', days=selected_days)
    altcoin_df = get_price_history(selected_coin, days=selected_days)

    if btc_df is None or altcoin_df is None:
        result_label.config(text="Fehler beim Abrufen der Preisdaten. Bitte versuchen Sie es später erneut.")
        return

    # Daten zusammenführen
    df = pd.merge(btc_df, altcoin_df, on='timestamp', how='inner')
    df.rename(columns={f'{selected_coin}_price': 'altcoin_price'}, inplace=True)

    # Berechnung der täglichen Renditen
    df['btc_return'] = df['bitcoin_price'].pct_change()
    df['altcoin_return'] = df['altcoin_price'].pct_change()

    # Berechnung der Differenz der Renditen
    df['return_difference'] = df['altcoin_return'] - df['btc_return']

    # Berechnung der durchschnittlichen Fluktuation
    fluctuation_value = df['return_difference'].abs().mean() * 100  # In Prozent umwandeln

    # Simulation durchführen
    final_btc, trades = simulate_trading(df, buy_percentage=buy_percentage, sell_percentage=sell_percentage, initial_btc=initial_btc)
    result_label.config(text=f"Startkapital: {initial_btc:.6f} BTC, Endkapital: {final_btc:.6f} BTC")

    # Fluktuationswert anzeigen
    fluctuation_label.config(text=f"Durchschnittliche tägliche Fluktuation zwischen {selected_coin.capitalize()} und BTC: {fluctuation_value:.2f}%")

    # Trades anzeigen in scrollbarem Fenster mit farblicher Markierung
    trades_textbox.delete(1.0, tk.END)
    for trade in trades:
        date_str = trade['timestamp'].date()
        action = trade['action']
        price_usd = trade['price_usd']
        price_btc = trade['price_btc']
        profit = trade['profit']
        profit_str = f"{profit:.6f} BTC"

        if 'holding' in trade and trade['holding']:
            color = 'blue'
            altcoin_balance = trade['altcoin_balance']  # Zugriff auf altcoin_balance
            trade_text = f"{date_str} - HALTEN von {altcoin_balance:.6f} Einheiten - Aktueller Preis: {price_usd:.2f} USD ({price_btc:.8f} BTC)\n"
        else:
            if profit > 0:
                color = 'green'
            elif profit < 0:
                color = 'red'
            else:
                color = 'black'
            trade_text = f"{date_str} - {action} bei Preis {price_usd:.2f} USD ({price_btc:.8f} BTC) - Gewinn/Verlust: {profit_str}\n"

        trades_textbox.insert(tk.END, trade_text, color)

    # Tags für Farben definieren
    trades_textbox.tag_configure('green', foreground='green')
    trades_textbox.tag_configure('red', foreground='red')
    trades_textbox.tag_configure('black', foreground='black')
    trades_textbox.tag_configure('blue', foreground='blue')

    # Plot aktualisieren
    plot_trades(df, trades, selected_coin, frame_plot)


def plot_trades(df, trades, altcoin_id, frame_plot):
    # Vorherigen Inhalt von frame_plot löschen
    for widget in frame_plot.winfo_children():
        widget.destroy()

    # Figure mit zwei Subplots erstellen
    fig, (ax1, ax3) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

    # Erster Subplot: Preisentwicklung
    ax1.plot(df['timestamp'], df['bitcoin_price'], label='BTC Preis (USD)', color='blue')
    ax1.set_ylabel('BTC Preis (USD)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    ax1_2 = ax1.twinx()
    ax1_2.plot(df['timestamp'], df['altcoin_price'], label=f'{altcoin_id.capitalize()} Preis (USD)', color='orange')
    ax1_2.set_ylabel(f'{altcoin_id.capitalize()} Preis (USD)', color='orange')
    ax1_2.tick_params(axis='y', labelcolor='orange')

    # Kauf- und Verkaufspunkte markieren
    buy_dates = [trade['timestamp'] for trade in trades if 'BUY' in trade['action']]
    sell_dates = [trade['timestamp'] for trade in trades if 'SELL' in trade['action']]
    buy_prices = df[df['timestamp'].isin(buy_dates)]['altcoin_price']
    sell_prices = df[df['timestamp'].isin(sell_dates)]['altcoin_price']

    # Gewinne und Verluste bei Verkäufen unterscheiden
    profits = [trade['profit'] for trade in trades if 'SELL' in trade['action']]
    profit_colors = ['green' if profit > 0 else 'red' if profit < 0 else 'black' for profit in profits]

    # Käufe plotten
    ax1_2.scatter(buy_dates, buy_prices, color='green', marker='^', s=100, label='Kauf')

    # Verkäufe plotten mit farblicher Unterscheidung
    for i, sell_date in enumerate(sell_dates):
        ax1_2.scatter(sell_date, sell_prices.iloc[i], color=profit_colors[i], marker='v', s=100, label='Verkauf' if i == 0 else "")

    ax1.set_title(f'Preisentwicklung von BTC und {altcoin_id.capitalize()}')
    ax1.legend(loc='upper left')
    ax1_2.legend(loc='upper right')

    # Zweiter Subplot: Fluktuation darstellen
    ax3.plot(df['timestamp'], df['return_difference'] * 100, color='purple')
    ax3.set_xlabel('Datum')
    ax3.set_ylabel('Fluktuation (%)', color='purple')
    ax3.tick_params(axis='y', labelcolor='purple')
    ax3.axhline(0, color='black', linewidth=0.5, linestyle='--')
    ax3.set_title('Tägliche Differenz der Renditen zwischen Altcoin und BTC')

    ax3.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    fig.autofmt_xdate()

    fig.tight_layout()

    # Plot in tkinter-Fenster einfügen
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def display_gainers_and_losers(frame_gainers_losers, notebook, coin_var, frame_simulation):
    gainers, losers = get_top_gainers_and_losers()

    # Label für Gainers
    gainers_label = ttk.Label(frame_gainers_losers, text="Top 10 Gewinner (24h):")
    gainers_label.grid(row=0, column=0, padx=5, pady=5)

    gainers_listbox = tk.Listbox(frame_gainers_losers)
    gainers_listbox.grid(row=1, column=0, padx=5, pady=5)

    for coin in gainers:
        gainers_listbox.insert(tk.END, f"{coin['name']} ({coin['symbol'].upper()}): {coin['price_change_percentage_24h']:.2f}%")

    # Label für Losers
    losers_label = ttk.Label(frame_gainers_losers, text="Top 10 Verlierer (24h):")
    losers_label.grid(row=0, column=1, padx=5, pady=5)

    losers_listbox = tk.Listbox(frame_gainers_losers)
    losers_listbox.grid(row=1, column=1, padx=5, pady=5)

    for coin in losers:
        losers_listbox.insert(tk.END, f"{coin['name']} ({coin['symbol'].upper()}): {coin['price_change_percentage_24h']:.2f}%")

    # Event-Handler für das Laden der Coin-Daten bei Klick
    gainers_listbox.bind('<<ListboxSelect>>', lambda event: load_coin_data(event, gainers, coin_var, notebook, frame_simulation))
    losers_listbox.bind('<<ListboxSelect>>', lambda event: load_coin_data(event, losers, coin_var, notebook, frame_simulation))


def load_coin_data(event, coin_list, coin_var, notebook, frame_simulation):
    widget = event.widget
    index = int(widget.curselection()[0])
    selected_coin = coin_list[index]
    coin_id = selected_coin['id']

    # Setzen des ausgewählten Coins in der Simulation
    coin_var.set(coin_id)
    # Wechsel zum Simulationstab
    notebook.select(frame_simulation)

    # Optional: Starten Sie die Simulation automatisch
    # run_simulation()


def create_parameter_analysis_tab(frame_parameter_analysis, notebook, available_altcoins):
    # Oberes Frame für Eingabefelder im Parameteranalyse-Tab
    frame_analysis_top = tk.Frame(frame_parameter_analysis)
    frame_analysis_top.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

    # Dropdown-Menü zur Auswahl eines Altcoins
    altcoin_label = ttk.Label(frame_analysis_top, text="Altcoin auswählen:")
    altcoin_label.grid(row=0, column=0, sticky=tk.W, padx=5)

    altcoin_var_analysis = tk.StringVar()
    altcoin_var_analysis.set(available_altcoins[0])  # Standardwert
    altcoin_menu_analysis = ttk.OptionMenu(frame_analysis_top, altcoin_var_analysis, available_altcoins[0], *available_altcoins)
    altcoin_menu_analysis.grid(row=0, column=1, padx=5)

    # Eingabefelder für Kaufprozentsatz
    min_buy_label = ttk.Label(frame_analysis_top, text="Min. Kaufprozentsatz (%):")
    min_buy_label.grid(row=1, column=0, sticky=tk.W, padx=5)
    min_buy_entry = ttk.Entry(frame_analysis_top)
    min_buy_entry.insert(0, "1")  # Standardwert
    min_buy_entry.grid(row=1, column=1, padx=5)

    max_buy_label = ttk.Label(frame_analysis_top, text="Max. Kaufprozentsatz (%):")
    max_buy_label.grid(row=2, column=0, sticky=tk.W, padx=5)
    max_buy_entry = ttk.Entry(frame_analysis_top)
    max_buy_entry.insert(0, "15")  # Standardwert
    max_buy_entry.grid(row=2, column=1, padx=5)

    buy_step_label = ttk.Label(frame_analysis_top, text="Schrittweite Kaufprozentsatz (%):")
    buy_step_label.grid(row=3, column=0, sticky=tk.W, padx=5)
    buy_step_entry = ttk.Entry(frame_analysis_top)
    buy_step_entry.insert(0, "1")  # Standardwert
    buy_step_entry.grid(row=3, column=1, padx=5)

    # Eingabefelder für Verkaufsprozentsatz
    min_sell_label = ttk.Label(frame_analysis_top, text="Min. Verkaufsprozentsatz (%):")
    min_sell_label.grid(row=1, column=2, sticky=tk.W, padx=5)
    min_sell_entry = ttk.Entry(frame_analysis_top)
    min_sell_entry.insert(0, "5")  # Standardwert
    min_sell_entry.grid(row=1, column=3, padx=5)

    max_sell_label = ttk.Label(frame_analysis_top, text="Max. Verkaufsprozentsatz (%):")
    max_sell_label.grid(row=2, column=2, sticky=tk.W, padx=5)
    max_sell_entry = ttk.Entry(frame_analysis_top)
    max_sell_entry.insert(0, "25")  # Standardwert
    max_sell_entry.grid(row=2, column=3, padx=5)

    sell_step_label = ttk.Label(frame_analysis_top, text="Schrittweite Verkaufsprozentsatz (%):")
    sell_step_label.grid(row=3, column=2, sticky=tk.W, padx=5)
    sell_step_entry = ttk.Entry(frame_analysis_top)
    sell_step_entry.insert(0, "1")  # Standardwert
    sell_step_entry.grid(row=3, column=3, padx=5)

    # Zeitraum in Tagen
    days_label = ttk.Label(frame_analysis_top, text="Zeitraum in Tagen:")
    days_label.grid(row=4, column=0, sticky=tk.W, padx=5)
    days_var_analysis = tk.StringVar()
    days_var_analysis.set('90')  # Standardwert
    days_options = ['90', '180', '365']
    days_menu_analysis = ttk.OptionMenu(frame_analysis_top, days_var_analysis, days_var_analysis.get(), *days_options)
    days_menu_analysis.grid(row=4, column=1, padx=5)

    # Tabelle für die Ergebnisse mit zusätzlicher Spalte für Anzahl der Transaktionen
    analysis_treeview = ttk.Treeview(
        frame_parameter_analysis,
        columns=('buy_percentage', 'sell_percentage', 'profit', 'num_trades'),
        show='headings'
    )
    analysis_treeview.heading('buy_percentage', text='Kaufprozentsatz')
    analysis_treeview.heading('sell_percentage', text='Verkaufsprozentsatz')
    analysis_treeview.heading('profit', text='Gewinn/Verlust (BTC)')
    analysis_treeview.heading('num_trades', text='Anzahl der Transaktionen')
    analysis_treeview.pack(fill=tk.BOTH, expand=True)

    # Label für den Analysebericht hinzufügen
    analysis_report_label = ttk.Label(frame_parameter_analysis, text="", font=('Arial', 12), foreground='blue')
    analysis_report_label.pack(pady=10)

    # Button zum Starten der Analyse mit Übergabe des Labels
    run_analysis_button = ttk.Button(
        frame_analysis_top,
        text="Analyse starten",
        command=lambda: run_parameter_analysis(
            altcoin_var_analysis.get(),
            min_buy_entry,
            max_buy_entry,
            buy_step_entry,
            min_sell_entry,
            max_sell_entry,
            sell_step_entry,
            days_var_analysis,
            analysis_treeview,
            analysis_report_label  # Label übergeben
        )
    )
    run_analysis_button.grid(row=5, column=0, padx=5, pady=10)

    return analysis_treeview




def create_simulation_tab(frame_simulation, notebook):
    # Oberes Frame für Eingabefelder und Buttons im Simulationstab
    frame_top = tk.Frame(frame_simulation)
    frame_top.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

    # Unterer Frame für Ausgabe im Simulationstab
    frame_bottom = tk.Frame(frame_simulation)
    frame_bottom.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Frame für Trades und Plot im Simulationstab
    frame_trades = tk.Frame(frame_bottom, width=500)
    frame_trades.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    frame_plot = tk.Frame(frame_bottom, width=700)
    frame_plot.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Auswahl des Altcoins im Simulationstab
    coin_label = ttk.Label(frame_top, text="Altcoin auswählen:")
    coin_label.grid(row=0, column=0, sticky=tk.W, padx=5)
    coin_var = tk.StringVar()
    coin_var.set('ethereum')  # Standardwert auf 'ethereum' gesetzt
    coin_options = ['ethereum', 'litecoin', 'ripple', 'bitcoin-cash', 'eos']
    coin_menu = ttk.OptionMenu(frame_top, coin_var, coin_var.get(), *coin_options)
    coin_menu.grid(row=0, column=1, padx=5)

    # Eingabefelder für prozentuale Schwankungen im Simulationstab
    buy_label = ttk.Label(frame_top, text="Kauf bei Rückgang um (%):")
    buy_label.grid(row=1, column=0, sticky=tk.W, padx=5)
    buy_entry = ttk.Entry(frame_top)
    buy_entry.insert(0, "5")  # Standardwert
    buy_entry.grid(row=1, column=1, padx=5)
    buy_info = ttk.Label(frame_top, text="Altcoin wird gekauft, wenn das Verhältnis um diesen Prozentsatz vom letzten Hoch gefallen ist.")
    buy_info.grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=5)

    sell_label = ttk.Label(frame_top, text="Verkauf bei Anstieg um (%):")
    sell_label.grid(row=3, column=0, sticky=tk.W, padx=5)
    sell_entry = ttk.Entry(frame_top)
    sell_entry.insert(0, "5")  # Standardwert
    sell_entry.grid(row=3, column=1, padx=5)
    sell_info = ttk.Label(frame_top, text="Altcoin wird verkauft, wenn das Verhältnis um diesen Prozentsatz vom Kaufpreis gestiegen ist.")
    sell_info.grid(row=4, column=0, columnspan=2, sticky=tk.W, padx=5)

    # Startkapital eingeben
    initial_usd_label = ttk.Label(frame_top, text="Startkapital in USD:")
    initial_usd_label.grid(row=5, column=0, sticky=tk.W, padx=5)
    initial_usd_entry = ttk.Entry(frame_top)
    initial_usd_entry.insert(0, str(DEFAULT_USD))  # Standardwert
    initial_usd_entry.grid(row=5, column=1, padx=5)
    initial_usd_info = ttk.Label(frame_top, text="Das Startkapital wird in BTC umgerechnet basierend auf dem aktuellen BTC-Preis.")
    initial_usd_info.grid(row=6, column=0, columnspan=2, sticky=tk.W, padx=5)

    # Zeitraum auswählen
    days_label = ttk.Label(frame_top, text="Zeitraum in Tagen:")
    days_label.grid(row=7, column=0, sticky=tk.W, padx=5)
    days_var = tk.StringVar()
    days_var.set('90')  # Standardwert
    days_options = ['90', '180', '365']
    days_menu = ttk.OptionMenu(frame_top, days_var, days_var.get(), *days_options)
    days_menu.grid(row=7, column=1, padx=5)

    run_button = ttk.Button(frame_top, text="Simulation starten", command=lambda: run_simulation(coin_var, buy_entry, sell_entry, days_var, initial_usd_entry, result_label, fluctuation_label, trades_textbox, frame_plot))
    run_button.grid(row=8, column=0, padx=5, pady=10)

    result_label = ttk.Label(frame_top, text="Startkapital: - BTC, Endkapital: - BTC")
    result_label.grid(row=8, column=1, padx=5, pady=10)

    # Fluktuationswert anzeigen
    fluctuation_label = ttk.Label(frame_top, text="Durchschnittliche tägliche Fluktuation: -")
    fluctuation_label.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

    # Scrollbarer Textbereich für Trades mit Tags für Farben
    trades_textbox = scrolledtext.ScrolledText(frame_trades, wrap=tk.WORD, width=40, height=10)
    trades_textbox.pack(fill=tk.BOTH, expand=True)
    trades_textbox.tag_configure('green', foreground='green')
    trades_textbox.tag_configure('red', foreground='red')
    trades_textbox.tag_configure('black', foreground='black')
    trades_textbox.tag_configure('blue', foreground='blue')

    return frame_simulation

def run_parameter_analysis(
    altcoin,
    min_buy_entry,
    max_buy_entry,
    buy_step_entry,
    min_sell_entry,
    max_sell_entry,
    sell_step_entry,
    days_var_analysis,
    analysis_treeview,
    analysis_report_label
):
    try:
        # Eingabewerte abrufen
        min_buy = float(min_buy_entry.get())
        max_buy = float(max_buy_entry.get())
        buy_step = float(buy_step_entry.get())
        min_sell = float(min_sell_entry.get())
        max_sell = float(max_sell_entry.get())
        sell_step = float(sell_step_entry.get())
        days = int(days_var_analysis.get())

        # Historische Preisdaten für den ausgewählten Altcoin laden
        altcoin_df = get_price_history(altcoin, days=days)
        if altcoin_df is None or altcoin_df.empty:
            print(f"Fehler: Keine Daten für den Altcoin {altcoin} verfügbar.")
            return

        # Bitcoin-Preisdaten laden
        btc_df = get_price_history('bitcoin', days=days)
        if btc_df is None or btc_df.empty:
            print("Fehler beim Abrufen der Bitcoin-Preisdaten.")
            return

        # Daten zusammenführen
        df = pd.merge(btc_df, altcoin_df, on='timestamp', how='inner')
        df.rename(columns={f'{altcoin}_price': 'altcoin_price'}, inplace=True)

        if df.empty:
            print("Fehler: Der kombinierte DataFrame ist leer.")
            return

        # Leere das Treeview vor dem Hinzufügen neuer Daten
        for i in analysis_treeview.get_children():
            analysis_treeview.delete(i)

        # Ergebnisse sammeln
        results = []

        # Analysiere jede Kombination von Kauf- und Verkaufsprozentsätzen
        for buy_percentage in range(int(min_buy), int(max_buy + 1), int(buy_step)):
            for sell_percentage in range(int(min_sell), int(max_sell + 1), int(sell_step)):
                # Simulation durchführen
                final_btc, trades = simulate_trading(
                    df,
                    buy_percentage / 100,
                    sell_percentage / 100,
                    initial_btc=0.01667
                )
                num_trades = len(trades)
                profit = final_btc - 0.01667  # Gewinn/Verlust berechnen
                # Ergebnisse zur Tabelle hinzufügen
                analysis_treeview.insert(
                    "",
                    "end",
                    values=(buy_percentage, sell_percentage, round(profit, 6), num_trades)
                )
                # Ergebnisse speichern
                results.append({
                    'buy_percentage': buy_percentage,
                    'sell_percentage': sell_percentage,
                    'profit': profit,
                    'num_trades': num_trades
                })

        # Analysebericht erstellen
        if results:
            # Bestes Ergebnis finden
            best_result = max(results, key=lambda x: x['profit'])
            # Bericht erstellen
            report = (
                f"Beste Einstellungen:\n"
                f"Kaufprozentsatz: {best_result['buy_percentage']}%\n"
                f"Verkaufsprozentsatz: {best_result['sell_percentage']}%\n"
                f"Gewinn/Verlust: {best_result['profit']:.6f} BTC\n"
                f"Anzahl der Transaktionen: {best_result['num_trades']}\n"
            )
            # Bericht im Label anzeigen
            analysis_report_label.config(text=report)
        else:
            analysis_report_label.config(text="Keine Ergebnisse gefunden.")
    except Exception as e:
        print(f"Fehler: {e}")






def create_gui():
    # GUI erstellen
    root = tk.Tk()
    root.title("Trading Simulation")
    root.geometry("1200x900")

    # Notebook für Tabs erstellen
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Tab für Trading-Simulation hinzufügen
    frame_simulation = tk.Frame(notebook)
    notebook.add(frame_simulation, text="Trading-Simulation")

    # Tab für Gainers und Losers hinzufügen
    frame_gainers_losers = tk.Frame(notebook)
    notebook.add(frame_gainers_losers, text="Gainers & Losers")

    # Tab für Parameteranalyse hinzufügen
    frame_parameter_analysis = tk.Frame(notebook)
    notebook.add(frame_parameter_analysis, text="Parameteranalyse")

    # Verfügbare Altcoins (Beispiel)
    available_altcoins = ['ethereum', 'litecoin', 'ripple', 'bitcoin-cash', 'eos']

    # GUI-Komponenten für den Simulationstab und Parameteranalyse-Tab erstellen
    create_simulation_tab(frame_simulation, notebook)
    # display_gainers_and_losers(frame_gainers_losers, notebook)
    
    # Übergabe der Altcoins-Liste an die Funktion create_parameter_analysis_tab
    analysis_treeview = create_parameter_analysis_tab(frame_parameter_analysis, notebook, available_altcoins)

    # Hauptloop starten
    root.mainloop()