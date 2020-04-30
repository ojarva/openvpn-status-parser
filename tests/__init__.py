import glob
import unittest
import datetime
import json

import openvpn_status_parser
import openvpn_status_parser.exceptions


class TestBroken(unittest.TestCase):
    def _test_file(self, filename, broken = True):
        parsed = openvpn_status_parser.OpenVPNStatusParser(filename)

        def _call_details():
            parsed.details

        if broken:
            self.assertRaises(openvpn_status_parser.exceptions.MalformedFileException, _call_details)
        else:
            json.loads(parsed.json)


def ch(filename, broken = True):
    return lambda self: self._test_file(filename, broken)

for filename in glob.glob("tests/testfiles/valid/*.status"):
    print("Adding %s" % filename)
    setattr(TestBroken, "test_%s" % filename.replace(".", "_"), ch(filename, False))

if __name__ == '__main__':
    unittest.main()
