"""Actions enabled by the Abilities in ScreenPy: Playwright."""

from .click import Click
from .enter import Enter
from .open import Open
from .refresh_the_page import RefreshThePage
from .save_screenshot import SaveScreenshot
from .scroll import Scroll
from .select import Select

# Natural-language-enabling syntactic sugar
Visit = Open


__all__ = [
    "Click",
    "Enter",
    "Open",
    "RefreshThePage",
    "SaveScreenshot",
    "Scroll",
    "Select",
    "Visit",
]
