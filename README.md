<div align="center">

# WahooArt Art Search MCP

**Give your AI assistant a fine art catalog, with live prices for reproductions.**

[![Check the live server](https://github.com/WahooArt-com/art-search-mcp/actions/workflows/check-live-server.yml/badge.svg)](https://github.com/WahooArt-com/art-search-mcp/actions/workflows/check-live-server.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Authentication: none](https://img.shields.io/badge/authentication-none-brightgreen.svg)
![Tools: read-only](https://img.shields.io/badge/tools-read--only-brightgreen.svg)

[Website](https://wahooart.com/) · [Server documentation](https://wahooart.com/en/mcp/) · [Tool reference](TOOLS.md)

</div>

| 644,615 | 52,888 | 5,406 | 19,446 | 32 |
|:---:|:---:|:---:|:---:|:---:|
| artworks | artists | museums | articles | languages |

<sub>Approved catalog rows on 4 November 2026. The catalog keeps growing.</sub>

[WahooArt](https://wahooart.com/) is a full-service art destination: oil reproductions hand-painted by trained painters on linen canvas, giclée prints, digital images, and custom paintings from your own photos. With this server, your assistant can search that catalog, read the details, check what is for sale now and quote a price.

The server runs on our side, so there is nothing to install or host. No account, no key, no OAuth, and it's free to use.

## Quick start

Add this address to your assistant as a remote MCP server:

```text
https://direct.wahooart.com/mcp/
```

Then ask, for example:

> How much is a hand-painted oil copy of The Starry Night at 90 x 70 cm, framed, in euros?

> Find me calm landscape paintings for a hotel lobby.

> What would a 60 x 80 cm oil painting of my own photo cost?

> Which oil paintings are in stock now, under 500 dollars?

## Connect your client

**Claude or ChatGPT:** open the connector settings, add a custom connector, paste the address and leave the authentication empty.

**Claude Code:**

```bash
claude mcp add --transport http wahooart https://direct.wahooart.com/mcp/
```

<details>
<summary><strong>Cursor</strong></summary>

In `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "wahooart": {
      "url": "https://direct.wahooart.com/mcp/"
    }
  }
}
```

</details>

<details>
<summary><strong>VS Code</strong></summary>

In `.vscode/mcp.json`:

```json
{
  "servers": {
    "wahooart": {
      "type": "http",
      "url": "https://direct.wahooart.com/mcp/"
    }
  }
}
```

</details>

<details>
<summary><strong>Other clients</strong></summary>

Copy [`.mcp.json`](.mcp.json), or enter these values:

| Setting | Value |
|---|---|
| Transport | Streamable HTTP, JSON answers only |
| Address | `https://direct.wahooart.com/mcp/` |
| Method | POST |
| Authentication | None |

</details>

> [!NOTE]
> Opening the address in a browser takes you to the [server documentation](https://wahooart.com/en/mcp/). MCP clients send POST requests, and any other GET answers **HTTP 405**, which is normal. Keep the final slash, because without it the request is redirected and its body is lost.

## Tools

All 14 tools are read-only. Each one takes an optional `language` parameter, English by default.

### Search

| You have | You want | Tool |
|---|---|---|
| A name or keywords | Matching artworks, artists, museums and articles | `search_fts` |
| A name or keywords | One kind of object, with its own filters | `search_artworks`, `search_artists`, `search_museums`, `search_articles` |
| A question | The passages of our texts that answer it | `search_sections_semantically` |
| A text | The objects it is about | `search_objects_semantically` |

### Details, prices and availability

| Tool | What it does |
|---|---|
| `get_detail_artwork`, `get_detail_artist`, `get_detail_museum`, `get_detail_article` | The full data of one object, by the `pk` a search returned |
| `get_quotation` | The price of a print or a hand-painted oil reproduction of an artwork, at a given size and in a given currency, with an order link |
| `get_custom_reproduction_quotation` | The same price from size, type and currency alone, for your own image or an artwork the catalog does not have |
| `get_artwork_availability` | Whether the artwork itself is for sale now (ready-made painting in stock, auction lot, original, collectible), with its price, or the list of objects for sale in one of those channels |

The server cannot place an order, take a payment or change anything. It gives you links: you order and pay on the website, in your browser.

For every parameter, read [TOOLS.md](TOOLS.md) or call `tools/list`.

## Call it from your own code

Try it from a terminal:

```bash
curl -s https://direct.wahooart.com/mcp/ \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_artworks","arguments":{"query":"Monet water lilies","limit":3}}}'
```

The [`examples`](examples) folder holds the same small program in [Python](examples/python/find_and_price_an_artwork.py) and [JavaScript](examples/javascript/find_and_price_an_artwork.mjs). It finds an artwork, reads its details and prices an oil reproduction. A run in Python on 4 November 2026 printed:

```text
Vincent van Gogh, Starry Night Over the Rhone
https://wahooart.com/en/art/vincent-willem-van-gogh-starry-night-over-the-rhone-5ZKG45-en/
Luminous yellow reflections dance upon the dark water under a deep blue, swirling night sky.
Hand-painted oil painting, 87.7 x 71.9 cm, unframed, delivered rolled: 328 EUR — [Order](https://wahooart.com/en/art/vincent-willem-van-gogh-starry-night-over-the-rhone-5ZKG45-en/ArtistReproduction/?reproduction_medium=OilPainting&size_type=custom&size_unit=CM&size_width_cm=87.6698&size_height_cm=71.8605&frame=Rolled)
```

## Good to know

- **Tool names:** until November 2026 the two quotation tools were named `get_a_quotation` and `get_a_custom_reproduction_quotation`. The old names still answer.
- **Sizes:** the quoted size follows the artwork's own proportions, and a size outside 25 to 250 cm per side is quoted at the nearest valid size. Read `width_cm` and `height_cm` in the answer, as the example above shows.
- **`offer_text`:** every quotation carries this ready-made line with the type, size, price and order link. Show it to the user as it is, translating its words if needed but never changing its numbers or link.
- **Semantic search:** it can answer `index_unavailable`. Use the full-text search tools in that case.
- **Rate limit:** 30 requests per second per IP address, with short bursts of 20 more. Beyond that the server answers HTTP 429.

## Your own orders

One more tool, `get_my_orders_details`, returns a customer's own orders and needs a personal token. WahooArt customers can copy theirs from [their account](https://wahooart.com/en/accounts/profile/mcp/). Treat it like a password, and keep it out of your code and your repository.

## Privacy

The tools above read public catalog data only and ask for no name, account or key. For each tool call we record the tool name, the language, the website, the time, the client's user agent and a salted hash of its IP address. Your search words are not part of this record. Read the [full notice](https://wahooart.com/en/mcp/#privacy).

## Support

A question or a problem with the server? Write to [Contact@WahooArt.com](mailto:Contact@WahooArt.com) or [open an issue](https://github.com/WahooArt-com/art-search-mcp/issues).

## License

The examples and files in this repository are under the [MIT License](LICENSE). It does not cover the WahooArt catalog, its texts and images, or the server.
