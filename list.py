import pandas as pd

url = "https://www.ikea.co.id/in/produk/dekorasi/tanaman-hias/trades-variegata-art-00001130"

with open("ikea.html","r",encoding="utf-8") as file:
    html = file.read()
    file.close()
df = pd.read_html(html)

for i in df:
    print(i)

