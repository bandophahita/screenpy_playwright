from __future__ import annotations

from unittest import mock

from playwright.sync_api import Browser, Locator, Playwright

from screenpy_playwright import Target


def get_mocked_target_and_element() -> tuple[mock.Mock, mock.Mock]:
    """Get a mocked target which finds a mocked element."""
    target = mock.Mock(spec=Target)
    element = mock.Mock(spec=Locator)
    target.found_by.return_value = element

    return target, element


def get_mocked_playwright_and_browser() -> tuple[mock.Mock, mock.Mock]:
    playwright = mock.Mock(spec=Playwright)
    browser = mock.Mock(spec=Browser)

    return playwright, browser
