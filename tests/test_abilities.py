from screenpy import Forgettable

from screenpy_playwright import BrowseTheWebSynchronously


class TestBrowseTheWebSynchronously:
    def test_can_be_instantiated(self) -> None:
        b = BrowseTheWebSynchronously.using(None, None)

        assert isinstance(b, BrowseTheWebSynchronously)

    def test_implements_protocol(self) -> None:
        assert isinstance(BrowseTheWebSynchronously(None, None), Forgettable)
