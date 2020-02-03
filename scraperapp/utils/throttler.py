from twisted.internet import defer
from twisted.internet import task


class Throttler(object):
    """
    A simple throttler helps you limit the number of requests you make
    to a limited resource
    """

    def __init__(self, rate):
        """It will callback at most ```rate``` enqueued things per second"""
        self.queue = []
        self.looping_call = task.LoopingCall(self._allow_one)
        self.looping_call.start(1. / float(rate))

    def stop(self):
        """Stop the throttler"""
        self.looping_call.stop()

    def throttle(self):
        """
        Call this function to get a deferred that will become available
        in some point in the future in accordance with the throttling rate
        """
        d = defer.Deferred()
        self.queue.append(d)
        return d

    def _allow_one(self):
        """Makes deferred callbacks periodically"""
        if self.queue:
            self.queue.pop(0).callback(None)
