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

Or using Python:

::

  import pprint
  from openvpn_status_parser import OpenVPNStatusParser

  parser = OpenVPNStatusParser("/var/run/openvpn/openvpn.status")
  pprint.pprint(parser.connected_clients)
  pprint.pprint(parser.routing_table)
  pprint.pprint(parser.details)

License
-------

MIT License; see LICENSE.txt for full details.