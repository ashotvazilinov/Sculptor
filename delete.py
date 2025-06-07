from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright, Page
from playwright_utils import (create_opportunity, Add_Product_to_the_Opportunity,
    click_product_if_condition_met, Create_Quote, Add_Product_to_the_Quote,
    click_Quote_product_if_condition_met
    )
from salesforce_utils import (
    connect_to_salesforce, delete_test_bundles_salesforce, 
    delete_test_opportunity_salesforce, delete_test_quote_salesforce)
from simple_salesforce import Salesforce  
import config


# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --remote-debugging-address=127.0.0.1 --no-first-run --user-data-dir="C:\Temp\ChromeDebugProfile"

# set PWDEBUG=1 && python "D:\vs code\Sculptor current page.py"


# Salesforce Data
login_value = config.LOGIN
password_value = config.PASSWORD
sec_tok = config.SECURITY_TOKEN

# Authorisation in Salesforce API

sf = Salesforce(username=login_value, password=password_value, security_token=sec_tok)

# Main function
def run_current_tasks(unique_number: int):
    with sync_playwright() as p:
        # Connecting to an open browser via CDP
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")  
        context = browser.contexts[0]  
        page = context.pages[0]  
        delete_test_opportunity_salesforce(sf, unique_number)
        delete_test_bundles_salesforce(sf, unique_number) 
        delete_test_quote_salesforce(sf, unique_number)


# start
if __name__ == "__main__":
    unique_number = 33  
    run_current_tasks(unique_number)

