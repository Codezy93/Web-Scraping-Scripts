from bs4 import BeautifulSoup
import requests
from colorama import Fore
from pprint import pprint
import urllib3

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"}
url = "https://www.salary.com/research"
print('| Country | Link |')
print('| -- | -- |')
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content, 'html5lib')
countries = soup.find('div', attrs={'class':'sal-browse-country-container'}).find_all('a')
for country in countries:
    link = country['href']
    country = country.find('span').text
    print(f'| {country} | https://www.salary.com{link} |')