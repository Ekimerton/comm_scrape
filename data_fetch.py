import requests
import csv
import re
from bs4 import BeautifulSoup
import os
import xml.etree.ElementTree as ET
from decimal import *

# Follow all a-tag links from given base, forming a web
# Returns list of sub-urls for base-url
def get_urls(base):
    visited = {'/': True}
    master_list = []
    parse_stack = ['/']

    while len(parse_stack) > 0:
        print("Left to parse:", len(parse_stack))
        try:
            url_end = parse_stack.pop()
            new_url = base + url_end
            source = requests.get(new_url)
            soup = BeautifulSoup(source.text, 'html.parser')

            # Extract href from links (<a> tags)
            links = soup.find_all('a', href=True)

            # Extract href from buttons (<button> tags)
            button_links = soup.find_all('button')
            for button_link in button_links:
                try:
                    button_link = button_link['onclick']
                    print(button_link)
                    start = button_link.index("(") + 2
                    end = button_link.index(")") - 1
                    print(button_link[start:end])
                    button_href = button_link[start:end]
                    links.append(button_href)
                except:
                    pass

            # Add any new links to the parse stack
            for link in links:
                href = link['href']

                try:
                    start = href.index(base)
                    href = href[start + len(base):]
                except:
                    pass

                if not href or href[0] != '/' or href in visited or '&' in href:
                    continue

                visited[href] = True
                parse_stack.append(href)
            master_list.append(url_end)
        except Exception as e:
            pass

    master_list.sort()
    return master_list

def average_price(file_name):
    with open("./" + file_name + '/products.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        total = Decimal(0)
        skip = True # Skip Headers
        item_count = 0
        for row in reader:
            if skip:
                skip = False
                continue

            total += Decimal(row[2])
            item_count += 1

        return total / item_count

def get_price(identifier, url):
    try:
        sub = re.sub
        source = requests.get(url)
        soup = BeautifulSoup(source.text, 'html.parser')
        prices = soup.find_all(re.compile(r'.'), class_=identifier)

        if len(prices) > 1:
            return None

        cost_sum = Decimal(0)
        for price in prices:
            try:
                price_val = Decimal(sub(r'[^\d.]', '', price.text))
                cost_sum += price_val
            except:
                pass

        if prices:
            return float(cost_sum / len(prices))
        else:
            return None
    except Exception as e:
        print(e)

def get_name(url):
    r = requests.get(url=url)
    soup = BeautifulSoup(r.text, 'html.parser')
    web_title = soup.title.string
    meta_title = soup.find("meta", property="og:title")
    if meta_title:
        return meta_title['content']
    else:
        return web_title


def alexa_info(url):
    info = {}
    try:
        api_key = os.environ['API_KEY']
    except:
        print("Please set your aws alexa api key")

    base_url = "https://awis.api.alexa.com/api"
    headers = {"x-api-key": api_key}
    params = {
        "Action": "UrlInfo",
        "ResponseGroup": "Rank,SiteData,UsageStats,Categories,RankByCountry",
        "Url": url
    }

    r = requests.get(url=base_url, params=params, headers=headers)

    root = ET.fromstring(r.text)
    print(r.text)

    # Basic Info
    try:
        info['date_created'] = root.find("").text
    except:
        info['date_created'] = None

    try:
        info['country'] = root.find("./Results/Result/Alexa/TrafficData/RankByCountry/Country").attrib['Code']
    except:
        info['country'] = None

    try:
        info['keywords'] = root.find("./Results/Result/Alexa/TrafficData/").text
    except:
        info['keywords'] = None

    # Time Range for Metrics
    try:
        info['time_range'] = root.find("./Results/Result/Alexa/TrafficData/UsageStatistics/UsageStatistic/TimeRange/Months").text
    except:
        info['time_range'] = None

    # Alexa Rank
    try:
        info['alexa_rank'] = int(root.find("./Results/Result/Alexa/TrafficData/UsageStatistics/UsageStatistic/Rank/Value").text)
    except:
        info['alexa_rank'] = None

    try:
        info['alexa_rank_delta'] = root.find("./Results/Result/Alexa/TrafficData/UsageStatistics/UsageStatistic/Rank/Delta").text
    except:
        info['alexa_rank_delta'] = None

    # Reach
    try:
        info['reach_permil'] = float(root.find("./Results/Result/Alexa/TrafficData/UsageStatistics/UsageStatistic/Reach/PerMillion/Value").text)
    except:
        info['react_permil'] = None

    try:
        info['reach_permil_delta'] = root.find("./Results/Result/Alexa/TrafficData/UsageStatistics/UsageStatistic/Reach/PerMillion/Delta").text or None
    except:
        info['reach_permil_delta'] = None

    return info
