import time


def time_str(t):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(int(t) + 3600 * 8))


def time_str_datetime(t):
    return time.strftime("%Y-%m-%dT%H:%M", time.gmtime(int(t) + 3600 * 8))


filters = {
    'time_str': time_str,
    'time_str_datetime': time_str_datetime,
}
