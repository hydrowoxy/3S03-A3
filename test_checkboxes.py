import pytest
from playwright.sync_api import sync_playwright, expect

URL = "https://the-internet.herokuapp.com/checkboxes"
# run with pytest test_checkboxes.py -v

@pytest.fixture
def page():
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_context().new_page()
        yield pg
        b.close()


def test_initial_checkbox_states(page):
    page.goto(URL)

    boxes = page.locator("input[type=checkbox]")

    expect(boxes.nth(0)).not_to_be_checked()
    expect(boxes.nth(1)).to_be_checked()


def test_check_first_checkbox(page):
    page.goto(URL)

    box = page.locator("input[type=checkbox]").nth(0)
    box.check()

    expect(box).to_be_checked()


def test_uncheck_second_checkbox(page):
    page.goto(URL)

    box = page.locator("input[type=checkbox]").nth(1)
    box.uncheck()

    expect(box).not_to_be_checked()


def test_toggle_twice_returns_original(page):
    page.goto(URL)

    box = page.locator("input[type=checkbox]").nth(0)

    box.check()
    box.uncheck()

    expect(box).not_to_be_checked()


def test_both_checkboxes_checked(page):
    page.goto(URL)

    boxes = page.locator("input[type=checkbox]")

    boxes.nth(0).check()
    boxes.nth(1).check()

    expect(boxes.nth(0)).to_be_checked()
    expect(boxes.nth(1)).to_be_checked()