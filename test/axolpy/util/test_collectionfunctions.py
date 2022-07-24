from axolpy.util import collectionfunctions as cf


def test_expand_iter() -> None:
    """
    Test to get random bits.
    """

    assert list(cf.expand_iter(
        elements=[2, 3],
        from_elements=[1, 2, 3, 4, 5],
        expand_func=lambda x: [x, x + 1])) == [2, 3, 3, 4]
