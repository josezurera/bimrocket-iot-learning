import unittest

from server import ROOMS, build_reading


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

    def test_can_build_reading_for_each_known_room(self):
        for room in ROOMS:
            with self.subTest(room=room):
                reading = build_reading(0, room=room)

                self.assertEqual(reading["room"], room)
                self.assertEqual(reading["ifcGlobalId"], ROOMS[room]["ifcGlobalId"])

    def test_rooms_have_different_simulated_values(self):
        a101 = build_reading(0, room="A-101")
        a102 = build_reading(0, room="A-102")

        self.assertNotEqual(a101["ifcGlobalId"], a102["ifcGlobalId"])
        self.assertNotEqual(a101["co2"], a102["co2"])


if __name__ == "__main__":
    unittest.main()

