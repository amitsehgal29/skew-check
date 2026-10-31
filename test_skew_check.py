import unittest
from skew_check import skew

def rows(keys):
    return [{"k": k} for k in keys]

class T(unittest.TestCase):
    def test_hot_key(self):
        r = skew(rows(["a"] * 8 + ["b", "c"]), "k")
        self.assertEqual(r["hot_keys"], ["a"])
        self.assertEqual(r["top"][0]["share"], 0.8)
        self.assertEqual(r["max_to_mean"], 2.4)
    def test_even(self):
        r = skew(rows(list("abcdefghij")), "k")
        self.assertEqual(r["hot_keys"], [])
        self.assertEqual(r["max_to_mean"], 1.0)
    def test_empty_and_missing(self):
        self.assertEqual(skew([], "k")["rows"], 0)
        with self.assertRaises(KeyError):
            skew([{"x": 1}], "k")

if __name__ == "__main__":
    unittest.main()
