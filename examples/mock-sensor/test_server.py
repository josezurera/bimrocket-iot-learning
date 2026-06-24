import unittest

from server import build_reading


class BuildReadingTest(unittest.TestCase):
    def test_contains_expected_fields(self):
        reading = build_reading(0)

        self.assertEqual(reading["room"], "A-101")
        self.assertEqual(reading["status"], "online")
        self.assertIn("ifcGlobalId", reading)
        self.assertIsInstance(reading["temperature"], float)
        self.assertIsInstance(reading["co2"], int)

    def test_can_simulate_offline_sensor(self):
        reading = build_reading(0, offline=True)

        self.assertEqual(reading["status"], "offline")


if __name__ == "__main__":
    unittest.main()

