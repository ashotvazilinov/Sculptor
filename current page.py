from playwright.sync_api import sync_playwright, expect, Page
from playwright_utils import *
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


        Sculptor_settings_tab = ('//span[contains(text(), "Sculptor Settings")]')
        Fields_and_layouts = ('//a[contains(text(), "Fields and Layouts")]')
        Sculptor_settings_QLI_VAT = ("//div[@role='group' and .//*[text()='Quote Builder Fields']]//*[text()='VAT Percent']") # ('//div[normalize-space(text())="Sidebar Product Fields"]/ancestor::div[contains(@part, "dual-listbox")]//span[text()="Active"]')
        Sculptor_settings_QLI_VAT_move_right = ("//div[text()='Quote Builder Fields']//following::button[contains(@title, 'Move')][1]")
        
        Sculptor_settings_Quote_VAT = ("//div[@role='group' and .//*[text()='Quote Fields for Quote Details']]//*[text()='VAT Percent']") # ('//div[normalize-space(text())="Sidebar Product Fields"]/ancestor::div[contains(@part, "dual-listbox")]//span[text()="Active"]')
        Sculptor_settings_Quote_VAT_move_right = ("//div[text()='Quote Fields for Quote Details']//following::button[contains(@title, 'Move')][1]")
        
        Sculptor_settings_Save_Success_message = ("//*[text()='Configurations successfully updated']")
        Save_Button = ("(//button[contains(text(), 'Save')])[last()]")
        page.wait_for_selector(Sculptor_settings_Quote_VAT, state='visible')
        page.click(Sculptor_settings_Quote_VAT)
        page.wait_for_selector(Sculptor_settings_Quote_VAT_move_right, state='visible')
        page.click(Sculptor_settings_Quote_VAT_move_right)
        

        page.wait_for_selector(Save_Button, state='visible')
        page.click(Save_Button)

        page.wait_for_selector(Sculptor_settings_Save_Success_message, state='visible')






# Start
if __name__ == "__main__":
    unique_number = 33 
    run_current_tasks(unique_number)