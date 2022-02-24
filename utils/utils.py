import random
import itertools


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return list(zip(a, b))


def flatten_list(the_list):
    return [item for sublist in the_list for item in sublist]


def random_value_of_type(var_type):
    vals = {
        'boolean': ['true', 'false'],
        'int': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    }
    return random.choice(vals[var_type])


def weighted_random_choices(choices, count):
    return [weighted_random_choice(choices) for i in range(count)]


def weighted_random_choice(choices, returnWeight=False):
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            if returnWeight:
                return (c, w)
            return c
        upto += w
    assert False, "Shouldn't get here"


def tuple_to_string(tup):
    return '({})'.format(','.join([x for x in tup]))


def remove_duplicates_array(arr):
    arr.sort()
    return list(arr for arr, _ in itertools.groupby(arr))
