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
        # TODO: add example when assertTrue

    def test_preprocessing_input(self):
        # test a string input with no prefix
        self.assertEqual(ah.preprocessing_input('1017',
                         'http://mygene.info/v3/querygene'), ['1017'])
        # test a string input with prefix
        self.assertEqual(ah.preprocessing_input('ncibgene:1017',
                         'http://mygene.info/v3/querygene'), ['1017'])
        # test a string input with prefix
        self.assertEqual(ah.preprocessing_input('gene:ncibgene:1017',
                         'http://mygene.info/v3/querygene'), ['1017'])
        # test a list of string input with no prefix
        self.assertEqual(ah.preprocessing_input(['1017', '1018', '1111'],
                         'http://mygene.info/v3/querygene'),
                         ['1017', '1018', '1111'])
        # test a list of string input with prefix
        self.assertEqual(ah.preprocessing_input(['ncibigene:1017',
                                                 'ncibigene:1018',
                                                 'ncbigene:1111'],
                         'http://mygene.info/v3/querygene'),
                         ['1017', '1018', '1111'])
        # test a list of string input with mix of prefix or no prefix
        self.assertEqual(ah.preprocessing_input(['1017',
                                                 'ncibigene:1018',
                                                 'ncbigene:1111'],
                         'http://mygene.info/v3/querygene'),
                         ['1017', '1018', '1111'])
        # test invalid input, integer
        with self.assertRaises(TypeError):
            ah.preprocessing_input(1017, 'http://mygene.info/v3/querygene')
        # test invalid input, dict
        with self.assertRaises(TypeError):
            ah.preprocessing_input({'k': 'v'},
                                   'http://mygene.info/v3/querygene')
        # test invalid input, list of integer
        with self.assertRaises(TypeError):
            ah.preprocessing_input([1111, 12323],
                                   'http://mygene.info/v3/querygene')
        # test invalid input, list of mixed type
        with self.assertRaises(TypeError):
            ah.preprocessing_input([1111, '12323'],
                                   'http://mygene.info/v3/querygene')

    def test_preprocess_json_doc(self):
        # check if input is a list
        json_doc = ['a', 'b', 'c']
        self.assertEqual(ah.preprocess_json_doc(json_doc), {'data': json_doc})
        # check if input is a dict with integers
        json_doc = {'a': 1}
        self.assertEqual(ah.preprocess_json_doc(json_doc), {'a': '1'})
        # check if input is a dict without integers
        json_doc = {'a': '1'}
        self.assertEqual(ah.preprocess_json_doc(json_doc), json_doc)
        # check if input is not dict or list
        json_doc = 1
        with self.assertRaises(TypeError):
            ah.preprocess_json_doc(json_doc)
        # check if input is a string
        json_doc = 'string'
        with self.assertRaises(TypeError):
            ah.preprocess_json_doc(json_doc)


if __name__ == "__main__":
    unittest.main()
