from .utils import readFile
from .config import FILE_PATHS
from .api_registry_parser import RegistryParser


class OutputOrganizor:
    def __init__(self):
        self.attribute_mapping_path = FILE_PATHS['attribute_mapping']['file']
        self.attribute_dict = {}
        self.attribute_dict = self.read_attribute_mapping_file()
        self.registry = RegistryParser(readmethod='filepath', initialize=True)

    def uri2curie_helper(self, URI):
        """
        Given an URI, e.g. http://identifiers.org/ncbigene/1017
        Return it in CURIE format, e.g. NCBIGene:1017

        Return
        ======
        CURIE
        """
        _value = URI.split('/')[-1]
        _uri = URI[:len(URI)-len(_value)]
        if _uri in self.registry.bioentity_info:
            prefix = self.registry.bioentity_info[_uri]['preferred_name']
            return (prefix + ':' + _value)
        else:
            return _value

    def uri2curie(self, URIs):
        """
        Given a list of URIs, e.g. http://identifiers.org/ncbigene/1017
        Return them all in CURIE format, e.g. NCBIGene:1017

        Return
        ======
        CURIE
        """
        if type(URIs) == str:
            return self.uri2curie_helper(URIs)
        else:
            results = []
            for _uri in URIs:
                results.append(self.uri2curie_helper(_uri))
            if len(results) == 1:
                return results[0]
            else:
                return results

    def uri2value_helper(self, URI):
        """
        Given an URI, e.g. http://identifiers.org/ncbigene/1017
        extract the value from it, e.g. 1017

        Return
        ======
        value
        """
        return URI.split('/')[-1]
    
    def uri2value(self, URIs):
        """
        Given a list of URIs, e.g. http://identifiers.org/ncbigene/1017
        Return them all in value format, e.g. 1017

        Return
        ======
        values
        """
        if type(URIs) == str:
            return self.uri2value_helper(URIs)
        else:
            results = []
            for _uri in URIs:
                results.append(self.uri2value_helper(_uri))
            if len(results) == 1:
                return results[0]
            else:
                return results

    def read_attribute_mapping_file(self):
        """
        read in the ATTRIBUTE_LIST.csv file
        and parse it into dictionary
        The dictionary key is the URI, and it's value contains name and category
        """
        data = readFile(self.attribute_mapping_path)
        # turn data frame into a dictionary and store in bioentity_info
        for index, row in data.iterrows():
            self.attribute_dict[row['URI']] = {'name': row['NAME'], 'category': row['CATEGORY']}
        return self.attribute_dict

    def nquads2dict(self, properties):
        """
        This function converts nquads into a list of dictionary with specified format
        top level fields
        1) id (required)
        2) description
          a) secondary-id
          b) label
          c) taxonomy
        3) edge

        """
        reorganized_data = {'target': {}, 'edge': {}}
        for attribute_uri, _value in properties.items():
            attribute_label = self.attribute_dict[attribute_uri]['name']
            attribute_category = self.attribute_dict[attribute_uri]['category']
            # first handle cases where the property key is object.id
            if attribute_label == 'id' and attribute_category == 'object':
                reorganized_data['target']['id'] = self.uri2curie(_value)
            # then handle cases where the property key is object.secondary-ids
            elif attribute_label == 'secondary-id' and attribute_category == 'object':
                reorganized_data['target']['secondary-id'] = self.uri2curie(_value)
            # next handle cases where the property key belongs to 'object' category
            elif attribute_category == 'object':
                reorganized_data['target'][attribute_label] = self.uri2value(_value)
            elif attribute_category == 'edge':
                reorganized_data['edge'][attribute_label] = self.uri2value(_value)
            else:
                print('the data could not be parsed. attribute_uri is :{}, value is: {}'.format(attribute_uri, _value))
        return {k: v for k, v in reorganized_data.items() if v}

    def organize_synonym_output(self, outputs):
        outputs = [_output['output'][0]['target']['id'] for _output in outputs]
        return set(outputs)