# Commodity_Prices
Scrape prices of Gold and Silver and Retrieve it via API built in Flask

1. Run fetch_prices.py first to fetch all teh historical prices of Gold andd silver from:
  'gold': "https://www.investing.com/commodities/gold-historical-data/"
  'silver': "https://www.investing.com/commodities/silver-historical-data"
   This saves the data in a file named as historical_prices.csv

2. Once the retrieval is done, run the commodity_price.py file. This will sart teh API on port 8080. Once this is started, fetch teh data    using below command:
   curl 'http://127.0.0.1:8080/commodity?start_date=2019-05-10&end_date=2019-05-15&commodity_type=gold'
