"""Checks that what this repository says still matches the live server. Standard library only.

    python -m unittest discover tests
"""

import json
import pathlib
import unittest
import urllib.request

REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parent.parent
ENDPOINT = "https://direct.wahooart.com/mcp/"
TOOLS_THE_README_DOCUMENTS = {
    "search_fts",
    "search_artworks",
    "search_artists",
    "search_museums",
    "search_articles",
    "search_sections_semantically",
    "search_objects_semantically",
    "get_detail_artwork",
    "get_detail_artist",
    "get_detail_museum",
    "get_detail_article",
    "get_quotation",
    "get_custom_reproduction_quotation",
    "get_artwork_availability",
}


def call_server(method, params=None, endpoint=ENDPOINT):
    message = {"jsonrpc": "2.0", "id": 1, "method": method}
    if params is not None:
        message["params"] = params
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(message).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "art-search-mcp-repository-tests"},
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        return json.load(response)


def call_tool(name, arguments):
    return call_server("tools/call", {"name": name, "arguments": arguments})["result"]


class LiveServerTests(unittest.TestCase):
    def test_the_public_tools_are_the_ones_the_readme_documents(self):
        listed = {tool["name"] for tool in call_server("tools/list")["result"]["tools"]}
        self.assertEqual(listed, TOOLS_THE_README_DOCUMENTS)

    def test_every_documented_tool_is_named_in_the_readme(self):
        readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        for tool_name in TOOLS_THE_README_DOCUMENTS:
            self.assertIn(f"`{tool_name}`", readme)

    def test_a_search_then_a_quotation_give_what_the_examples_read(self):
        artwork = call_tool("search_artworks", {"query": "Starry Night Van Gogh", "limit": 1})[
            "structuredContent"
        ]["results"][0]
        for field in ("pk", "artist_name", "title", "url", "image_url", "score"):
            self.assertIn(field, artwork)

        details = call_tool("get_detail_artwork", {"pk": artwork["pk"]})["structuredContent"]
        self.assertIn("meta_description", details)

        quotation = call_tool(
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
        self.assertFalse(quotation["isError"], quotation)
        self.assertIn("offer_text", quotation["structuredContent"])


class RepositoryFilesTests(unittest.TestCase):
    def registry_entries(self):
        server_files = sorted((REPOSITORY_ROOT / "servers").glob("*/server.json"))
        self.assertEqual(len(server_files), 8)
        return [json.loads(server_file.read_text(encoding="utf-8")) for server_file in server_files]

    def test_the_client_file_names_the_address_of_the_examples(self):
        client_file = json.loads((REPOSITORY_ROOT / ".mcp.json").read_text(encoding="utf-8"))
        self.assertEqual(client_file["mcpServers"]["wahooart"]["url"], ENDPOINT)
        self.assertIn(ENDPOINT, [entry["remotes"][0]["url"] for entry in self.registry_entries()])

    def test_every_registry_description_fits_its_limit_and_is_its_own(self):
        descriptions = [entry["description"] for entry in self.registry_entries()]
        for description in descriptions:
            self.assertLessEqual(len(description), 100)
        self.assertEqual(len(set(descriptions)), len(descriptions))

    def test_every_registry_entry_answers_with_its_title(self):
        for entry in self.registry_entries():
            address = entry["remotes"][0]["url"]
            with self.subTest(server=entry["name"]):
                server_info = call_server("initialize", {}, endpoint=address)["result"]["serverInfo"]
                self.assertEqual(server_info["title"], entry["title"])
                self.assertEqual(server_info["version"], entry["version"])


if __name__ == "__main__":
    unittest.main()
