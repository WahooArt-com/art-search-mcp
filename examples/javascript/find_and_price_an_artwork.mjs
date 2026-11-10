// Find an artwork in the WahooArt catalog, read its details and price an oil reproduction.
//
//   npm install
//   node find_and_price_an_artwork.mjs
//   node find_and_price_an_artwork.mjs "Mona Lisa"

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const ENDPOINT = "https://direct.wahooart.com/mcp/";
const searchWords = process.argv.slice(2).join(" ") || "The Starry Night Vincent van Gogh";

const client = new Client({ name: "art-search-mcp-example", version: "1.0.0" });
await client.connect(new StreamableHTTPClientTransport(new URL(ENDPOINT)));

try {
  const search = await client.callTool({
    name: "search_artworks",
    arguments: { query: searchWords, limit: 1 },
  });
  const [artwork] = search.structuredContent.results;

  if (!artwork) {
    console.log(`No artwork found for "${searchWords}".`);
  } else {
    console.log(`${artwork.artist_name}, ${artwork.title}`);
    console.log(artwork.url);

    const details = await client.callTool({
      name: "get_detail_artwork",
      arguments: { pk: artwork.pk },
    });
    console.log(details.structuredContent.meta_description);

    const quotation = await client.callTool({
      name: "get_quotation",
      arguments: {
        pk: artwork.pk,
        type: "oil painting",
        width: 90,
        height: 70,
        unit: "cm",
        currency: "EUR",
      },
    });
    // A request can be fine and the answer still be no: isError carries the reason.
    if (quotation.isError) {
      console.log(`No quotation: ${quotation.structuredContent.error}`);
    } else {
      console.log(quotation.structuredContent.offer_text);
    }
  }
} finally {
  await client.close();
}
