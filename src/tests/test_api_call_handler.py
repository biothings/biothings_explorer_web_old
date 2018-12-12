import unittest

from .context import BioThingsExplorer

ah = BioThingsExplorer().apiCallHandler


class TestFunctionsInAPICallHandler(unittest.TestCase):

    def test_check_if_exists_multiple_params(self):
        # test if raise keyerror when given an invalid endpoint name
        #self.assertRaises(KeyError,
                          #ah.check_if_exists_multiple_params(1))
        #self.assertRaises(KeyError,
                          #ah.check_if_exists_multiple_params('1'))
        #self.assertRaises(KeyError,
        #                  ah.check_if_exists_multiple_params('http://mygene.info/'))
        with self.assertRaises(KeyError):
            ah.check_if_exists_multiple_params(1)
        self.assertFalse(ah.check_if_exists_multiple_params('http://mygene.info/v3/querypathway'))
        self.assertFalse(ah.check_if_exists_multiple_params('http://mygene.info/v3/querygo'))


if __name__ == "__main__":
    unittest.main()
