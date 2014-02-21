
class Config(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    # http://stackoverflow.com/questions/2060972
    # subclassing-python-dictionary-to-override-setitem
    def update(self, *args, **kwargs):
        if args:
            if len(args) > 1:
                raise TypeError("update expected at most 1 arguments, "
                                "got %d" % len(args))
            other = dict(args[0])
            for key in other:
                self[key] = other[key]
        for key in kwargs:
            self[key] = kwargs[key]

    def setdefault(self, key, value=None):
        if key not in self:
            self[key] = value
        return self[key]
    # end - redefinition of methods to make sure __setitem__ is always called

    def __setitem__(self, key, value):
        assert key in self
        super(Config, self).__setitem__(key, value)

    def copy(self):
        """copy that returns a Config object instead of plain dict"""
        return self.__class__(dict.copy(self))


    # extra methods
    def push(self, other):
        result = self.copy()
        if other is not None:
            result.update(other)
        return result

