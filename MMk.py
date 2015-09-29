"""Demo model of SimpleKit usage."""
from simplekit import SimpleKit
import numpy
import math

class MMk(SimpleKit):
    """Implementation of an M/M/k queueing model using SimpleKit."""

    def __init__(self, arrivalRate, serviceRate, maxServers):
        """Construct an instance of the M/M/k."""
        SimpleKit.__init__(self)
        self.arrivalRate = arrivalRate
        self.serviceRate = serviceRate
        self.maxServers = maxServers
        self.qLength = 0
        self.numAvailableServers = 0

    def init(self):
        """Initialize all state variables, schedule first arrival and halt."""
        self.numAvailableServers = self.maxServers
        self.qLength = 0
        self.schedule(self.arrival, 0.0)
        self.schedule(self.halt, 100.0)
        self.dumpState("Init")

    def arrival(self):
        """Increment queue, schedule next arrival, beginService if possible."""
        self.qLength += 1
        self.schedule(self.arrival, self.exponential(self.arrivalRate))
        if self.numAvailableServers > 0:
            self.schedule(self.beginService, 0.0)
        self.dumpState("Arrival")

    def beginService(self):
        """Remove customer from line, allocate server, schedule endService."""
        self.qLength -= 1
        self.numAvailableServers -= 1
        self.schedule(self.endService, self.exponential(self.serviceRate))
        self.dumpState("beginService")

    def endService(self):
        """Free server, if customers are waiting initiate another service."""
        self.numAvailableServers += 1
        if self.qLength > 0:
            self.schedule(self.beginService, 0.0)
        self.dumpState("endService")

    def exponential(self, rate):
        """Generate an exponential RV with specified rate using inversion."""
        return -math.log(numpy.random.random()) / rate

    def dumpState(self, event):
        """Dump of the current state of the model."""
        print "Model Time:", self.model_time, "\tEvent:\t", event, \
              "\tQueue Length: ", self.qLength, "\t# Available Servers: ", \
              self.numAvailableServers

if __name__ == '__main__':
    numpy.random.seed(12345)    # Same seed => identical results to Ruby/Java!
    MMk(4.5, 1.0, 5).run()      # Instantiate and run a copy of the MMk model.
