from data_fetch import get_price
import json

with open('data.json', 'r') as f:
    data = json.load(f)

urls = data['sites'][0]['links']
print(get_price(url="https://googansquad.com/collections/accessories/products/basshers-lunkers-wristband",
                identifier="ProductMeta__Price Price Text--subdued u-h4"))

