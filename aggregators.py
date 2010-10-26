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

from interfaces import Aggregator


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
