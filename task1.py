from bs4 import BeautifulSoup
import requests
import lxml


def get_url_1(sites, base_url, URLS, type, class_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
    for ur in URLS:
        website_url = requests.get(base_url+ur, headers=headers).text
        soup = BeautifulSoup(website_url, "lxml")
        div = soup.find_all(type, {'class': class_name})
        for film in div:
            url = film.find_all('a')[0].get('href').strip()
            if url.startswith("http"):
                continue
            else:
                url = base_url + url
            sites.append(url)

# https://starwars.ru/universe/characters/
# def get_url_2(sites):
#     base_url = 'https://starwars.ru'
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
#     website_url = requests.get(base_url+'/universe/characters/', headers=headers).text
#     soup = BeautifulSoup(website_url, "lxml")
#     div = soup.find_all('div', {'class': 'item show'})
#     for film in div:
#         films = film.find('div', {'class': 'item-part'})
#         url = films.find_all('a')[0].get('href').strip()
#         if url.startswith("http"):
#             sites.append(url)
#         else:
#             sites.append(base_url + url)

sites = []
sites_name = open("index.txt", "w")
get_url_1(sites, 'https://starwars.ru', ['/films','/soundtracks'], 'div', 'item')
get_url_1(sites, 'https://starwars.ru', ['/universe/characters/'], 'div', 'item show')
get_url_1(sites, 'https://starwars.fandom.com', ['/ru/wiki/Категория:Кинофильмы#', '/ru/wiki/Категория:Документальные_фильмы',
                                                 '/ru/wiki/Категория:Легендарные_отдельные_романы'], 'li', 'category-page__member')
i = 1
for url in sites:
    file_name = 'site_' + str(i) + '.txt'
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    text = str(soup)
    sites_name.write(str(i) + ': ' + url + '\n')
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(text)
    i+=1


