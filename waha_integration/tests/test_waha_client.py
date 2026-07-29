import unittest
from waha_integration.waha_client import format_chat_id, WahaService

class TestWahaClient(unittest.TestCase):
    def test_format_chat_id(self):
        self.assertEqual(format_chat_id("+1234567890"), "1234567890@c.us")
        self.assertEqual(format_chat_id("1234567890@c.us"), "1234567890@c.us")
        self.assertEqual(format_chat_id("1234567890@g.us"), "1234567890@g.us")
        self.assertEqual(format_chat_id("  +44 7700 900077 "), "447700900077@c.us")

    def test_service_init(self):
        service = WahaService("http://localhost:3000", api_key="secret")
        self.assertEqual(service.base_url, "http://localhost:3000")
        self.assertEqual(service.api_key, "secret")


if __name__ == "__main__":
    unittest.main()
