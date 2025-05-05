# Sculptor_Unit_Tests.py
import time
from playwright.sync_api import sync_playwright, expect, Page
from html_elements import *
import config


def Bundle_contains_of_three_sections(page, unique_number):
    page.wait_for_selector('text="Bundle Builder"', state='visible')
    page.click('text="Bundle Builder"')
    right_sidebar = page.locator("//c-cpq-sidebar[@sclp-cpqapp_cpqapp]//div[contains(@class, 'cpq-sidebar cpq-sidebar-right')]")
    page.wait_for_selector("//c-cpq-sidebar[@sclp-cpqapp_cpqapp]//div[contains(@class, 'cpq-sidebar cpq-sidebar-right')]", state='visible')
    expect(right_sidebar).to_be_visible()
    Middle_exists = page.locator("//c-cpq-bundle-editor")
    page.wait_for_selector("//c-cpq-bundle-editor", state='visible')
    expect(Middle_exists).to_be_visible()
    Left_sidebar = page.locator("//c-cpq-sidebar[@sclp-cpqapp_cpqapp]//div[contains(@class, 'cpq-sidebar cpq-sidebar-left')]")
    page.wait_for_selector("//c-cpq-sidebar[@sclp-cpqapp_cpqapp]//div[contains(@class, 'cpq-sidebar cpq-sidebar-left')]", state='visible')
    expect(Left_sidebar).to_be_visible()

def Bundle_Middle_exists(page, unique_number):
    page.wait_for_selector('text="Bundle Builder"', state='visible')
    page.click('text="Bundle Builder"')
    Middle_exists = page.locator("//c-cpq-bundle-editor")
    page.wait_for_selector("//c-cpq-bundle-editor", state='visible')
    expect(Middle_exists).to_be_visible()

def Bundle_Left_sidebar_exists(page, unique_number):
    page.wait_for_selector('text="Bundle Builder"', state='visible')
    page.click('text="Bundle Builder"')
    Left_sidebar = page.locator("//c-cpq-sidebar[@sclp-cpqapp_cpqapp]//div[contains(@class, 'cpq-sidebar cpq-sidebar-left')]")
    page.wait_for_selector("//c-cpq-sidebar[@sclp-cpqapp_cpqapp]//div[contains(@class, 'cpq-sidebar cpq-sidebar-left')]", state='visible')
    expect(Left_sidebar).to_be_visible()

def Bundle_Left_Sidebar_can_be_sorted_by_Displayed_fields(page, unique_number):
    page.wait_for_selector('text="Bundle Builder"', state='visible')
    page.click('text="Bundle Builder"')
    page.wait_for_selector("//c-cpq-menu-sub[@class='cpq-search cpq-search-button']", state='visible')
    page.click("//c-cpq-menu-sub[@class='cpq-search cpq-search-button']")
    pricebook_locator = page.locator("//span[@title='Pricebook']")
    pricebook_locator.hover()
    page.wait_for_selector("//span[@title='Standard Price Book']", state='visible')
    page.click("//span[@title='Standard Price Book']")
    time.sleep(2)
    accordion_down_exists = page.locator("//span[@title='Product Name']//lightning-icon[@icon-name='utility:up']")
    Product_name_sort = page.locator("//span[@title='Product Name']//span")
    if accordion_down_exists.count() == 0:
        Product_name_sort.click()
    time.sleep(2)

    for i in range(20, -1, -1):
        Accordions = page.locator('//c-cpq-sidebar-product-list//button[@aria-expanded="true"]').nth(i)
        if Accordions.count() > 0:
            Accordions.click()
    time.sleep(1)
    Accordions = page.locator('//c-cpq-sidebar-product-list//button[@aria-expanded="false"]').nth(0)
    Accordions.click()
    time.sleep(1)
    locator = "//span[@sclp-cpqsidebarproductlistitem_cpqsidebarproductlistitem][@class='slds-truncate cpq-list-item-name cpq-locked slds-col cpq-list-item-name-top']"
    elements = page.locator(locator)
    
        
    titles = []
    count = elements.count()

    for i in range(count):
        title = elements.nth(i).get_attribute("title")
        if title:
            titles.append(title.strip())
    
    assert titles
    print(titles)
    assert titles == sorted(titles, reverse=False), f"The elements are NOT in the alphabetical order:\n{titles}"
def Bundle_Left_Sidebar_can_be_filtered_by_Displayed_fields(page, unique_number):
        page.wait_for_selector('text="Bundle Builder"', state='visible')
        page.click('text="Bundle Builder"')
        page.wait_for_selector("//c-cpq-menu-sub[@class='cpq-search cpq-search-button']", state='visible')
        page.click("//c-cpq-menu-sub[@class='cpq-search cpq-search-button']")
        pricebook_locator = page.locator("//span[@title='Pricebook']")
        pricebook_locator.hover()
        page.wait_for_selector("//span[@title='Standard Price Book']", state='visible')
        page.click("//span[@title='Standard Price Book']")
        time.sleep(2)
        
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
        # test_product = 'Boat regatta'
        page.fill("//c-cpq-side-panel-filter-item//input", "Test Product to be deleted 3")
        page.click("button[title='Accept']")
        # page.type('input[placeholder="Products"]', f"{test_product}")
        All_Closed_Accordions = page.locator('//c-cpq-sidebar-product-list//button[@aria-expanded="false"]')
        First_Closed_Accordions = page.locator('//c-cpq-sidebar-product-list//button[@aria-expanded="false"]').nth(0)
        time.sleep(1)
        if All_Closed_Accordions.count() > 0:
            First_Closed_Accordions.click()
            print('accordion is expanded')
        else:
            pass
        page.wait_for_selector('//span[@sclp-cpqsidebarproductlistitem_cpqsidebarproductlistitem and @title="Test Product to be deleted 3"]', state='visible')
        expect(page.locator('//span[@sclp-cpqsidebarproductlistitem_cpqsidebarproductlistitem and @title="Test Product to be deleted 3"]')).to_be_visible()
        print("the Product Test Product to be deleted 3 is found")
        products = page.locator("//span[@sclp-cpqsidebarproductlistitem_cpqsidebarproductlistitem][@class='slds-truncate cpq-list-item-name cpq-locked slds-col cpq-list-item-name-top']")
        expect(products).to_have_count(1)
        page.click('//c-cpq-sidebar-product-list//button[contains(text(), "Remove All")]')
        print("All the filters are removed")