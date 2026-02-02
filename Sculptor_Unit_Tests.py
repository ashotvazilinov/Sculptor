# Sculptor_Unit_Tests.py
import time
from playwright.sync_api import sync_playwright, expect, Page
from html_elements import *
import config


def Bundle_consists_of_three_sections(page, unique_number):
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
    page.click("//span[text()='Product.Product Name']")
    filter_Product_name = page.locator("//c-cpq-side-panel-filter-item//span[contains(text(), 'Product Name')]")
    filter_Operator_contains = page.locator("//c-cpq-side-panel-filter-item//span[contains(text(), 'CONTAINS')]")
    
    page.wait_for_selector("//c-cpq-side-panel-filter-item//input", state='visible')
    expect(filter_Product_name).to_be_visible()
    print('Field name Product Name is set by default')
    expect(filter_Operator_contains).to_be_visible()
    print('Operator is set to Contains by default')
    # test_product = 'Boat regatta'
    page.fill("//c-cpq-side-panel-filter-item//input", "Test Product 003")
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
    page.wait_for_selector('//span[@sclp-cpqsidebarproductlistitem_cpqsidebarproductlistitem and @title="Test Product 003"]', state='visible')
    expect(page.locator('//span[@sclp-cpqsidebarproductlistitem_cpqsidebarproductlistitem and @title="Test Product 003"]')).to_be_visible()
    print("the Product Test Product 003 is found")
    products = page.locator("//span[@sclp-cpqsidebarproductlistitem_cpqsidebarproductlistitem][@class='slds-truncate cpq-list-item-name cpq-locked slds-col cpq-list-item-name-top']")
    expect(products).to_have_count(1)
    page.click('//c-cpq-sidebar-product-list//button[contains(text(), "Remove All")]')
    print("All the filters are removed")
def Bundle_Left_Sidebar_Active_grouping(page, unique_number):
    page.wait_for_selector(Sculptor_settings_tab, state='visible')
    page.click(Sculptor_settings_tab)
    page.wait_for_selector(Fields_and_layouts, state='visible')
    page.click(Fields_and_layouts)
    li_group = page.locator(Sculptor_settings_Product_sidebar_group_li_count)#convert to locator
    active_is_already_right = page.locator(Sculptor_settings_Product_right_sidebar_contains_active)
    page.wait_for_selector(Sculptor_settings_Product_sidebar_group_li_count, state='visible')
    if active_is_already_right.count() == 0:
        print("Active is not in right sidebar, proceeding with moving it...")
    
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
        print('Save button is clicked')

        page.wait_for_selector(Sculptor_settings_Save_Success_message, state='visible')
        print("Active grouping is set successfully")
        active_is_already_right = page.locator(Sculptor_settings_Product_right_sidebar_contains_active)


    page.wait_for_selector(Bundle_builder_tab, state='visible')
    page.click(Bundle_builder_tab)#go to bundle builder
    print("Bundle Builder tab is opened")

    Accordions = page.locator('//c-cpq-sidebar-product-list//button[@aria-expanded="false"]').nth(0)
    while Accordions.count() > 0:
        Accordions.click()
        Accordions = page.locator('//c-cpq-sidebar-product-list//button[@aria-expanded="false"]').nth(0)
    page.wait_for_selector(BB_Product_Name_exists, state='visible')
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

    page.wait_for_selector(BB_Active_exists, state='visible')
    print('Active exists')