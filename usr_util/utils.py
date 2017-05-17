import time
from uuid import uuid4


def timestamp():
    return int(time.time())


def time_str(t):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(int(t) + 3600 * 8))


def short_uuid():
    seed = str(uuid4())
    short_seed = seed.split('-')[-1]
    return short_seed


def safe_list_get(l, idx, default):
    try:
        return l[idx]
    except IndexError:
        return default
