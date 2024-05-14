import screenpy_playwright


def test_screenpy_playwright() -> None:
    expected = [
        "Attribute",
        "BrowserURL",
        "BrowseTheWebSynchronously",
        "Click",
        "Element",
        "Enter",
        "IsVisible",
        "NoPageError",
        "Number",
        "Open",
        "PageObject",
        "RefreshThePage",
        "SaveScreenshot",
        "Select",
        "Target",
        "TargetingError",
        "Text",
        "Visible",
        "Visit",
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
        "Enter",
        "Open",
        "RefreshThePage",
        "SaveScreenshot",
        "Select",
        "Visit",
    ]
    assert sorted(screenpy_playwright.actions.__all__) == sorted(expected)


def test_questions() -> None:
    expected = [
        "Attribute",
        "BrowserURL",
        "Element",
        "Number",
        "Text",
    ]
    assert sorted(screenpy_playwright.questions.__all__) == sorted(expected)


def test_resolutions() -> None:
    expected = [
        "IsVisible",
        "Visible",
    ]
    assert sorted(screenpy_playwright.resolutions.__all__) == sorted(expected)
