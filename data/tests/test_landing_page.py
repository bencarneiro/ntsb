import re
from playwright.sync_api import Page, expect


def test_homepage_to_accident_details(playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://roadway.report/")
    page.get_by_role("link", name="Roadway Report: The").click()
    
    page.locator(".leaflet-marker-icon").first.click()
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="Details Here").click()
    page1 = page1_info.value
    page1.get_by_role("heading", name="Comments / Obituaries / Links").click()

    # ---------------------
    context.close()
    browser.close()


def test_date_selectors(playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://roadway.report/")
    page.get_by_role("link", name="Roadway Report: The").click()
    page.locator(".leaflet-marker-icon").first.click()
    page.locator("#input-control-date-picker1").fill("2009-01-01")
    page.locator("#input-control-date-picker2").fill("2015-01-01")
    page.locator(".leaflet-marker-icon").first.click()
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="Details Here").click()
    # ---------------------
    context.close()
    browser.close()