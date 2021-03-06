from aiohttp.client import ClientSession
from flask import Flask, jsonify, request
from flask_cors import CORS
import asyncio
from configparser import ConfigParser

app = Flask(__name__)
CORS(app)
ROUTE = "/api"
config = ConfigParser()
config.read('config.ini')
external_api = config['DEFAULT']['api_add']
requests_number = int(config['DEFAULT']['requests'])

# Async function to fetch results from Exponea testing server, standard blocking
# cannot be used, otherwise implementing "first" would be unenecessairly difficult.
# Added the url parameter to make function more reusable
async def get(session, url):
  response = await session.get(url)
  try:
    text = await response.json()
    return text
  except Exception as e:
    # IF we're here it means that the server responed with something that isn't json,
    # wich means that the request failed
    return(False)

  

@app.route(ROUTE+'/all', methods = ['GET'])
async def get_all():
    #timeout = request.get_json().get('timeout')
    async with ClientSession() as session:
      tasks = []
      # I know this part is not so necessary, but it allows you to modify the
      # number of calls to the Exponea api if needed
      for x in range(requests_number):
        tasks.append(asyncio.create_task(get(session, external_api)))
      # I put a default timeout (10 sec) even if it wasn't explicitly asked since I just
      # couldn't let the server hang forever if there was a problem with the 
      # request to the Exponea server
      timeout = request.args.get('timeout') or 10000
      # Transform milliseconds to seconds
      timeout = float(timeout) / 1000
      # I implemented the timeout feature on the asyncio call, which technically
      # doesn't encompass the whole function but is close enough, I can't think
      # of a reason to justify writing verbose code and lowering code readibility
      # just so it's a few milliseconds more precise.
      responses = await asyncio.wait(tasks, timeout=timeout)
    # Check response tuple, if only one element means timeout reached. Added second
    # condition since it's possible (although extremely improbable) that one request
    # was successful before timeout
    if len(responses) == requests_number and len(responses[0]) == requests_number:
      response_list = []
      for x in range(requests_number):
        response_list.append(list(responses[0])[x].result())
      # Check if both responses are valid
      if not False in response_list:
        # Transform touple to json list before return
        return(jsonify(response_list))
      else:
        return 'Internal server error 500', 500
    else:
      return 'Internal server error 500', 500


@app.route(ROUTE+'/first', methods = ['GET'])
async def get_first():
    #timeout = request.get_json().get('timeout')
    async with ClientSession() as session:
      tasks = []
      for x in range(requests_number):
        tasks.append(asyncio.create_task(get(session, external_api)))

      timeout = request.args.get('timeout') or 10000
      timeout = float(timeout) / 1000

      # Essentially equal to /api/all, just uses the first response instead of both
      response = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
      if len(response) == 2:
        response = list(response[0])[0].result()
        if response:
          return(response)
        else:
          return 'Internal server error 500', 500
      else:
        return 'Internal server error 500', 500
