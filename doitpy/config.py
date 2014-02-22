
class Config(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def __setitem__(self, key, value):
        """make sure new items are not added after initialization"""
        if key not in self:
            msg = 'New items can not be added to Config, invalid key:{}'
            raise KeyError(msg.format(key))
        super(Config, self).__setitem__(key, value)

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

    def copy(self):
        """copy that returns a Config object instead of plain dict"""
        return self.__class__(self)


    # non-dict methods
    def make(self, *args, **kwargs):
        """return new Config, updating with given values

        Also accepts None as single argument, in this case just return a copy
        of self.
        """
        result = self.copy()
        if not(args and args[0] is None):
            result.update(*args, **kwargs)
        return result

