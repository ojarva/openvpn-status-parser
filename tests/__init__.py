import glob
import unittest
import datetime

import openvpn_status_parser
import openvpn_status_parser.exceptions


class TestBroken(unittest.TestCase):
    def _test_file(self, filename):
        parsed = openvpn_status_parser.OpenVPNStatusParser(filename)

        def _call_details():
            parsed.details

        self.assertRaises(openvpn_status_parser.exceptions.MalformedFileException, _call_details)


def ch(filename):
    return lambda self: self._test_file(filename)

for filename in glob.glob("tests/testfiles/broken/*.status"):
    print("Adding %s" % filename)
    setattr(TestBroken, "test_%s" % filename.replace(".", "_"), ch(filename))

if __name__ == '__main__':
    unittest.main()
