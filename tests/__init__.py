import datetime
import glob
import unittest

import openvpn_status_parser
import openvpn_status_parser.exceptions


class TestBroken(unittest.TestCase):
    def _test_file(self, filename):
        parsed = openvpn_status_parser.OpenVPNStatusParser(filename)

        def _call_details():
            parsed.details  # pylint: disable=pointless-statement

        self.assertRaises(openvpn_status_parser.exceptions.MalformedFileException, _call_details)


def ch(filename):
    return lambda self: self._test_file(filename)  # pylint: disable=protected-access


for fn in glob.glob("tests/testfiles/broken/*.status"):
    print(f"Adding {fn}")
    test_func_name = fn.replace(".", "_")
    setattr(TestBroken, f"test_{test_func_name}", ch(fn))

if __name__ == '__main__':
    unittest.main()