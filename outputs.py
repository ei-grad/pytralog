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
import logging


class Output(object):

    def __init__(self, prefix):
        self.prefix = prefix
        if not os.path.exists(prefix):
            os.mkdir(prefix)
        if not os.path.isdir(prefix):
            raise ValueError('%s is not a directory!' % prefix)

    def write_report(self, records, **kwargs):
        pass


class PlainTextOutput(Output):

    TITLE_FORMAT = "{0}\n"
    SUBTITLE_FORMAT = "{0}\n\n"
    BEFORE_DATA = "\n"
    RECORD_REPR = lambda self, l: "\t".join(l)
    RECORD_FORMAT = "{0}\n"
    AFTER_DATA = "\n"

    def write_report(self, records, **kwargs):

        fname = kwargs.get('filename', 'report.txt')

        with open(os.path.join(self.prefix, fname), 'w') as f_out:
            if 'title' in kwargs:
                f_out.write(self.TITLE_FORMAT.format(kwargs['title'].upper()))
                if 'subtitle' in kwargs:
                    f_out.write(
                            self.SUBTITLE_FORMAT.format(kwargs['subtitle'])
                        )
            f_out.write(self.BEFORE_DATA)
            if records:
                fields = list(records.values())[0]._get_fields()
                f_out.write(self.RECORD_FORMAT.format(self.RECORD_REPR(fields)))
                for key, rec in records.items():
                    f_out.write(self.RECORD_FORMAT.format(
                            self.RECORD_REPR(rec._get_values()))
                        )
            else:
                logging.warning("Empty record set!")
            f_out.write(self.AFTER_DATA)

class SimpleHTMLTableOutput(PlainTextOutput):
    TITLE_FORMAT = """<xhtml>
<head></head><body>
<h1>{0}</h1>
"""
    SUBTITLE_FORMAT = "<h2>{0}</h2>\n"
    BEFORE_DATA = "<table>"
    RECORD_REPR = lambda self, l: "<tr><td>" + "</td><td>".join(l) + "</td></tr>"
    RECORD_FORMAT = "{0}\n"
    AFTER_DATA = "</table></body></xhtml>\n"

