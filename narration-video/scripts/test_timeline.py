"""Run with python3 scripts/test_timeline.py."""
import copy
import unittest
from timeline import validate, srt, stamp


class TimingTests(unittest.TestCase):
    def setUp(self):
        self.data = {"version": 1, "duration": 10,
                     "cues": [{"time": 0, "page": "p1", "visible": []},
                              {"time": 5, "page": "p1", "visible": ["card"]}],
                     "subtitles": [{"start": 1, "end": 2, "text": "这是 Tool"},
                                   {"start": 2, "end": 3, "text": "下一句\n第二行"}]}

    def test_valid_srt(self):
        self.assertEqual(srt(self.data), "1\n00:00:01,000 --> 00:00:02,000\n这是 Tool\n\n2\n00:00:02,000 --> 00:00:03,000\n下一句\n第二行\n\n")

    def test_timestamp_carry(self):
        self.assertEqual(stamp(3599.9996), "01:00:00,000")

    def test_invalid_times(self):
        for start, end in [(-1, 2), (2, 2), (3, 2), (1, 11), (float('nan'), 2), (True, 2), (1.0001, 1.0002)]:
            with self.subTest(start=start, end=end):
                data = copy.deepcopy(self.data)
                data['subtitles'][0].update(start=start, end=end)
                with self.assertRaises(ValueError):
                    validate(data)

    def test_overlap(self):
        self.data['subtitles'][1]['start'] = 1.9
        with self.assertRaises(ValueError):
            validate(self.data)

    def test_bad_cues(self):
        for t in [0, -1, 10, float('inf')]:
            self.data['cues'][1]['time'] = t
            with self.assertRaises(ValueError):
                validate(self.data)

    def test_blank_text(self):
        for text in ['', ' ', 'a\n\nb', 'a\r\nb']:
            self.data['subtitles'][0]['text'] = text
            with self.assertRaises(ValueError):
                validate(self.data)

    def test_missing_zero(self):
        self.data['cues'][0]['time'] = .2
        with self.assertRaises(ValueError):
            validate(self.data)


if __name__ == '__main__':
    unittest.main()
