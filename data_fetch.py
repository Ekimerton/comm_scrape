import requests
import re
from bs4 import BeautifulSoup
import os
import xml.etree.ElementTree as ET

# Follow all a-tag links from given base, forming a web
# Returns list of sub-urls for base-url
def get_urls(base):
    visited = {'/': True}
    master_list = []
    parse_stack = ['/']

    while len(parse_stack) > 0:
        if len (parse_stack) > 1000:
            return ["Too many links, disable block to parse"]
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
            print('error')
            print(e)

    master_list.sort()
    return master_list

def get_price(identifier, url):
    item_prices = []

    source = requests.get(url)
    soup = BeautifulSoup(source.text, 'html.parser')
    prices = soup.find_all(re.compile(r'.'), class_=identifier)
    for price in prices:
        item_prices.append(price.text)

    if not item_prices:
        return None

    return item_prices

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
        "ResponseGroup": "Rank,SiteData,UsageStats",
        "Url": url
    }

    r = requests.get(url=base_url, params=params, headers=headers)

    root = ET.fromstring(r.text)

    info['name'] = root.find("./Results/Result/Alexa/ContentData/SiteData/Title").text
    # info['date_created']
    # info['description']
    info['url'] = root.find("./Results/Result/Alexa/ContentData/DataUrl").text

    info['time_range'] = root.find("./Results/Result/Alexa/TrafficData/UsageStatistics/UsageStatistic/TimeRange/Months").text

    # Alexa rank
    info['alexa_rank'] = root.find("./Results/Result/Alexa/TrafficData/UsageStatistics/UsageStatistic/Rank/Value").text
    info['alexa_rank_delta'] = root.find("./Results/Result/Alexa/TrafficData/UsageStatistics/UsageStatistic/Rank/Delta").text

    # Reach
    # info['reach_rank'] = root.find("./Results/Result/Alexa/TrafficData/UsageStatistics/UsageStatistic/Reach/Rank/Value").text
    # info['reach_rank_delta'] = root.find("./Results/Result/Alexa/TrafficData/UsageStatistics/UsageStatistic/Reach/Rank/Delta").text
    info['reach_permil'] = root.find("./Results/Result/Alexa/TrafficData/UsageStatistics/UsageStatistic/Reach/PerMillion/Value").text
    info['reach_permil_delta'] = root.find("./Results/Result/Alexa/TrafficData/UsageStatistics/UsageStatistic/Reach/PerMillion/Delta").text

    print(info)
