import unittest
from config import Settings
from deidentify import perform_deidentification
from depseudonymize import perform_depseudonymization
from pseudonymize import perform_pseudonymization
from processor import process_data
from cli import deidentify, read_resource_from_file
import dateutil.parser as parser
from datetime import timedelta
import copy
import json


class TestConfig(unittest.TestCase):
    """
    Testing settings applied to FHIR resources
    """

    def test_read_settings(self):
        print(f"=========== TEST READ SETTINGS ===========")
        settings = Settings()
        self.assertIsNotNone(settings.rules)

    def test_read_lists(self):
        print(f"=========== TEST READ LIST ===========")
        config_filename = 'test/config/keep.yaml'
        resource_filename = 'test/fhir/patient_list.json'
        resource = read_resource_from_file(resource_filename)
        original_value = resource[0]['name']
        settings = Settings(config_filename)
        #ret = perform_deidentification(resource, settings)
        ret = process_data(resource, settings)
        self.assertEqual(ret[0]['name'], original_value)

    def test_keep(self):
        print(f"=========== TEST KEEP ===========")
        config_filename = 'test/config/keep.yaml'
        resource_filename = 'test/fhir/simple_patient.json'
        resource = read_resource_from_file(resource_filename)
        original_value = resource['name']
        settings = Settings(config_filename)
        #ret = perform_deidentification(resource, settings)
        ret = process_data(resource, settings)
        self.assertEqual(ret['name'], original_value)

    def test_deidentify_redact(self):
        print(f"========== TEST REDACT ==========")
        config_filename = 'test/config/redact.yaml'
        resource_filename = 'test/fhir/simple_patient.json'
        resource = read_resource_from_file(resource_filename)
        settings = Settings(config_filename)
        #ret = perform_deidentification(resource, settings)
        ret = process_data(resource, settings)
        self.assertRaises(KeyError, lambda: ret['name'])

    def test_deidentify_perturb(self):
        print(f"========== TEST PERTURB =========")
        config_filename = 'test/config/perturb.yaml'
        resource_filename = 'test/fhir/patient_R5DB.json'
        resource = read_resource_from_file(resource_filename)
        settings = Settings(config_filename)
        #ret = perform_deidentification(resource, settings)
        ret = process_data(resource, settings)
        # check if the perturbation is in the stated range
        perturbed_date = parser.parse(ret['birthDate'])
        ref_date = parser.parse('1974-12-25')
        min_date = ref_date - timedelta(days=5)
        max_date = ref_date + timedelta(days=10)
        self.assertTrue(perturbed_date <= max_date)
        self.assertTrue(perturbed_date >= min_date)

    def test_deidentify_cryptohash(self):
        print(f"======== TEST CRYPTOHASH ========")
        config_filename = 'test/config/cryptohash.yaml'
        resource_filename = 'test/fhir/simple_patient.json'
        resource = read_resource_from_file(resource_filename)
        settings = Settings(config_filename)
        #ret = perform_deidentification(resource, settings)
        ret = process_data(resource, settings)
        # what if the target is a list ? (e.g. patient['name']) ----> for each elem in the list compute the hash;
        #                                                             if the elem is a dict, converts it to a string and hash it
        self.assertEqual(
            ret['name'][0], 'b7340931fb4ee512d5d5f68f6da7a027c5ba8dd8a8d5ea4705416f0b85e1b9ca')
        self.assertEqual(
            ret['name'][1], '6f4bae1f49ee29890cbfcf8ffb26eccc2520cb543fa30a28458e2952f40b7ea3')
        self.assertEqual(
            ret['name'][2], 'dad3235c168df9f3ad295af27f18866e09c4c41009ca555c7706d90474c02626')

    def test_deidentify_substitute(self):
        print(f"======== TEST SUBSTITUTE ========")
        config_filename = 'test/config/substitute.yaml'
        resource_filename = 'test/fhir/simple_patient.json'
        resource = read_resource_from_file(resource_filename)
        settings = Settings(config_filename)
        #ret = perform_deidentification(resource, settings)
        ret = process_data(resource, settings)
        self.assertEqual(ret['name'][0]['family'], 'foo')
        self.assertEqual(ret['name'][2]['family'], 'foo')


if __name__ == '__main__':
    unittest.main()
