from twisted.internet import defer
from twisted.internet import reactor


class DeferredCache(object):
    """
    A cache that always returns a value, an error or a deferred
    """

    def __init__(self, key_not_found_callback):
        """Takes as an argument """
        self.records = {}
        self.deferreds_waiting = {}
        self.key_not_found_callback = key_not_found_callback

    @defer.inlineCallbacks
    def find(self, key):
        """
        This function either returns something directly from the cache or it
        calls ```key_not_found_callback``` to evaluate a value and return it.
        Uses deferreds to do this is a non-blocking manner.
        """
        # This is the deferred for this call
        rv = defer.Deferred()

        if key in self.deferreds_waiting:
            # We have other instances waiting for this key. Queue
            self.deferreds_waiting[key].append(rv)
        else:
            # We are the only guy waiting for this key right now.
            self.deferreds_waiting[key] = [rv]

            if key not in self.records:
                # If we don't have a value for this key we will evaluate it
                # using key_not_found_callback.
                try:
                    value = yield self.key_not_found_callback(key)

                    # If the evaluation succeeds then the action for this key
                    # is to call deferred's callback with value as an argument
                    # (using Python closures)
                    self.records[key] = lambda d: d.callback(value)
                except Exception as exp:
                    # If the evaluation fails with an exception then the
                    # action for this key is to call deferred's errback with
                    # the exception as an argument (Python closures again)
                    self.records[key] = lambda d: d.errback(exp)

            # At this point we have an action for this key in self.records
            action = self.records[key]

            # Note that due to ```yield key_not_found_callback```, many
            # deferreds might have been added in deferreds_waiting[key] in
            # the meanwhile
            # For each of the deferreds waiting for this key....
            for d in self.deferreds_waiting.pop(key):
                # ...perform the action later from the reactor thread
                reactor.callFromThread(action, d)

        value = yield rv
        defer.returnValue(value)
