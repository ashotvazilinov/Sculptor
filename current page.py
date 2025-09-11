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
import pytest
from playwright.sync_api import sync_playwright, Page
from salesforce_utils import *

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --remote-debugging-address=127.0.0.1 --no-first-run --user-data-dir="C:\Temp\ChromeDebugProfile"

# set PWDEBUG=1 && python "D:\vs code\Sculptor\current page.py"

# Automation in Salesforce API
sf = Salesforce(username=config.LOGIN, password=config.PASSWORD, security_token=config.SECURITY_TOKEN)

# Main function
def run_current_tasks(unique_number: int = 33):
    with sync_playwright() as p:
        # Connect to the existing browser instance
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]  # Using the first context
        page = context.pages[0]  # Taking the first tab


        page.wait_for_selector(Sculptor_settings_tab, state='visible')
        page.click(Sculptor_settings_tab)
        page.wait_for_selector(Fields_and_layouts, state='visible')
        page.click(Fields_and_layouts)
        li_group = page.locator(Sculptor_settings_Product_sidebar_group_li_count)#convert to locator

        
        li_group.first.wait_for(state='visible')#wait for elements to be visible


        while li_group.count() > 1: #while there are more than 1 element, click and move to left
            li_group.nth(-1).click()
            page.click(Sculptor_settings_Product_sidebar_group_move_left)

        page.wait_for_selector(Sculptor_settings_Product_sidebar_group_active, state='visible')
        page.click(Sculptor_settings_Product_sidebar_group_active) #select avitve

        page.wait_for_selector(Sculptor_settings_Product_sidebar_group_move_right, state='visible')
        page.click(Sculptor_settings_Product_sidebar_group_move_right)#move active to right

        page.wait_for_selector(Save_Button, state='visible')
        page.click(Save_Button)#save

        page.wait_for_selector(Sculptor_settings_Save_Success_message, state='visible')
        page.click(Sculptor_settings_Save_Success_message)#check if it is saved
        print("Active grouping is set successfully")

        page.wait_for_selector(Bundle_builder_tab, state='visible')
        page.click(Bundle_builder_tab)#go to bundle builder
        print("Bundle Builder tab is opened")

        try:
            if page.locator(BB_Active_exists).is_visible():
                print("Active exists, go on.")
            else:
                raise Exception("Active not found")  
        except:
            print("Active not found — lets set Price Book.")
            page.wait_for_selector(f"{BB_Price_book_needs_to_be_selected} | {BB_No_Products_were_found}", state="visible")
            print("Price book needs to be selected")
            if page.locator(f"{BB_Price_book_needs_to_be_selected} | {BB_No_Products_were_found}").count() > 0:
                print(">0")
                page.wait_for_selector("//c-cpq-menu-sub[@class='cpq-search cpq-search-button']", state='visible')
                page.click("//c-cpq-menu-sub[@class='cpq-search cpq-search-button']")
                pricebook_locator = page.locator("//span[@title='Pricebook']")
                pricebook_locator.hover()
                page.wait_for_selector("//span[@title='Standard Price Book']", state='visible')
                page.click("//span[@title='Standard Price Book']")
                time.sleep(2)



# Start
if __name__ == "__main__":
    unique_number = 33 
    run_current_tasks(unique_number)


