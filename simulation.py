def simulate_trading(df, buy_percentage=0.1, sell_percentage=0.1, initial_btc=0.0):
    btc_balance = initial_btc
    altcoin_balance = 0
    position = None  # None oder 'long' (Altcoin-Position)
    trade_log = []
    buy_price_btc = None
    last_peak = None
    last_trough = None

    for index, row in df.iterrows():
        btc_price = row['bitcoin_price']
        altcoin_price = row['altcoin_price']
        timestamp = row['timestamp']

        # Berechnung des Altcoin/BTC-Verhältnisses
        altcoin_btc_ratio = altcoin_price / btc_price

        if position is None:
            # Aktualisieren des letzten Hochs
            if last_peak is None or altcoin_btc_ratio > last_peak:
                last_peak = altcoin_btc_ratio
            # Kaufentscheidung
            elif (last_peak - altcoin_btc_ratio) / last_peak >= buy_percentage:
                # Kauf von Altcoin mit BTC
                altcoin_balance = btc_balance / altcoin_btc_ratio
                btc_balance = 0
                position = 'long'
                buy_price_btc = altcoin_btc_ratio
                trade_log.append({
                    'timestamp': timestamp,
                    'action': 'BUY_ALTCOIN',
                    'price_usd': altcoin_price,
                    'price_btc': altcoin_btc_ratio,
                    'profit': 0
                })
                # Setzen des letzten Tiefs nach dem Kauf
                last_trough = altcoin_btc_ratio
        else:
            # Aktualisieren des letzten Tiefs
            if altcoin_btc_ratio < last_trough:
                last_trough = altcoin_btc_ratio
            # Verkaufsentscheidung
            elif (altcoin_btc_ratio - buy_price_btc) / buy_price_btc >= sell_percentage:
                potential_btc_balance = altcoin_balance * altcoin_btc_ratio
                profit = potential_btc_balance - initial_btc
                if potential_btc_balance > initial_btc:
                    # Verkauf von Altcoin zurück in BTC
                    btc_balance = potential_btc_balance
                    altcoin_balance = 0
                    position = None
                    trade_log.append({
                        'timestamp': timestamp,
                        'action': 'SELL_ALTCOIN',
                        'price_usd': altcoin_price,
                        'price_btc': altcoin_btc_ratio,
                        'profit': profit
                    })
                    # Setzen des letzten Hochs nach dem Verkauf
                    last_peak = altcoin_btc_ratio
                else:
                    # Nicht verkaufen, da Verlust entstehen würde
                    continue

    # Am Ende der Simulation
    if position == 'long':
        # Wir behalten die Altcoins, da ein Verkauf zu Verlust führen würde
        potential_btc_balance = altcoin_balance * altcoin_btc_ratio
        unrealized_profit = potential_btc_balance - initial_btc
        trade_log.append({
            'timestamp': df.iloc[-1]['timestamp'],
            'action': 'HOLD_ALTCOIN',
            'price_usd': df.iloc[-1]['altcoin_price'],
            'price_btc': altcoin_btc_ratio,
            'profit': unrealized_profit,
            'holding': True,
            'altcoin_balance': altcoin_balance  # Hinzugefügt
        })
    else:
        unrealized_profit = btc_balance - initial_btc


    final_btc = btc_balance + (altcoin_balance * altcoin_btc_ratio if position == 'long' else 0)

    return final_btc, trade_log
