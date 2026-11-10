# AllPaintingsStore Trade Art Catalog

Wholesale art for hotels and trade: search paintings, check stock, price any size at volume.

AllPaintingsStore is built for volume and trade buyers: paintings in repeatable standard sizes, hand-painted on linen canvas, prints, digital licensing, custom sizing, and framing at volume.

- MCP server: `https://direct.allpaintingsstore.com/mcp/`
- Documentation: https://allpaintingsstore.com/en/mcp/
- Name in the official MCP Registry: `com.allpaintingsstore/art-search`

## Connect

The server address is `https://direct.allpaintingsstore.com/mcp/`. No account, no key, no installation.

- **Claude** (claude.ai, Claude Desktop): Settings, Connectors, "Add custom connector", paste the address.
- **ChatGPT** (developer mode): add a connector with the address and no authentication.
- **Cursor, VS Code, Windsurf and other clients with a JSON configuration:**

```json
{
  "mcpServers": {
    "allpaintingsstore-art-search": {
      "url": "https://direct.allpaintingsstore.com/mcp/"
    }
  }
}
```

Transport: Streamable HTTP, protocol revision 2025-06-18, plain JSON answers (no event stream, no session). Every tool is read-only.

## What to ask

- "Price this painting as a print at 50 x 70 cm and at 100 x 140 cm, in US dollars."
- "Which oil paintings are in stock now, under 500 dollars?"
- "Find seascapes suitable for a corridor of guest rooms."

## Try it from a terminal

```bash
curl -s https://direct.allpaintingsstore.com/mcp/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "search_fts", "arguments": {"query": "seascape"}}}'
```

## Tools (14)

- `search_artworks`: Search artworks
- `search_museums`: Search museums
- `search_artists`: Search artists
- `search_articles`: Search articles
- `search_sections_semantically`: Search passages by meaning (articles, museums, artists, artworks)
- `search_objects_semantically`: Find artworks, artists, museums or articles by meaning
- `search_fts`: Find artworks, artists, museums and articles by name or keywords
- `get_detail_artwork`: Get artwork details
- `get_detail_artist`: Get artist details
- `get_detail_museum`: Get museum details
- `get_detail_article`: Get article details
- `get_quotation`: Get a reproduction price quotation
- `get_custom_reproduction_quotation`: Get a custom reproduction price quotation (no catalog artwork needed)
- `get_artwork_availability`: Is this artwork available now, and at what price (stock, auction, originals, collectibles)

Parameters and results of each tool: [TOOLS.md](../../TOOLS.md). The 7 other servers and examples in Python and JavaScript: [the repository README](../../README.md).
