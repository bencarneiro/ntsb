import re
import csv
from playwright.sync_api import Page, expect

url = "https://www.michigantrafficcrashfacts.org/data/querytool/#q1;2;2015;;0,49:1,2/list/0,0:0,14:0,2:0,25:0,3:0,4:0,5:0,50:0,51:0,7:0,8:1,0:1,16:1,3:1,4:1,67:2,0:2,10:2,11:2,3:2,9%7C0%7C90"

def test_has_title(page: Page):
    year = 2015
    page.goto(url)


    pagination_data = page.get_by_text("Records").inner_html()
    start_row = int(pagination_data.split('="">')[1].split("</b>")[0].replace(",", ""))
    end_row = int(pagination_data.split('="">')[2].split("</b>")[0].replace(",", ""))
    total_records = int(pagination_data.split('="">')[3].split("</b>")[0].replace(",", ""))
    while end_row != total_records:
        print(f"{start_row} to {end_row} of {total_records}")
        with page.expect_download() as download_info:
            page.get_by_text("Export", exact=True).click()
            page.get_by_text("CSV", exact=True).click()

        download = download_info.value

        # Wait for the download process to complete and save the downloaded file somewhere
        download.save_as(f"data/crash_data_{year}__{start_row}_to_{end_row}_of_{total_records}.csv")
        # reset pagination tracking
        page.get_by_text("Next").click()
        page.wait_for_timeout(3000)
        pagination_data = page.get_by_text("Records").inner_html()
        start_row = int(pagination_data.split('="">')[1].split("</b>")[0].replace(",", ""))
        end_row = int(pagination_data.split('="">')[2].split("</b>")[0].replace(",", ""))
        total_records = int(pagination_data.split('="">')[3].split("</b>")[0].replace(",", ""))

    with page.expect_download() as download_info:
        page.get_by_text("Export", exact=True).click()
        page.get_by_text("CSV", exact=True).click()

    download = download_info.value

    # Wait for the download process to complete and save the downloaded file somewhere
    download.save_as(f"data/crash_data_{year}__{start_row}_to_{end_row}_of_{total_records}.csv")