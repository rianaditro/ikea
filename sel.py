from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument("--enable-javascript")

driver = webdriver.Chrome(options)

main_url = "https://www.ikea.co.id/in/produk/dekorasi-kamar-tidur/tanaman-hias"
driver.get(main_url)

element = driver.find_element(By.XPATH,'//*[@id="pagination-component-content"]/div/div/div/div/nav/ul/li[3]/a/span[1]')
element.click()

time.sleep(5)

driver.quit()
