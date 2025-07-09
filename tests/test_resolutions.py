from screenpy_playwright import IsPresent, IsVisible
from screenpy_playwright.resolutions.custom_matchers.is_present_element import (
    IsPresentElement,
)
from screenpy_playwright.resolutions.custom_matchers.is_visible_element import (
    IsVisibleElement,
)

from .useful_mocks import get_mocked_locator


class TestIsPresent:
    def test_can_be_instantiated(self) -> None:
        ip = IsPresent()

        assert isinstance(ip, IsPresent)

    def test_describe(self) -> None:
        assert IsPresent().describe() == "present"

    def test_resolve(self) -> None:
        assert isinstance(IsPresent().resolve(), IsPresentElement)

    def test_the_test(self) -> None:
        single_locator = get_mocked_locator()
        multi_locator = get_mocked_locator()
        single_locator.count.return_value = 1
        multi_locator.count.return_value = 1337

        assert IsVisible().resolve().matches(single_locator)
        assert IsVisible().resolve().matches(multi_locator)

    def test_the_test_fails(self) -> None:
        locator = get_mocked_locator()
        locator.count.return_value = 0

        assert not IsPresent().resolve().matches(locator)

    def test_the_test_fails_for_none(self) -> None:
        assert not IsPresent().resolve().matches(None)


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
