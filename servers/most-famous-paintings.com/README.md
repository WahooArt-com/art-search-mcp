# Most-Famous-Paintings Masterpiece Guide

Famous paintings: Mona Lisa, Starry Night. Their story, their museum, a reproduction price.

Most-Famous-Paintings is dedicated to the great masterpieces: the story behind each work, museum-quality reproductions hand-painted on linen canvas, archival prints and digital images.

- MCP server: `https://direct.most-famous-paintings.com/mcp/`
- Documentation: https://most-famous-paintings.com/en/mcp/
- Name in the official MCP Registry: `com.most-famous-paintings/art-search`

## Connect

The server address is `https://direct.most-famous-paintings.com/mcp/`. No account, no key, no installation.

- **Claude** (claude.ai, Claude Desktop): Settings, Connectors, "Add custom connector", paste the address.
- **ChatGPT** (developer mode): add a connector with the address and no authentication.
- **Cursor, VS Code, Windsurf and other clients with a JSON configuration:**

```json
{
  "mcpServers": {
    "most-famous-paintings-art-search": {
      "url": "https://direct.most-famous-paintings.com/mcp/"
    }
  }
}
```

Transport: Streamable HTTP, protocol revision 2025-06-18, plain JSON answers (no event stream, no session). Every tool is read-only.

## What to ask

- "Where is the Mona Lisa kept, and how much is a hand-painted copy at 50 x 70 cm?"
- "Why is The Birth of Venus so famous?"
- "List the famous paintings kept in the Louvre."

## Try it from a terminal

```bash
curl -s https://direct.most-famous-paintings.com/mcp/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "search_fts", "arguments": {"query": "Mona Lisa"}}}'
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
