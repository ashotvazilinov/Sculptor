# Sculptor_Unit_Tests.py
import time
from playwright.sync_api import sync_playwright, expect, Page
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
    Arrow_down_exists = page.locator("//span[@title='Product Name']//lightning-icon[@icon-name='utility:up']")
    Product_name_sort = page.locator("//span[@title='Product Name']//span")
    if Arrow_down_exists.count() == 0:
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