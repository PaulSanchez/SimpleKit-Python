from simplekit import SimpleKit
import numpy.random as rnd
import math

class MyModel(SimpleKit):
    """
    Silly model keeps doubling its state until simulated time exceeds 10.
    Along the way it demonstrates argument passing for events & priorities.
    """
    def init(self):
        self.x = 1
        self.schedule(self.increment, rnd.randint(2), 1, ord('a'), priority = 2)

    def increment(self, n, c):
        self.x += n
        self.schedule(self.increment, rnd.randint(2), self.x, c + 1)
        print(self.model_time, self.x, chr(c))
        if self.model_time > 10:
            self.schedule(self.halt, 0.0, priority = 1)

rnd.seed(42)
MyModel().run()
