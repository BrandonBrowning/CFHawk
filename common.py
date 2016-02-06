
class HashEquality:
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            return hash(self) == hash(other)

