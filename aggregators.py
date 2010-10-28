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

