import sys
from datetime import datetime
import random


def timestr():
    return datetime.now().strftime("%H:%M:%S.%f")


def output(message, end='\n'):
    sys.stdout.write(str(message) + end)
    sys.stdout.flush()


def rand(min=0, max=100000):
    return random.randint(min, max)


def randstr(target_len, seed='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    res = ''
    while len(res) < target_len:
        res += seed[rand(0, len(seed) - 1)]
    return res
