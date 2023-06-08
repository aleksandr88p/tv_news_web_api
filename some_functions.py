import datetime
import json

import requests
from bs4 import BeautifulSoup

# today = datetime.date.today()
# week_number = today.isocalendar()[1]

def make_soup_here():
    today = datetime.date.today()
    week_number = today.isocalendar()[1]
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }

    response = requests.get(f'https://flixpatrol.com/top10/streaming/world/2023-0{week_number}/', headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def find_platforms_names():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }

    response = requests.get('https://flixpatrol.com/top10/streaming/world/2023-023/', headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    div_tags = soup.find_all('div', id=True)
    platforms_names = []
    for div in div_tags:
        div_id = div.get('id')
        platforms_names.append(div_id)
    return platforms_names

platforms_names_OLD = ['netflix-1', 'netflix-2', 'hbo-1', 'hbo-2', 'disney-1', 'disney-2', 'amazon-prime-1',
                   'amazon-prime-2', 'paramount-plus-1', 'paramount-plus-2', 'hulu-1', 'hulu-2', 'amazon-1', 'amazon-2',
                   'itunes-1', 'itunes-2', 'google-1', 'google-2', 'rakuten-tv-1', 'rakuten-tv-2', 'chili-1', 'chili-2',
                   'vudu-1', 'vudu-2', 'star-plus-1', 'star-plus-2', 'freevee-1', 'freevee-2', 'globoplay-1',
                   'globoplay-2', 'osn-1', 'osn-2', 'shahid-1', 'shahid-2', 'starz-1', 'starz-2', 'viaplay-1',
                   'viaplay-2', 'apple-tv-1', 'apple-tv-2']

platforms_names = ['netflix-1', 'netflix-2', 'hbo-1', 'hbo-2', 'disney-1', 'disney-2', 'amazon-prime-1',
                   'amazon-prime-2', 'paramount-plus-1', 'paramount-plus-2', 'hulu-1', 'hulu-2', 'apple-tv-1', 'apple-tv-2']


platforms_dict = {"Netflix": ['netflix-1', 'netflix-2'], "HBO": ['hbo-1', 'hbo-2'], "Disney": ['disney-1', 'disney-2'],
                  "Prime Video": ['amazon-prime-1','amazon-prime-2'], "Paramount": ['paramount-plus-1', 'paramount-plus-2'],
                  "Hulu": ['hulu-1', 'hulu-2'], "Apple+": ['apple-tv-1', 'apple-tv-2']}
def find_top_by_platform(platform_dict, soup):
    res_dict = {}

    for key_name, value in platform_dict.items():
        d = {}
        for platform in value:
            try:
                div_by_id = soup.find('div', attrs={'id': platform}).find('table').find('a')

                movie_or_show = div_by_id.text.strip()
            except Exception as e:
                movie_or_show = f'somthing wrong in {platform}'

            if platform[-2::] == '-1':
                platform_name = platform[0:-2] + ' Movie'
                type_show = 'Movie'
            elif platform[-2::] == '-2':
                platform_name = platform[0:-2] + ' TV show'
                type_show = 'TV SHOW'
            else:
                platform_name = platform
                type_show = 'None'

            d[type_show] = movie_or_show
        res_dict[key_name] = d

    return res_dict

# soup = make_soup_here()


# d = find_top_by_platform(platform_dict=platforms_dict, soup=soup)
# print(json.dumps(d, indent=4))