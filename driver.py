import requests
from data_fetch import get_urls

urls = ['https://googansquad.com', 'https://www.uswatersystems.com',
        'https://www.ricoinc.com', 'https://www.monodsports.com',
        'https://www.sonsoflibertytees.com', 'https://www.shirtpunch.com',
        'https://www.snapklik.com', 'healthwick.ca', 'https://utahskigear.com/',
        'quickcandles.com', 'https://www.needforseatusa.com']

links = get_urls(urls[4])
for link in links:
    print(link)
print(len(links))
