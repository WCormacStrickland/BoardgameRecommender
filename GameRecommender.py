import requests
import json
# import pandas as pd
import collections

from RawgDataProcess import RawgDataProcess
from TFIDF import TFIDF


def main():
    games = input_games()
    tags = get_tags(games)

    rawgDataProcess = RawgDataProcess(str(tags))
    rawgDataProcess.process()
    tags = rawgDataProcess.get_tags()

    tfidf = TFIDF()
    rec_games = tfidf.get_recommendation(tags)
    for game in rec_games:
        print(game)



def input_games():
    games = []
    print('Enter Game Names, Enter exit To finish:')
    for i in range(0, 10):
        gameInput = input()
        if gameInput == 'exit':
            break
        else:
            games.append(gameInput.replace(" ", "-").lower())
    return games


def get_tags(games):
    tag_list = []
    for game in games:
        url = requests.get(f'https://api.rawg.io/api/games/{game}?key=be67fbc682e9486b91f280b7a1ccaf27')
        game_json = json.loads(url.text)
        tags = game_json["tags"]
        for tag in tags:
            tag_list.append(tag.get('name').strip('"'))
    return tag_list

# def get_tags(game_json):
#     tag_list = []
#     tags = game_json["tags"]
#     for tag in tags:
#         tag_list.append(tag.get('name').strip('"'))
#     return tag_list

if __name__ == "__main__":
    main()
