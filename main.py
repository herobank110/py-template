"""Template syntax system like C++.

You can use template classes like so
```
my_array = Array<T(int)>()
my_array.resize(10)  # default constructed
my_array[0] = 2
my_array[0] = 2.5  # can cast or throw
```
"""

class Template(type):
    """Metaclass for templates.
    """
    def __new__(self, *template_args):
        self.template_args = template_args
        return super().__new__(self, "T", tuple(), {})

    def __gt__(self, other):
        """Starts and ends the syntax for the template argument.
        """
        if (not isinstance(other, tuple)):
            # The start of a template argument.
            if (not issubclass(other, Template)):
                raise Exception("'%s' is not a template class" % other.__name__)

            self.__template_class = other
            return self
        else:
            # The end of a template argument.
            self.__template_class.__template_args__ = self.template_args
            # Construct and return object.
            return self.__template_class(*other)


class T(Template):
    """Wrapper for template arguments.
    """

class Templatable(Template):
    """Wrapper for template classes.
    """


class Array(Templatable):
    """Template array type.
    """
    def __init__(self, *vals):
        self.array_type = self.__template_args__[0]
        if self.array_type is None:
            raise Exception("Array template cannot be 'None'")
        self.vals = list(map(self.array_type, vals))

    def __str__(self):
        return (
            "Array<%s>(%s)"
            % (
                self.__template_args__[0].__name__,
                ", ".join(map(str, self.vals))
            )
        )

    def __getitem__(self, index):
        return self.vals[index]
    def __setitem__(self, index, value):
        self.vals[index] = self.array_type(value)
    def __len__(self):
        return len(self.vals)

    def resize(self, new_length):
        if len(self) == new_length:
            # No need to change length.
            return

        for _ in range(len(self), new_length):
            # Construct default objects until reaching final size.
            self.vals.append(self.array_type())
        else:
            # We need to shrink the array.
            for _ in range(len(self) - new_length):
                self.vals.pop()


my_array = Array<T(int)>()
my_array.resize(10)  # default constructed
my_array[0] = 2
my_array[0] = 2.5  # can cast or throw
print(my_array)
