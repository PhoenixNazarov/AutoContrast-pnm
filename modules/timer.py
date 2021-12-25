import time
from functools import wraps


def work_time(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        st = time.time()
        ret = func(*args, **kwargs)
        print(f'{func.__name__} work: {round(time.time() - st, 2)} sec')
        return ret
    return wrap
