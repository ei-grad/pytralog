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

"""
Outputs
"""

import os

from interfaces import Output


class PlainTextOutput(Output):

    def write_report(self, records, **kwargs):
        path = kwargs.get('path', 'report')
        with open(os.path.join(self.prefix, path), 'w') as f_out:
            f_out.write("%s\n" % "\t".join([
                    field for field in dir(records.items()[0][1])
                        if field[0] != '_' ]))
            for key, rec in records.items():
                values = [ str(getattr(rec, field)) for field in dir(rec)
                        if field[0] != '_' ]
                f_out.write('\t'.join(values) + '\n')

