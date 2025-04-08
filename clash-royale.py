from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import mysql.connector

def setup_database():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="FSLtqMnRt18@19400A"
    )
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS clash_royale")
    cursor.execute("USE clash_royale")
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS cards (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        url VARCHAR(255) NOT NULL
    );
    '''
    cursor.execute(create_table_query)
    
    connection.commit()
    cursor.close()
    connection.close()

def create_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="FSLtqMnRt18@19400A",
        database="clash_royale"
    )
    return connection

def get_list():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://clashroyale.fandom.com/wiki/Card_Overviews")
    soup = BeautifulSoup(driver.page_source, 'html5lib')
    cards = soup.find_all('div', attrs={'class': 'card-overview'})
    connection = create_db_connection()
    cursor = connection.cursor()
    for card in cards:
        name = card.find('h4').find('span').find('a').text
        url = card.find('h4').find('span').find('a')['href']
        query = "INSERT INTO cards (name, url) VALUES (%s, %s)"
        values = (name, url)
        cursor.execute(query, values)
        connection.commit()
    cursor.close()
    connection.close()
    driver.quit()

setup_database()
get_list()