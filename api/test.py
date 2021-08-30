import aiohttp
import asyncio
import json

async def main():

    async with aiohttp.ClientSession() as session:
        async with session.get('https://exponea-engineering-assignment.appspot.com/api/work') as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            t = json.loads(html)
            print(t[time])

loop = asyncio.get_event_loop()
loop.run_until_complete(main())