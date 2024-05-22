from __future__ import annotations

from typing import TYPE_CHECKING
from unittest import mock

import pytest

from screenpy_playwright import BrowseTheWebSynchronously, Target, TargetingError
from screenpy_playwright.target import _Manipulation

if TYPE_CHECKING:
    from screenpy import Actor

    from screenpy_playwright.target import (
        _ManipulationArgsType,
        _ManipulationKwargsType,
    )


class Test_Manipulations:
    def test_proper_display(self) -> None:
        name = "viking"
        args: _ManipulationArgsType = ("spam", "eggs", 1, None)
        kwargs: _ManipulationKwargsType = {
            "has_text": "spam",
            "exact": True,
            "include_hidden": None,
            "level": 1,
        }
        args_str = "'spam', 'eggs', 1, None"
        kwargs_str = "has_text='spam', exact=True, include_hidden=None, level=1"

        m_for_attribute = _Manipulation(Target(), name)
        m_with_neither = _Manipulation(Target(), name, (), {})
        m_with_both = _Manipulation(Target(), name, args, kwargs)
        m_with_args_but_no_kwargs = _Manipulation(Target(), name, args=args)
        m_with_no_args_but_kwargs = _Manipulation(Target(), name, kwargs=kwargs)

        assert repr(m_for_attribute) == name
        assert repr(m_with_neither) == f"{name}()"
        assert repr(m_with_both) == f"{name}({args_str}, {kwargs_str})"
        assert repr(m_with_args_but_no_kwargs) == f"{name}({args_str})"
        assert repr(m_with_no_args_but_kwargs) == f"{name}({kwargs_str})"

    def test_defers_to_target_for_unknown_attributes(self) -> None:
        target = Target.the("spam")
        m = _Manipulation(target, "eggs")

        assert m.target_name == target.target_name


class TestTarget:
    def test_can_be_instantiated(self) -> None:
        t1 = Target.the("test")
        t2 = Target.the("test").located_by("test")
        t3 = Target("test")
        t4 = Target().located_by("test")
        t5 = Target()
        t6 = Target("test").get_by_label("test", exact=True)

        assert isinstance(t1, Target)
        assert isinstance(t2, Target)
        assert isinstance(t3, Target)
        assert isinstance(t4, Target)
        assert isinstance(t5, Target)
        assert isinstance(t6, Target)

    def test_auto_describe(self) -> None:
        t1 = Target().located_by("#yellow")
        t2 = Target("favorite color").located_by("#no greeeeen")
        t3 = Target()
        t4 = Target("").get_by_label("baz")
        t5 = Target().located_by("foo").get_by_label("bar").first

        assert t1.target_name == "locator('#yellow')"
        assert t2.target_name == "favorite color"
        assert t3.target_name == "None"
        assert t4.target_name == "get_by_label('baz')"
        assert t5.target_name == "locator('foo').get_by_label('bar').first"

    def test_found_by(self, Tester: Actor) -> None:
        test_locator = "#spam>baked-beans>eggs>sausage+spam"
        mocked_btws = Tester.ability_to(BrowseTheWebSynchronously)
        mocked_btws.current_page = mock.Mock()

        Target.the("test").located_by(test_locator).found_by(Tester)

        locator = mocked_btws.current_page.locator("html").locator
        locator.assert_called_once_with(test_locator)

    def test_found_by_with_frames(self, Tester: Actor) -> None:
        test_locator = "#spam>baked-beans>eggs>sausage+spam"
        mocked_btws = Tester.ability_to(BrowseTheWebSynchronously)
        mocked_btws.current_page = mock.Mock()
        frame_path = ["#frame1", "#frame2"]
        target = Target.the("test")
        for frame in frame_path:
            target.in_frame(frame)

        target.located_by(test_locator).found_by(Tester)

        frame1 = mocked_btws.current_page.locator("html").frame_locator
        frame1.assert_called_once_with(frame_path[0])
        frame2 = frame1().frame_locator
        frame2.assert_called_once_with(frame_path[1])
        locator = frame2().locator
        locator.assert_called_once_with(test_locator)

    # list from https://playwright.dev/python/docs/locators
    @pytest.mark.parametrize(
        ("strategy", "args", "kwargs"),
        [
            ("get_by_role", ("button",), {}),
            ("get_by_text", ("Log In",), {"exact": True}),
            ("get_by_label", ("spam",), {"level": 1, "exact": None}),
            ("get_by_placeholder", ("eggs",), {}),
            ("get_by_alt_text", ("sausage",), {}),
            ("get_by_title", ("baked beans",), {}),
            ("get_by_test_id", ("spam",), {}),
            ("nth", (1,), {}),
        ],
    )
    def test_found_by_with_playwright_strategies(
        self,
        Tester: Actor,
        strategy: str,
        args: _ManipulationArgsType,
        kwargs: _ManipulationKwargsType,
    ) -> None:
        mocked_btws = Tester.ability_to(BrowseTheWebSynchronously)
        mocked_btws.current_page = mock.Mock()

        target = Target.the("test")
        getattr(target, strategy)(*args, **kwargs).found_by(Tester)

        func = getattr(mocked_btws.current_page.locator("html"), strategy)
        func.assert_called_once_with(*args, **kwargs)

    def test_found_by_chain(self, Tester: Actor) -> None:
        test_locator = "#spam>baked-beans>eggs>sausage+spam"
        mocked_btws = Tester.ability_to(BrowseTheWebSynchronously)
        mocked_btws.current_page = mock.Mock()

        manipulation = Target.the("test").located_by(test_locator).first
        # mypy thinks this will be a Target. It will not be.
        target = manipulation.get_by_label("foo")  # type: ignore[operator]

        assert isinstance(manipulation, _Manipulation)
        assert isinstance(target, Target)

    def test_found_by_raises_if_no_locator(self, Tester: Actor) -> None:
        test_name = "John Cleese"

        with pytest.raises(TargetingError) as excinfo:
            Target.the(test_name).found_by(Tester)

        assert test_name in str(excinfo.value)

    def test_unknown_locator_strategy_raises(self) -> None:
        with pytest.raises(AttributeError):
            Target.the("test").shuffled_off_this_mortal_coil("Parrot")

    def test_repr(self) -> None:
        t1 = Target()
        t2 = Target("foo")

        assert repr(t1) == "None"
        assert repr(t2) == "foo"

    def test_str(self) -> None:
        t1 = Target()
        t2 = Target("foo")

        assert str(t1) == "None"
        assert str(t2) == "foo"
