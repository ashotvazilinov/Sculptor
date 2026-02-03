from simple_salesforce import Salesforce, SalesforceLogin, SalesforceError, SalesforceMalformedRequest
import time
from playwright.sync_api import sync_playwright, expect, Page
import config
import random


USERNAME='test-cvuxkuy6hua0@example.com'
PASSWORD='#lmyu6olLwrth'
SECURITE_TOKEN='jQtYddA6Lw5txX4oMKTW3eEr'
DOMAIN='test' 

session_id, instance = SalesforceLogin(

    username=USERNAME, 
    password=PASSWORD,
    security_token=SECURITE_TOKEN,
    domain=DOMAIN 
)
sf = Salesforce(instance=instance, session_id=session_id)
print("Connected!")

def start(page):
    page.goto(config.SITE_URL)
    username_input = page.locator('input[id="username"]')
    password_input = page.locator('input[id="password"]')
    username_input.fill(config.LOGIN)
    password_input.fill(config.PASSWORD)
    page.press('input[id="password"]', 'Enter')
    
    page.wait_for_selector('button[title="App Launcher"]', state='visible')
    time.sleep(1)
    page.click('button[title="App Launcher"]')
    print('App Launcher is clicked')

    page.fill('input.slds-input[placeholder="Search apps and items..."]', 'Sculptor CPQ')
    page.wait_for_selector('text="Sculptor CPQ"', state='visible')
    print('ready to be clicked')
    time.sleep(1)
    page.click('text="Sculptor CPQ"')
    print('clicked')
    time.sleep(1)

def create_bundle(page, unique_number: int):

    page.wait_for_selector('text="Bundle Builder"', state='visible')
    time.sleep(1)
    page.click('text="Bundle Builder"')
    page.wait_for_selector("//c-cpq-menu-sub[@class='cpq-search cpq-search-button']", state='visible')
    time.sleep(5)
    page.click("//c-cpq-menu-sub[@class='cpq-search cpq-search-button']")

    pricebook_locator = page.locator("//span[@title='Pricebook']")
    pricebook_locator.hover()
    page.wait_for_selector("//span[@title='Standard Price Book']", state='visible')
    page.click("//span[@title='Standard Price Book']")


    page.click("//button[@title='Create bundle']")
    page.wait_for_selector("//button[@title='Edit']", state='visible')
    time.sleep(1)
    page.click("//button[@title='Edit']")


    bundle_input = page.locator("//div[@class='slds-form-element__control slds-grow']//input[@class='slds-input']")
    bundle_input.fill(f"Test Bundle {unique_number}")

    page.click("//button[@title='Accept']")
    time.sleep(1)
   
def drag_and_drop_product1(page, unique_number: int):

    # Вводим продукт
    page.locator('input[placeholder="Products"]').type("Test Product")
    print("The text is entered 'Products'")
    time.sleep(2)


    for i in range(1, 10000):
        left_sidebar_button = page.locator(f'button[aria-expanded="false"][aria-controls="lgt-accordion-section-{i}"]')
        product_found = page.locator(f"//span[contains(@title, 'Test Product 003')]")
        all_products = page.locator('//c-cpq-sidebar-product-list//button[@aria-expanded="false"]//span[contains(@title, "All products")]')
        if all_products.count() > 0:
            all_products.click()
        elif left_sidebar_button.count() > 0:
            left_sidebar_button.click()
        elif product_found.count() > 0:
            break


    print("accerdeons are opened")


    Test_product_to_be_deleted_1_box = page.locator('div[data-name="Test Product 003"]').bounding_box()
    print('')

    if Test_product_to_be_deleted_1_box:
        Test_bundle_to_be_deleted_locator = page.locator(f'strong[title="Test Bundle {unique_number}"]')
        Test_bundle_to_be_deleted_1_box = Test_bundle_to_be_deleted_locator.bounding_box()

        if Test_bundle_to_be_deleted_1_box:
            page.mouse.move(Test_product_to_be_deleted_1_box['x'], Test_product_to_be_deleted_1_box['y'])
            page.mouse.down()

            duration = 1
            steps = 30
            delay = duration / steps
            start_x, start_y = Test_product_to_be_deleted_1_box['x'], Test_product_to_be_deleted_1_box['y']
            end_x, end_y = Test_bundle_to_be_deleted_1_box['x'], Test_bundle_to_be_deleted_1_box['y'] + 30

            for step in range(steps):
                x = start_x + (end_x - start_x) * (step / steps)
                y = start_y + (end_y - start_y) * (step / steps)
                page.mouse.move(x, y)
                time.sleep(delay)

            page.mouse.up()
            print("Drag & drop 1 is completed")
        else:
            print("Bundle is not found")
    else:
        print("Product is not found")
    time.sleep(1)
def drag_and_drop_product2(page, unique_number: int):

    Test_product_to_be_deleted_1_box = page.locator('div[data-name="Test Product 002"]').bounding_box()

    if Test_product_to_be_deleted_1_box:
        Test_bundle_to_be_deleted_locator = page.locator(f'strong[title="Test Bundle {unique_number}"]')
        Test_bundle_to_be_deleted_1_box = Test_bundle_to_be_deleted_locator.bounding_box()

        if Test_bundle_to_be_deleted_1_box:
            page.mouse.move(Test_product_to_be_deleted_1_box['x'], Test_product_to_be_deleted_1_box['y'])
            page.mouse.down()

            duration = 1
            steps = 30
            delay = duration / steps
            start_x, start_y = Test_product_to_be_deleted_1_box['x'], Test_product_to_be_deleted_1_box['y']
            end_x, end_y = Test_bundle_to_be_deleted_1_box['x'], Test_bundle_to_be_deleted_1_box['y'] + 30

            for step in range(steps):
                x = start_x + (end_x - start_x) * (step / steps)
                y = start_y + (end_y - start_y) * (step / steps)
                page.mouse.move(x, y)
                time.sleep(delay)

            page.mouse.up()
            print("Drag & drop 2 is completed")
        else:
            print("Bundle is not found")
    else:
        print("Product is not found")
    time.sleep(2)

def create_opportunity(page, unique_number: int):
    # Open Opportunity Builder
    page.wait_for_selector('text="Opportunity Builder"', state='visible')
    page.click('text="Opportunity Builder"') 

    page.wait_for_selector("//button[@title='Create opportunity']", state='visible')
    page.click("//button[@title='Create opportunity']")
    time.sleep(1)

    page.wait_for_selector("//input[@name='Name']", state='visible')
    opportunity_name = f"Test Opportunity {unique_number}"
    page.fill("//input[@name='Name']", opportunity_name)

    page.wait_for_selector("//input[@name='CloseDate']", state='visible')
    page.fill("//input[@name='CloseDate']", "06/10/1997")

    page.wait_for_selector("//button[@aria-label='Stage']", state='visible')
    page.click("//button[@aria-label='Stage']")
    time.sleep(0.5)
    
    if page.locator("//button[@aria-label='Stage']").get_attribute("aria-expanded") == "false":
        page.keyboard.press("Enter")


    page.get_by_role("option", name="Prospecting").locator("span").nth(1).wait_for(state="visible")
    page.get_by_role("option", name="Prospecting").locator("span").nth(1).click()



    page.wait_for_selector("//input[@placeholder='Search Accounts...']", state='visible')
    page.type("//input[@placeholder='Search Accounts...']", "test account")
    page.click("//input[@placeholder='Search Accounts...']")
    # page.pause()
    page.get_by_role("option", name="test account", exact=True).locator("span").nth(2).wait_for(state="visible")
    page.get_by_role("option", name="test account", exact=True).locator("span").nth(2).click()



    page.wait_for_selector("//button[@name='SaveEdit']", state='visible')
    page.click("//button[@name='SaveEdit']")

    time.sleep(1)  

    page.wait_for_selector('text="Opportunity Builder"', state='visible')
    page.click('text="Opportunity Builder"') 

    page.reload()
    time.sleep(3)

    page.wait_for_selector('input[placeholder="Opportunities"]', state='visible')
    page.locator('input[placeholder="Opportunities"]').type(f"Test opportunity {unique_number}", delay=50)
    time.sleep(2)

    for i in range(1, 10000):
        opportunity_right_sidebar_button = page.locator(f'button[aria-expanded="false"][aria-controls="lgt-accordion-section-{i}"]')
        Opportunity_found = page.locator(f"//span[contains(@title, 'Test Opportunity {unique_number}')]")
        Opportunity_Account_name_accordion = page.locator('//lightning-accordion-section[@sclp-cpqsidebaropportunitylist_cpqsidebaropportunitylist]//button[@aria-expanded="false"]//span[contains(@title, "Account Name: test account")]')

        if Opportunity_Account_name_accordion.count() > 0:
            Opportunity_Account_name_accordion.click()
        elif opportunity_right_sidebar_button.count() > 0:
            opportunity_right_sidebar_button.click()
        elif Opportunity_found.count() > 0:
            break
    print("break worked")

    page.wait_for_selector(f"//span[contains(@title, 'Test Opportunity {unique_number}')]",
                             state='visible')
    
    page.click(f"//span[contains(@title, 'Test Opportunity {unique_number}')]")
    print("оппа кликнута")
    time.sleep(1)


def Add_Product_to_the_Opportunity(page, unique_number: int):
    menu_sub_locator = page.locator("header.slds-split-view__header.slds-p-around_small.slds-p-vertical_xx-small c-cpq-menu-sub").nth(0)
    print('open F12')
    time.sleep(1)

    try:
        menu_sub_locator.wait_for(state='visible', timeout=5000)
        print("нашел первый элемент")
    except:
        print("первый элемент is not found за 5 секунд, ищем второй")
        menu_sub_locator = page.locator("header.slds-split-view__header.slds-p-around_small.slds-p-vertical_xx-small c-cpq-menu-sub").nth(1)
        menu_sub_locator.wait_for(state='visible')
        print("нашел второй элемент")

    time.sleep(2)
    menu_sub_locator.click()

    print("кликнул")
    time.sleep(2)

    pricebook_locator = page.locator("//span[@title='Pricebook']")
    pricebook_locator.hover()
    page.wait_for_selector("//span[@title='Standard Price Book']", state='visible')
    page.click("//span[@title='Standard Price Book']")
    print("прайсбук открыли, щас буду нажимать на прайсбук, момент истины")
    time.sleep(1)
    page.wait_for_selector("(//button[normalize-space()='Yes'])[last()]", state='visible')
    page.click("(//button[normalize-space()='Yes'])[last()]")
    print("прайсбук выбрали")



    page.locator('input[placeholder="Products"]').type(f"Test Bundle {unique_number}")
    time.sleep(3)


    # Open accordeons
    accordion_buttons = page.locator('button[aria-controls^="lgt-accordion-section-"]')

    for i in range(accordion_buttons.count()):
        btn = accordion_buttons.nth(i)

        btn.wait_for(state="visible")

        if btn.get_attribute("aria-expanded") == "false":
            btn.click()

            
        print("accordeons are oppened")


    Test_Bundle_to_be_added = page.locator(f'div[data-name="Test Bundle {unique_number}"]').bounding_box()

    if Test_Bundle_to_be_added:
        Product_Name_anchor = page.locator('text="Product Name"').nth(1)
        Product_Name_anchor = Product_Name_anchor.bounding_box()

        if Product_Name_anchor:
            page.mouse.move(Test_Bundle_to_be_added['x'], Test_Bundle_to_be_added['y'])
            page.mouse.down()

            duration = 1
            steps = 30
            delay = duration / steps
            start_x, start_y = Test_Bundle_to_be_added['x'], Test_Bundle_to_be_added['y']
            end_x, end_y = Product_Name_anchor['x'], Product_Name_anchor['y'] + 30

            for step in range(steps):
                x = start_x + (end_x - start_x) * (step / steps)
                y = start_y + (end_y - start_y) * (step / steps)
                page.mouse.move(x, y)
                time.sleep(delay)

            page.mouse.up()
            print("Drag & drop is completed")
        else:
            print("Bundle is not found")
    else:
        print("Product is not found")



def click_product_if_condition_met(page):
    page.wait_for_selector('//div[@class="slds-size_1-of-1 slds-p-around_xx-small slds-text-title_caps slds-border_top"]/following::span[@title="Test Product 002"]', state='visible')
    page.click('//div[@class="slds-size_1-of-1 slds-p-around_xx-small slds-text-title_caps slds-border_top"]/following::span[@title="Test Product 002"]')
    page.wait_for_selector('//div[@class="slds-size_1-of-1 slds-p-around_xx-small slds-text-title_caps slds-border_top"]/following::span[@title="Test Product 003"]', state='visible')
    page.click('//div[@class="slds-size_1-of-1 slds-p-around_xx-small slds-text-title_caps slds-border_top"]/following::span[@title="Test Product 003"]')
    time.sleep(1)
    page.wait_for_selector('text="Save"', state='visible')
    page.click('text="Save"')
    time.sleep(5)
def Create_Quote(page, unique_number: int):
    page.wait_for_selector('//a[@title="Quote Builder" and @draggable="false"]', state='visible')
    page.click('//a[@title="Quote Builder" and @draggable="false"]')
    page.wait_for_selector("//button[@title='New']", state='visible')
    page.reload()
    page.wait_for_selector("//button[@title='New']", state='visible')
    page.click("//button[@title='New']")
    page.wait_for_selector("//input[@name='Name']", state='visible')
    page.fill("//input[@name='Name']", f"Test quote")
    page.wait_for_selector("//input[@placeholder='Search Opportunities...']", state='visible')
    page.click("//input[@placeholder='Search Opportunities...']")



    page.wait_for_selector("//input[@placeholder='Search Accounts...']", state='visible')
    page.type("//input[@placeholder='Search Opportunities...']", f"test Opportunity {unique_number}")
    page.click("//input[@placeholder='Search Opportunities...']")
    page.wait_for_selector(f"//lightning-base-combobox-formatted-text[@title='Test Opportunity {unique_number}']", state='visible')
    page.click(f"//lightning-base-combobox-formatted-text[@title='Test Opportunity {unique_number}']")
    time.sleep(1)
    page.wait_for_selector("//*[text()='Create Quote']", state='visible')
    page.click("//*[text()='Create Quote']")


def Add_Product_to_the_Quote(page, unique_number: int):
    page.wait_for_selector('//input[@placeholder="Products"]')
    page.locator('//input[@placeholder="Products"]').type(f"Test Bundle {unique_number}")
    time.sleep(3)
    

    accordion_buttons = page.locator('button[aria-controls^="lgt-accordion-section-"]')

    for i in range(accordion_buttons.count()):
        btn = accordion_buttons.nth(i)

        btn.wait_for(state="visible")

        if btn.get_attribute("aria-expanded") == "false":
            btn.click()

            
        print("accordeons are oppened")


    time.sleep(1)
    Test_Bundle_to_be_added = page.locator(f'div[data-name="Test Bundle {unique_number}"]').bounding_box()

    if Test_Bundle_to_be_added:
        Product_Name_anchor = page.locator('text="Product Name"').nth(1)
        Product_Name_anchor = Product_Name_anchor.bounding_box()

        if Product_Name_anchor:
            page.mouse.move(Test_Bundle_to_be_added['x'], Test_Bundle_to_be_added['y'])
            page.mouse.down()

            duration = 1
            steps = 30
            delay = duration / steps
            start_x, start_y = Test_Bundle_to_be_added['x'], Test_Bundle_to_be_added['y']
            end_x, end_y = Product_Name_anchor['x'], Product_Name_anchor['y'] + 30

            for step in range(steps):
                x = start_x + (end_x - start_x) * (step / steps)
                y = start_y + (end_y - start_y) * (step / steps)
                page.mouse.move(x, y)
                time.sleep(delay)

            page.mouse.up()
            print("Drag & drop is completed")
        else:
            print("Bundle is not found")
    else:
        print("Product is not found")

def click_Quote_product_if_condition_met(page):
    time.sleep(5)
    page.wait_for_selector('//div[@class="cpq-grid slds-size_1-of-1 cpq-option"]//span[@title="Test Product 002"]', state='visible')
    page.click('//div[@class="cpq-grid slds-size_1-of-1 cpq-option"]//span[@title="Test Product 002"]')

    page.wait_for_selector('//div[@class="cpq-grid slds-size_1-of-1 cpq-option"]//span[@title="Test Product 003"]', state='visible')
    page.click('//div[@class="cpq-grid slds-size_1-of-1 cpq-option"]//span[@title="Test Product 003"]')
    time.sleep(3)

    page.wait_for_selector("//button[@class='slds-button slds-button_brand' and text()='Save']", state='visible')
    page.click("//button[@class='slds-button slds-button_brand' and text()='Save']")
    time.sleep(2)

def main():
    unique_number = random.randint(1, 5)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        context = browser.new_context(
            record_video_dir=config.VIDEO_DIR,
            record_video_size={"width": 1920, "height": 1080}
        )

        page = context.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})

        start(page)
        create_bundle(page, unique_number)
        drag_and_drop_product1(page, unique_number)
        drag_and_drop_product2(page, unique_number)
        create_opportunity(page, unique_number)
        Add_Product_to_the_Opportunity(page, unique_number)
        click_product_if_condition_met(page)
        Create_Quote(page, unique_number)
        Add_Product_to_the_Quote(page, unique_number)
        click_Quote_product_if_condition_met(page)

        browser.close()

if __name__ == "__main__":
    main()
