import requests
import json
from data_fetch import get_urls, get_price, get_name, average_price, alexa_info
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

def get_conversion_rate(average_price):
    if average_price <= 100:
        return 0.02
    elif average_price <= 600:
        return 0.01
    elif average_price <= 1000:
        return 0.005
    else:
        return 0.001

def main():
    # base = 'https://googansquad.com'
    # keyword = "ProductMeta__Price Price Text--subdued u-h4"
    base = "https://www.sonsoflibertytees.com"
    keyword = "price"
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
            json.dump(new_json, f, indent=2)

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
    if not os.path.isfile("./" + file_name + "/metrics.csv"):
        info = alexa_info(base)
        avg_price = round(average_price(file_name), 2)
        conversion_rate = get_conversion_rate(avg_price)
        headers = ['Name', 'Url', 'Country', 'Date Created', 'Keywords',
                   'Time Range (Months)', 'Alexa Rank', 'Alexa Rank Change', "Monthly Traffic", "Monthly Traffic Change",
                   "Average Item Price ($)", "Conversion Rate", "Sales Estimate"]
        metrics = {
            "Name": get_name(base),
            "Url": base,
            "Country": info['country'],
            "Date Created": info['date_created'],
            "Keywords": info['keywords'],
            "Time Range (Months)": info['time_range'],
            "Alexa Rank": info['alexa_rank'],
            "Alexa Rank Change": info['alexa_rank_delta'],
            "Monthly Traffic": info['reach_permil'] * 750000,
            "Monthly Traffic Change": info['reach_permil_delta'],
            "Average Item Price ($)": avg_price,
            "Conversion Rate": conversion_rate,
            "Sales Estimate": float(info['reach_permil']) * 750000 * conversion_rate
        }

        with open("./" + file_name + "/metrics.csv", mode="w+") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            writer.writerow(metrics)

    print("All reports generated in directory: " + file_name)

if __name__ == "__main__":
    main()
