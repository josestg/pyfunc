def reduce(reducer, array, initial):
    """
    reduce executes a user-supplied "reducer" callback function on each element
    of the array, in order, passing in the return value from the calculation on
    the preceding element.

    The final result of running the reducer across all elements of the array is
    a single value.

    >>> reduce(lambda accumulated, current: accumulated + current, [1, 2, 3, 4], 0)
    10
    >>> reduce(lambda accumulated, current: accumulated + current, [], 0)
    0
    >>> reduce(lambda accumulated, current: accumulated + current, [2, 4, 6, 8], -20)
    0
    """

    # terminate condition always returns the initial value.
    if len(array) == 0:
        return initial

    # splits array into two parts,
    # the first part contains the first element of the array
    # and the second parts contains the rest of elements of the array.
    [item, *rest_items] = array

    # calculates the "next initial" by execute a user-supplied "reducer".
    reduced = reducer(initial, item)

    # calls reduce with the same "reducer" but differs "initial" and
    # rest of element of the array.
    return reduce(reducer, rest_items, reduced)


def pluck(value_extractor, array):
    """
    pluck populates specific value from arrays of object.
    >>> pluck(lambda obj: obj['price'], [{'price': 10}, {'price': 20}])
    [10, 20]
    >>> pluck(lambda obj: obj['x'], [{'price': 10}, {'x': 20}])
    [20]
    """

    # skip if value_extractor raised KeyError.
    def _value_extractor(current):
        try:
            return [value_extractor(current)]
        except KeyError:
            return []

    return reduce(lambda acc, cur: [*acc, *_value_extractor(cur)], array, [])


def array_filter(fn, array):
    """
    filter creates a new array with all elements that pass the test
    implemented by the provided function fn.

    >>> array_filter(lambda x: x % 2 == 0, [1, 2, 3, 4])
    [2, 4]
    >>> array_filter(lambda x: x % 2 == 1, [1, 2, 3, 4])
    [1, 3]
    """

    # internal _fn always returns an array, even the
    # test function is not satisfied.
    def _fn(current):
        return [] if not fn(current) else [current]

    return reduce(lambda acc, cur: [*acc, *_fn(cur)], array, [])


def array_map(fn, array):
    """
    array_map creates a new array populated with the results of calling a provided function fn
    on every element in the calling array.

    >>> array_map(lambda x: x ** 2, [1, 2, 3, 4])
    [1, 4, 9, 16]
    >>> array_map(lambda x: x ** 2, [])
    []
    """

    # terminate condition always returns an empty array.
    if len(array) == 0:
        return []

    # splits array into two parts,
    # the first part contains the first element of the array
    # and the second parts contains the rest of elements of the array.
    [item, *rest_items] = array
    return [fn(item), *array_map(fn, rest_items)]


def array_find(fn, array):
    """
    array_find returns the first element in the provided array that
    satisfies the provided testing function.
    If no values satisfy the testing function, None is returned.

    >>> array_find(lambda x: x==3, [1, 2, 3, 4])
    3
    >>> array_find(lambda x: x==6, [1, 2, 3, 4]) is None
    True
    """
    # terminate condition.
    if len(array) == 0:
        return None

    # splits array into two parts,
    # the first part contains the first element of the array
    # and the second parts contains the rest of elements of the array.
    [item, *rest_items] = array
    if fn(item):
        return item

    return array_find(fn, rest_items)
