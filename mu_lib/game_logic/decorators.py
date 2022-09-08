import logging
import time


def repeated_value_counter(foo: callable):
    """
    Return how many times a function returned same value.
    """
    def wrapper(*args, **kwargs):
        if not hasattr(wrapper, "counter"):
            wrapper.counter = 0
        if not hasattr(wrapper, "value"):
            wrapper.value = None

        value = foo()
        if value == getattr(wrapper, "value", None):
            wrapper.counter += 1
        else:
            print(f"{wrapper.value}:{wrapper.counter} times")
            wrapper.counter = 0
            wrapper.value = value
        return value

    return wrapper


def d_logger(foo: callable):
    """
    Decorator for logging.
    """
    def wrapper(*args, **kwargs):
        logging.debug(f"{foo.__name__}({args}, {kwargs})")
        ret = foo(*args, **kwargs)
        logging.debug(f"{foo.__name__} returned {ret}")
        return ret

    return wrapper


def d_perf_measure(foo: callable):
    """
    Decorator for measuring from the call of the function to the return of the function.
    """
    def wrapper(*args, **kwargs):
        t1 = time.perf_counter()
        ret = foo(*args, **kwargs)
        t2 = time.perf_counter()
        print(f"{foo.__name__} took {t2 - t1} seconds")
        return ret, t2 - t1

    return wrapper
