from __future__ import annotations

from typing import TYPE_CHECKING, cast
from unittest import mock

from playwright.sync_api import Browser, Locator, Playwright

from screenpy_playwright import BrowseTheWebSynchronously, Target

if TYPE_CHECKING:
    from screenpy import Actor


def get_mocked_locator() -> mock.Mock:
    return mock.create_autospec(Locator, instance=True)


def get_mock_target_class() -> mock.Mock:
    class FakeTarget(Target):
        def __new__(cls, *args: object, **kwargs: object) -> FakeTarget:  # noqa: ARG003
            return mock.create_autospec(FakeTarget, instance=True)

    return cast(mock.Mock, FakeTarget)


def get_mocked_target_and_locator() -> tuple[mock.Mock, mock.Mock]:
    """Get a mocked target which finds a mocked element."""
    target = get_mock_target_class().the("test object").located_by("test locator")
    locator = get_mocked_locator()
    target.found_by.return_value = locator

    return target, locator


def get_mocked_browser(actor: Actor) -> mock.Mock:
    return cast(mock.Mock, actor.ability_to(BrowseTheWebSynchronously).browser)


def get_mocked_playwright_and_browser() -> tuple[mock.Mock, mock.Mock]:
    playwright = mock.Mock(spec=Playwright)
    browser = mock.Mock(spec=Browser)

    return playwright, browser
