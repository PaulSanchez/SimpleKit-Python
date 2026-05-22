"""Demo model of SimpleKit usage."""
from simplekit import SimpleKit
import numpy
import math
import sys

class MMk(SimpleKit):
    """Implementation of an M/M/k queueing model using SimpleKit."""

    def __init__(self, arrivalRate, serviceRate, maxServers, shutdownTime):
        """Construct an instance of the M/M/k."""
        SimpleKit.__init__(self)
        self.meanArrival = 1.0 / arrivalRate
        self.meanSvc = 1.0 / serviceRate
        self.maxServers = maxServers
        self.shutdownTime = shutdownTime

    def init(self):
        """Initialize all state variables, schedule first arrival and halt."""
        self.numAvailableServers = self.maxServers
        self.qLength = 0
        self.schedule(self.arrival, 0.0)
        self.schedule(self.shutdown, self.shutdownTime, priority = 0)
        self.dumpState("Init")

    def arrival(self):
        """Increment queue, schedule next arrival, beginService if possible."""
        self.qLength += 1
        self.schedule(self.arrival, numpy.random.exponential(self.meanArrival))
        if self.numAvailableServers > 0:
            self.schedule(self.beginService, 0.0, priority = 2)
        self.dumpState("Arrival")

    def beginService(self):
        """Remove customer from line, allocate server, schedule endService."""
        self.qLength -= 1
        self.numAvailableServers -= 1
        self.schedule(self.endService, numpy.random.exponential(self.meanSvc))
        self.dumpState("beginService")

    def endService(self):
        """Free server, if customers are waiting initiate another service."""
        self.numAvailableServers += 1
        if self.qLength > 0:
            self.schedule(self.beginService, 0.0, priority = 1)
        self.dumpState("endService")

    def shutdown(self):
        """Close shop by shutting doors, i.e., no more arrivals."""
        self.cancel_next(self.arrival)
        self.dumpState("shutdown")

    def dumpState(self, event):
        """Dump of the current state of the model."""
        print("Time: %6.2f" % self.model_time, "  Event: %-12s" % event,
              "  Queue Length: %3d" % self.qLength, " Available Servers: ",
              self.numAvailableServers)

if __name__ == '__main__':
    numpy.random.seed(12345)
    # Instantiate and run a copy of the MMk model.
    if len(sys.argv) == 1:
        model = MMk(4.5, 1.0, 5, 100.0).run()
    elif len(sys.argv) == 5:
        model = MMk(float(sys.argv[1]), float(sys.argv[2]),
                    int(sys.argv[3]), float(sys.argv[4])).run()
    else:
        m1 = "Please specify arrival rate, per-server service rate, # servers,"
        m2 = "and shutdown time separated by spaces on the command-line."
        m3 = "If no arguments are given, these default to: 4.5 1.0 5 100.0"
        print("\n\t" + m1, file = sys.stderr)
        print("\t" + m2, file = sys.stderr)
        print("\n\t" + m3 + "\n", file = sys.stderr)
