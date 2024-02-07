import os
from unittest import mock

import pytest
from screenpy import Actor, Describable, Performable, UnableToAct

from screenpy_playwright import BrowseTheWebSynchronously, Click, Enter, Visit

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

        mock_browser.new_page.assert_called_once()
        mock_page = mock_browser.new_page.return_value
        mock_page.goto.assert_called_once_with(url)
        assert mock_ability.current_page == mock_page
        assert mock_page in mock_ability.pages
