import aiohttp

OPENPHISH_FEEDS_URL = "https://opfeeds.s3-us-west-2.amazonaws.com/OPBL/phishing_blocklist.txt"

async def fetch_openphish_feeds():
    async with aiohttp.ClientSession() as session:
        async with session.get(OPENPHISH_FEEDS_URL) as response:
            if response.status == 200:
                feeds = await response.text()
