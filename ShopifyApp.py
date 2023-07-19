import shopify
from googlesheet.core import GetShopifyCSVData
import sys

value1 = sys.argv[1]
value2 = sys.argv[2]
value3 = sys.argv[3]
value4 = sys.argv[4]
value5 = sys.argv[5]

print(f"Spreadsheet_id : {value1}")
print(f"shopify_access_token: {value2}")
print(f"shopify_api_key: {value3}")
print(f"shopify_secret: {value4}")
print(f"shop_url: {value5}")

#Variables
Spreadsheet_id = str(value1)
shopify_access_token = str(value2)
shopify_api_key = str(value3)
shopify_secret = str(value4)
shop_url = str(value5)

CSV = GetShopifyCSVData(Spreadsheet_id)

def GetShopifyProducts():
    api_version = '2023-01'

    shopify.Session.setup(api_key=shopify_api_key, secret=shopify_secret)
    session = shopify.Session(shop_url, api_version, shopify_access_token)
    shopify.ShopifyResource.activate_session(session)
    shop = shopify.Shop.current()

    products = []
    page = shopify.Product.find()
    for product in page:
        product_details = {
            'ID': product.id,
            'Name': product.title,
            'product': product
        }
        products.append(product_details)

    while page.has_next_page():
        page = page.next_page()
        for product in page:
            product_details = {
                'ID': product.id,
                'Name': product.title,
                'product': product
            }
            products.append(product_details)

    return products


def GetProduct(sku, products):
    for product in products:
        title = product['Name']
        pos = title.find('#')
        rug = title[pos+1:1000]
        if str(sku) == rug:
            return product['product']

tags = {
    'Handle': 'handle',
    'Title': 'title',
    'Body (HTML)': 'body_html',
    'Vendor': 'vendor',
    'Tags': 'tags',
    'Variant Price': 'price',
    'SEO Title': 'metafields_global_title_tag',
    'SEO Description': 'metafields_global_description_tag'
}
products = GetShopifyProducts()
for row in CSV:
    handle = row['Handle']
    sku = row['Variant SKU']
    product = GetProduct(sku, products)
    if product != None:
        print(product.title)
        for header in CSV[0]:
            try:
                tag = tags[header]
                product.attributes[tag] = row[header]
            except:
                pass
        product.save()