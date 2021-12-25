import time
from functools import wraps


def work_time(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        st = time.time()
        ret = func(*args, **kwargs)
        print(f'DELTA_TIME: {round(time.time() - st, 2)} s, {func.__name__}\n')
        return ret
    return wrap
