from typing import Any, Callable, Generator, Iterable

__all__ = ['expand_iter']


def expand_iter(elements: Iterable,
                from_elements: Iterable,
                expand_func: Callable[[Any], Iterable]) -> Generator[Any, None, None]:
    """
    Expand *from_element* in *elements*.

    :param elements: Original set of elements.
    :type elements: Iterable
    :param from_elements: Elements that need expansion.
    :type from_elements: Iterable
    :param expand_func: Function to expand
    :type expand_func: Callable[[Any], Iterable])

    :return: Expanded elements.
    :rtype: Generator[Any, None, None]
    """

    for i in elements:
        if i in from_elements:
            for j in expand_func(i):
                yield j
        else:
            yield i
