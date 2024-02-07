from screenpy import Forgettable

from screenpy_playwright import BrowseTheWebSynchronously

from .useful_mocks import get_mocked_playwright_and_browser


class TestBrowseTheWebSynchronously:
    def test_can_be_instantiated(self) -> None:
        playwright, browser = get_mocked_playwright_and_browser()

        b = BrowseTheWebSynchronously.using(playwright, browser)

        assert isinstance(b, BrowseTheWebSynchronously)

    def test_implements_protocol(self) -> None:
        playwright, browser = get_mocked_playwright_and_browser()

        assert isinstance(BrowseTheWebSynchronously(playwright, browser), Forgettable)
