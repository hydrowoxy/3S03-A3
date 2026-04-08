import pytest
from playwright.sync_api import sync_playwright, expect

URL = "https://the-internet.herokuapp.com/dropdown"
# run with pytest test_dropdown.py -v

@pytest.fixture
def page():
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_context().new_page()
        yield pg
        b.close()


def test_default_dropdown_state(page):
    page.goto(URL)

    dropdown = page.locator("#dropdown")
    expect(dropdown).to_have_value("")   # placeholder selected by default  


def test_select_first_option(page):
    page.goto(URL)

    page.select_option("#dropdown", "1")
    expect(page.locator("#dropdown")).to_have_value("1")


def test_select_second_option(page):
    page.goto(URL)

    page.select_option("#dropdown", "2")
    expect(page.locator("#dropdown")).to_have_value("2")


def test_switch_between_options(page):
    page.goto(URL)

    page.select_option("#dropdown", "1")
    page.select_option("#dropdown", "2")

    expect(page.locator("#dropdown")).to_have_value("2")


def test_reselect_same_option(page):
    page.goto(URL)

    page.select_option("#dropdown", "1")
    page.select_option("#dropdown", "1")

    expect(page.locator("#dropdown")).to_have_value("1")