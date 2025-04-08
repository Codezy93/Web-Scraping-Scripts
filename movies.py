from bs4 import BeautifulSoup
import requests
from colorama import Fore
from pprint import pprint
import urllib3

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"}

def get_title(number):
    url = f"https://www.imdb.com/title/tt{number}/"
    map = {
            'id' : number,
            "title": "",
            "duration": "",
            "release" : "",
            "rating" : "",
            "director" : [],
            "writer" : [],
            "stars" : [],
            "crew" : [],
            "storyline" : "",
            "tagline" : "",
            "genres" : [],
            "country" : "",
            "language" : "",
            "production" : [],
            "box-office" : {},
            "color" : "",
            "sound-mix" : "",
            "aspect-ratio" : "",
        }
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        map['id'] = number
        map['title'] = soup.find('span', attrs={'class':'hero__primary-text'}).text
        map['rating'] = soup.find('ul', attrs={'class':'ipc-inline-list ipc-inline-list--show-dividers sc-ec65ba05-2 joVhBE baseAlt'}).find_all('li')[1].find('a').text
        map['duration'] = soup.find('ul', attrs={'class':'ipc-inline-list ipc-inline-list--show-dividers sc-ec65ba05-2 joVhBE baseAlt'}).find_all('li')[2].text
        map['cover'] = soup.find('img', attrs={'class':'ipc-image'})['src']
        map['storyline'] = soup.find('div', attrs={'class':'sc-3c16af05-0 kefoZk'}).find('div', attrs={'class':'ipc-html-content-inner-div'}).text
        pprint(map)
        map['tagline'] = soup.find('div', attrs={'class':'sc-3c16af05-0 kefoZk'}).find('ul', attrs={'class':'ipc-metadata-list ipc-metadata-list--dividers-all sc-3c16af05-1 izVAgC ipc-metadata-list--base'}).find_all('li')[0].find('span', attrs={'class':'ipc-metadata-list-item__list-content-item'}).text
        map['genres'] = [i.find('a').text for i in soup.find('div', attrs={'class':'sc-3c16af05-0 kefoZk'}).find('ul', attrs={'class':'ipc-metadata-list ipc-metadata-list--dividers-all sc-3c16af05-1 izVAgC ipc-metadata-list--base'}).find_all('li')[1].find('ul', attrs={'class':'ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base'}).find_all('li')]
    except urllib3.exceptions.NameResolutionError:
        print(Fore.RED + f"{number} : Name Resolution Error")
    except Exception as e:
        print(Fore.RED + f"{number} : {e}")

# for i in range(1000000, 9999999):
#     get_title(f"{i:07}")

if __name__ == "__main__":
    get_title('28259207')