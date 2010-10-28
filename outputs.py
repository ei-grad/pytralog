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
Outputs
"""

import os

from interfaces import Output


class PlainTextOutput(Output):

    def write_report(self, records, **kwargs):
        path = kwargs.get('path', 'report')
        with open(os.path.join(self.prefix, path), 'w') as f_out:
            if 'title' in kwargs:
                f_out.write("%s\n" % kwargs['title'].upper())
                if 'subtitle' in kwargs:
                    f_out.write("%s\n\n" % kwargs['subtitle'])
                else:
                    f_out.write("\n")
            f_out.write("%s\n" % "\t".join([
                    field for field in dir(records.items()[0][1])
                        if field[0] != '_' ]))
            for key, rec in records.items():
                values = [ str(getattr(rec, field)) for field in dir(rec)
                        if field[0] != '_' ]
                f_out.write('\t'.join(values) + '\n')

