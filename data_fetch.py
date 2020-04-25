import requests
import re
from bs4 import BeautifulSoup

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



