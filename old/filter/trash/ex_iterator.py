# iterator.py


class MyIterator(object):

    """docstring for MyIterator"""

    def __init__(self, step):
        self.step = step

    def next(self):
        """Returns the next element. """
        if self.step == 0:
            raise StopIteration
        self.step -= 1
        return self.step

    __next__ = next

    def __iter__(self):
        """Returns the iterator itself."""
        return self


Iter = MyIterator(4)
for el in Iter:
	print el