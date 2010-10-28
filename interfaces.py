#!/usr/bin/env python
#
# Copyright (c) 2010 Andrew Grigorev <andrew@ei-grad.ru>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Base classes for pytralog.
"""

import os

class EventSource(object):
    pass

class Record(object):

    def __str__(self):
        return " ".join([ "%s=%s" % (i, getattr(self, i)) for i in dir(self)
                if i[0] != "_" ])

    def __repr__(self):
        return "<Record %s>" % self.__str__()

class Aggregator(object):

    def __init__(self, storage, output):
        self.db = storage
        self.output = output
        self.records = {}

    def sync(self):
        for key, value in self.records.items():
            self.ds.set_record(key, value)

    def get_record(self, record_id):
        if record_id not in self.records:
            try:
                self.records[record_id] = self.db.load_record(record_id)
            except IndexError:
                record = Record()
                self.format_record(record_id, record)
                self.records[record_id] = record

        return self.records[record_id]

    def format_record(self, record_id, record):
        raise NotImplemented()

    def add_connection(self, timestamp, proto, src, sport, dst, dport,
            bytes_in, bytes_out):
        raise NotImplemented()

    def make_report(self, **kwargs):
        for key, value in self.db.load_all_records():
            if key not in self.records:
                self.records[key] = value
        self.output.write_report(self.records, **kwargs)
        self.records = {}
        self.db.flush()


class DataStorage(object):

    def set_record(self, record_id, data):
        raise NotImplemented()

    def get_record(self, record_id):
        raise NotImplemented()

    def get_all(self):
        raise NotImplemented()

    def flush(self):
        raise NotImplemented()


class Output(object):

    def __init__(self, prefix):
        self.prefix = prefix
        if not os.path.exists(prefix):
            os.mkdir(prefix)
        if not os.path.isdir(prefix):
            raise ValueError('%s is not a directory!' % prefix)

    def write_report(self, records, **kwargs):
        pass

