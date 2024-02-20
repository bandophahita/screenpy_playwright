import os
from typing import cast
from unittest import mock

import pytest
from screenpy import Actor, Describable, Performable, UnableToAct

from screenpy_playwright import (
    BrowseTheWebSynchronously,
    Click,
    Enter,
    SaveScreenshot,
    Visit,
)

from .useful_mocks import get_mocked_target_and_element


class TestClick:
    def test_can_be_instantiated(self) -> None:
        target, _ = get_mocked_target_and_element()

        c1 = Click(target)
        c2 = Click.on_the(target)

        assert isinstance(c1, Click)
        assert isinstance(c2, Click)

    def test_implements_protocol(self) -> None:
        target, _ = get_mocked_target_and_element()

        c = Click(target)

        assert isinstance(c, Describable)
        assert isinstance(c, Performable)

    def test_describe(self) -> None:
        target, _ = get_mocked_target_and_element()
        target._description = "The Holy Hand Grenade"

        assert Click(target).describe() == f"Click on the {target}."

    def test_perform_click(self, Tester: Actor) -> None:
        target, element = get_mocked_target_and_element()

        Click.on_the(target).perform_as(Tester)

        target.found_by.assert_called_once_with(Tester)
        element.click.assert_called_once()


class TestEnter:
    def test_can_be_instantiated(self) -> None:
        target, _ = get_mocked_target_and_element()

        e1 = Enter("")
        e2 = Enter.the_text("")
        e3 = Enter.the_secret("")
        e4 = Enter.the_text("").into_the(target)

        assert isinstance(e1, Enter)
        assert isinstance(e2, Enter)
        assert isinstance(e3, Enter)
        assert isinstance(e4, Enter)

    def test_implements_protocol(self) -> None:
        e = Enter("")

        assert isinstance(e, Describable)
        assert isinstance(e, Performable)

    def test_describe(self) -> None:
        target, _ = get_mocked_target_and_element()
        target._description = "Sir Robin ran away away, brave brave Sir Robin!"
        text = "Sir Robin ran away!"

        description = Enter.the_text(text).into_the(target).describe()

        assert description == f'Enter "{text}" into the {target}.'

    def test_secret_is_masked(self) -> None:
        e = Enter.the_secret("The master sword")

        assert e.text != e.text_to_log
        assert "CENSORED" in e.text_to_log

    def test_complains_for_no_target(self, Tester: Actor) -> None:
        with pytest.raises(UnableToAct):
            Enter.the_text("").perform_as(Tester)

    def test_perform_enter(self, Tester: Actor) -> None:
        target, element = get_mocked_target_and_element()
        text = "I wanna be, the very best."

        Enter.the_text(text).into_the(target).perform_as(Tester)

        target.found_by.assert_called_once_with(Tester)
        element.fill.assert_called_once_with(text)


class TestSaveScreenshot:

    class_path = "screenpy_playwright.actions.save_screenshot"

    def test_can_be_instantiated(self) -> None:
        ss1 = SaveScreenshot("./screenshot.png")
        ss2 = SaveScreenshot.as_("./screenshot.png")
        ss3 = SaveScreenshot.as_("./screenshot.png").and_attach_it()
        ss4 = SaveScreenshot.as_("./a_witch.png").and_attach_it(me="newt")

        assert isinstance(ss1, SaveScreenshot)
        assert isinstance(ss2, SaveScreenshot)
        assert isinstance(ss3, SaveScreenshot)
        assert isinstance(ss4, SaveScreenshot)

    def test_implements_protocol(self) -> None:
        ss = SaveScreenshot("./screenshot.png")

        assert isinstance(ss, Describable)
        assert isinstance(ss, Performable)

    def test_filepath_vs_filename(self) -> None:
        test_name = "mmcmanus.png"
        test_path = f"boondock/saints/{test_name}"

        ss = SaveScreenshot.as_(test_path)

        assert ss.path == test_path
        assert ss.filename == test_name

    @mock.patch(f"{class_path}.AttachTheFile", autospec=True)
    def test_perform_sends_kwargs_to_attach(
        self, mocked_attachthefile: mock.Mock, Tester: Actor
    ) -> None:
        test_path = "souiiie.png"
        test_kwargs = {"color": "Red", "weather": "Tornado"}
        current_page = mock.Mock()
        btws = Tester.ability_to(BrowseTheWebSynchronously)
        btws.pages.append(current_page)
        btws.current_page = current_page

        with mock.patch(f"{self.class_path}.Path") as mocked_path:
            SaveScreenshot(test_path).and_attach_it(**test_kwargs).perform_as(Tester)

        mocked_attachthefile.assert_called_once_with(test_path, **test_kwargs)
        mocked_path().write_bytes.assert_called_once()

    def test_describe(self) -> None:
        assert SaveScreenshot("pth").describe() == "Save screenshot as pth"

    def test_subclass(self) -> None:
        """test code for mypy to scan without issue"""

        class SubSaveScreenshot(SaveScreenshot):
            pass

        sss1 = SubSaveScreenshot("./screenshot.png")
        sss2 = SubSaveScreenshot.as_("./screenshot.png")
        sss3 = SubSaveScreenshot.as_("./screenshot.png").and_attach_it()

        assert isinstance(sss1, SubSaveScreenshot)
        assert isinstance(sss2, SubSaveScreenshot)
        assert isinstance(sss3, SubSaveScreenshot)


class TestVisit:
    def test_can_be_instantiated(self) -> None:
        v = Visit("")

        assert isinstance(v, Visit)

    def test_implements_protocol(self) -> None:
        v = Visit("")

        assert isinstance(v, Describable)
        assert isinstance(v, Performable)

    def test_describe(self) -> None:
        url = "https://very.secure.url/ssl"

        assert Visit(url).describe() == f"Visit {url}"

    @mock.patch.dict(os.environ, {"BASE_URL": "https://base.url"})
    def test_environment_base_url(self) -> None:
        assert Visit("/path").url == "https://base.url/path"

    def test_using_page_object(self) -> None:
        class PageObject:
            url = "https://page.object.url/"

        assert Visit(PageObject()).url == "https://page.object.url/"

    @mock.patch.dict(os.environ, {"BASE_URL": "https://base.url"})
    def test_environment_base_and_page_object_url(self) -> None:
        class PageObject:
            url = "/popath"

        assert Visit(PageObject()).url == "https://base.url/popath"

    def test_perform_visit(self, Tester: Actor) -> None:
        url = "https://example.org/itsdotcom"
        mock_ability = Tester.ability_to(BrowseTheWebSynchronously)
        mock_browser = mock_ability.browser

        Visit(url).perform_as(Tester)

        mock_new_page_func = cast(mock.Mock, mock_browser.new_page)
        mock_new_page_func.assert_called_once()
        mock_page = mock_new_page_func.return_value
        mock_page.goto.assert_called_once_with(url)
        assert mock_ability.current_page == mock_page
        assert mock_page in mock_ability.pages
