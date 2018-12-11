import unittest
import sys

from .context import BioThingsExplorer


class TestFunctionsInAPICallHandler(unittest.TestCase):
	def __init__(self):
		self.ah = BioThingsExplorer().apiCallHandler

	def test_endpoint_locator(self):
		self.assertEqual(len(self.ah.api_endpoint_locator("wrong", "wrong"), 0))

if __name__ == "__main__":
    unittest.main()