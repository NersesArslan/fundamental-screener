import yfinance as yf



def get_stock_info(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    price = ticker.info.get('currentPrice')

    earnings_per_share = ticker.info.get('earningsPerShare')
    trailing_pe = ticker.info.get('trailingPE')
    forward_pe = ticker.info.get('forwardPE')
    debt_to_equity = ticker.info.get('debtToEquity')
    pe_ratio = (price / earnings_per_share)
    return_on_equity = ticker.info.get('returnOnEquity')
    free_cashflow = ticker.info.get('freeCashflow')

    return {
        'price': price,
        'pe_ratio': pe_ratio,
        'debt_to_equity': debt_to_equity,
        'returnonequity': return_on_equity,
        'free_cashflow': free_cashflow,
    }


print(get_stock_info("AAPL"))