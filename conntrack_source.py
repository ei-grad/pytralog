#!/usr/bin/env python
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
ConntrackSource
"""

from time import time, sleep

from Conntrack import EventListener, NFCT_T_DESTROY, NFCT_O_PLAIN

from interfaces import EventSource

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
                event = event.split()
                proto = event[1]
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

