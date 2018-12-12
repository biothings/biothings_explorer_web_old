import unittest

from .context import BioThingsExplorer

ah = BioThingsExplorer().apiCallHandler


class TestFunctionsInAPICallHandler(unittest.TestCase):

    def test_check_if_exists_multiple_params(self):
        # test invalid endpoint, 1 is integer
        with self.assertRaises(KeyError):
            ah.check_if_exists_multiple_params(1)
        # test invalid endpoint, '1' is string
        with self.assertRaises(KeyError):
            ah.check_if_exists_multiple_params('1')
        # test invalid endpoint, 'mygene.info' is API name, not endpoint
        with self.assertRaises(KeyError):
            ah.check_if_exists_multiple_params('http://mygene.info/')
        self.assertFalse(ah.check_if_exists_multiple_params('http://mygene.info/v3/querypathway'))
        self.assertFalse(ah.check_if_exists_multiple_params('http://mygene.info/v3/querygo'))


if __name__ == "__main__":
    unittest.main()
