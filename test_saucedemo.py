import re
import pytest
from playwright.sync_api import sync_playwright, expect

BASE_URL = "https://www.saucedemo.com/"
# run with pytest test_saucedemo.py -v


@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        pg = context.new_page()
        yield pg
        browser.close()


def login(page, username="standard_user", password="secret_sauce"):
    page.goto(BASE_URL)
    page.fill("#user-name", username)
    page.fill("#password", password)
    page.click("#login-button")


def test_complete_purchase_flow(page):
    login(page)

    # Display products
    expect(page).to_have_url(re.compile(r"/inventory"))
    expect(page.locator(".inventory_item")).to_have_count(6)

    # Sort products by price
    page.select_option(".product_sort_container", "lohi")
    prices = [
        float(item.inner_text().replace("$", ""))
        for item in page.locator(".inventory_item_price").all()
    ]
    assert prices == sorted(prices)

    # Add items to cart
    page.click("#add-to-cart-sauce-labs-bike-light")
    page.click("#add-to-cart-sauce-labs-backpack")
    expect(page.locator(".shopping_cart_badge")).to_have_text("2")

    # Remove an item from cart
    page.click("#remove-sauce-labs-backpack")
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")

    # Go to cart
    page.click(".shopping_cart_link")
    expect(page).to_have_url(re.compile(r"/cart"))
    expect(page.locator(".cart_item")).to_have_count(1)

    # Click checkout
    page.click("#checkout")

    # Enter shipping details
    page.fill("#first-name", "Test")
    page.fill("#last-name", "User")
    page.fill("#postal-code", "12345")
    page.click("#continue")

    # Review order
    expect(page).to_have_url(re.compile(r"/checkout-step-two"))
    subtotal = float(page.locator(".summary_subtotal_label").inner_text().split("$")[1])
    tax = float(page.locator(".summary_tax_label").inner_text().split("$")[1])
    total = float(page.locator(".summary_total_label").inner_text().split("$")[1])
    assert round(subtotal + tax, 2) == round(total, 2)

    # Click finish
    page.click("#finish")

    # Display confirmation
    expect(page).to_have_url(re.compile(r"/checkout-complete"))
    expect(page.locator(".complete-header")).to_contain_text("Thank you")

    # Click back home and log out
    page.click("#back-to-products")
    expect(page).to_have_url(re.compile(r"/inventory"))
    page.click("#react-burger-menu-btn")
    page.click("#logout_sidebar_link")
    expect(page).to_have_url(BASE_URL)


def test_invalid_user_displays_error(page):
    login(page, username="locked_out_user")
    expect(page.locator("[data-test=error]")).to_be_visible()


def test_checkout_with_missing_fields_displays_error(page):
    login(page)

    page.click("#add-to-cart-sauce-labs-bike-light")
    page.click(".shopping_cart_link")
    page.click("#checkout")

    # Fields not filled
    page.click("#continue")

    expect(page.locator("[data-test=error]")).to_be_visible()


def test_cancel_checkout_returns_to_cart(page):
    login(page)

    page.click("#add-to-cart-sauce-labs-bike-light")
    page.click(".shopping_cart_link")
    page.click("#checkout")

    # Cancel branch
    page.click("#cancel")

    expect(page).to_have_url(re.compile(r"/cart"))
    expect(page.locator(".cart_item")).to_have_count(1)