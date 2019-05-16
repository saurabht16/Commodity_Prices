'''
Program to fetch historical prices of Gold and Silver for below Urls:
'gold': "https://www.investing.com/commodities/gold-historical-data/"
'silver': "https://www.investing.com/commodities/silver-historical-data"
'''

from bs4 import BeautifulSoup
import requests
import os
import os.path
import csv
import time


def writerows(rows, filename):
	'''
	Method to write to csv file
	'''
    try:
        with open(filename, 'a', encoding='utf-8', newline='') as toWrite:
            writer = csv.writer(toWrite)
            writer.writerows(rows)
    except Exception as e:
        print("Unable to write to file")
        print(e)
        exit()

def getlistings(listingurl, type):
    '''
    scrape Gold and Silver data from the page and write to CSV
    '''

    # Setting the header
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}

    # fetching the url, raising error if operation fails
    try:
        response = requests.get(listingurl, headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
        exit()
    # Initialize soup object to store the response in text format
    soup = BeautifulSoup(response.text, "html.parser")
    listings = []
    table = soup.find_all('table')[1]
    rows = table.find_all("tr")
    header = [th.text.rstrip() for th in rows[0].find_all('th') if th.text.rstrip() in ['Date', 'Price'] ]
    header.insert(0, 'Type')
    # loop through the table, get data from the columns
    for row in rows[1:]:
        data = [th.text.rstrip() for th in row.find_all('td')[0:2]]
        # Insert the type as first column
        data.insert(0, type)
        # append data to the list
        listings.append(data)
    return listings


if __name__ == "__main__":
    '''
    Set CSV file name.  
    Remove if file already exists to ensure a fresh start
    '''
    filename = "historical_prices.csv"
    if os.path.exists(filename):
        os.remove(filename)

    #write the header
    writerows([['Type', 'Date', 'Price'],], filename)
    '''
    Url to fetch Gold and silver prices
    '''
    url = {'gold': "https://www.investing.com/commodities/gold-historical-data/",
            'silver': "https://www.investing.com/commodities/silver-historical-data/"}
    # scrap all urls
    for key in url:
       listings = getlistings(url[key], key)
       # write to CSV
       writerows(listings, filename)

    #take a break
    time.sleep(3)

    print("Listings fetched successfully.")