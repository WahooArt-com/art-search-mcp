# WahooArt Art Search & Quotation

Search 640,000 artworks and price hand-painted oil reproductions, giclée prints and custom art.

WahooArt is a premium, full-service art destination: oil reproductions hand-painted by trained painters on linen canvas, giclée prints, digital images, and custom paintings from your own photos.

- MCP server: `https://direct.wahooart.com/mcp/`
- Documentation: https://wahooart.com/en/mcp/
- Name in the official MCP Registry: `com.wahooart/art-search`

## Connect

The server address is `https://direct.wahooart.com/mcp/`. No account, no key, no installation.

- **Claude** (claude.ai, Claude Desktop): Settings, Connectors, "Add custom connector", paste the address.
- **ChatGPT** (developer mode): add a connector with the address and no authentication.
- **Cursor, VS Code, Windsurf and other clients with a JSON configuration:**

```json
{
  "mcpServers": {
    "wahooart-art-search": {
      "url": "https://direct.wahooart.com/mcp/"
    }
  }
}
```

Transport: Streamable HTTP, protocol revision 2025-06-18, plain JSON answers (no event stream, no session). Every tool is read-only.

## What to ask

- "How much is a hand-painted oil copy of The Starry Night at 90 x 70 cm, framed, in euros?"
- "Find me calm landscape paintings for a hotel lobby."
- "What would a 60 x 80 cm oil painting of my own photo cost?"

## Try it from a terminal

```bash
curl -s https://direct.wahooart.com/mcp/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "search_fts", "arguments": {"query": "Starry Night"}}}'
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

Parameters and results of each tool: [TOOLS.md](../../TOOLS.md). Examples in Python and JavaScript: [the repository README](../../README.md).
