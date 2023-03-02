import requests
import json
import argparse

DESCRIPTION = "Get game information from howlongtobeat.com"
HLTB_URL = "https://howlongtobeat.com"
SEARCH_URL = "https://howlongtobeat.com/api/search"
DEFAULT_HEADERS = {
    "content-type": "application/json",
    "accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "referer": HLTB_URL
}

class GameEntry:
    def __init__(self, json):
        self.name = json["game_name"]
        self.id = json["game_id"]
        self.link = "{}/game/{}".format(HLTB_URL, self.id)
        self.main = "{} Hours".format(round(json["comp_main"] / 3600))
        self.main_extra = "{} Hours".format(round(json["comp_plus"] / 3600))
        self.completion = "{} Hours".format(round(json["comp_100"] / 3600))
        self.all = "{} Hours".format(round(json["comp_all"] / 3600))
    
    def __str__(self):
        display = f"{self.name}\n" +                          \
                  f"\tLink: {self.link}\n" +                          \
                  f"\tMain Story Time: {self.main}\n" +               \
                  f"\tMain + Extra Time: {self.main_extra}\n" +       \
                  f"\tCompletionist Time: {self.completion}\n" +      \
                  f"\tAll Styles Avg: {self.all}"
        return display

    
def getQuery(name: str, page: int = 1):
    query = {
        "searchType": "games",
        "searchTerms": name.split(),
        "searchPage": page,
        "size": 20,
        "searchOptions": {
            "games": {
                "userId": 0,
                "platform": "",
                "sortCategory": "popular",
                "rangeCategory": "main",
                "rangeTime": {
                    "min": 0,
                    "max": 0
                },
                "gameplay": {
                    "perspective": "",
                    "flow": "",
                    "genre": ""
                },
                "modifier": "",
            },
            "users": {
                "sortCategory": "postcount"
            },
            "filter": "",
            "sort": 0,
            "randomizer": 0
        }
    }

    return json.dumps(query)

def main():

    parser = argparse.ArgumentParser(description = DESCRIPTION)
    parser.add_argument("-n", "--number", type = int, help = "Number of results to display")
    parser.add_argument("game", type = str, help = "Name of game to search")
    args = parser.parse_args()

    resp = requests.post(SEARCH_URL, headers = DEFAULT_HEADERS, data = getQuery(args.game, 0))
    json_data = json.loads(resp.text)

    if len(json_data["data"]) == 0:
        print("No games found for search: {}".format(args.game))
        return
    
    gameList = []

    for entry in json_data["data"]:
        game = GameEntry(entry)
        gameList.append(game)

    print('There are {} total results for your search: "{}"\n\n'.format(len(gameList), args.game))
    count = 1
    for game in gameList:
        if args.number and count > args.number:
            break

        count = count + 1

        print("{}\n\n".format(game))

if __name__ == "__main__":
    main()