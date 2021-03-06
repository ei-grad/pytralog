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
from threading import Lock


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
        self.lock = Lock()

    def _open_record(self, record_id, mode):
        if os.path.sep in record_id:
            raise ValueError("Can't use "+os.path.sep+" in record_id.")
        path = os.path.realpath(os.path.join(self.prefix, record_id))
        if not path.startswith(self.prefix):
            raise ValueError('Permission denied')
        if not os.path.isfile(path):
            raise IndexError('No record with id %s!' % record_id)
        return open(path, mode)

    def save_record(self, record_id, data):
        with self.lock:
            with self._open_record(record_id, 'w') as record_file:
                dump(data, record_file)

    def load_record(self, record_id):
        with self.lock:
            return load(self._open_record(record_id, 'r'))

    def pop(self):
        with self.lock:
            ret = {}
            for i in os.listdir(self.prefix):
                path = os.join(self.prefix, i)
                if os.path.isfile(path):
                    ret[i] = load(open(path))
                os.remove(os.join(self.prefix, i))
            return ret

