from bs4 import BeautifulSoup
import requests
from colorama import Fore
from pprint import pprint
import urllib3
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['library']
book = db['book_information']
author_collection = db['author_information']

def get_title(number, letter):
    key = f"OL{number}{letter}"
    url = f"https://openlibrary.org/books/"+key
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        map = {
            "title": "",
            "author": "",
            "rating": "",
            "cover": "",
        }
        title = soup.find('h1', attrs={'class':'work-title'})
        if title:
            map['title'] = title
            author = soup.find('h2', attrs={"class":"edition-byline"})
            if author:
                author_code = author.find('a')['href'].replace('/authors/', "").split("/")[0]
                author = author.find('a').text
                map['author'] = author
            rating = soup.find('span', attrs={'itemprop':'ratingValue'})
            if rating:
                rating = rating.text
                map['rating'] = rating
            cover = soup.find('img', attrs={'itemprop':'image'})
            if cover:
                cover = cover['src']
                map['cover'] = cover
            print(Fore.GREEN)
            pprint(map)
        else:
            print(Fore.RED + f"OL{number}{letter}")
    except urllib3.exceptions.NameResolutionError:
        print(Fore.RED + f"OL{number}{letter} : Name Resolution Error")
    except Exception as e:
        print(Fore.RED + f"OL{number}{letter} : {e}")

for i in range(10000, 99999):
    for j in ['W', 'M']:
        get_title(f"{i:05}", j)
