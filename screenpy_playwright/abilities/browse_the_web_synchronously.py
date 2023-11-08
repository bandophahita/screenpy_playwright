from __future__ import annotations

from typing import TYPE_CHECKING

from playwright.sync_api import sync_playwright

if TYPE_CHECKING:
    from typing import TypeVar

    from playwright.sync_api import Browser, Page, Playwright

    SelfBrowseTheWebSynchronously = TypeVar(
        "SelfBrowseTheWebSynchronously", bound="BrowseTheWebSynchronously"
    )


class BrowseTheWebSynchronously:
    """Use a synchronous Playwright instance to browse the web.

    Examples::

        the_actor.can(BrowseTheWebSynchronously.using_firefox())

        the_actor.can(BrowseTheWebSynchronously.using_webkit())

        the_actor.can(BrowseTheWebSynchronously.using_chromium())

        the_actor.can(
            BrowseTheWebSynchronously.using(playwright, cust_browser)
        )
    """

    playwright: Playwright = None

    @classmethod
    def using(
        cls: type[SelfBrowseTheWebSynchronously],
        playwright: Playwright,
        browser: Browser,
    ) -> SelfBrowseTheWebSynchronously:
        """Supply a pre-defined Playwright browser to use."""
        return cls(playwright, browser)

    @classmethod
    def using_firefox(
        cls: type[SelfBrowseTheWebSynchronously],
    ) -> SelfBrowseTheWebSynchronously:
        """Use a synchronous Firefox browser."""
        if cls.playwright is None:
            cls.playwright = sync_playwright().start()
        browser = cls.playwright.firefox.launch()
        return cls(cls.playwright, browser)

    @classmethod
    def using_chromium(
        cls: type[SelfBrowseTheWebSynchronously],
    ) -> SelfBrowseTheWebSynchronously:
        """Use a synchronous Chromium (i.e. Chrome, Edge, Opera, etc.) browser."""
        cls.playwright = sync_playwright().start()
        browser = cls.playwright.chromium.launch()
        return cls(cls.playwright, browser)

    @classmethod
    def using_webkit(
        cls: type[SelfBrowseTheWebSynchronously],
    ) -> "BrowseTheWebSynchronously":
        """Use a synchronous WebKit (i.e. Safari, etc.) browser."""
        cls.playwright = sync_playwright().start()
        browser = cls.playwright.webkit.launch()
        return cls(cls.playwright, browser)

    def forget(self: SelfBrowseTheWebSynchronously) -> None:
        """Forget everything you knew about being a playwright."""
        self.browser.close()
        self.playwright.stop()
        self.__class__.playwright = None

    def __init__(
        self: SelfBrowseTheWebSynchronously,
        playwright: Playwright,
        browser: Browser,
    ) -> None:
        if self.__class__.playwright is None:
            self.__class__.playwright = playwright
        self.playwright = playwright
        self.browser = browser
        self.current_page: Page = None
        self.pages: Page = []
