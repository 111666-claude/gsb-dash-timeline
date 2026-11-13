import unittest

from dash_timeline import expand_timeline


class TimelineTests(unittest.TestCase):
    def test_expands_fixed_repeat(self):
        result = expand_timeline({"timescale": 1000, "segments": [{"t": 0, "d": 2000, "r": 2}]})
        self.assertEqual(len(result["segments"]), 3)
        self.assertEqual(result["segments"][1]["start_ms"], 2000)

    def test_empty(self):
        self.assertEqual(expand_timeline({})["segments"], [])


if __name__ == "__main__":
    unittest.main()
