import re
from playwright.sync_api import Page, expect


def test_chromium_access(playwright) -> None:
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

def test_safari_access(playwright) -> None:
    browser = playwright.webkit.launch(headless=False)
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

def test_firefox_access(playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
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


def test_iphone_access(playwright) -> None:
    iphone_13 = playwright.devices['iPhone 13']
    browser = playwright.webkit.launch(headless=False)
    context = browser.new_context(
        **iphone_13,
    )
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


def test_android_access(playwright) -> None:
    pixel = playwright.devices['Pixel 5']
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        **pixel,
    )
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



# this test exists because there was an issue in safari where clicking the map would send two api requests instead of 1
def test_double_click(playwright) -> None:

    iphone_13 = playwright.devices['iPhone 13']
    browser = playwright.webkit.launch(headless=False)
    context = browser.new_context(**iphone_13)
    page = context.new_page()
    page.on("console", lambda msg: print(f"error: {msg.text}"))
    page.goto("http://127.0.0.1:8000/")
    page.get_by_role("link", name="Roadway Report: The").click()
    page.locator(".leaflet-marker-icon").first.click()
    page.locator("#input-control-date-picker1").fill("2009-01-01")
    # page.locator("#input-control-date-picker2").fill("2015-01-01")
    page.locator(".leaflet-marker-icon").first.click()
    page.locator("#input-control-date-picker2").fill("2015-01-01")
    page.locator(".leaflet-marker-icon").first.click()
    page.locator(".leaflet-container").click()
    page.on("console", lambda msg: print(f"error: {msg.text}"))
    page.locator(".leaflet-marker-icon").first.click()
    # with page.expect_popup() as page1_info:
    #     page.get_by_role("link", name="Details Here").click()
    # ---------------------
    context.close()
    browser.close()

