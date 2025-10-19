import time
from playwright.sync_api import sync_playwright, expect, Page
import config


def open_sculptor_cpq(page):
    """ Переход в Sculptor CPQ. """
    page.wait_for_selector('button[title="App Launcher"]', state='visible')
    time.sleep(1)
    page.click('button[title="App Launcher"]')

    page.fill('input.slds-input[placeholder="Search apps and items..."]', 'Sculptor CPQ')
    page.wait_for_selector('text="Sculptor CPQ"', state='visible')
    time.sleep(1)
    page.click('text="Sculptor CPQ"')

def create_bundle(page, unique_number: int):
    """ Создает новый бандл в системе. """
    page.wait_for_selector('text="Bundle Builder"', state='visible')
    time.sleep(1)
    page.click('text="Bundle Builder"')
    page.wait_for_selector("//c-cpq-menu-sub[@class='cpq-search cpq-search-button']", state='visible')
    time.sleep(5)
    page.click("//c-cpq-menu-sub[@class='cpq-search cpq-search-button']")

    # Кликаем по price book gear и выбираем Standard Price Book
    pricebook_locator = page.locator("//span[@title='Pricebook']")
    pricebook_locator.hover()
    page.wait_for_selector("//span[@title='Standard Price Book']", state='visible')
    page.click("//span[@title='Standard Price Book']")

    # Создаем бандл
    page.click("//button[@title='Create bundle']")
    page.wait_for_selector("//button[@title='Edit']", state='visible')
    time.sleep(1)
    page.click("//button[@title='Edit']")

    # Вводим название бандла
    bundle_input = page.locator("//div[@class='slds-form-element__control slds-grow']//input[@class='slds-input']")
    bundle_input.fill(f"Test Bundle to be deleted {unique_number}")

    # Подтверждаем создание
    page.click("//button[@title='Accept']")
    time.sleep(1)
   
def drag_and_drop_product1(page, unique_number: int):
    """ Перетаскивает продукт в бандл. """
    # Вводим продукт
    page.locator('input[placeholder="Products"]').type("test product to be deleted")
    print("Текст введен в поле 'Products'")
    time.sleep(2)


    for i in range(1, 10000):
        left_sidebar_button = page.locator(f'button[aria-expanded="false"][aria-controls="lgt-accordion-section-{i}"]')
        product_found = page.locator(f"//span[contains(@title, 'Test Product to be deleted')]")
        all_products = page.locator('//c-cpq-sidebar-product-list//button[@aria-expanded="false"]//span[contains(@title, "All products")]')
        if all_products.count() > 0:
            all_products.click()
        elif left_sidebar_button.count() > 0:
            left_sidebar_button.click()
        elif product_found.count() > 0:
            break


    print("закончил открывать аккордеоны")

    # Перетаскивание продукта
    Test_product_to_be_deleted_1_box = page.locator('div[data-name="Test Product to be deleted 1"]').bounding_box()

    if Test_product_to_be_deleted_1_box:
        Test_bundle_to_be_deleted_locator = page.locator(f'strong[title="Test Bundle to be deleted {unique_number}"]')
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
            print("Drag & drop 1 выполнен")
        else:
            print("Bundle не найден")
    else:
        print("Product не найден")
    time.sleep(1)
def drag_and_drop_product2(page, unique_number: int):

    # Перетаскивание продукта
    Test_product_to_be_deleted_1_box = page.locator('div[data-name="Test Product to be deleted 2"]').bounding_box()

    if Test_product_to_be_deleted_1_box:
        Test_bundle_to_be_deleted_locator = page.locator(f'strong[title="Test Bundle to be deleted {unique_number}"]')
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
            print("Drag & drop 2 выполнен")
        else:
            print("Bundle не найден")
    else:
        print("Product не найден")
    time.sleep(2)

def create_opportunity(page, unique_number: int):
    # Open Opportunity Builder
    page.wait_for_selector('text="Opportunity Builder"', state='visible')
    page.click('text="Opportunity Builder"') 

    page.wait_for_selector("//button[@title='Create opportunity']", state='visible')
    page.click("//button[@title='Create opportunity']")
    time.sleep(1)

    page.wait_for_selector("//input[@name='Name']", state='visible')
    opportunity_name = f"Test Opportunity to be deleted {unique_number}"
    page.fill("//input[@name='Name']", opportunity_name)

    page.wait_for_selector("//input[@name='CloseDate']", state='visible')
    page.fill("//input[@name='CloseDate']", "6.10.1997")

    page.wait_for_selector("//button[@aria-label='Stage']", state='visible')
    page.click("//button[@aria-label='Stage']")
        

    if page.locator("//button[@aria-label='Stage']").get_attribute("aria-expanded") == "false":
        page.keyboard.press("Enter")


    page.wait_for_selector('text="Value Proposition"', state='visible')
    page.click('text="Value Proposition"')



    page.wait_for_selector("//input[@placeholder='Search Accounts...']", state='visible')
    page.type("//input[@placeholder='Search Accounts...']", "test account to be deleted")
    page.click("//input[@placeholder='Search Accounts...']")
    page.wait_for_selector("//lightning-base-combobox-formatted-text[@title='test account to be deleted']", state='visible')
    page.click("//lightning-base-combobox-formatted-text[@title='test account to be deleted']")
   

    page.wait_for_selector("//button[@name='SaveEdit']", state='visible')
    page.click("//button[@name='SaveEdit']")

    time.sleep(1)  

    page.wait_for_selector('text="Opportunity Builder"', state='visible')
    page.click('text="Opportunity Builder"') 

    page.reload()
    time.sleep(3)

    page.wait_for_selector('input[placeholder="Opportunities"]', state='visible')
    page.locator('input[placeholder="Opportunities"]').type(f"Test opportunity to be deleted {unique_number}", delay=50)
    time.sleep(2)

    for i in range(1, 10000):
        opportunity_right_sidebar_button = page.locator(f'button[aria-expanded="false"][aria-controls="lgt-accordion-section-{i}"]')
        Opportunity_found = page.locator(f"//span[contains(@title, 'Test Opportunity to be deleted {unique_number}')]")
        Opportunity_Account_name_accordion = page.locator('//lightning-accordion-section[@sclp-cpqsidebaropportunitylist_cpqsidebaropportunitylist]//button[@aria-expanded="false"]//span[contains(@title, "Account Name: test account to be deleted")]')

        if Opportunity_Account_name_accordion.count() > 0:
            Opportunity_Account_name_accordion.click()
        elif opportunity_right_sidebar_button.count() > 0:
            opportunity_right_sidebar_button.click()
        elif Opportunity_found.count() > 0:
            break
    print("брейк сработал")

    page.wait_for_selector(f"//span[contains(@title, 'Test Opportunity to be deleted {unique_number}')]",
                             state='visible')
    
    page.click(f"//span[contains(@title, 'Test Opportunity to be deleted {unique_number}')]")
    print("оппа кликнута")
    time.sleep(1)


def Add_Product_to_the_Opportunity(page, unique_number: int):
    menu_sub_locator = page.locator("header.slds-split-view__header.slds-p-around_small.slds-p-vertical_xx-small c-cpq-menu-sub").nth(0)

    try:
        menu_sub_locator.wait_for(state='visible', timeout=5000)
        print("нашел первый элемент")
    except:
        print("первый элемент не найден за 5 секунд, ищем второй")
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
    page.wait_for_selector("lightning-button[data-id='01sQy000009iBYsIAM']", state='visible')
    page.click("lightning-button[data-id='01sQy000009iBYsIAM']")
    print("прайсбук выбрали")

    page.locator('input[placeholder="Products"]').type(f"Test Bundle to be deleted {unique_number}")
    time.sleep(1)

    # Открываем аккордеоны
    for i in range(1, 10000):
        left_sidebar_button = page.locator(f'button[aria-expanded="false"][aria-controls="lgt-accordion-section-{i}"]')
        product_found = page.locator(f"//span[contains(@title, 'Test Bundle to be deleted')]")
        all_products = page.locator(f"//span[contains(@title, 'All products')]")
        if all_products.count() > 0:
            all_products.click()
        if left_sidebar_button.count() > 0:
            left_sidebar_button.click()
        elif product_found.count() > 0:
            break


        
    print("открыли аккордеоны")

    # Перетаскивание продукта
    Test_Bundle_to_be_added = page.locator(f'div[data-name="Test Bundle to be deleted {unique_number}"]').bounding_box()

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
            print("Drag & drop выполнен")
        else:
            print("Bundle не найден")
    else:
        print("Product не найден")



def click_product_if_condition_met(page):
    page.wait_for_selector('//div[@class="slds-size_1-of-1 slds-p-around_xx-small slds-text-title_caps slds-border_top"]/following::span[@title="Test Product to be deleted 1"]', state='visible')
    page.click('//div[@class="slds-size_1-of-1 slds-p-around_xx-small slds-text-title_caps slds-border_top"]/following::span[@title="Test Product to be deleted 1"]')
    page.wait_for_selector('//div[@class="slds-size_1-of-1 slds-p-around_xx-small slds-text-title_caps slds-border_top"]/following::span[@title="Test Product to be deleted 2"]', state='visible')
    page.click('//div[@class="slds-size_1-of-1 slds-p-around_xx-small slds-text-title_caps slds-border_top"]/following::span[@title="Test Product to be deleted 2"]')
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
    page.fill("//input[@name='Name']", f"Test quote to be deleted {unique_number}")
    page.wait_for_selector("//input[@placeholder='Search Opportunities...']", state='visible')
    page.click("//input[@placeholder='Search Opportunities...']")


    page.wait_for_selector("//input[@placeholder='Search Accounts...']", state='visible')
    page.type("//input[@placeholder='Search Opportunities...']", "test account to be deleted")
    page.click("//input[@placeholder='Search Opportunities...']")
    page.wait_for_selector(f"//lightning-base-combobox-formatted-text[@title='Test Opportunity to be deleted {unique_number}']", state='visible')
    page.click(f"//lightning-base-combobox-formatted-text[@title='Test Opportunity to be deleted {unique_number}']")
    time.sleep(1)
    page.wait_for_selector("//*[text()='Create Quote']", state='visible')
    page.click("//*[text()='Create Quote']")

def Add_Product_to_the_Quote(page, unique_number: int):
    page.wait_for_selector('//input[@placeholder="Products"]')
    page.locator('//input[@placeholder="Products"]').type(f"Test Bundle to be deleted {unique_number}")
    time.sleep(1)
    

    for i in range(1, 10000):
        left_sidebar_button = page.locator(f'button[aria-expanded="false"][aria-controls="lgt-accordion-section-{i}"]')
        product_found = page.locator(f"//span[contains(@title, 'Test Bundle to be deleted')]")
        all_products = page.locator('//c-cpq-sidebar-product-list//button[@aria-expanded="false"]//span[contains(@title, "All products")]')
        if all_products.count() > 0:
            all_products.click()
        elif left_sidebar_button.count() > 0:
            left_sidebar_button.click()
        elif product_found.count() > 0:
            break

    # Перетаскивание продукта
    Test_Bundle_to_be_added = page.locator(f'div[data-name="Test Bundle to be deleted {unique_number}"]').bounding_box()

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
            print("Drag & drop выполнен")
        else:
            print("Bundle не найден")
    else:
        print("Product не найден")

def click_Quote_product_if_condition_met(page):
    page.wait_for_selector('//div[@class="cpq-grid slds-size_1-of-1 cpq-option"]//span[@title="Test Product to be deleted 1"]', state='visible')
    page.click('//div[@class="cpq-grid slds-size_1-of-1 cpq-option"]//span[@title="Test Product to be deleted 1"]')
    time.sleep(3)
    page.wait_for_selector('//div[@class="cpq-grid slds-size_1-of-1 cpq-option"]//span[@title="Test Product to be deleted 2"]', state='visible')
    page.click('//div[@class="cpq-grid slds-size_1-of-1 cpq-option"]//span[@title="Test Product to be deleted 2"]')
    time.sleep(3)

    page.wait_for_selector("//button[@class='slds-button slds-button_brand' and text()='Save']", state='visible')
    page.click("//button[@class='slds-button slds-button_brand' and text()='Save']")
    time.sleep(5)

