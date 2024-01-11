from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import pandas

def access(url):
    session = HTMLSession()
    r = session.get(url)
    r.html.render(sleep=1)
    return r

def get_next_url_catalog(url):
    r = access(url)
    r.html.next(fetch=False)
    return r

def get_all_links(url):
    r = access(url)
    product_links = r.html.xpath('//*[@id="product-list-component"]/div[4]/div', first=True).absolute_links
    return product_links

def parse_catalog_product(url):
    next_url = get_next_url_catalog(url)
    product_links = get_all_links(url)
    catalog = []
    n_product = len(product_links)
    print(f"Found {n_product} links")
    x = 1
    for product in product_links:
        product_parse = parse_product(product)
        catalog.append(product_parse)
        print(f"Scraping {x} of {n_product} ...")
        x += 1
    if next_url:
        print("Next page found! Processing..")
    return next_url,catalog

def parse_product(product_url):
    r = access(product_url)
    soup = BeautifulSoup(r.html.html,"html.parser")
    name = find_data("div","d-flex flex-row",soup)
    summary = find_data("span", "itemFacts font-weight-normal",soup)
    price = find_data("p","itemNormalPrice display-6",soup)
    price = get_int(price)
    stocks = find_data("div", "quantityInStock",soup)
    stocks = get_int(stocks)

    result = {"product name":name,
              "summary":summary,
              "price":price,
              "stocks":stocks,
              "url":product_url}
    return result

def find_data(tag, class_,soup):
    try:
        data = soup.find(tag,class_).get_text().strip()
    except AttributeError:
        data = None
    return data

def get_int(input):
    number = re.findall(r'[\d]+',str(input))
    result = ""
    for n in number:
        result += n
    return result

def result_to_excel(data):
    df = pandas.DataFrame(data)
    df.to_excel("ikea.xlsx",index = False)


if __name__=="__main__":
    main_url = "https://www.ikea.co.id/in/produk/dekorasi-kamar-tidur/tanaman-hias"
    result = []
    next_url,catalog = parse_catalog_product(main_url)
    result.append(catalog)
    while next_url:
        next_url,catalog = parse_catalog_product(next_url)    
    result_to_excel(result)

