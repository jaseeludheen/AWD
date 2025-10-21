from django.shortcuts import render, redirect, get_object_or_404
from dal import autocomplete
from .models import Stock, StockData
from .forms import StockForm
from .utils import scrape_stock_data
from django.contrib import messages


def stocks(request):

    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            stock_id = request.POST.get('stock')
#           print("Selected Stock:", stock_id)

            # Fetch the stock object
            stock = Stock.objects.get(id=stock_id)
            symbol = stock.symbol
            print("Selected Stock Symbol ==> ", symbol)
            exchange = stock.exchange
            print("Selected Stock Exchange ==> ", exchange)

            # Call the scraping function
            stock_response = scrape_stock_data(symbol, exchange) 
#           print(stock_response)


            if stock_response:
                try:
                    stock_data = StockData.objects.get(stock=stock)
                except StockData.DoesNotExist:
                    stock_data = StockData(stock=stock)

                # update the StockData instance with the response data
                stock_data.current_price = stock_response['current_price']
                stock_data.price_change = stock_response['price_change']
                stock_data.percentage_change = stock_response['percentage_change']
                stock_data.previous_close = stock_response['previous_close']
                stock_data.week_52_low = stock_response['week_52_low']
                stock_data.week_52_high = stock_response['week_52_high']
                stock_data.market_cap = stock_response['market_cap']
                stock_data.pe_ratio = stock_response['pe_ratio']
                stock_data.dividend_yield = stock_response['dividend_yield']

                stock_data.save()
                print(f"Stock data for {symbol} updated successfully.")
                return redirect('stock_detail', stock_data.id) 
            

            else:
                messages.error(request, f'Could not fetch the data for {symbol}')
                return redirect('stocks')


        else:
            print("Form is not valid")
    
    else: 
        form = StockForm()

        context = {
            'form': form
        }
        return render(request, 'stockanalysis/stocks.html', context)



# Autocomplete view for Stock model
class StockAutoComplete(autocomplete.Select2QuerySetView): 
    def get_queryset(self):
        
        qs = Stock.objects.all()

        if self.q:

            print('Entered Keyword=>', self.q)
            qs = qs.filter(name__istartswith=self.q)
            print('Result =>', qs)

        return qs
    



def stock_detail(request, pk):
    stock_data = get_object_or_404(StockData, pk=pk)
    context = {
        'stock_data': stock_data,
    }
    return render(request, 'stockanalysis/stock_detail.html', context)