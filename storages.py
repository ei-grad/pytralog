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

import os
from pickle import load, dump


class Record(object):

    def __str__(self):
        return " ".join([ "%s=%s" % (i, getattr(self, i)) for i in dir(self)
                if i[0] != "_" ])

    def __repr__(self):
        return "<Record %s>" % self.__str__()

    def _get_fields(self):
        return [ field for field in dir(self) if field[0] != '_' ]

    def _get_values(self):
        return [ str(getattr(rec, field)) for field in self._get_fields() ]

class DataStorage(object):

    def set_record(self, record_id, data):
        raise NotImplemented()

    def get_record(self, record_id):
        raise NotImplemented()

    def get_all(self):
        raise NotImplemented()

    def flush(self):
        raise NotImplemented()


class FilesystemStorage(object):

    def __init__(self, prefix):
        self.prefix = prefix

    def _open_record(self, record_id, mode=None):
        if os.path.sep in record_id:
            raise ValueError("Can't use "+os.path.sep+" in record_id.")
        path = os.path.realpath(os.path.join(self.prefix, record_id))
        if not path.startswith(self.prefix):
            raise ValueError('Permission denied')
        if not os.path.isfile(path):
            raise IndexError('No record with id %s!' % record_id)
        if mode is None:
            return open(path)
        return open(path, mode)

    def save_record(self, record_id, data):
        with self._open_record(record_id, 'w') as record_file:
            dump(data, record_file)

    def load_record(self, record_id):
        return load(self._open_record(record_id, 'r'))

    def load_all_records(self):
        ret = {}
        for i in os.listdir(self.prefix):
            path = os.join(self.prefix, i)
            if os.path.isfile(path):
                ret[i] = load(open(path))
        return ret

    def flush(self):
        for i in os.listdir(self.prefix):
            os.remove(os.join(self.prefix, i))

