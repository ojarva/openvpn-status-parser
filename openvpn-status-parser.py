""" This is a parser for openvpn status files, version 3.

How to use:

- add "status-version 3" to openvpn server configuration. Reload/restart openvpn server.
- locate openvpn status file. Usually it's under /var/run in Unix based systems.
- Run "python openvpn-status-parser.py <filename>" for demo. Sample file with random data
  is included in the repository, try it with "python openvpn-status-parser.py".

MIT License:

Copyright (C) 2012, Olli Jarva <olli.jarva@futurice.com>

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

"""

import pprint
import csv
import datetime
import logging
import sys

class OpenVPNStatusParser:
    def __init__(self, filename):
        self.filename = filename
        self._connected_clients = None
        self._routing_table = None
        self._details = None

    def _parse_file(self):
        self._details = {}
        self._connected_clients = {}
        self._routing_table = {}
        topics_for = {}
        csvreader = csv.reader(open(self.filename), delimiter='\t')
        for row in csvreader:
            row_title = row[0]
            if row_title == "TITLE":
                try:
                    self._details["title"] = row[1]
                except IndexError:
                    logging.error("TITLE row is invalid: %s" % row)

            elif row_title == "TIME":
                try:
                    self._details["timestamp"] = datetime.datetime.fromtimestamp(int(row[2]))
                except (IndexError, ValueError):
                    logging.error("TIME row is invalid: %s" % row)

            elif row_title == "HEADER":
                try:
                    topics_for[row[1]] = row[2:]
                except IndexError:
                    logging.error("HEADER row is invalid: %s" % row)

            elif row_title == "CLIENT_LIST":
                try:
                    self._connected_clients[row[1]] = dict(zip(topics_for["CLIENT_LIST"], row[1:]))
                    self._connected_clients[row[1]]["connected_since"] = datetime.datetime.fromtimestamp(int(row[-1]))
                except IndexError:
                    logging.error("CLIENT_LIST row is invalid: %s" % row)

            elif row_title == "ROUTING_TABLE":
                try:
                    self._routing_table[row[2]] = dict(zip(topics_for["ROUTING_TABLE"], row[1:]))
                    self._routing_table[row[2]]["last_ref"] = datetime.datetime.fromtimestamp(int(row[-1]))
                except IndexError:
                    logging.error("ROUTING_TABLE row is invalid: %s" % row)

            elif row_title == "GLOBAL_STATS":
                try:
                    self._details[row[1]] = row[2]
                except IndexError:
                    logging.error("GLOBAL_STATS row is invalid: %s" % row)

            elif row_title == "END":
                return True

            else:
                logging.warning("Line was not parsed. Keyword %s not recognized. %s" % (row_title, row))
        logging.error("File was incomplete. END line was missing.")
        return False

    @property
    def details(self):
        """ Returns miscellaneous details from status file """
        if not self._details:
            self._parse_file()
        return self._details

    @property
    def connected_clients(self):
        """ Returns dictionary of connected clients with details."""
        if not self._connected_clients:
            self._parse_file()
        return self._connected_clients

    @property
    def routing_table(self):
        """ Returns dictionary of routing_table used by OpenVPN """
        if not self._routing_table:
            self._parse_file()
        return self._routing_table


def main():
    if len(sys.argv) == 1:
        files = ["sample-file"]
    else:
        files = sys.argv[1:]

    for file in files:
        parser = OpenVPNStatusParser(file)
        print "="*79
        print file
        print "-"*79
        print "Connected clients"
        pprint.pprint(parser.connected_clients)
        print "-"*79
        print "Routing table"
        pprint.pprint(parser.routing_table)
        print "-"*79
        print "Additional details"
        pprint.pprint(parser.details)

if __name__ == '__main__':
    main()
