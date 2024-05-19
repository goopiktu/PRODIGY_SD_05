import requests
from bs4 import BeautifulSoup
import pandas as pd

page = 1
name = []
current_price = []
old_price = []
rating = []
isHaveNextPage = True

while isHaveNextPage:
    url = requests.get(f"https://www.jumia.co.ke/catalog/?q=vitamin+c+serum&page={page}#catalog-listing")
    soup = BeautifulSoup(url.text, 'html.parser')
    product = soup.find_all('article', class_="prd _fb col c-prd")

    for item in product:
        names = item.find("h3", class_="name")
        names = names.text if names else 'N/A'

        current_prices = item.find("div", class_="prc")
        current_prices = current_prices.text if current_prices else 'N/A'

        old_prices = item.find("div", class_="old")
        old_prices = old_prices.text if old_prices else 'N/A'

        ratings = item.find("div", class_="rev")
        ratings = ratings.find("div", class_="stars _s").text if ratings and ratings.find("div", class_="stars _s") else 'N/A'

        name.append(names)
        current_price.append(current_prices)
        old_price.append(old_prices)
        
        rating.append(ratings)

    # Check if there is a next page
    next_page = soup.find('a', {'aria-label': 'Next Page'})
    if not next_page or page == 50:
        isHaveNextPage = False
    page += 1

df = pd.DataFrame({
    'Product Name': name,
    'Current Price': current_price,
    'Old Price': old_price,
    'Rating': rating
})

df.to_csv('jumia_data_new_001.csv', index=False, encoding='utf-8')
