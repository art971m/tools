from os import linesep


class Restricted:
    def __init__(self, a_dict=None):
        if a_dict:
            for item in self._list_of_keys():
                if item in a_dict:
                    self.__dict__[item] = None if isinstance(a_dict[item], str) and not a_dict[item] else a_dict[item]

    def __repr__(self):
        # This method must be overridden
        return 'Restricted()'

    def __eq__(self, other):
        # This method must be overridden
        return self.__dict__ == other.__dict__

    @classmethod
    def _list_of_keys(cls):
        # This method must be overridden
        return {'attr_a', 'attr_b', 'attr_c'}

    @classmethod
    def _is_attr_allowed(cls, attr_name):
        if attr_name not in cls._list_of_keys():
            raise AttributeError(f"Attribute {attr_name} is not allowed in {cls}")

    def __contains__(self, item):
        try:
            if self.__getattr__(item) is not None:
                return True
            else:
                False
        except:
            return False

    def __getattr__(self, item):
        self._is_attr_allowed(item)
        return self.__dict__[item] if item in self.__dict__ else None

    def __setattr__(self, item, value):
        self._is_attr_allowed(item)
        self.__dict__[item] = value

    def __delattr__(self, item):
        self._is_attr_allowed(item)
        if item in self.__dict__:
            del self.__dict__[item]

    def __getitem__(self, item):
        return self.__getattr__(item)

    def __setitem__(self, item, value):
        self.__setattr__(item, value)

    def __delitem__(self, item):
        self.__delattr__(item)

    def __str__(self):
        string = type(self).__name__ + linesep
        for item in sorted(self._list_of_keys()):
            if item in self.__dict__ and self.__dict__[item] is not None:
                string += f"    {item}: {str(self.__dict__[item])}{linesep}"
        return string.strip()
