"""Tests for the Questions an Actor can ask using ScreenPy Playwright."""

from unittest import mock

import pytest
from screenpy import Actor, Answerable, Describable, UnableToAnswer

from screenpy_playwright import (
    Attribute,
    BrowserURL,
    BrowseTheWebSynchronously,
    Element,
    Number,
    Text,
)

from .useful_mocks import get_mock_target_class, get_mocked_target_and_locator

FakeTarget = get_mock_target_class()
TARGET = FakeTarget()


class TestAttribute:
    def test_can_be_instantiated(self) -> None:
        a1 = Attribute("")
        a2 = Attribute("").of_the(TARGET)

        assert isinstance(a1, Attribute)
        assert isinstance(a2, Attribute)

    def test_implements_protocol(self) -> None:
        a = Attribute("")

        assert isinstance(a, Answerable)
        assert isinstance(a, Describable)

    def test_raises_error_if_no_target(self, Tester: Actor) -> None:
        with pytest.raises(UnableToAnswer):
            Attribute("").answered_by(Tester)

    def test_ask_for_attribute(self, Tester: Actor) -> None:
        attr = "foo"
        value = "bar"
        target, locator = get_mocked_target_and_locator()
        locator.get_attribute.return_value = value
        mocked_btws = Tester.ability_to(BrowseTheWebSynchronously)
        mocked_btws.current_page = mock.Mock()

        assert Attribute(attr).of_the(target).answered_by(Tester) == value
        target.found_by.assert_called_once_with(Tester)
        locator.get_attribute.assert_called_once_with(attr)

    def test_describe(self) -> None:
        assert Attribute("foo").describe() == 'The "foo" attribute of the None.'


class TestBrowserURL:
    def test_can_be_instantiated(self) -> None:
        burl = BrowserURL()

        assert isinstance(burl, BrowserURL)

    def test_implements_protocol(self) -> None:
        burl = BrowserURL()

        assert isinstance(burl, Answerable)
        assert isinstance(burl, Describable)

    def test_describe(self) -> None:
        assert BrowserURL().describe() == "The current browser URL."

    def test_ask_browser_url(self, Tester: Actor) -> None:
        url = "https://www.nintendo.com"
        mocked_btws = Tester.ability_to(BrowseTheWebSynchronously)
        mocked_btws.current_page = mock.Mock()
        mocked_btws.current_page.url = url

        assert BrowserURL().answered_by(Tester) == url


class TestElement:
    def test_can_be_instantiated(self) -> None:
        e = Element(TARGET)

        assert isinstance(e, Element)

    def test_implements_protocol(self) -> None:
        e = Element(TARGET)

        assert isinstance(e, Answerable)
        assert isinstance(e, Describable)

    def test_describe(self) -> None:
        assert Element(TARGET).describe() == f"The {TARGET} element."

    def test_ask_for_element(self, Tester: Actor) -> None:
        target, locator = get_mocked_target_and_locator()
        actual_answer = Element(target).answered_by(Tester)

        target.found_by.assert_called_once_with(Tester)
        assert actual_answer == locator


class TestNumber:
    def test_can_be_instantiated(self) -> None:
        n = Number.of(TARGET)

        assert isinstance(n, Number)

    def test_implements_protocol(self) -> None:
        n = Number(TARGET)

        assert isinstance(n, Answerable)
        assert isinstance(n, Describable)

    def test_describe(self) -> None:
        target = FakeTarget()
        target._description = "Somebody once told me"

        assert Number.of(target).describe() == f"The number of {target}."

    def test_ask_number(self, Tester: Actor) -> None:
        target, locator = get_mocked_target_and_locator()
        num_elements = 10
        locator.count.return_value = num_elements

        assert Number.of(target).answered_by(Tester) == num_elements


class TestText:
    def test_can_be_instantiated(self) -> None:
        t = Text.of_the(TARGET)

        assert isinstance(t, Text)

    def test_implements_protocol(self) -> None:
        t = Text(TARGET)

        assert isinstance(t, Answerable)
        assert isinstance(t, Describable)

    def test_describe(self) -> None:
        target = FakeTarget()
        target._description = "the world is gonna roll me"

        assert Text.of_the(target).describe() == f"The text from the {target}."

    def test_ask_text(self, Tester: Actor) -> None:
        target, locator = get_mocked_target_and_locator()
        words = "Number 1, the larch."
        locator.text_content.return_value = words

        assert Text.of_the(target).answered_by(Tester) == words
