import requests
import json
from data_fetch import get_urls, get_price, get_name
import csv
import os

urls = ['https://googansquad.com', 'https://www.uswatersystems.com',
        # 'https://www.ricoinc.com', 
        'https://www.monodsports.com',
        'https://www.sonsoflibertytees.com', 'https://www.shirtpunch.com',
        'https://www.snapklik.com', 'healthwick.ca', 'https://utahskigear.com/',
        'quickcandles.com', 'https://www.needforseatusa.com']

def product_list(base, param, file_name):
    product_names = {}

    with open("./" + file_name + '/urls.json') as f:
        data = json.load(f)

    urls = data['links']
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

    return products

def average_price(file_name):
    with open("./" + file_name + '/products.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        total = 0.0
        skip = True # Skip Headers
        for row in reader:
            if skip:
                skip = False
                continue

            total += float(row[2])

        print(total)

def main():
    base = 'https://googansquad.com'
    keyword = "ProductMeta__Price Price Text--subdued u-h4"
    file_name = get_name(base).replace(" ", "-").lower()

    # Step 0: Generate file struct
    if not os.path.isdir('./' + file_name):
        print("Created directory: " + file_name)
        os.mkdir(file_name)

    # Step 1: Create url web 
    if not os.path.isfile('./' + file_name + "/urls.json"):
        with open("./" + file_name + '/urls.json', 'w+') as f:
            print("Starting forming a url web. (Takes a long time)")
            links = get_urls(base)
            new_json = {'links': links}
            json.dump(new_json, f)

    # Step 2: Generate product prices spreadsheet
    if not os.path.isfile('./' + file_name + "/products.csv"):
        products = product_list(base, keyword, file_name)
        fieldnames = ['Name', 'Url', 'Price ($)']
        with open('./' + file_name + '/products.csv', mode='w+') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for product in products:
                pname, purl, pprice = product
                writer.writerow({'Name': pname, 'Url': purl, 'Price ($)': pprice})

    # Step 3: Generate final spreadsheet
    average_price(file_name)


if __name__ == "__main__":
    main()
