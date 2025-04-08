from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from pymongo import MongoClient

def get_list():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    client = MongoClient('mongodb://localhost:27017/')
    db = client['pokemon_db']  # Create/use a database called 'pokemon_db'
    collection = db['pokemon_data']
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://pokemondb.net/pokedex/all")
    soup = BeautifulSoup(driver.page_source, 'html5lib')
    table = soup.find('table', attrs={'id': 'pokedex'}).find('tbody').find_all('tr')
    count = 0 
    for i in table:
        id = i.find('td', attrs={'class': 'cell-num cell-fixed'})
        thumbnail = id.find('img')['src']
        id = id.find('span').text
        name = i.find('td', attrs={'class': 'cell-name'})
        url = name.find('a')['href']
        if name.find('small') is None:
            name = name.find('a').text
        else:
            name = name.find('small').text
        pokemon_data = {
            "_id": f"{count:04}",
            "pokemon_id": id,
            "name": name,
            "thumbnail": thumbnail,
            "url": url
        }
        count += 1
        collection.insert_one(pokemon_data)
    driver.quit()
    client.close()