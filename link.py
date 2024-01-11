from requests_html import HTMLSession

url = "https://www.ikea.co.id/in/produk/dekorasi/jam"

session = HTMLSession()
r = session.get(url)
r.html.render(sleep=1)
links = r.html.absolute_links
#link = r.html.next(fetch=False)
len = len(links)
print(len)
print(links)