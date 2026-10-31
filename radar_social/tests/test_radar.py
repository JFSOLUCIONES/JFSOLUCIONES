import unittest
from radar_social.radar import parse_feed, public_https_url

RSS = b"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0"><channel><title>Prensa</title>
<item><title>Contraloria revisa contrato municipal</title>
<link>https://example.org/noticias/123</link>
<description>Autoridades evaluan licitacion</description><pubDate>Sat, 31 Oct 2026 12:00:00 GMT</pubDate></item>
</channel></rss>"""

class RadarTests(unittest.TestCase):
    def test_private_urls_rejected(self):
        for url in ["http://example.org/feed", "https://127.0.0.1/", "https://169.254.169.254/latest", "https://localhost/feed"]:
            self.assertFalse(public_https_url(url), url)
    def test_classification_no_auto_publish(self):
        data = parse_feed(RSS, {"name":"Ejemplo", "platform":"web", "region":"Lambayeque"})
        self.assertEqual(len(data), 1)
        self.assertIn("fiscalizacion", data[0]["topics"])
        self.assertEqual(data[0]["status"], "PENDIENTE_VERIFICACION")
        self.assertFalse(data[0]["approved"])
        self.assertFalse(data[0]["autopublish"])
    def test_invalid_xml_rejected(self):
        with self.assertRaises(Exception):
            parse_feed(b"<bad", {"name":"Ejemplo", "platform":"web"})
if __name__ == "__main__":
    unittest.main()
