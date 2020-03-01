import bottle
import json
from src.controller import controller
import os


@bottle.post('/start')
def start():
    # print(json.dumps(bottle.request.json, indent=2))
    snake_config = {
        'color': '#43E5DF',
        'headType': 'tongue',
        'tailType': 'pixel'
    }
    return snake_config


@bottle.post('/move')
def move():
    # print(json.dumps(bottle.request.json, indent=2))
    move = controller(bottle.request.json)
    print(bottle.request.json)
    return {'move': move}


@bottle.post('/end')
def end():
    print(json.dumps(bottle.request.json, indent=2))
    return 'end'


@bottle.post('/ping')
def ping():
    # print(json.dumps(bottle.request.json, indent=2))
    return 'I am alive.'

if os.environ.get('APP_LOCATION') == 'heroku':
    bottle.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
else:
    bottle.run(host='localhost', port=8080, reloader=True, debug=True)
