from typing import Generator
from unittest import mock

import pytest
from screenpy import Forgettable

from screenpy_playwright import BrowseTheWebSynchronously

from .useful_mocks import get_mocked_playwright_and_browser


class TestBrowseTheWebSynchronously:
    mock_path = "screenpy_playwright.abilities.browse_the_web_synchronously"

    @pytest.fixture(autouse=True)
    def _clean_up_ability(self) -> Generator:
        """Reset the class's playwright attribute to None."""
        yield
        BrowseTheWebSynchronously.playwright = None

    def test_can_be_instantiated(self) -> None:
        mock_playwright, mock_browser = get_mocked_playwright_and_browser()
        btws1 = BrowseTheWebSynchronously.using(mock_playwright, mock_browser)
        btws2 = BrowseTheWebSynchronously.using_chromium()
        btws3 = BrowseTheWebSynchronously.using_firefox()
        btws4 = BrowseTheWebSynchronously.using_webkit()

        assert isinstance(btws1, BrowseTheWebSynchronously)
        assert isinstance(btws2, BrowseTheWebSynchronously)
        assert isinstance(btws3, BrowseTheWebSynchronously)
        assert isinstance(btws4, BrowseTheWebSynchronously)
        assert BrowseTheWebSynchronously.playwright is mock_playwright

    def test_implements_protocol(self) -> None:
        _, mock_browser = get_mocked_playwright_and_browser()
        assert isinstance(BrowseTheWebSynchronously(mock_browser), Forgettable)

    def test_sets_class_attribute(self) -> None:
        mock_playwright, mock_browser = get_mocked_playwright_and_browser()
        BrowseTheWebSynchronously.using(mock_playwright, mock_browser)

        assert BrowseTheWebSynchronously.playwright is mock_playwright

    def test_can_have_separate_instance_attribute(self) -> None:
        mock_playwright, mock_browser = get_mocked_playwright_and_browser()
        mock_sync_playwright = mock.MagicMock()
        mock_sync_playwright.return_value.start.return_value = mock_playwright

        with mock.patch(f"{self.mock_path}.sync_playwright", mock_sync_playwright):
            BrowseTheWebSynchronously.using_chromium()
            BrowseTheWebSynchronously.using_firefox()
            BrowseTheWebSynchronously.using_webkit()
            BrowseTheWebSynchronously.using(mock_playwright, mock_browser)

        assert BrowseTheWebSynchronously.playwright is mock_playwright
        assert mock_playwright.chromium.launch.call_count == 1
        assert mock_playwright.firefox.launch.call_count == 1
        assert mock_playwright.webkit.launch.call_count == 1
