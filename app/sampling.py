import random


def should_store_log(rate=0.5):

    return random.random() < rate