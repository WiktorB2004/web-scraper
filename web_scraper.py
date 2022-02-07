## Morele.net CPUs web scraper project, GitHub: WiktorB2004
from pprint import pprint
import requests
from bs4 import BeautifulSoup

proc_man = input('Do you want to search for AMD or Intel products? ')
available_proc_man = ['amd', 'intel']
if proc_man.lower() not in available_proc_man:
    print('Invalid proccesor manufacturer selected!!')
else: 
    url = f'https://www.morele.net/kategoria/procesory-45/?q={proc_man}'
    page = requests.get(url).text
    doc = BeautifulSoup(page, 'html.parser')
    try:
        pages_num = int(doc.find('div', class_='pagination-btn-nolink-anchor').contents[0].string.strip())
    except AttributeError:
        pages_num = int(doc.find_all('ul', class_='pagination dynamic')[0].find_all('li', class_='pagination-lg')[-2].contents[1].string.strip())
    for page in range(pages_num):
        url = f'https://www.morele.net/kategoria/procesory-45/,,,,,,,,0,,,,/{page}/?q={proc_man}'
        page = requests.get(url).text
        doc = BeautifulSoup(page, 'html.parser')
        products_data = doc.find_all('div', class_='cat-product')
        found_products = []
        for product in products_data:
            product_link = 'https://www.morele.net' + product.find('a', class_='productLink')['href']
            name, clock, cache, *other = product['data-product-name'].split(',')
            product_price = product['data-product-price']
            product = {'name': name, 'clock': clock, 'cache': cache ,'price': float(product_price), 'link': product_link}
            found_products.append(product)

    sorted_products = sorted(found_products,key= lambda x: x['price'])
    for product in sorted_products:
        print(f'''
        Product: {product['name']}
        Clock speed: {product['clock']}
        Cache memory: {product['cache']}
        Price: {product['price']}
        Link: {product['link']}
        ''')
    print('Sorted by descending price, source: morele.net')    