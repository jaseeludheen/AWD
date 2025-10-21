from bs4 import BeautifulSoup
import requests

def scrape_stock_data(symbol, exchange):
    if exchange.upper() == "NASDAQ":
        url = f"https://finance.yahoo.com/quote/{symbol}"
    elif exchange.upper() == "NSE":
        url = f"https://finance.yahoo.com/quote/{symbol}.NS"
    else:
        print(f"{exchange} is Unsupported exchange. Use 'NASDAQ' or 'NSE'.")
        return

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            current_price = soup.find("span", {"data-testid": "qsp-price"})
            price_change = soup.find("span", {"data-testid": "qsp-price-change"})
            percentage_change = soup.find("span", {"data-testid": "qsp-price-change-percent"})
            previous_close = soup.find("fin-streamer", {"data-field": "regularMarketPreviousClose"})
            week_52_range = soup.find("fin-streamer", {"data-field":"fiftyTwoWeekRange"})
            market_cap = soup.find("fin-streamer", {"data-field": "marketCap"})
            pe_ratio = soup.find("fin-streamer", {"data-field": "trailingPE"})
            dividend_yield = soup.find("span", {"title": "Forward Dividend & Yield"})
    
    


    
            current_price = current_price.get_text(strip=True) if current_price else "N/A"
            price_change = price_change.get_text(strip=True) if price_change else "N/A"
            percentage_change = percentage_change.get_text(strip=True) if percentage_change else "N/A"
            previous_close = previous_close.get_text(strip=True) if previous_close else "N/A"
            week_52_range = week_52_range.get_text(strip=True) if week_52_range else "N/A"
            week_52_low, week_52_high = week_52_range.split(" - ") if " - " in week_52_range else ("N/A", "N/A")
            market_cap = market_cap.get_text(strip=True) if market_cap else "N/A"
            pe_ratio = pe_ratio.get_text(strip=True) if pe_ratio else "N/A"
            dividend_yield = dividend_yield.find_next("span", class_="value").get_text(strip=True) if dividend_yield and dividend_yield.find_next("span", class_="value") else "N/A"

            stock_response =  {
                'current_price': current_price,
                'price_change': price_change,
                'percentage_change': percentage_change,
                'previous_close': previous_close,
                'week_52_low': week_52_low,
                'week_52_high': week_52_high,
                'market_cap': market_cap,
                'pe_ratio': pe_ratio,
                'dividend_yield': dividend_yield,
            }
            
            return stock_response

        
    except Exception as e:
        print(f"An error occurred while scraping data for {symbol} on {exchange}: {e}")
        return None


