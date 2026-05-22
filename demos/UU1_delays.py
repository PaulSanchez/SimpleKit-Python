"""Demo model of SimpleKit usage."""
from simplekit import SimpleKit
from collections import deque
from numpy.random import default_rng
import sys

class UU1(SimpleKit):
    """Implementation of a U/U/1 queueing model using SimpleKit."""

    """ Object initialization """
    def __init__(self, seed = 1234567):
        """Construct an instance of the U/U/1."""
        SimpleKit.__init__(self)
        self.queue = deque()
        self.rng = default_rng(seed)

    """ Model initialization """
    def init(self):
        """Initialize all state variables, schedule first arrival and halt."""
        self.numAvailableServers = 1
        self.customer_number = 0
        self.queue.clear()
        self.schedule(self.arrival, 0)  # start at time of first arrival
        self.schedule(self.shutdown, 10000.0, priority = 0)
        print("time,customer#,delay_in_queue")

    """ What happens when there is a new arrival """
    def arrival(self):
        """Add customer to queue, schedule next arrival, beginService if possible."""
        self.customer_number += 1
        self.queue.append((self.customer_number, self.model_time))
        if self.customer_number < 1000:
            self.schedule(self.arrival, self.rng.uniform(1.0, 6.0))
        if self.numAvailableServers > 0:
            self.schedule(self.beginService, 0.0, priority = 2)

    """ What happens when somebody begins service """
    def beginService(self):
        """Remove customer from line, allocate server, schedule endService."""
        customer, arrival_time = self.queue.popleft()
        delay_in_queue = self.model_time - arrival_time
        print("%f,%d,%f" % (self.model_time, customer, delay_in_queue))
        self.numAvailableServers -= 1
        self.schedule(self.endService, self.rng.uniform(1.0, 4.0), customer)

    """ What happens when the customer completes service """
    def endService(self, customer):
        """Free server, if customers are waiting initiate another service."""
        self.numAvailableServers += 1
        if len(self.queue) > 0 and customer < 1000:
            self.schedule(self.beginService, 0.0, priority = 1)

    """ Schedule this for a graceful shutdown of the system """
    def shutdown(self):
        """
        Close shop by shutting doors, i.e., no more arrivals. People
        already in the system are processed, since they may have
        greater than average delays (which is why they're still here).
        """
        self.cancel_next(self.arrival)


if __name__ == '__main__':
    # Instantiate and run a copy of the UU1 model.
    if len(sys.argv) == 1:
        UU1().run()
