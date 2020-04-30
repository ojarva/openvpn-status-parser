openvpn-status-parser
=====================

Installation:

::

  pip install openvpn-status-parser

or clone `the repository <https://github.com/ojarva/openvpn-status-parser>`_ and run

::

  python setup.py install

Usage:

- add `status-version 3` to openvpn server configuration. Reload/restart openvpn server.
- locate openvpn status file. Usually it's under /var/run in Unix based systems.

::

  openvpn-status-parser /var/run/openvpn/openvpn.status
  openvpn-status-parser /var/run/openvpn/openvpn.status --json

Or using Python:

::

  import pprint
  from openvpn_status_parser import OpenVPNStatusParser

  parser = OpenVPNStatusParser("/var/run/openvpn/openvpn.status")
  pprint.pprint(parser.connected_clients)
  pprint.pprint(parser.routing_table)
  pprint.pprint(parser.details)


MIT License:

Copyright (C) 2012-2016, Olli Jarva \<olli@jarva.fi\>

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
