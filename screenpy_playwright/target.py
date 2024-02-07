"""Represent an element on the page using its locator and a description."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .abilities import BrowseTheWebSynchronously
from .exceptions import TargetingError

if TYPE_CHECKING:
    from playwright.sync_api import Locator
    from screenpy import Actor


class Target:
    """A described element on a webpage.

    Examples::

        Target.the('"Log In" button').located_by("button:has-text('Log In')")

        Target.the("toast message").located_by("//toast")

        Target.the('"Pick up Milk" todo item").located_by(
            "_vue=list-item[text *= 'milk' i]"
        )

        Target().located_by("#enter-todo-field")
    """

    locator: str | None
    _description: str | None

    @staticmethod
    def the(name: str) -> Target:
        """Provide a human-readable description of the target."""
        return Target(name)

    def located_by(self, locator: str) -> Target:
        """Provide the Playwright locator which describes the element."""
        self.locator = locator
        return self

    @property
    def target_name(self) -> str:
        """Get the name of the Target.

        Returns:
            The text representation of this Target.
        """
        return self._description or self.locator or "None"

    @target_name.setter
    def target_name(self, value: str) -> None:
        """Set the target_name.

        Args:
            value: the new description to use.
        """
        self._description = value

    def found_by(self, the_actor: Actor) -> Locator:
        """Get the Playwright Locator described by this Target.

        Args:
            the_actor: the Actor who should find this Locator.

        Returns:
            The Locator which describes the element.
        """
        browse_the_web = the_actor.ability_to(BrowseTheWebSynchronously)
        if browse_the_web.current_page is None:
            msg = f"There is no active page! {the_actor} cannot find the {self}."
            raise TargetingError(msg)

        return browse_the_web.current_page.locator(self.locator)

    def __repr__(self) -> str:
        """Get a human-readable representation of this Target.

        Returns:
            A string representing this Target.
        """
        return self.target_name

    def __init__(self, name: str | None = None) -> None:
        self._description = name
        self.locator = None
