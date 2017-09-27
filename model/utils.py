import random
import string
import re

def random_string(prefix="", max_len=10):
    # symbols = string.ascii_letters + string.digits + string.punctuation + " " * 10
    symbols = string.ascii_letters + string.digits + " "*10
    return prefix + "".join([random.choice(symbols) for _ in range(random.randrange(max_len))])

def trim_spaces(string):
    return re.sub(" +", " ", string).strip(" ")
