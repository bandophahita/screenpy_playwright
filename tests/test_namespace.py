import screenpy_playwright


def test_screenpy_playwright() -> None:
    expected = [
        "Attribute",
        "BrowserURL",
        "BrowseTheWebSynchronously",
        "Click",
        "Clicks",
        "Element",
        "Enter",
        "Enters",
        "GoesTo",
        "GoTo",
        "IsVisible",
        "NoPageError",
        "Number",
        "Open",
        "Opens",
        "PageObject",
        "RefreshesThePage",
        "RefreshThePage",
        "SaveAScreenshot",
        "SavesAScreenshot",
        "SaveScreenshot",
        "SavesScreenshot",
        "Scroll",
        "Scrolls",
        "Select",
        "Selects",
        "Target",
        "TargetingError",
        "Text",
        "TheAttribute",
        "TheBrowserURL",
        "TheElement",
        "TheNumber",
        "TheText",
        "Visible",
        "Visit",
        "Visits",
    ]
    assert sorted(screenpy_playwright.__all__) == sorted(expected)


def test_abilities() -> None:
    expected = [
        "BrowseTheWebSynchronously",
    ]
    assert sorted(screenpy_playwright.abilities.__all__) == sorted(expected)


def test_actions() -> None:
    expected = [
        "Click",
        "Clicks",
        "Enter",
        "Enters",
        "GoTo",
        "GoesTo",
        "Open",
        "Opens",
        "RefreshThePage",
        "RefreshesThePage",
        "SaveScreenshot",
        "SaveAScreenshot",
        "SavesScreenshot",
        "SavesAScreenshot",
        "Scroll",
        "Scrolls",
        "Select",
        "Selects",
        "Visit",
        "Visits",
    ]
    assert sorted(screenpy_playwright.actions.__all__) == sorted(expected)


def test_questions() -> None:
    expected = [
        "Attribute",
        "BrowserURL",
        "Element",
        "Number",
        "Text",
        "TheAttribute",
        "TheBrowserURL",
        "TheElement",
        "TheNumber",
        "TheText",
    ]
    assert sorted(screenpy_playwright.questions.__all__) == sorted(expected)


def test_resolutions() -> None:
    expected = [
        "IsVisible",
        "Visible",
    ]
    assert sorted(screenpy_playwright.resolutions.__all__) == sorted(expected)
