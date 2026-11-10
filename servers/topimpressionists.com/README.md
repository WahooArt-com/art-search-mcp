# TopImpressionists Impressionist Art Search

Impressionist art: Monet, Renoir, Degas, Van Gogh. Search works and price oil reproductions.

TopImpressionists is the home of Impressionist and Post-Impressionist art, from Monet and Renoir to Degas, Cézanne and Van Gogh: hand-painted reproductions on linen canvas, archival prints and digital images.

- MCP server: `https://direct.topimpressionists.com/mcp/`
- Documentation: https://topimpressionists.com/en/mcp/
- Name in the official MCP Registry: `com.topimpressionists/art-search`

## Connect

The server address is `https://direct.topimpressionists.com/mcp/`. No account, no key, no installation.

- **Claude** (claude.ai, Claude Desktop): Settings, Connectors, "Add custom connector", paste the address.
- **ChatGPT** (developer mode): add a connector with the address and no authentication.
- **Cursor, VS Code, Windsurf and other clients with a JSON configuration:**

```json
{
  "mcpServers": {
    "topimpressionists-art-search": {
      "url": "https://direct.topimpressionists.com/mcp/"
    }
  }
}
```

Transport: Streamable HTTP, protocol revision 2025-06-18, plain JSON answers (no event stream, no session). Every tool is read-only.

## What to ask

- "Show me Monet water lilies and price one as an oil painting at 100 x 100 cm."
- "Which Impressionist painters were alive in 1880?"
- "What does your site say about how Degas painted dancers?"

## Try it from a terminal

```bash
curl -s https://direct.topimpressionists.com/mcp/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "search_fts", "arguments": {"query": "Monet water lilies"}}}'
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
