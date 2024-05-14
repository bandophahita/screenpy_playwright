import os
from typing import cast
from unittest import mock

import pytest
from screenpy import Actor, Describable, Performable, UnableToAct

from screenpy_playwright import (
    BrowseTheWebSynchronously,
    Click,
    Enter,
    RefreshThePage,
    SaveScreenshot,
    Select,
    Visit,
)

from .useful_mocks import get_mock_target_class, get_mocked_target_and_locator

FakeTarget = get_mock_target_class()
TARGET = FakeTarget()


class TestClick:
    def test_can_be_instantiated(self) -> None:
        c1 = Click(TARGET)
        c2 = Click.on_the(TARGET)

        assert isinstance(c1, Click)
        assert isinstance(c2, Click)

    def test_implements_protocol(self) -> None:
        c = Click(TARGET)

        assert isinstance(c, Describable)
        assert isinstance(c, Performable)

    def test_describe(self) -> None:
        target = FakeTarget()
        target._description = "The Holy Hand Grenade"

        assert Click(target).describe() == f"Click on the {target}."

    def test_perform_click(self, Tester: Actor) -> None:
        target, locator = get_mocked_target_and_locator()

        Click(target, delay=0.5).perform_as(Tester)

        target.found_by.assert_called_once_with(Tester)
        locator.click.assert_called_once_with(delay=0.5)


class TestEnter:
    def test_can_be_instantiated(self) -> None:
        e1 = Enter("")
        e2 = Enter.the_text("")
        e3 = Enter.the_secret("")
        e4 = Enter.the_text("").into_the(TARGET)

        assert isinstance(e1, Enter)
        assert isinstance(e2, Enter)
        assert isinstance(e3, Enter)
        assert isinstance(e4, Enter)

    def test_implements_protocol(self) -> None:
        e = Enter("")

        assert isinstance(e, Describable)
        assert isinstance(e, Performable)

    def test_describe(self) -> None:
        target = FakeTarget()
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
        target, locator = get_mocked_target_and_locator()
        text = "I wanna be, the very best."

        Enter(text, force=True).into_the(target).perform_as(Tester)

        target.found_by.assert_called_once_with(Tester)
        locator.fill.assert_called_once_with(text, force=True)


class TestRefreshThePage:
    def test_can_be_instantiated(self) -> None:
        r1 = RefreshThePage()

        assert isinstance(r1, RefreshThePage)

    def test_implements_protocol(self) -> None:
        r = RefreshThePage()

        assert isinstance(r, Describable)
        assert isinstance(r, Performable)

    def test_describe(self) -> None:
        assert RefreshThePage().describe() == "Refresh the page."

    def test_perform_refresh(self, Tester: Actor) -> None:
        current_page = mock.Mock()
        btws = Tester.ability_to(BrowseTheWebSynchronously)
        btws.pages.append(current_page)
        btws.current_page = current_page

        RefreshThePage(timeout=20).perform_as(Tester)

        current_page.reload.assert_called_once_with(timeout=20)


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

        with mock.patch(f"{self.class_path}.Path", autospec=True) as mocked_path:
            SaveScreenshot(test_path).and_attach_it(**test_kwargs).perform_as(Tester)

        mocked_attachthefile.assert_called_once_with(test_path, **test_kwargs)
        mocked_path(test_path).write_bytes.assert_called_once()

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


class TestSelect:
    def test_can_be_instantiated(self) -> None:
        s1 = Select("option")
        s2 = Select.the_option("option")
        s3 = Select.the_option("option").from_the(TARGET)

        assert isinstance(s1, Select)
        assert isinstance(s2, Select)
        assert isinstance(s3, Select)

    def test_implements_protocol(self) -> None:
        s = Select("option")

        assert isinstance(s, Describable)
        assert isinstance(s, Performable)

    def test_describe(self) -> None:
        target = FakeTarget()
        target._description = "The Holy Hand Grenade"
        option = "option"
        s1 = Select(option).from_the(target)
        s2 = Select(option, option).from_the(target)

        assert s1.describe() == f"Select '{option}' from the {target}."
        assert s2.describe() == f"Select '{option}', '{option}' from the {target}."

    def test_perform_select(self, Tester: Actor) -> None:
        target, locator = get_mocked_target_and_locator()
        option = "option"

        Select(option, no_wait_after=True).from_the(target).perform_as(Tester)

        target.found_by.assert_called_once_with(Tester)
        locator.select_option.assert_called_once_with((option,), no_wait_after=True)

    def test_raises_with_no_target(self, Tester: Actor) -> None:
        with pytest.raises(UnableToAct):
            Select("option").perform_as(Tester)


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

        Visit(url, wait_until="commit").perform_as(Tester)

        mock_new_page_func = cast(mock.Mock, mock_browser.new_page)
        mock_new_page_func.assert_called_once()
        mock_page = mock_new_page_func.return_value
        mock_page.goto.assert_called_once_with(url, wait_until="commit")
        assert mock_ability.current_page == mock_page
        assert mock_page in mock_ability.pages
