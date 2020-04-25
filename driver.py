import requests
import json
from data_fetch import get_urls, get_price
import csv
# from alexa import get_metrics


urls = ['https://googansquad.com', 'https://www.uswatersystems.com',
        # 'https://www.ricoinc.com', 
        'https://www.monodsports.com',
        'https://www.sonsoflibertytees.com', 'https://www.shirtpunch.com',
        'https://www.snapklik.com', 'healthwick.ca', 'https://utahskigear.com/',
        'quickcandles.com', 'https://www.needforseatusa.com']

# Initialize json file
'''
try:
    with open('data.json', 'r') as f:
        pass
except:
    print("Couldn't find data.json!")
    with open('data.json', 'w+') as f:
        new_json = {'sites': []}
        json.dump(new_json, f)
    print("Created data.json.")

start = int(input("Enter starting point: "))
for url in urls[start:]:
    print("Starting web on ", url)
    with open('data.json', 'r') as f:
        data = json.load(f)
        sites = data['sites']

    links = get_urls(url)
    sites.append({"base": url, "links": links})

    data = {"sites": sites}
    with open('data.json', 'w+') as outfile:
        json.dump(data, outfile, indent=2)
'''

def product_list(base, param):
    product_names = {}

    with open('data.json') as f:
        data = json.load(f)

    urls = data['sites'][0]['links']
    products = []
    print(len(urls))
    for idx, url in enumerate(urls):
        print(idx)
        name = url[url.rindex("/") + 1:].replace("-", " ").title()

        # If product already listed or has no name
        if not name or name in product_names:
            continue

        full_url = base + url
        price = get_price(identifier=param, url=full_url)
        if name and price:
            product_names[name] = True
            products.append((name, full_url, price))

    fieldnames = ['Name', 'Url', 'Price']
    with open('googansquad.csv', mode='w+') as csv_file: # TODO dynamic name
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for product in products:
            pname, purl, pprice = product
            writer.writerow({'Name': pname, 'Url': purl, 'Price': pprice})



def main():
    base = 'https://googansquad.com'
    keyword = "ProductMeta__Price Price Text--subdued u-h4"

    product_list(base, keyword)

if __name__ == "__main__":
    main()
