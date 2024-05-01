import screenpy_playwright


def test_screenpy_playwright() -> None:
    expected = [
        "Attribute",
        "BrowseTheWebSynchronously",
        "Click",
        "Enter",
        "Number",
        "Open",
        "PageObject",
        "SaveScreenshot",
        "Select",
        "Target",
        "TargetingError",
        "Text",
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
        "SaveScreenshot",
        "Select",
        "Visit",
    ]
    assert sorted(screenpy_playwright.actions.__all__) == sorted(expected)


def test_questions() -> None:
    expected = [
        "Attribute",
        "Number",
        "Text",
    ]
    assert sorted(screenpy_playwright.questions.__all__) == sorted(expected)
