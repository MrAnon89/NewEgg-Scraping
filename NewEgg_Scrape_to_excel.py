from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

search_term = input("What product do you want to search for? ")

url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

page_text = doc.find(class_="list-tool-pagination-text").strong
pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])

items_found = []

for page in range(1, pages + 1):
	url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131&page={page}"
	page = requests.get(url).text
	doc = BeautifulSoup(page, "html.parser")

	div = doc.find(class_="item-cells-wrap border-cells short-video-box items-list-view is-list")
	items = div.find_all(text=re.compile(search_term))

	for item in items:
		parent = item.parent
		if parent.name != "a":
			continue

		link = parent['href']
		next_parent = item.find_parent(class_="item-container")
		try:
			price = next_parent.find(class_="price-current").find('strong').string
			items_found.append({
				"Item": item,
				"price": int(price.replace(',', '')),
				"link": link
			})
		except:
			pass

sorted_items = sorted(items_found, key=lambda x: x['price'])

df = pd.DataFrame(sorted_items)
df.to_excel(search_term+'_NewEgg.xlsx', index=False)
print('done')

