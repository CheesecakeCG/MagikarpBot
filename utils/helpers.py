import types
import functools

def copy_func(f):
    """Copied from https://stackoverflow.com/questions/13503079/how-to-create-a-copy-of-a-python-function/13503277#13503277"""
    g = types.FunctionType(f.__code__, f.__globals__, name=f.__name__,
                           argdefs=f.__defaults__,
                           closure=f.__closure__)
    g = functools.update_wrapper(g, f)
    g.__kwdefaults__ = f.__kwdefaults__
    return g
