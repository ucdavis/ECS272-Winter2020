import logging


def get_default_logger():
    return logging.getLogger('alt')


def format_time(time_seconds):
    m, s = divmod(time_seconds, 60)
    m = int(round(m))
    if m == 0:
        to_return = "%.2fs" % s
    else:
        to_return = str(int(round(s)))
        h, m = divmod(m, 60)
        if h == 0:
            to_return = str(m) + "m:" + to_return
        else:
            d, h = divmod(h, 24)
            to_return = str(h) + "h:" + to_return
            if d > 0:
                to_return = str(d) + "d:" + to_return
    return to_return