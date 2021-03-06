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
Schedulers for pytralog.
"""

from gettext import gettext as _

from threading import Timer
from datetime import datetime, timedelta
from time import time, mktime

class Job(object):

    def __init__(self, aggregator, output, offset=timedelta(),
            context=None):
        dt = mktime((self.next_sched() + offset).timetuple()) - time()
        self.timer = Timer(dt, self.job)
        if context is None:
            context = {}
        self.context = context
        self.aggregator = aggregator
        self.output = output
        self.timer.start()

    def job(self):
        # preparing report parameters
        if 'title' not in self.context:
            self.context['title'] = self.title

        records = self.aggregator.pop()
        self.output.make_report(records, self.context)

    def next_sched(self):
        raise NotImplemented()

class Hourly(Job):

    title = _("Hourly report at %Y-%m-%d %H:%M")

    def next_sched(self):
        n = datetime.now()
        return datetime(*(n+timedelta(hours=1)).timetuple()[:4])

class Daily(Job):

    title = _("Daily report at %Y-%m-%d %H:%M")

    def next_sched(self):
        n = datetime.now()
        return datetime(*(n+timedelta(days=1)).timetuple()[:3])

class Weekly(Job):

    title = _("Weekly report at %Y-%m-%d %H:%M")

    def next_sched(self):
        n = datetime.now()
        days = 7 - n.weekday()
        return datetime(*(n + timedelta(days=days)).timetuple()[:3])

class Monthly(Job):

    title = _("Monthly report at %Y-%m-%d %H:%M")

    def next_sched(self):
        y, m = datetime.now().timetuple()[:2]
        if m == 12:
            y += 1
            m = 1
        else:
            m += 1
        return datetime(y, m, 1)


