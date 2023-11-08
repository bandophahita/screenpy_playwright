from unittest import mock

import pytest
from playwright.sync_api import Browser, Playwright
from screenpy.protocols import Forgettable

from screenpy_playwright.abilities import BrowseTheWebSynchronously


class TestBrowseTheWebSynchronously:
    mock_path = "screenpy_playwright.abilities.browse_the_web_synchronously"

    @pytest.fixture(autouse=True)
    def clean_up_ability(self):
        """Reset the class's playwright attribute to None."""
        yield
        BrowseTheWebSynchronously.playwright = None

    @pytest.fixture()
    def mock_playwright(self):
        yield mock.MagicMock(spec=Playwright)

    @pytest.fixture()
    def mock_browser(self):
        yield mock.MagicMock(spec=Browser)

    def test_can_be_instantiated(self, mock_playwright, mock_browser):
        btws1 = BrowseTheWebSynchronously.using(mock_playwright, mock_browser)
        btws2 = BrowseTheWebSynchronously.using_chromium()
        btws3 = BrowseTheWebSynchronously.using_firefox()
        btws4 = BrowseTheWebSynchronously.using_webkit()

        assert isinstance(btws1, BrowseTheWebSynchronously)
        assert isinstance(btws2, BrowseTheWebSynchronously)
        assert isinstance(btws3, BrowseTheWebSynchronously)
        assert isinstance(btws4, BrowseTheWebSynchronously)
        assert BrowseTheWebSynchronously.playwright is mock_playwright

    def test_implements_protocol(self, mock_browser):
        assert isinstance(BrowseTheWebSynchronously(mock_browser), Forgettable)

    def test_sets_class_attribute(self, mock_playwright, mock_browser):
        BrowseTheWebSynchronously.using(mock_playwright, mock_browser)

        assert BrowseTheWebSynchronously.playwright is mock_playwright

    def test_can_have_separate_instance_attribute(self, mock_playwright, mock_browser):
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
