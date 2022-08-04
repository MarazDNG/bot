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
