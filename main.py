import requests
import json
import pandas as pd
import collections

def create_games_df(results):
    # create dataframe of games
    games_list = []
    for game in results:
        # print(game.get('name'))
        row = {'name_slug': game.get('slug'), 'name': game.get('name'), 'tags': []}
        for tag in game.get('tags'):
            row['tags'].append(tag.get('name').strip('"').lower())
        games_list.append(row)
    return pd.DataFrame(games_list, columns=['nameSlug', 'name', 'tags'])

def main():
    eng_tags = []
    for i in range(1, 100):
        url = f'https://api.rawg.io/api/games?key=be67fbc682e9486b91f280b7a1ccaf27&dates=1970-09-01,2020-01-01&page_size=40&page={i}&ordering=-metacritic'
        df = pd.read_json(url)
        results = df.results

        df = create_games_df(results)

        # create list of tags
        tags_list = []
        for tags in df.tags:
            tags_list.extend(tags)
        for tag in tags_list:
            for char in tag:
                if ord(char) > 255:
                    break
                else:
                    eng_tags.append(tag)
                    break
    # print(eng_tags)
    print(collections.Counter(eng_tags))

    with open('tags.txt', 'w') as file:
        file.write(json.dumps(collections.Counter(eng_tags).most_common()))

    # with open('tags.txt', 'w') as w:
    #     w.write("The word frequency is " + str(freq))
    # filename.close()

    # with open("tags.txt") as f:
    #     for k, v in eng_tags:
    #         f.write("{} {}\n".format(k, v))


    # tagsdf.to_csv('output.txt', sep=' ', index=False)

    # tags = df.tags.tolist()
    # print(tags)
    # for gameTags in df.tags:
    #     tags += gameTags
    # tags = tags.lower()



if __name__ == "__main__":
    main()



# rawg = rawgpy.RAWG("WCormacStrickland@gmail.com")
# derp = rawgpy.RAWG.game_request('', 10, additional_param='?dates=2016-01-01,2021-01-01&ordering=-added')
# pd.read_json(rawgpy.RAWG.game_request('', 10, additional_param='?dates=2016-01-01,2021-01-01&ordering=-added'))
# print(GenreChart("Action"))

#
# results = rawg.search("Warframe")
# game = results[0]
# game.populate()
#
# print(game._yearchart)
# print(game.tags)

#for year in range(2010, 2020):
