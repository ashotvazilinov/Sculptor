# conftest.py
import pytest
from playwright.sync_api import sync_playwright, Page
from salesforce_utils import *
import config
import os
import shutil
from datetime import datetime
import time
@pytest.fixture(scope="function")
def page2(request):
    unique_number = getattr(request, "param", None)
    if unique_number is None:
        raise ValueError("The test should provide a value for the unique_number through parameterization.")
    
    with sync_playwright() as p:
        try:
            sf = connect_to_salesforce()
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
            record_video_dir=config.VIDEO_DIR,
            record_video_size={"width": 1920, "height": 1080}
            )
            page = context.new_page()
            page.set_viewport_size({"width": 1920, "height": 1080})

            page.goto(config.SITE_URL)
            username_input = page.locator('input[id="username"]')
            password_input = page.locator('input[id="password"]')
            username_input.fill(config.LOGIN)
            password_input.fill(config.PASSWORD)
            page.press('input[id="password"]', 'Enter')
            
            page.wait_for_selector('button[title="App Launcher"]', state='visible')
            time.sleep(1)
            page.click('button[title="App Launcher"]')

            page.fill('input.slds-input[placeholder="Search apps and items..."]', 'Sculptor CPQ')
            page.wait_for_selector('text="Sculptor CPQ"', state='visible')
            time.sleep(1)
            page.click('text="Sculptor CPQ"')
            context.tracing.start(screenshots=True, snapshots=True, sources=True)
            time.sleep(1)

            yield page, unique_number

        finally:
            # First, we complete the tracing
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 
            trace_path = f"{config.TRACING_DIR}/{request.node.name}_{current_time}.zip"
            context.tracing.stop(path=trace_path)
            
            video_path = page.video.path()

            # Then we close the page and the browser.
            page.close()
            context.close() 
            browser.close()
            
            # Deleting the test data
            delete_test_opportunity_salesforce(sf, unique_number)
            delete_test_bundles_salesforce(sf, unique_number)
            delete_test_quote_salesforce(sf, unique_number)
            

            new_video_name = f"{request.node.name}_{current_time}.webm"
            new_video_path = os.path.join(config.VIDEO_DIR, new_video_name)

            shutil.move(video_path, new_video_path)
            
            # Closing the Salesforce session if it is open
            if hasattr(sf, 'session_id'):
                sf.session.close()

def pytest_unconfigure():
    """A function executed after all tests are completed."""
    """Renaming the HTML report AFTER it is actually recorded."""
    reports_dir = config.REPORT_DIR
    original_report = os.path.join(reports_dir, "report.html")

    if os.path.exists(original_report):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        new_name = f"report_{timestamp}.html"
        new_path = os.path.join(reports_dir, new_name)

        os.rename(original_report, new_path) #rename of report
        print(f"\n[INFO] The HTML report has been renamed to: {new_name}")

