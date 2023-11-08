from unittest import mock

import pytest
from playwright.sync_api import Browser, Playwright
from screenpy.protocols import Forgettable

from screenpy_playwright.abilities import BrowseTheWebSynchronously


class TestBrowseTheWebSynchronously:
    mock_path = "screenpy_playwright.abilities.browse_the_web_synchronously"

    @pytest.fixture(scope="class", autouse=True)
    def clean_up_ability(self):
        """Reset the class's playwright attribute to None."""
        yield
        BrowseTheWebSynchronously.playwright = None

    def test_can_be_instantiated(self):
        btws = BrowseTheWebSynchronously.using(None, None)

        assert isinstance(btws, BrowseTheWebSynchronously)

    def test_implements_protocol(self):
        assert isinstance(BrowseTheWebSynchronously(None, None), Forgettable)

    def test_sets_class_attribute(self):
        BrowseTheWebSynchronously.playwright = None
        mock_playwright = mock.MagicMock(spec=Playwright)
        mock_browser = mock.MagicMock(spec=Browser)

        BrowseTheWebSynchronously.using(mock_playwright, mock_browser)

        try:
            assert BrowseTheWebSynchronously.playwright is mock_playwright
        finally:
            # teardown
            BrowseTheWebSynchronously.playwright = None

    def test_can_have_separate_instance_attribute(self):
        mock_playwright1 = mock.MagicMock(spec=Playwright)
        mock_playwright2 = mock.MagicMock(spec=Playwright)
        mock_browser = mock.MagicMock(spec=Browser)
        mock_sync_playwright = mock.MagicMock()
        mock_sync_playwright.return_value.start.return_value = mock_playwright1

        with mock.patch(f"{self.mock_path}.sync_playwright", mock_sync_playwright):
            BrowseTheWebSynchronously.using_firefox()  # sets class playwright
            btws = BrowseTheWebSynchronously.using(mock_playwright2, mock_browser)

        try:
            assert BrowseTheWebSynchronously.playwright is mock_playwright1
            assert btws.playwright is mock_playwright2
        finally:
            # teardown
            BrowseTheWebSynchronously.playwright = None
