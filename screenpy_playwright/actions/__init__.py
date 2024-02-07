"""Actions enabled by the Abilities in ScreenPy: Playwright."""

from .click import Click
from .enter import Enter
from .open import Open

# Natural-language-enabling syntactic sugar
Visit = Open


__all__ = [
    "Click",
    "Enter",
    "Open",
    "Visit",
]
