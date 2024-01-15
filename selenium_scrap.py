from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re, time
import pandas as pd
from io import StringIO


def get_html(url):
    options = Options()
    options.add_argument("--enable-javascript")
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    html = driver.page_source
    driver.quit()
    return html

def get_urls(url):
    list_of_urls = []

    options = Options()
    options.add_argument("--enable-javascript")
    options.add_argument("--headless=new")
    options.add_argument("--blink-settings=imagesEnabled=false")

    driver = webdriver.Chrome(options)

    page_counter = 1
    while True:
        new_url = f"{url}{page_counter}"
        driver.get(new_url)
        driver.implicitly_wait(3)
        elements = driver.find_elements(By.CSS_SELECTOR,'div[class="d-flex flex-row"]')
        print(f"Getting {len(elements)} of links in pages {page_counter}")

        if len(elements) > 0:
            for element in elements:
                urls = element.find_element(By.TAG_NAME,"a").get_attribute('href')
                list_of_urls.append(urls)
        else:
            break
        page_counter += 1
    print(f"Getting {len(list_of_urls)} of links in total")
    return list_of_urls

def find_soup(tag, class_name):
    try:
        value = soup.find(tag,class_=class_name).text.strip()
    except AttributeError as e:
        print(e)
        value = "0"
    return value

def get_number(text):
    try:
        remove_dot_text = text.replace(".","")
        numb = re.findall(r'\d+',remove_dot_text)
        return numb[0]
    except IndexError:
        print(f"Index Error, output: ",text)
        return text

def scrap_product(url):
    item_name = find_soup("div","d-flex flex-row")
    item_details = find_soup("span","itemFacts font-weight-normal")
    price = find_soup("p","itemNormalPrice display-6")
    price = get_number(price)
    sold = find_soup("p","partNumber")
    sold = get_number(sold)
    stock = find_soup("div","quantityInStock")
    stock = get_number(stock)
    try:
        image = soup.find("div",class_="image-container slick-slide slick-current slick-active")
        imageslices = image.span.img['src']
    except Exception as e:
        print(e)
        print("image cant be found. Get:",image)
        imageslices = ""

    result = {
        "Item Name" : item_name,
        "Details" : item_details,
        "Price":price,
        "Sold":sold,
        "In Stock":stock,
        "Image URL":imageslices,
        "URL":url
        }
    return result

def save_to_excel(list_of_data):
    df = pd.DataFrame(list_of_data)
    df.to_excel("ikea.xlsx",index=False)
    print("saved to ikea.xlsx")      


def scrap_table_rexsy(soup : BeautifulSoup, output : dict = {}):
    html = soup.find("div", id="modal-measurements")
    tables = html.find_all("table")
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            td = row.find_all("td")
            key = td[0].get_text().replace(": ","").replace("\n","").replace(":","")
            value = td[1].get_text()
            output[key] = value
    return output

if __name__=="__main__":
    result = []
    main_url = "https://www.ikea.co.id/in/produk/dekorasi-kamar-tidur/tanaman-hias?sort=SALES&page="
    product_url = get_urls(main_url)
    #product_url = ["https://www.ikea.co.id/in/produk/dekorasi/tanaman-hias/chrysalidocarpus-lutescens-27-art-00001103","https://www.ikea.co.id/in/produk/dekorasi/tanaman-hias/pachira-aquatica-braided-17-art-00001091","https://www.ikea.co.id/in/produk/dekorasi/tanaman-hias/cereus-peruvianus-30-art-00001095"]
    counter = 0
    try:
        for url in product_url:
            print("#",counter+1)
            print("getting through ",url)
            html = get_html(url)
            soup = BeautifulSoup(html,"html.parser")
            product_data = scrap_product(url)
            table = scrap_table_rexsy(soup)
            product_list = {**product_data, **table}
            result.append(product_list)
            counter += 1
        save_to_excel(result)
    except Exception as e:
        save_to_excel(result)
