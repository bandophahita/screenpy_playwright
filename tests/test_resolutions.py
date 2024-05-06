from screenpy_playwright import IsVisible
from screenpy_playwright.resolutions.custom_matchers.is_visible_element import (
    IsVisibleElement,
)

from .useful_mocks import get_mocked_locator


class TestIsVisible:
    def test_can_be_instantiated(self) -> None:
        iv = IsVisible()

        assert isinstance(iv, IsVisible)

    def test_describe(self) -> None:
        assert IsVisible().describe() == "visible"

    def test_resolve(self) -> None:
        assert isinstance(IsVisible().resolve(), IsVisibleElement)

    def test_the_test(self) -> None:
        locator = get_mocked_locator()
        locator.is_visible.return_value = True

        assert IsVisible().resolve().matches(locator)

    def test_the_test_fails(self) -> None:
        locator = get_mocked_locator()
        locator.is_visible.return_value = False

        assert not IsVisible().resolve().matches(locator)

    def test_the_test_fails_for_none(self) -> None:
        assert not IsVisible().resolve().matches(None)
