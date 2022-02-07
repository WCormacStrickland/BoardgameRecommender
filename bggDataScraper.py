import csv
import json
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

cat_dict = {}
mech_dict = {}
fam_dict = {}


def main():
    df = pd.read_csv('bgg_data.csv')
    bgg_df = df[['name', 'category', 'mechanic', 'family', 'bayes_rating']]

    scrape_categories()
    scrape_mechanics()
    scrape_families()
    rows_list = []
    for index in bgg_df.index:
        cat_list = []
        for key in str(bgg_df.loc[index, 'category']).split(","):
            cat_list.append(cat_dict.get(key))
        mech_list = []
        for key in str(bgg_df.loc[index, 'mechanic']).split(","):
            mech_list.append(mech_dict.get(key))
        fam_list = []
        for key in str(bgg_df.loc[index, 'family']).split(","):
            fam_list.append(fam_dict.get(key))
        rows_list.append({'name': bgg_df.loc[index, 'name'], 'category': cat_list, 'mechanic': mech_list, 'family': fam_list, 'bayes_rating': bgg_df.loc[index, 'bayes_rating']})
    my_df = pd.DataFrame(rows_list, columns=['name', 'category', 'mechanic', 'family', 'bayes_rating'])

    my_df.to_csv('bgg_data3.csv')


def scrape_families():
    url = 'https://boardgamegeek.com/browse/boardgamefamily/page/1'
    base_url = "https://boardgamegeek.com"
    while True:
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find("table", {"class": "forum_table"})
        hrefs = table.find_all("a", href=re.compile(r"/boardgamefamily/"))
        for href in hrefs:
            href_str = str(href)
            key = re.search(r'/boardgamefamily/(.*?)/', href_str).group(1)
            value = re.search(r'\">(.*?)</a>', href_str).group(1)
        try:
            url = (base_url + soup.find('a', {'title': 'next page'})['href'])
        except TypeError:
            break


def scrape_mechanics():
    html = requests.get("https://boardgamegeek.com/browse/boardgamemechanic").text
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table", {"class": "forum_table"})
    hrefs = table.find_all("a", href=re.compile(r"/boardgamemechanic/"))
    for href in hrefs:
        href_str = str(href)
        key = re.search(r'/boardgamemechanic/(.*?)/', href_str).group(1)
        value = re.search(r'\">(.*?)</a>', href_str).group(1)
        mech_dict[key] = value


def scrape_categories():
    html = requests.get("https://boardgamegeek.com/browse/boardgamecategory").text
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table", {"class": "forum_table"})
    hrefs = table.find_all("a", href=re.compile(r"/boardgamecategory/"))
    for href in hrefs:
        href_str = str(href)
        key = re.search(r'/boardgamecategory/(.*?)/', href_str).group(1)
        value = re.search(r'\">(.*?)</a>', href_str).group(1)
        cat_dict[key] = value


if __name__ == "__main__":
    main()
