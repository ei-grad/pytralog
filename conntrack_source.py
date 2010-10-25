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

from time import time

from Conntrack import EventListener, NFCT_T_DESTROY, NFCT_O_PLAIN

from interfaces import EventSource

class ConntrackSource(EventSource):

    def __init__(self, aggregator):
        self.aggregator = aggregator
        e = EventListener(self.event_callback, NFCT_T_DESTROY, NFCT_O_PLAIN)
        e.start()
        self._running = True
        self.loop()

    def loop(self):
        while self._running or self.events:
            events = self.events
            self.events = []

            for event in events:
                l = events.split()
                proto = l[1]
                l = [ r.split('=') for r in l if '=' in r ]
                p_in, p_out = dict(l[:6]), dict(l[6:])

                self.aggregator.add_connection(int(time()), proto,
                        p_in['src'], p_in['sport'],
                        p_in['dst'], p_in['dport'],
                        p_in['bytes'], p_out['bytes'])

    def stop(self):
        self.e.stop()
        self._running = False

    def event_callback(self, e):
        self.events.append(e)

