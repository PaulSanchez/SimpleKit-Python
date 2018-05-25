"""A discrete event modeling toolkit based on event graphs."""

from queue import PriorityQueue
import abc

__author__ = 'Hayley Oliver and Paul J Sanchez'
__copyright__ = 'Copyright 2015-2018, The SEED Center'
__credits__ = ['Hayley Oliver', 'Paul J Sanchez']
__license__ = 'MIT'
__version__ = '3.2.0'
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
        """
        Initialize a pending events list and set model_time to 0.
        """
        self.__event_list = PriorityQueue()
        self.__model_time = 0.0
        self.__cancel_next_event_set = set()

    @abc.abstractmethod
    def init(self):
        """This abstract method must be overridden in your model class."""

    @property
    def model_time(self):
        return self.__model_time

    def run(self):
        """Execute the model logic."""
        self.init()
        while not self.__event_list.empty():
            event_notice = self.__event_list.get_nowait()
            if len(self.__cancel_next_event_set) > 0:
                if event_notice.event in self.__cancel_next_event_set:
                    self.__cancel_next_event_set.remove(event_notice.event)
                    continue
            self.__model_time = event_notice.time
            event_notice.event(*(event_notice.args))

    def schedule(self, event, delay, *args, priority=10):
        """
        Add an event to the pending events.

        Args:
            event: The name of the event method to be scheduled.
            delay: The amount of model time by which to delay the execution.
            args: (optional) Any arguments required by the event.
        """
        if delay < 0:
            raise RuntimeError('Negative delay is not allowed.')
        self.__event_list.put_nowait(
            self.__EventNotice(event, self.__model_time, delay, args, priority))

    def cancel_next(self, event):
        """Cancel the next occurrence of the specified event"""
        self.__cancel_next_event_set.add(event)

    def cancel_all(self, event):
        """
        Cancel all currently scheduled occurrences of the specified event.
        WARNING - copies entire event list excluding the targeted event,
        so this can get expensive if done indiscriminately.
        """
        new_pq = PriorityQueue()
        while not self.__event_list.empty():
            event_notice = self.__event_list.get_nowait()
            if not event_notice.event == event:
                new_pq.put_nowait(event_notice)
        self.__event_list = new_pq

    def halt(self):
        """
        Terminate a simulation run by clearing the pending events list.
        """
        while not self.__event_list.empty():
            self.__event_list.get_nowait()

    class __EventNotice:
        """
        Internal class for storage & retrieval of event notice info.
        """

        def __init__(self, event, current_time, delay, args, priority=10):
            self.event = event
            self.time = current_time + delay
            self.priority = priority
            self.args = args

        def __eq__(self, other):
            return self.time == other.time and self.priority == other.priority

        def __lt__(self, other):
            return (self.time < other.time or
                (self.time == other.time and self.priority < other.priority))
