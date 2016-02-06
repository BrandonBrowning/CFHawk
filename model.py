
from common import HashEquality

class Person(HashEquality):
    def __init__(self, handle, name=None):
        self.handle = handle
        self.name = name

    def __hash__(self):
        return hash(self.handle)

class Problem(HashEquality):
    def __init__(self, contest_id, letter, name):
        self.contest_id = contest_id
        self.letter = letter
        self.name = name
    
    def __hash__(self):
        return hash('%s%s' % (self.contest_id, self.letter))

