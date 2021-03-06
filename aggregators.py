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
A collection of pytralog aggregators.
"""


class Record(object):

    def __str__(self):
        return " ".join([ "%s=%s" % (i, getattr(self, i)) for i in dir(self)
                if i[0] != "_" ])

    def __repr__(self):
        return "<Record %s>" % self.__str__()

    def _get_fields(self):
        return [ field for field in dir(self) if field[0] != '_' ]

    def _get_values(self):
        return [ str(getattr(self, field)) for field in self._get_fields() ]


class Aggregator(object):

    def __init__(self, storage):
        self.db = storage
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

    def pop(self, **kwargs):
        records = self.records
        self.records = {}
        for key, value in self.db.pop():
            if key not in self.records:
                records[key] = value
        return records


class HubAggregator(Aggregator):

    def __init__(self, storage):
        super(HubAggregator, self).__init__(self, storage)
        self.aggregators = []

    def add_aggregator(self, aggregator):
        self.aggregators.append(aggregator)

    def add_connection(self, *args):
        for aggr in self.aggregators:
            aggr.add_connection(*args)


class SrcAggregator(Aggregator):

    def format_record(self, record_id, record):
        record.src = record_id
        record.bytes_in = 0
        record.bytes_out = 0

    def add_connection(self, timestamp, proto, src, sport, dst, dport,
            bytes_in, bytes_out):
        record = self.get_record(src)
        record.bytes_in += int(bytes_in)
        record.bytes_out += int(bytes_out)

class DstAggregator(Aggregator):

    def format_record(self, record_id, record):
        record.dst = record_id
        record.bytes_in = 0
        record.bytes_out = 0

    def add_connection(self, timestamp, proto, src, sport, dst, dport,
            bytes_in, bytes_out):
        record = self.get_record(dst)
        record.bytes_in += int(bytes_in)
        record.bytes_out += int(bytes_out)

class SrcDstAggregator(Aggregator):

    def format_record(self, record_id, record):
        record.src, record.dst = record_id.split('-')
        record.bytes_in = 0
        record.bytes_out = 0

    def add_connection(self, timestamp, proto, src, sport, dst, dport,
            bytes_in, bytes_out):
        record = self.get_record("%s-%s" %(src, dst))
        record.bytes_in += int(bytes_in)
        record.bytes_out += int(bytes_out)

