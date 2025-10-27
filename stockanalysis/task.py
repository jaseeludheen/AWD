from awd_main.celery import app
from .utils import scrape_stock_data



@app.task
def scrape_stock_data_task(symbol, exchange):
    scrape_stock_data(symbol, exchange) 
    return f'Stock data scraping task for {symbol} on {exchange} executed successfully.'