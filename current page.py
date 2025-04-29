from playwright.sync_api import sync_playwright, expect, Page
from playwright_utils import *
from simple_salesforce import Salesforce  
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

# Авторизация в Salesforce API
sf = Salesforce(username=config.LOGIN, password=config.PASSWORD, security_token=config.SECURITY_TOKEN)

# Основная функция
def run_current_tasks(unique_number: int = 33):
    with sync_playwright() as p:
        # Подключаемся к открытому браузеру через CDP
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]  # Используем первый контекст
        page = context.pages[0]  # Берем первую открытую вкладку

        Product_Filter_exists = page.locator("//*[text()='Product.Product Name']")
        
        page.wait_for_selector("//c-cpq-sidebar-product-list//button[@title='Filter']", state='visible') #find filter
        page.click("//c-cpq-sidebar-product-list//button[@title='Filter']") #click on filter
        page.wait_for_selector("(//div[@sclp-cpqsidepanel_cpqsidepanel]//*[text()='Add Filter'])[1]", state='visible') #find Add Filter button
        if Product_Filter_exists.count() == 0: #if there is 0 filter we click on it
            page.click("(//div[@sclp-cpqsidepanel_cpqsidepanel]//*[text()='Add Filter'])[1]")
        else:
            pass
        page.click("//span[text()='Product.Product Name']")
        filter_Product_name = page.locator("//c-cpq-side-panel-filter-item//span[contains(text(), 'Product Name')]")
        filter_Operator_contains = page.locator("//c-cpq-side-panel-filter-item//span[contains(text(), 'CONTAINS')]")
        
        page.wait_for_selector("//c-cpq-side-panel-filter-item//input", state='visible')
        expect(filter_Product_name).to_be_visible()
        print('Field name Product Name is set by default')
        expect(filter_Operator_contains).to_be_visible()
        print('Operator is set to Contains by default')
        test_product = 'Boat regatta'
        page.fill("//c-cpq-side-panel-filter-item//input", f"{test_product}")
        page.click("button[title='Accept']")
        # page.type('input[placeholder="Products"]', f"{test_product}")
        All_Closed_Accordions = page.locator('//c-cpq-sidebar-product-list//button[@aria-expanded="false"]')
        First_Closed_Accordions = page.locator('//c-cpq-sidebar-product-list//button[@aria-expanded="false"]').nth(0)

        if All_Closed_Accordions.count() > 0:
            First_Closed_Accordions.click()
            print('accordion is expanded')
        else:
            pass
        page.wait_for_selector(f'//span[@sclp-cpqsidebarproductlistitem_cpqsidebarproductlistitem and @title="{test_product}"]', state='visible')
        expect(page.locator(f'//span[@sclp-cpqsidebarproductlistitem_cpqsidebarproductlistitem and @title="{test_product}"]')).to_be_visible()
        print(f"the Product {test_product} is found")
        products = page.locator("//span[@sclp-cpqsidebarproductlistitem_cpqsidebarproductlistitem][@class='slds-truncate cpq-list-item-name cpq-locked slds-col cpq-list-item-name-top']")
        expect(products).to_have_count(1)
        page.click('//c-cpq-sidebar-product-list//button[contains(text(), "Remove All")]')
        print("All the filters are removed")








# Запуск
if __name__ == "__main__":
    unique_number = 33 
    run_current_tasks(unique_number)

