
import logging

log = logging.getLogger(__name__)


class Job(object):

    def __init__(self, interval, function):
        self.function = function
        self.interval = interval
        self.lastrun = 0

    def __str__(self):
        return "{} {} {}".format(self.function, self.interval, self.lastrun)

    def __repr__(self):
        return self.__str__()

    def check(self):
        if self.lastrun + self.interval < time.time():
            try:
                self.function()
            except:
                log.exception("Checking job function.")

            self.lastrun = time.time()
            pass
