from functools import wraps

def log_param_types(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        param_info = {}

        for index, value in enumerate(args):
            param_info[f"arg{index}"] = type(value).__name__

        for key, value in kwargs.items():
            param_info[key] = type(value).__name__

        print(param_info)
        return func(*args, **kwargs)

    return wrapper

@log_param_types
def example_function(a, b, name="Jerzy"):
    return a + b

example_function(5, 10, name="Andrzej")
