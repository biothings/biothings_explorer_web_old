import unittest

from .context import BioThingsExplorer

registry = BioThingsExplorer().registry


class TestFunctionsInAPIRegistryParser(unittest.TestCase):

    def test_prefix2uri(self):
        """Test for prefix2uri function
        """
        # given a correct input, return correct result
        self.assertEqual(registry.prefix2uri('ncbigene'),
                         'http://identifiers.org/ncbigene/')
        self.assertEqual(registry.prefix2uri('hgnc.symbol'),
                         'http://identifiers.org/hgnc.symbol/')
        # given a invalid input, return None
        self.assertIsNone(registry.prefix2uri('nc'))

    def test_prefix2semantictype(self):
        """Test for prefix2semantictype function
        """
        # given a correct input, return correct result
        self.assertEqual(registry.prefix2semantictype('ncbigene'), 'gene')
        self.assertEqual(registry.prefix2semantictype('chembl.compound'),
                         'chemical')
        self.assertEqual(registry.prefix2semantictype('mondo'), 'disease')
        # given an invalid input, return None
        self.assertIsNone(registry.prefix2semantictype('mm'))

    def test_semantictype2prefix(self):
        """Test for semantictype2prefix function
        """
        # given a correct input, return correct result
        self.assertIn('ncbigene', list(registry.semantictype2prefix('gene')))
        self.assertIn('mondo', list(registry.semantictype2prefix('disease')))
        self.assertNotIn('chembl.compound',
                         list(registry.semantictype2prefix('anatomy')))
        self.assertNotIn('chembl',
                         list(registry.semantictype2prefix('anatomy')))
        # given an invalid input, return None
        self.assertEqual(list(registry.semantictype2prefix('dd')), [])


if __name__ == "__main__":
    unittest.main()
