import requests
from bs4 import BeautifulSoup

# Follow all a-tag links from given base, forming a web
# Returns list of sub-urls for base-url
def get_urls(base):
    source = requests.get(base)
    visited = {'/': True}
    master_list = []
    parse_stack = ['/']

    while len(parse_stack) > 0:
        url_end = parse_stack.pop()
        new_url = base + url_end
        soup = BeautifulSoup(source.text, 'html.parser')
        links = soup.find_all('a', href=True)

        for link in links:
            href = link['href']

            if not href or href[0] != '/' or href in visited:
                continue

            visited[href] = True
            parse_stack.append(href)
        master_list.append(url_end)

    master_list.sort()
    return master_list

