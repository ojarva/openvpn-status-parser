import datetime
import glob
import json
import os
import re
import unittest

import openvpn_status_parser
import openvpn_status_parser.exceptions


class Encoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()


def Decoder(d):
    for f in ['connected_since', 'last_ref', 'timestamp']:
        if f in d:
            d[f] = datetime.datetime.strptime(d[f], "%Y-%m-%dT%H:%M:%S")
    return d


class TestValid(unittest.TestCase):

    def _test_file(self, filename):
        parsed = openvpn_status_parser.OpenVPNStatusParser(filename)

        self._test_expectation(
            filename, '.connected_clients', parsed.connected_clients)
        self._test_expectation(
            filename, '.routing_table', parsed.routing_table)
        self._test_expectation(
            filename, '.details', parsed.details)

    def _test_expectation(self, filename, expected_extension, result):
        expected_filename = re.sub('\.status$', expected_extension, filename)
        print('checking against %s' % expected_filename)
        if not os.path.exists(expected_filename):
            print('Missing expected file %r:\n%s' % (
                expected_filename, json.dumps(
                    result, cls=Encoder, indent=4, sort_keys=True)))
            raise Exception('Missing expected file %r' % expected_filename)
        with open(expected_filename, 'r') as f:
            expected = json.loads(f.read(), object_hook=Decoder)
            self.assertDictEqual(expected, result)


class TestBroken(unittest.TestCase):

    def _test_file(self, filename):
        parsed = openvpn_status_parser.OpenVPNStatusParser(filename)

        def _call_details():
            parsed.details  # pylint: disable=pointless-statement

        self.assertRaises(openvpn_status_parser.exceptions.MalformedFileException, _call_details)


def ch(filename):
    return lambda self: self._test_file(filename)  # pylint: disable=protected-access


for fn in glob.glob("tests/testfiles/valid/*.status"):
    print(f"Adding {fn}")
    test_func_name = fn.replace(".", "_")
    setattr(TestValid, f"test_{test_func_name}", ch(fn))
for fn in glob.glob("tests/testfiles/broken/*.status"):
    print(f"Adding {fn}")
    test_func_name = fn.replace(".", "_")
    setattr(TestBroken, f"test_{test_func_name}", ch(fn))


if __name__ == '__main__':
    unittest.main()
