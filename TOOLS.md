# Tools

The 14 tools every one of the 8 servers offers to a caller without a token. All of them are read-only.

## Which search tool

| You have | Use |
|---|---|
| You know a name or keywords and want the matching artworks, artists, museums and articles. | `search_fts` |
| You want one kind of object only, with its own filters such as city, country or article category. | `search_artworks`, `search_artists`, `search_museums`, `search_articles` |
| You have a question and want the passages of our texts that answer it. | `search_sections_semantically` |
| You have a text and want the artworks, artists, museums or articles it is about. | `search_objects_semantically` |

## `search_artworks`

**Search artworks**

Keyword search of ONE model, the artworks: words of the title, the artist name and the description. Use it when you are looking for a work (a painting, a drawing, a sculpture). When the words may name an artist, a museum or an article instead, use search_fts, which searches the four models in one call; when you have a sentence or a paragraph and no name, use search_objects_semantically. Returns only good-confidence matches with pk, artist_name, title, url, image_url (absolute URL of the large artwork image, null when the artwork has no image) and relevance score.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string | yes | Words from the artwork title, artist name and/or description. |
| `language` | string | no | Site language code (2 letters, e.g. "en", "fr"). Default "en". |
| `limit` | integer | no | Maximum number of results (1-10, default 10). |

## `search_museums`

**Search museums**

Keyword search of ONE model, the museums, by name, with two filters no other search tool has: city and country. Use it when you are looking for a museum or for the museums of a place; when the words may name something else than a museum, use search_fts. Returns only good-confidence matches with pk, name, url, image_url (absolute URL of the large museum image, null when there is none), city, country and relevance score.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string | yes | Museum name or words from it. |
| `city` | string | no | Optional city to narrow the search. |
| `country` | string | no | Optional country to narrow the search. |
| `language` | string | no | Site language code (2 letters, e.g. "en", "fr"). Default "en". |
| `limit` | integer | no | Maximum number of results (1-10, default 10). |

## `search_artists`

**Search artists**

Keyword search of ONE model, the artists, by name and biography, with three filters no other search tool has: birth city, birth country and a year the artist was alive (born <= year <= died, or born + 80 years when the death year is unknown). Use it when you are looking for a person; when the words may name a work, a museum or an article, use search_fts. Returns pk, artist_name, url, image_url (absolute URL of the large artist portrait, null when there is none), city, country, date_born, date_death and score.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string | yes | Artist name or words from the biography. |
| `city` | string | no | Optional birth city. |
| `country` | string | no | Optional birth country. |
| `alive_in_year` | integer | no | Optional year the artist was alive, e.g. 1503. |
| `language` | string | no | Site language code (2 letters, e.g. "en", "fr"). Default "en". |
| `limit` | integer | no | Maximum number of results (1-10, default 10). |

## `search_articles`

**Search articles**

Keyword search of ONE model, the articles of the website, with a category filter no other keyword search has. Use it to LIST the articles on a subject; to get the passages that answer a question, use search_sections_semantically. Returns pk, title, url, image_url (absolute URL of the large article image, null when there is none), category_code, meta_description and relevance score.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string | yes | Words to search in the article texts. |
| `category_code` | string | no | Optional article category filter. Allowed values: Video, Blog, Testimonial, Top10, Top25, Top10Versus, Top, Ebook, Support, Misc, Menu, Website, Compare, QuestionAnswer, ArtVsArt. |
| `language` | string | no | Site language code (2 letters, e.g. "en", "fr"). Default "en". |
| `limit` | integer | no | Maximum number of results (1-10, default 10). |

## `search_sections_semantically`

**Search passages by meaning (articles, museums, artists, artworks)**

Search by MEANING that returns TEXT PASSAGES, not objects: the sections of our texts that answer a question best, whatever words they use, each WHOLE (section_text is never cut), from the requested models - "article" (our articles: how reproductions are made, policies, art history), "museum", "artist", "artwork" (their descriptions / biographies); default all models indexed on this server. Each result: model, object_pk (use it with the matching get_detail_* tool), object_title, object_url, category_code (articles), section_heading, section_text, is_faq_question, score (cosine; higher is closer). Ask in a full sentence; any language works (the texts are in English). Sections are packed best first into about 9,000 characters: sections_omitted_for_size says how many more matched. Use it to answer a question from what our texts say; to find a work, artist or museum by name or keywords, use search_fts; to find the objects a text is about, use search_objects_semantically. Error index_unavailable: fall back to the search_* full-text tools.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string | yes | The question or text to find passages for (up to 2000 characters). |
| `models` | array | no | Which texts to search (default: every model indexed on this server). |
| `category_code` | string | no | Optional article category filter (Support / Website for service and policy questions); applies to articles only. Allowed values: Video, Blog, Testimonial, Top10, Top25, Top10Versus, Top, Ebook, Support, Misc, Menu, Website, Compare, QuestionAnswer, ArtVsArt. |
| `language` | string | no | Site language code (2 letters, e.g. "en", "fr"). Default "en". |
| `limit` | integer | no | Maximum number of sections (1-10, default 5). |

## `search_objects_semantically`

**Find artworks, artists, museums or articles by meaning**

Search by MEANING that returns OBJECTS, not passages: the artworks, artists, museums or articles whose texts are closest in meaning to a text (a description, a paragraph, a section of an article), e.g. "a woman reading by a window in soft morning light". The query is a text, not a name. Each result: model, object_pk (use it with the matching get_detail_* tool), object_title, object_url, best_score (cosine of the object's single best passage; higher is closer), score_sum (its matching passages added up) and matched_vectors_count. rank_by "score_sum" (default) favours objects matching in many passages; "best_score" favours the one passage closest to the text - use it to find the exact work a text is about. Any language works (the texts are in English). Use it when you have a text and want the objects it is about; with a name or keywords, use search_fts; for the passages that answer a question, use search_sections_semantically. Error index_unavailable: fall back to the search_* full-text tools.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string | yes | The text to find objects for (up to 2000 characters). |
| `models` | array | no | Which objects to search (default: artwork, artist, museum). |
| `rank_by` | string | no | Ranking: sum of the matching passages (default) or the single best one. Allowed values: score_sum, best_score. |
| `language` | string | no | Site language code (2 letters, e.g. "en", "fr"). Default "en". |
| `limit` | integer | no | Maximum number of objects (1-20, default 10). |

## `search_fts`

**Find artworks, artists, museums and articles by name or keywords**

Keyword search of the FOUR models in one call: artworks, artists, museums and articles (maximum 10 results per model, merged by relevance; each result names its model). It is the first search to try when you have a name or keywords and do not know which kind of object they name ("Monet", "Orsay", "Water Lilies"). It has no filter: once you know the model, search_artworks / search_artists / search_museums / search_articles search that model alone, with its filters (city, country, year alive, category). It matches WORDS: for a sentence or a paragraph without a name, use search_objects_semantically (the objects a text is about) or search_sections_semantically (the passages that answer a question). Each result carries pk, model, title, artist_name, city, country, date_born, date_death, url, image_url (absolute URL of the large image, null when there is none), meta_description and score.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string | yes | Words to search across all four catalogs. |
| `language` | string | no | Site language code (2 letters, e.g. "en", "fr"). Default "en". |

## `get_detail_artwork`

**Get artwork details**

Full data of ONE artwork identified by pk (use a search tool first to find the pk). Always returns: pk, title, meta_description, meta_keywords (first 5), description_html (the artwork description as HTML), url (the artwork page), image_url, and "links" — up to 5 ready-to-give absolute URLs of the most useful related pages (download_page, buy_print_page, buy_oil_painting_page (only for channels on sale), student_guide_page, similar_artworks_page, preview_in_room_page). Also for every caller: "museum" - where the original is kept (pk, name, url of its page on this site, city, country), null when unknown. artwork_not_found when no such artwork is published. The result is capped at 25000 characters: when description_html had to be shortened to fit, "truncated" is true.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `pk` | integer | yes | The object pk, as returned by a search tool. |
| `language` | string | no | Site language code (2 letters, e.g. "en", "fr"). Default "en". |

## `get_detail_artist`

**Get artist details**

Full data of ONE artist identified by pk (use a search tool first to find the pk). Always returns: pk, title, meta_description, meta_keywords (first 5), description_html (the artist biography as HTML), url (the artist page), image_url, and "links" — up to 5 ready-to-give absolute URLs of the most useful related pages (artwork_timeline_page, all_artworks_page, chronicle_page, subject_atlas_page, mood_room_page). artist_not_found when no such artist is published. The result is capped at 25000 characters: when description_html had to be shortened to fit, "truncated" is true.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `pk` | integer | yes | The object pk, as returned by a search tool. |
| `language` | string | no | Site language code (2 letters, e.g. "en", "fr"). Default "en". |

## `get_detail_museum`

**Get museum details**

Full data of ONE museum identified by pk (use a search tool first to find the pk). Always returns: pk, title, meta_description, meta_keywords (first 5), description_html (the museum description as HTML), url (the museum page), image_url, and "links" — up to 5 ready-to-give absolute URLs of the most useful related pages (city_museums_page, museums_by_country_page, official_website, all_museums_page). museum_not_found when no such museum is published. The result is capped at 25000 characters: when description_html had to be shortened to fit, "truncated" is true.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `pk` | integer | yes | The object pk, as returned by a search tool. |
| `language` | string | no | Site language code (2 letters, e.g. "en", "fr"). Default "en". |

## `get_detail_article`

**Get article details**

Full data of ONE article identified by pk (use a search tool first to find the pk). Always returns: pk, title, meta_description, meta_keywords (first 5), description_html (the full article content as HTML), url (the article page), image_url, and "links" — up to 5 ready-to-give absolute URLs of the most useful related pages (articles_by_category_page, all_articles_page, rss_feed). article_not_found when no such article is published. The result is capped at 25000 characters: when description_html had to be shortened to fit, "truncated" is true.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `pk` | integer | yes | The object pk, as returned by a search tool. |
| `language` | string | no | Site language code (2 letters, e.g. "en", "fr"). Default "en". |

## `get_quotation`

**Get a reproduction price quotation**

Price quotation for a reproduction of an artwork, as an art print or a hand-painted oil painting, at a given size and in a given currency. Leave type out to get BOTH in one call: the result then holds "quotations" (one full quotation per type the artwork sells, each with its own price, buy_url and offer_text) and "types_not_available". Every quotation carries offer_text, one ready-to-paste line (type, size, frame, price, order link): give it to the user as is, translating its words if needed but never changing its numbers or link. Optional frame_code adds the frame price to quotation_price ("WhiteWrap" = stretched on stretcher bars, "default" = a decorative frame chosen for the artwork, or a catalog code); optional senior_artist (oil painting only) adds the "Elite Senior Artist" upgrade — more detail and finesse, extra production time — to quotation_price. Identify the artwork by pk, or by title and/or artist_name (an exact title match wins; otherwise the first good-confidence search match is used, and its relevance is returned in "score"). A fuzzy match can be a different painting than the one asked for: when the result carries a "warning", verify the returned title before using the price, as the warning instructs. width/height need not match the artwork's own proportions: when its aspect ratio is known, the quoted size is snapped to that ratio while keeping the same surface area (width x height) you requested, so the reproduction is never stretched or distorted; the actual quoted size is returned as width_cm/height_cm (vs. your original requested_width_cm/requested_height_cm), with size_ratio_adjusted set to true when this happened. Give only width OR only height (e.g. "25 cm high", "smallest side 25 cm") to keep that side exactly: the other side is then derived from the artwork's aspect ratio and size_derived_from names the side you gave (fails with invalid_size when the ratio is unknown - then give both). Each side must be 25-250 cm (about 10-98 inches): a size outside that range is NOT refused but quoted at the nearest valid size with the same proportions, with size_adjusted_to_minimum / size_adjusted_to_maximum set to true; whenever the quoted size differs from the request, size_note says in one sentence what changed and why - repeat it to the user. invalid_size only comes back when no size of these proportions can fit the range. Returns pk, artist_name, title, meta_description, quotation_price, currency, frame_code (+ frame_description, frame_delivery), url (catalog page) and buy_url. buy_url is a ready-to-open, fully-parameterised buy form: reproduction medium, size and frame are all set from the query string, so the page opens showing exactly quotation_price. Give it to the user as the link to order the artwork at the quoted configuration. When the artwork ITSELF is for sale right now (a ready-made oil painting in stock, an open auction lot, an original, a studio collectible), the result also carries available_now (offers with price, stock quantity and offer_text, plus a note): tell the customer about the real object in the same answer — a quotation is a copy made to order. An artwork sold only as such an object answers with quotations empty and available_now set, not with channel_not_available.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `pk` | integer | no | Artwork pk (from a search tool). |
| `title` | string | no | Artwork title (used when pk is not given). |
| `artist_name` | string | no | Artist name (used when pk is not given). |
| `type` | string | no | Reproduction type: "print" (art print) or "oil painting" (hand-painted). Omit to quote both at once. Allowed values: print, oil painting. |
| `width` | number | no | Width in the given unit. Omit to derive it from height. |
| `height` | number | no | Height in the given unit. Omit to derive it from width. |
| `unit` | string | yes | Unit of width/height. Allowed values: inches, cm. |
| `currency` | string | yes | ISO currency code, e.g. "USD", "EUR", "GBP". |
| `frame_code` | string | no | Optional frame; when set, quotation_price includes it. Omit it (or "NoFrame") for the canvas rolled in a tube. "WhiteWrap" = the canvas stretched on wooden stretcher bars, white edges, no outer frame (use it for any request for a stretcher, stretcher bars, a stretched canvas or a canvas ready to hang without a frame); "BlurSideWrap" / "ExtendedWrap" = the same with the image blurred / continued around the edges. "default" = a decorative outer frame chosen for you (the frame recommended for the artwork when it has one, else our best-selling frame) — use it to quote a framed option without knowing the catalog. Any other catalog code (e.g. "P118B", "P919G", "W316G", "H24-GOLD-Portrait") is that specific decorative frame. The result then carries frame_description, frame_delivery (assembled, or a disassembled kit over 105 cm) and, for "default", frame_chosen_by. buy_url prefills the frame. |
| `senior_artist` | boolean | no | Oil painting only: have an Elite Senior Artist paint it (more detail, finesse and extra production time). When true, quotation_price includes the upgrade and buy_url pre-selects it. |
| `language` | string | no | Site language code (2 letters, e.g. "en", "fr"). Default "en". |

## `get_custom_reproduction_quotation`

**Get a custom reproduction price quotation (no catalog artwork needed)**

Price quotation for a CUSTOM reproduction — one made from an image the customer supplies (their own photo, or an artwork that is not in the catalog) — as an art print or a hand-painted oil painting. No artwork identification is needed or accepted: the price depends only on the size, the reproduction type and the currency. Use this whenever the artwork cannot be found in the catalog (the search tools return nothing relevant, or get_quotation fails with artwork_not_found), or the customer wants their own picture reproduced. Optional frame_code ("WhiteWrap" = stretched on stretcher bars, "default" = a decorative frame chosen for you, or a catalog code) adds the frame price to quotation_price; optional senior_artist (oil painting only) adds the "Elite Senior Artist" upgrade — more detail and finesse, extra production time. Each side must be 25-250 cm (about 10-98 inches). Returns quotation_price (the base price: options chosen on the order form, like varnish or urgent delivery, cost extra — see "notes"), currency, frame_code (+ frame_description, frame_delivery), width_cm/height_cm, notes, and order_page_url — the page where the customer uploads their image and orders the reproduction. Give order_page_url to the user as the link to place this order. For a hand-painted portrait the price covers up to 3 faces; the per-extra-face surcharge is stated in notes.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `type` | string | yes | Reproduction type: "print" (art print) or "oil painting" (hand-painted). Allowed values: print, oil painting. |
| `width` | number | no | Width in the given unit. |
| `height` | number | no | Height in the given unit. |
| `unit` | string | yes | Unit of width/height. Allowed values: inches, cm. |
| `currency` | string | yes | ISO currency code, e.g. "USD", "EUR", "GBP". |
| `frame_code` | string | no | Optional frame; when set, quotation_price includes it. Omit it (or "NoFrame") for the canvas rolled in a tube. "WhiteWrap" = the canvas stretched on wooden stretcher bars, white edges, no outer frame (use it for any request for a stretcher, stretcher bars, a stretched canvas or a canvas ready to hang without a frame); "BlurSideWrap" / "ExtendedWrap" = the same with the image blurred / continued around the edges. "default" = a decorative outer frame chosen for you (the frame recommended for the artwork when it has one, else our best-selling frame) — use it to quote a framed option without knowing the catalog. Any other catalog code (e.g. "P118B", "P919G", "W316G", "H24-GOLD-Portrait") is that specific decorative frame. The result then carries frame_description, frame_delivery (assembled, or a disassembled kit over 105 cm) and, for "default", frame_chosen_by. The customer selects that frame on the order form (notes says which). |
| `senior_artist` | boolean | no | Oil painting only: have an Elite Senior Artist paint it (more detail, finesse and extra production time). When true, quotation_price includes the upgrade; the customer selects the option on the order form. |
| `language` | string | no | Site language code (2 letters, e.g. "en", "fr"). Default "en". |

## `get_artwork_availability`

**Is this artwork available now, and at what price (stock, auction, originals, collectibles)**

Every way to buy ONE artwork right now, on every sales channel it sells: the physical objects first — a ready-made oil painting in stock ("Stock Discount Oil Painting", a real canvas that ships within 48 hours), an auction lot (current bid, minimum next bid, closing time), an original sold by its owner, a studio collectible — each with available_now, stock_quantity, price (fixed, shipping included) in your currency, size, buy_url and offer_text (one ready-to-paste line: give it to the customer as is, numbers and link untouched); then the made-to-order channels (hand-painted oil reproduction, art print: price by size through get_quotation) and the digital image licence. available_now is true only when the artwork ITSELF can be bought or bid on today; available_now_summary says it in one sentence. Call it whenever a customer asks whether something is available, in stock, ready to ship, discounted, on auction, or what it costs as a real object — and before any "yes, it is available". Identify the artwork by pk, or by title and/or artist_name (exact title first, then a surname-guarded search whose relevance comes back in "score"; a "warning" means check the returned title). Without pk or title, give channel to LIST the objects of that channel for sale now (cheapest first; optional artist_name, query words from the title, max_price in your currency, limit 1-10): "what do you have in stock under 200 euros?", "which auctions are open?". Prices follow the strict no-fallback currency rule of the quotation tools.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `pk` | integer | no | Artwork pk (from a search tool or the page). |
| `title` | string | no | Artwork title (used when pk is not given). |
| `artist_name` | string | no | Artist name: with title/pk it identifies the artwork; in the list mode it filters the objects by artist. |
| `channel` | string | no | List mode (no pk, no title): which physical channel to list — PaintingReady (ready-made oil paintings in stock), ProductAuction (auction lots), SellerProduct (originals sold by their owner), FactoryProduct (studio collectibles). With pk/title it narrows the offers to that channel. Allowed values: ProductAuction, SellerProduct, FactoryProduct, PaintingReady. |
| `query` | string | no | List mode: words from the title (e.g. "flowers", "sunset"). |
| `max_price` | number | no | List mode: highest price, in the given currency. |
| `limit` | integer | no | List mode: how many objects (default 10). |
| `currency` | string | yes | ISO currency code, e.g. "USD", "EUR", "GBP". |
| `language` | string | no | Site language code (2 letters, e.g. "en", "fr"). Default "en". |
