"""Find an artwork in the WahooArt catalog, read its details and price an oil reproduction.

    pip install -r requirements.txt
    python find_and_price_an_artwork.py
    python find_and_price_an_artwork.py "Mona Lisa"
"""

import asyncio
import sys

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

ENDPOINT = "https://direct.wahooart.com/mcp/"


async def find_and_price_an_artwork(search_words):
    async with streamablehttp_client(ENDPOINT) as (read_stream, write_stream, _session_id):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            search = await session.call_tool("search_artworks", {"query": search_words, "limit": 1})
            results = search.structuredContent["results"]
            if not results:
                print(f"No artwork found for {search_words!r}.")
                return
            artwork = results[0]
            print(f"{artwork['artist_name']}, {artwork['title']}")
            print(artwork["url"])

            details = await session.call_tool("get_detail_artwork", {"pk": artwork["pk"]})
            print(details.structuredContent["meta_description"])

            quotation = await session.call_tool(
                "get_quotation",
                {
                    "pk": artwork["pk"],
                    "type": "oil painting",
                    "width": 90,
                    "height": 70,
                    "unit": "cm",
                    "currency": "EUR",
                },
            )
            # A request can be fine and the answer still be no: isError carries the reason.
            if quotation.isError:
                print(f"No quotation: {quotation.structuredContent['error']}")
                return
            print(quotation.structuredContent["offer_text"])


if __name__ == "__main__":
    asyncio.run(find_and_price_an_artwork(" ".join(sys.argv[1:]) or "The Starry Night Vincent van Gogh"))
