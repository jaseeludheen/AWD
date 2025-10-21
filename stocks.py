from bs4 import BeautifulSoup
import requests

def scrape_stock_data(symbol, exchange):
    # Build the correct Yahoo Finance URL
    if exchange.upper() == "NASDAQ":
        url = f"https://finance.yahoo.com/quote/{symbol}"
    elif exchange.upper() == "NSE":
        url = f"https://finance.yahoo.com/quote/{symbol}.NS"
    else:
        print(f"{exchange} is Unsupported exchange. Use 'NASDAQ' or 'NS'.")
        return

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the CURRENT PRICE 
    price_tag = soup.find("span", {"data-testid": "qsp-price"})
    
    if price_tag:
        current_price = price_tag.get_text(strip=True)
        print(f"{symbol} stock")
        print(f"Current price of {symbol}: {current_price}")
    else:
        print(f"⚠️ Could not find current price for {symbol}")

    # Find the PREVIOUS CLOSE price 
    previous_close = soup.find("fin-streamer", {"data-field": "regularMarketPreviousClose"})
    if previous_close:
        prev_close_price = previous_close.get_text(strip=True)
        print(f"Previous close price of {symbol}: {prev_close_price}")
    else:
        print(f"⚠️ Could not find previous close price for {symbol}")

# Test for NASDAQ and NSE stocks
print("-----------------------------------")

scrape_stock_data("GILD", "NASDAQ")
print("-----------------------------------")
scrape_stock_data("TCS", "NSE")
print("-----------------------------------")
scrape_stock_data("ABTS", "NASDAQ")
print("-----------------------------------")
scrape_stock_data("ACGL", "NASDAQ")
print("-----------------------------------")