#!/usr/bin/env python
#
# Copyright (c) 2010 Andrew Grigorev <andrew@ei-grad.ru>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import os

class EventSource(object):
    pass

class Record(object):

    def __str__(self):
        ret = ""
        for i in dir(self):
            if i[0] != "_":
                ret += "%s=%s" % (i, getattr(self, i))
        return ret

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

    def make_report(self, path):
        for key, value in self.db.load_all_records():
            if key not in self.records:
                self.records[key] = value
        self.output.write_report(path, self.records)
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

    def write_report(self, path, records):
        pass

