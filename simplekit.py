"""A discrete event modeling toolkit based on event graphs."""

from queue import PriorityQueue
import abc

__author__ = 'Hayley Oliver and Paul J Sanchez'
__copyright__ = 'Copyright 2015-2017, The SEED Center'
__credits__ = ['Hayley Oliver', 'Paul J Sanchez']
__license__ = 'GPL'
__version__ = '1.0.0'
__maintainer__ = 'Paul J Sanchez'
__email__ = 'pjs@alum.mit.edu'
__status__ = 'Development'


class SimpleKit:
    """
    To create a SimpleKit model:
        Your model class must be a subclass of SimpleKit.
        Your constructor (__init__()) must call SimpleKit.__init__(self).
        You must override the abstract init() method to start your model.
    Note:
        Your model cannot implement methods named run(), schedule(), or halt().
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """Initialize a pending events list and set model_time to 0."""
        self.event_list = PriorityQueue()
        self.model_time = 0.0

    @abc.abstractmethod
    def init(self):
        """This abstract method must be overridden in your model class."""

    def run(self):
        """Execute the model logic."""
        self.init()
        while not self.event_list.empty():
            event_notice = self.event_list.get_nowait()
            self.model_time = event_notice.time
            event_notice.event(*(event_notice.args))

    def schedule(self, event, delay, *args, priority=10):
        """Add an event to the pending events.

        Args:
            event: The name of the event method to be scheduled.
            delay: The amount of model time by which to delay the execution.
            args: (optional) Any arguments required by the event.
        """
        if delay < 0:
            raise RuntimeError('Negative delay is not allowed.')
        self.event_list.put_nowait(
            self.EventNotice(event, delay + self.model_time, args, priority))

    def halt(self):
        """Terminate a simulation run by clearing the pending events list."""
        while not self.event_list.empty():
            self.event_list.get_nowait()

    class EventNotice:
        """Internal class for storage & retrieval of event notice info."""

        def __init__(self, event, time, args, priority=10):
            self.event = event
            self.time = time
            self.priority = priority
            self.args = args

        def __eq__(self, other):
            return self.time == other.time and self.priority == other.priority

        def __lt__(self, other):
            return (self.time < other.time or
                (self.time == other.time and self.priority < other.priority))
