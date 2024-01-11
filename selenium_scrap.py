from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import pandas as pd
from io import StringIO


def get_html(url):
    options = Options()
    options.add_argument("--enable-javascript")
    #options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    
    driver.get(url)
    html = driver.page_source

    driver.quit()
    """
    with open("ikea.html","w",encoding="utf-8") as file:
        file.writelines(html)
        file.close()
    #it already save to a temp file, should it be returned?
    """
    #is it efficient to convert html to bs4 here?
    #soup = BeautifulSoup(html,"html.parser")
    print("getting html")
    return html

"""def open_html_file(filename):
    with open(filename,'r',encoding="utf-8") as file:
        html = file.read()
        file.close()
    return html"""

def get_urls(main_url):
    urls = []
    html = get_html(main_url)
    soup = BeautifulSoup(html,"html.parser")
    product_url = soup.find_all("div",class_="d-flex flex-row")
    #is there any faster way to get all links?
    for url in product_url:
        urls.append(url.a['href'])
    print("getting urls")
    return urls

def find(tag, class_name):
    try:
        value = soup.find(tag,class_=class_name).text.strip()
    except AttributeError:
        value = "NaN"
    return value

def get_number(text):
    try:
        text = text.replace(".","")
        numb = re.findall(r'\d+',text)
        return numb[0]
    except IndexError:
        print(f"Index Error, output: ",numb)
        return numb

def scrap_product():
    item_name = find("div","d-flex flex-row")
    item_details = find("span","itemFacts font-weight-normal")
    price = find("p","itemNormalPrice display-6")
    price = get_number(price)
    sold = find("p","partNumber")
    sold = get_number(sold)
    stock = find("div","quantityInStock")
    stock = get_number(stock)
    try:
        image = soup.find("div",class_="image-container slick-slide slick-current slick-active")
        imageslices = image.span.img['src']
    except TypeError:
        print("image cant be found. Get:",image)
        imageslices = None

    result = {
        "Item Name" : item_name,
        "Details" : item_details,
        "Price":price,
        "Sold":sold,
        "In Stock":stock,
        "Image URL":imageslices
    }

    table = scrap_table(html)
    result.update(table)

    print("getting product info")
    return result

def scrap_table(html):
    html = StringIO(html)
    df = pd.read_html(html)
    df1 = df[0].values.tolist()
    df2 = df[1].values.tolist()
    
    df1.extend(df2)

    table = dict()
    for i in df1:
        key = i[0].replace(":","") #some text be like "Tinggi :" gonna be "Tinggi " is it ok?
        value = i[1]
        table[key] = value
    print("getting table")
    return table

def save_to_excel(list_of_data):
    df = pd.DataFrame(list_of_data)
    df.to_excel("ikea.xlsx",index=False)
    print("saved to ikea.xlsx")

"""if __name__=="__main__":
    result = []
   
    main_url = "https://www.ikea.co.id/in/produk/dekorasi-kamar-tidur/tanaman-hias"
    product_url = get_urls(main_url)
    #product_url = ["/in/produk/dekorasi/tanaman-hias/succulent-8-art-00001084"]
    counter = 0
    for url in product_url:
        url = "https://www.ikea.co.id"+url
        print("#",counter+1)
        print("getting through ",url)
        html = get_html(url)
        soup = BeautifulSoup(html,"html.parser")
        product_data = scrap_product()
        result.append(product_data)
    
    #print(result)

    save_to_excel(result)
"""
    """
    last running 15 minutes for 40 data
    mode headless = false
    image tag not resolved yet
    

    second running 26 minutes for 40 data
    headless mode
    mobile hotspot
    """
