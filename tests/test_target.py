from __future__ import annotations

from typing import TYPE_CHECKING
from unittest import mock

import pytest

from screenpy_playwright import BrowseTheWebSynchronously, Target, TargetingError

if TYPE_CHECKING:
    from screenpy import Actor


def test_can_be_instantiated() -> None:
    t1 = Target.the("test")
    t2 = Target.the("test").located_by("test")
    t3 = Target("test")
    t4 = Target().located_by("test")
    t5 = Target()

    assert isinstance(t1, Target)
    assert isinstance(t2, Target)
    assert isinstance(t3, Target)
    assert isinstance(t4, Target)
    assert isinstance(t5, Target)


def test_auto_describe() -> None:
    """When no description is provided, automatically use the string of the locator"""
    t1 = Target().located_by("#yellow")
    t2 = Target("favorite color").located_by("#no greeeeen")
    t3 = Target()
    t4 = Target("").located_by("baz")

    assert t1.target_name == "#yellow"
    assert t2.target_name == "favorite color"
    assert t3.target_name == "None"
    assert t4.target_name == "baz"


def test_found_by(Tester: Actor) -> None:
    test_locator = "#spam>baked-beans>eggs>sausage+spam"
    mocked_btws = Tester.ability_to(BrowseTheWebSynchronously)
    mocked_btws.current_page = mock.Mock()

    Target.the("test").located_by(test_locator).found_by(Tester)

    mocked_btws.current_page.locator.assert_called_once_with(test_locator)


def test_found_by_with_frames(Tester: Actor) -> None:
    test_locator = "#spam>baked-beans>eggs>sausage+spam"
    mocked_btws = Tester.ability_to(BrowseTheWebSynchronously)
    mocked_btws.current_page = mock.Mock()
    frame_path = ["#frame1", "#frame2"]
    target = Target.the("test").located_by(test_locator)
    for frame in frame_path:
        target.in_frame(frame)

    target.found_by(Tester)

    page = mocked_btws.current_page
    page.frame_locator.assert_called_once_with(frame_path[0])
    page.frame_locator().frame_locator.assert_called_once_with(frame_path[1])
    page.frame_locator().frame_locator().locator.assert_called_once_with(test_locator)


def test_found_by_raises_if_no_locator(Tester: Actor) -> None:
    test_name = "John Cleese"

    with pytest.raises(TargetingError) as excinfo:
        Target.the(test_name).located_by("*").found_by(Tester)

    assert test_name in str(excinfo.value)


def test_repr() -> None:
    t1 = Target()
    t2 = Target("foo")

    assert repr(t1) == "None"
    assert repr(t2) == "foo"


def test_str() -> None:
    t1 = Target()
    t2 = Target("foo")

    assert str(t1) == "None"
    assert str(t2) == "foo"
