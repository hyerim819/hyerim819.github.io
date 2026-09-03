import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from sync_tistory import parse_feed, render_post  # noqa: E402


RSS = b"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><item>
  <title><![CDATA[RSS &amp; test]]></title>
  <link>https://sample.tistory.com/42</link>
  <description><![CDATA[<h2>Hello</h2><p>World</p><script>alert(1)</script>]]></description>
  <category><![CDATA[Security]]></category>
  <guid>https://sample.tistory.com/42</guid>
  <pubDate>Thu, 03 Sep 2026 10:00:00 +0900</pubDate>
</item></channel></rss>"""


class TistorySyncTests(unittest.TestCase):
    def test_accepts_empty_tistory_feed(self):
        empty_feed = b'<rss version="2.0"><channel><title>p1ki</title></channel></rss>'
        self.assertEqual(parse_feed(empty_feed), [])

    def test_parses_tistory_rss(self):
        entry = parse_feed(RSS)[0]
        self.assertEqual(entry.entry_id, "42")
        self.assertEqual(entry.title, "RSS & test")
        self.assertEqual(entry.category, "Security")

    def test_renders_safe_jekyll_post(self):
        post = render_post(parse_feed(RSS)[0], "티스토리")
        self.assertIn('categories: ["티스토리", "Security"]', post)
        self.assertIn('canonical_url: "https://sample.tistory.com/42"', post)
        self.assertIn("{% raw %}", post)
        self.assertNotIn("alert(1)", post)


if __name__ == "__main__":
    unittest.main()
