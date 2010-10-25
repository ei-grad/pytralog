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
from pickle import load, dump

from interfaces import DataStorage


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

