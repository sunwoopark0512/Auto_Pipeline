import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from keyword_auto_pipeline import select_top_keywords

class TestSelectTopKeywords(unittest.TestCase):
    def test_select_top_keywords(self):
        sample = [
            {'keyword': 'A', 'cpc': 1500},
            {'keyword': 'B', 'cpc': 2000},
            {'keyword': 'A', 'cpc': 1800},  # duplicate with higher CPC
            {'keyword': 'C', 'cpc': 500},
        ]
        result = select_top_keywords(sample, top_n=2)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['keyword'], 'B')
        self.assertEqual(result[1]['keyword'], 'A')
