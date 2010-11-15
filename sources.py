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
ConntrackSource
"""

from time import time, sleep
from Conntrack import EventListener, NFCT_T_DESTROY, NFCT_O_PLAIN

class EventSource(object):
    pass

class ConntrackSource(EventSource):
    """
    ConntrackSource
    """

    def __init__(self, aggregator):
        """
        ConntrackSource

        @param aggregator: Aggregator to use.
        """

        super(ConntrackSource, self).__init__()

        self.aggregator = aggregator
        self.listener = EventListener(self.event_callback,
                NFCT_T_DESTROY, NFCT_O_PLAIN)
        self.listener.start()
        self._running = False
        self.events = []

    def run(self):
        self._running = True
        self.loop()

    def loop(self):
        """
        Main loop.
        """

        while self._running or self.events:

            events = self.events
            self.events = []

            for event in events:
                event = str(event, 'utf-8').split()
                proto = event[1]
                print(event)
                event = [ i.split('=') for i in event if '=' in i ]
                c_in, c_out = dict(event[:6]), dict(event[6:])

                self.aggregator.add_connection(int(time()), proto,
                        c_in['src'], c_in['sport'],
                        c_in['dst'], c_in['dport'],
                        c_in['bytes'], c_out['bytes'])

            if self._running and not self.events:
                sleep(1.0)

    def stop(self):
        """
        Stop main loop.
        """

        self.listener.stop()
        self._running = False

    def event_callback(self, event):
        """
        Callback for Netfilter netlink interface.
        """

        self.events.append(event)

