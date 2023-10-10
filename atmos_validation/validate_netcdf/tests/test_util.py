from typing import List

from pytest import raises

from ..utils import Severity, almost_equal, get_file_paths_in_folder, validation_node


def test_almost_equal():
    assert almost_equal("equality!", "equality!")
    assert not almost_equal("equality!", "nope!")
    assert almost_equal(1, 1)
    assert not almost_equal(1, 2)
    assert almost_equal(1.10001, 1.10001)
    assert almost_equal(0.7, 0.5, diff=1)
    assert almost_equal(0.5, 0.7, diff=1)
    assert not almost_equal(0.7, 0.5, diff=0.1)
    assert not almost_equal(0.5, 0.7, diff=0.1)


def test_get_file_paths_in_folder():
    paths = get_file_paths_in_folder("examples/hindcast_example")
    assert len(paths) == 3


def test_wrong_validation_node_name():
    with raises(NameError):

        @validation_node(severity=Severity.WARNING)
        def wrong_function_name() -> List[str]:
            return []

        wrong_function_name()
