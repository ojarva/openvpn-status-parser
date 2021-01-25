""" This is a parser for openvpn status files, version 3.

MIT License:

Copyright (C) 2012-2016, Olli Jarva <olli.jarva@futurice.com>

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

import csv
import datetime
import logging
import sys

from . import exceptions


class OpenVPNStatusParser:
    """
    Usage:

    import pprint
    parser = OpenVPNStatusParser(filename)
    pprint.pprint(parser.connected_clients)
    """
    def __init__(self, filename):
        self.filename = filename
        self._connected_clients = None
        self._routing_table = None
        self._details = None
        self.topics_for = None
        self.title_processors = {
            "TITLE": self._process_title,
            "TIME": self._process_time,
            "HEADER": self._process_header,
            "CLIENT_LIST": self._process_client_list,
            "ROUTING_TABLE": self._process_routing_table,
            "GLOBAL_STATS": self._process_global_stats,
        }

    def _process_title(self, row):
        try:
            self._details["title"] = row[1]
        except IndexError as err:
            logging.error("TITLE row is invalid: %s", row)
            raise exceptions.MalformedFileException("TITLE row is invalid") from err

    def _process_time(self, row):
        try:
            self._details["timestamp"] = datetime.datetime.fromtimestamp(int(row[2]))
        except (IndexError, ValueError) as err:
            logging.error("TIME row is invalid: %s", row)
            raise exceptions.MalformedFileException("TIME row is invalid") from err

    def _process_header(self, row):
        try:
            self.topics_for[row[1]] = row[2:]
        except IndexError as err:
            logging.error("HEADER row is invalid: %s", row)
            raise exceptions.MalformedFileException("HEADER row is invalid") from err

    def _process_client_list(self, row):
        try:
            self._connected_clients[row[1]] = dict(zip(self.topics_for["CLIENT_LIST"], row[1:]))
            self._connected_clients[row[1]]["connected_since"] = (datetime.datetime.fromtimestamp(int(row[-1])))
        except IndexError as err:
            logging.error("CLIENT_LIST row is invalid: %s", row)
            raise exceptions.MalformedFileException("CLIENT_LIST row is invalid") from err
        except KeyError as err:
            raise exceptions.MalformedFileException("Topics for CLIENT_LIST are missing") from err

    def _process_routing_table(self, row):
        if len(row[1:]) != len(self.topics_for.get("ROUTING_TABLE", [])):
            raise exceptions.MalformedFileException("Invalid number of topics for ROUTING_TABLE row")
        try:
            self._routing_table[row[2]] = dict(zip(self.topics_for["ROUTING_TABLE"], row[1:]))
            self._routing_table[row[2]]["last_ref"] = datetime.datetime.fromtimestamp(int(row[-1]))
        except IndexError as err:
            logging.error("ROUTING_TABLE row is invalid: %s", row)
            raise exceptions.MalformedFileException("ROUTING_TABLE row is invalid") from err
        except ValueError as err:
            raise exceptions.MalformedFileException("Invalid timestamp") from err
        except KeyError as err:
            raise exceptions.MalformedFileException("Topics for ROUTING_TABLE are missing") from err

    def _process_global_stats(self, row):
        try:
            self._details[row[1]] = row[2]
        except IndexError as err:
            logging.error("GLOBAL_STATS row is invalid: %s", row)
            raise exceptions.MalformedFileException("GLOBAL_STATS row is invalid") from err

    def _parse_file(self):
        self._details = {}
        self._connected_clients = {}
        self._routing_table = {}
        self.topics_for = {}
        csvreader = csv.reader(open(self.filename), delimiter='\t')
        for row in csvreader:
            row_title = row[0]
            if row_title in self.title_processors:
                self.title_processors[row_title](row)
            elif row_title == "END":
                return True
            else:
                logging.warning("Line was not parsed. Keyword %s not recognized. %s", row_title, row)
                raise exceptions.MalformedFileException(f"Unhandled keyword {row_title}")

        logging.error("File was incomplete. END line was missing.")
        raise exceptions.MalformedFileException("END line was missing.")

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
