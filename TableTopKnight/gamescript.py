import json
from libbgg.apiv2 import BGG
from database.models import Game

conn = BGG()

results = conn.get_hotness(hot_type='boardgame')
gameids=[
   result['id'] for result in results['items']['item']
]
games = conn.boardgame(gameids, stats=False, videos=False, marketplace=False, ratingcomments=False)
for game in games['items']['item']:
    name = ''
    try:
        name = game["name"]["value"]
    except:
        name = game["name"][0]["value"]

    minplayers = int(game["minplayers"]["value"])
    maxplayers = int(game["maxplayers"]["value"])
    thumbnail = game["thumbnail"]["TEXT"]
    description = game['description']['TEXT']
    genre = game['link'][0]['value']

    Game.objects.create_game(
        gameName=name,
        playerMin=minplayers,
        playerMax=maxplayers,
        genre=genre,
        thmb=thumbnail,
        desc=description
    )

