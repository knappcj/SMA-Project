import pandas as pd
import yfinance as yf


def buySell(ticker, begin_day, end_day, best_day):
    data = yf.download(ticker, begin_day, end_day)
    # The Series of price and volume that is N-day ago (need time shifting?)
    price_data = data['Adj Close']
    volume_data = data['Volume']
    bought_price = price_data.iloc[0]
    shares_bought = 50000 / bought_price
    prior_price = price_data.shift(best_day)
    prior_volume = volume_data.shift(best_day)
    # Combine both price and SMA data and store them in a pandas' dataframe named 'price_sma_data'
    prices_volumes = pd.concat([price_data, volume_data, prior_price, prior_volume], axis=1)
    prices_volumes.columns = ['Price', 'Volume', 'Prior Price', 'Prior Volume']

    # Generate buy or sell signals
    # BUY for a 'rising' price and a 'falling' volume, both between t and t-N
    # SELL for a 'falling' price and a 'rising' volume, both between t and t-N
    buy_or_sell = 0
    buy_count = 0
    sell_count = 0

    for t in prices_volumes.index:
        today_price = prices_volumes.loc[t, 'Price']
        prior_price = prices_volumes.loc[t, 'Prior Price']
        today_volume = prices_volumes.loc[t, 'Volume']
        prior_volume = prices_volumes.loc[t, 'Prior Volume']

        # BUY is -1 due to cash outflow and SELL is +1 due to cash inflow
        if today_price > prior_price and today_volume < prior_volume and buy_count==sell_count:
                buy_or_sell = -1
                buy_count += 1
        elif today_price < prior_price and today_volume > prior_volume and buy_count-1 == sell_count:
                buy_or_sell = 1
                sell_count += 1
        else:
            buy_or_sell = 0


        # When it is the final day in the entire sample period
        if t == prices_volumes.index[-1]:
            # We need to add trades to have equal numbers of buy and sell
            additional_trade = buy_count - sell_count
            buy_or_sell += additional_trade
        prices_volumes.loc[t, 'Buy or Sell'] = buy_or_sell
        # Calcualte the cash flow for each trade
        cash_flow = today_price * buy_or_sell
        prices_volumes.loc[t, 'Cash Flow'] = cash_flow
    # Calculate total P&Ls
    trading_profit = prices_volumes['Cash Flow'].sum(axis=0)
    profit = trading_profit*shares_bought
    return prices_volumes, profit


