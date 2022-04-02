import unittest

from src.open_s3.helper import human_readable_to_byte


class TestHumanReadableToByte(unittest.TestCase):
    def test_simple_cases(self):
        self.assertEqual(human_readable_to_byte("1KB"), 1024)
        self.assertEqual(human_readable_to_byte("2KB"), 2048)

    def test_fractions(self):
        self.assertEqual(human_readable_to_byte("0.5KB"), 512)
        self.assertEqual(human_readable_to_byte("20.5KB"), 1024 * 20 + 512)

    def test_formating(self):
        self.assertEqual(human_readable_to_byte(" 1MB"), 1024 * 1024)
        self.assertEqual(human_readable_to_byte(" 2  MB"), 1024 * 1024 * 2)
        self.assertEqual(human_readable_to_byte("    4   MB "), 1024 * 1024 * 4)
        self.assertEqual(human_readable_to_byte("8MB    "), 1024 * 1024 * 8)
        self.assertEqual(human_readable_to_byte(" 1.5   MB  "), 1024 * 1024 * 1.5)

    def test_casing(self):
        self.assertEqual(human_readable_to_byte("0.5GB"), 0.5 * 1024 * 1024 * 1024)
        self.assertEqual(human_readable_to_byte("0.5gB"), 0.5 * 1024 * 1024 * 1024)
        self.assertEqual(human_readable_to_byte("0.5Gb"), 0.5 * 1024 * 1024 * 1024)
        self.assertEqual(human_readable_to_byte("0.5gb"), 0.5 * 1024 * 1024 * 1024)
