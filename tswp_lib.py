import requests
import json
from bs4 import BeautifulSoup
import datetime as dt
import time
from os import rename

#event_url = "imagine-dragons-evolve-world-tour/floor/c935b272-3019-48b9-877e-77f7f95b9a61/510954"
#url = "https://www.ticketswap.nl/event/"+event_url

def get_event_stats(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    available = -1
    sold = -1
    wanted = -1
    try:
        available = soup.find("div", {'class' : 'counter counter-available'}).find("div", {'class' : 'counter-value'}).text
        sold = soup.find("div", {'class' : 'counter counter-sold'}).find("div", {'class' : 'counter-value'}).text
        wanted = soup.find("div", {'class' : 'counter counter-wanted'}).find("div", {'class' : 'counter-value'}).text
    except:
        name = url[31:]
        name = name[:name.index("/")].split("-")
        print(name)
    return [int(available), int(sold), int(wanted)]

def get_event_title(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    
    return soup.find("h1", {'itemprop' : 'summary'}).find("a").text
    
def get_event_date(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    
    monthdict = {'januari' : '1', 'februari' : '2', 'maart' : '3', 'april' : '4', 'mei' : '5', 'juni' : '6', 'juli' : '7', 'augustus' : '8', 'september' : '9', 'oktober' : '10', 'november' : '11', 'december' : '12',}

    date = soup.find("span", {'class' : 'date'}).text[1:]
    
    try:
        date = date[:date.index("-")-1]
    except:
        pass
    
    date = date[date.index(" ")+1:]
    day = date[:date.index(" ")]
    month = monthdict[date[date.index(" ")+1:-5]]
    year = date[-4:]

    event_date = dt.datetime(int(year), int(month), int(day), 21)
    t = dt.datetime.today()
    today = dt.datetime(t.year, t.month, t.day, t.hour)

    event_timestamp = time.mktime(event_date.timetuple())
    return event_timestamp

def get_date_diff(event_timestamp):
    today_timestamp = int(time.time())

    diff_s = event_timestamp - today_timestamp
    diff_h = int(diff_s/3600.0)

    return diff_h
