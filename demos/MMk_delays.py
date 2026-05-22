"""Demo model of SimpleKit usage."""
from simplekit import SimpleKit
from collections import deque
from numpy.random import default_rng
import sys

class MMk(SimpleKit):
    """Implementation of an M/M/k queueing model using SimpleKit."""

    def __init__(self, arrivalRate, serviceRate, maxServers, numCustomers, seed = 1234567):
        """Construct an instance of the M/M/k."""
        SimpleKit.__init__(self)
        self.mean_interarrival_timeTime = 1.0 / arrivalRate
        self.mean_service_time = 1.0 / serviceRate
        self.maxServers = maxServers
        self.numCustomers = numCustomers
        self.queue = deque()
        self.rng = default_rng(seed)

    def init(self):
        """Initialize all state variables, schedule first arrival and halt."""
        self.numAvailableServers = self.maxServers
        self.customer_number = 0
        self.queue.clear()
        self.schedule(self.arrival, self.rng.exponential(self.mean_interarrival_timeTime))
        print("customer#,delay_in_queue")

    def arrival(self):
        """Add customer to queue, schedule next arrival, beginService if possible."""
        self.customer_number += 1
        self.queue.append((self.customer_number, self.model_time))
        if self.customer_number < self.numCustomers:
            self.schedule(self.arrival, self.rng.exponential(self.mean_interarrival_timeTime))
        if self.numAvailableServers > 0:
            self.schedule(self.beginService, 0.0, priority = 2)

    def beginService(self):
        """Remove customer from line, allocate server, schedule endService."""
        customer, arrival_time = self.queue.popleft()
        print("%d,%f" % (customer, self.model_time - arrival_time))
        self.numAvailableServers -= 1
        self.schedule(self.endService, self.rng.exponential(self.mean_service_time))

    def endService(self):
        """Free server, if customers are waiting initiate another service."""
        self.numAvailableServers += 1
        if len(self.queue) > 0:
            self.schedule(self.beginService, 0.0, priority = 1)


if __name__ == '__main__':
    # Instantiate and run a copy of the MMk model.
    if len(sys.argv) == 1:
        MMk(4.5, 1.0, 5, 100).run()
    elif len(sys.argv) == 5:
        MMk(float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])).run()
    else:
        m1 = "Please specify arrival rate, per-server service rate, # servers,"
        m2 = "and # customers separated by spaces on the command-line."
        m3 = "If no arguments are given, these default to: 4.5 1.0 5 100"
        print("\n\t" + m1, file = sys.stderr)
        print("\t" + m2, file = sys.stderr)
        print("\n\t" + m3 + "\n", file = sys.stderr)
