from playwright.sync_api import sync_playwright, expect, Page
from Demo import *
from simple_salesforce import Salesforce  
from html_elements import *
import config
from datetime import datetime
import os
import shutil
import time
import pytest
from playwright.sync_api import sync_playwright, Page
from salesforce_utils import *

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --remote-debugging-address=127.0.0.1 --no-first-run --user-data-dir="C:\Temp\ChromeDebugProfile"

# set PWDEBUG=1 && python "D:\vs code\Sculptor\current page.py"

# Automation in Salesforce API
# sf = Salesforce(username=config.LOGIN, password=config.PASSWORD, security_token=config.SECURITY_TOKEN, domain=config.DOMAIN)

# Main function
def run_current_tasks(unique_number: int = 33):
    with sync_playwright() as p:
                # Connect to the existing browser instance
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]  # Using the first context
        page = context.pages[0]  # Taking the first tab
        '''write here'''

        accordion_buttons = page.locator('button[aria-controls^="lgt-accordion-section-"]')

        for i in range(accordion_buttons.count()):
            btn = accordion_buttons.nth(i)

            btn.wait_for(state="visible")

            if btn.get_attribute("aria-expanded") == "false":
                btn.click()

                
            print("accordeons are oppened")






# Start
if __name__ == "__main__":
    unique_number = 33 
    run_current_tasks(unique_number)