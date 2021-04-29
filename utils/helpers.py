

def coroutine(func):
    """A decorator to automatically prime coroutines"""
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr
    return start


def array_to_tuple(a):
    try:
        return tuple(array_to_tuple(i) for i in a)
    except TypeError:
        return a
