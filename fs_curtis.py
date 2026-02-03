from simple_salesforce import Salesforce, SalesforceLogin, SalesforceError
from datetime import datetime
import random
import time
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

session_id, instance = SalesforceLogin(

    username='serge@twistellar.com.sculptorqa', 
    password='2K23workhard!',
    security_token='EeIdYKjLdwQVsQFuEryL87e7g',
    domain='test' 
)
sf = Salesforce(instance=instance, session_id=session_id)
print("Connected!")
# git add .

# git commit -m "changed smth"

# git push origin HEAD:main

# _ui/system/security/ResetApiTokenEdit

#setup - user interface - Enable SOAP API login()
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
timestamp_for_SF_date = datetime.now().strftime("%Y-%m-%d")
timestamp_for_SF_date_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0000")
timestamp_for_SF_time = datetime.now().strftime("%H:%M:%S.000Z")
print(timestamp)

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --remote-debugging-address=127.0.0.1 --no-first-run --user-data-dir="C:\Temp\ChromeDebugProfile"

# set PWDEBUG=1 && python "D:\vs code\Sculptor\current page.py"

# Automation in Salesforce API
# Main function
def run_current_tasks(unique_number: int = 33):
    with sync_playwright() as p:
                # Connect to the existing browser instance
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]  # Using the first context
        page = context.pages[0]  # Taking the first tab
        '''write here'''
        
        product_record = sf.query("SELECT Id, Name, FS_Curtis_Policy_Product_Type__c, FS_Curtis_Product_Division__c from Product2 where id = '01tUY000007szthYAA'")['records'][0]
        core_account_record = sf.query("SELECT Id, Name from account where id = '001cY00000LgtqQQAR'")['records'][0]
        community_account_record = sf.query("SELECT Id, Name from account where id = '001cY00000FWcT0QAL'")['records'][0]

        product_type = ['Equipment', #0
                        'Part'] #1

        divisions_apis = [
            'Toledo Tools', #0
            'Reciprocating Compressors', #1 
            'Small Oil Flooded Rotary Compressors', #2 
            'Large Oil Flooded Rotary Compressors', #3
            'Oil Free Compressors', #4
            'Blowers and Vaccuums',#5
            'Aftermarket and Service']#6

        core_ranks = ['Bronze', 'Silver', 'Gold', 'Platinum']

        itteration = 6
        core_rank = "Bronze"
        community_rank = "Platinum"
        type = 'Part'

        if itteration == 0:
            sf.product2.update(product_record['Id'], {
                'FS_Curtis_Product_Division__c': divisions_apis[0],
                'FS_Curtis_Policy_Product_Type__c': type
            })

            sf.account.update(community_account_record['Id'], {
                'Toledo_Tools__c': community_rank, #0
                'Reciprocating_Compressors__c': "",  #1
                'Small_Oil_Flooded_Rotary_Compressors__c': "",  #2
                'Large_Oil_Flooded_Rotary_Compressors__c': "", #3
                'Oil_Free_Compressors__c': "",#4
                'Blowers_and_Vaccuums__c': "", #5
                'Aftermarket_and_Service__c': ""#6
            })

            sf.account.update(core_account_record['Id'], {
                'Toledo_Tools__c': core_rank, #0
                'Reciprocating_Compressors__c': "",  #1
                'Small_Oil_Flooded_Rotary_Compressors__c': "",  #2
                'Large_Oil_Flooded_Rotary_Compressors__c': "", #3
                'Oil_Free_Compressors__c': "",#4
                'Blowers_and_Vaccuums__c': "", #5
                'Aftermarket_and_Service__c': ""#6
            })
            recalculate_button = page.locator("(//button[contains(text(), 'Recalculate')])[last()]")
            recalculate_button.click()
        elif itteration == 1:
            sf.product2.update(product_record['Id'], {
                'FS_Curtis_Product_Division__c': divisions_apis[1],
                'FS_Curtis_Policy_Product_Type__c': type
            })

            sf.account.update(community_account_record['Id'], {
                'Toledo_Tools__c': "", #0
                'Reciprocating_Compressors__c': community_rank,  #1
                'Small_Oil_Flooded_Rotary_Compressors__c': "",  #2
                'Large_Oil_Flooded_Rotary_Compressors__c': "", #3
                'Oil_Free_Compressors__c': "",#4
                'Blowers_and_Vaccuums__c': "", #5
                'Aftermarket_and_Service__c': ""#6
            })

            sf.account.update(core_account_record['Id'], {
                'Toledo_Tools__c': "", #0
                'Reciprocating_Compressors__c': core_rank,  #1
                'Small_Oil_Flooded_Rotary_Compressors__c': "",  #2
                'Large_Oil_Flooded_Rotary_Compressors__c': "", #3
                'Oil_Free_Compressors__c': "",#4
                'Blowers_and_Vaccuums__c': "", #5
                'Aftermarket_and_Service__c': ""#6
            })
            recalculate_button = page.locator("(//button[contains(text(), 'Recalculate')])[last()]")
            recalculate_button.click()

        elif itteration == 2:
            sf.product2.update(product_record['Id'], {
                'FS_Curtis_Product_Division__c': divisions_apis[2],
                'FS_Curtis_Policy_Product_Type__c': type
            })


            sf.account.update(community_account_record['Id'], {
                'Toledo_Tools__c': "", #0
                'Reciprocating_Compressors__c': "",  #1
                'Small_Oil_Flooded_Rotary_Compressors__c': community_rank,  #2
                'Large_Oil_Flooded_Rotary_Compressors__c': "", #3
                'Oil_Free_Compressors__c': "",#4
                'Blowers_and_Vaccuums__c': "", #5
                'Aftermarket_and_Service__c': ""#6
            })

            sf.account.update(core_account_record['Id'], {
                'Toledo_Tools__c': "", #0
                'Reciprocating_Compressors__c': "",  #1
                'Small_Oil_Flooded_Rotary_Compressors__c': core_rank,  #2
                'Large_Oil_Flooded_Rotary_Compressors__c': "", #3
                'Oil_Free_Compressors__c': "",#4
                'Blowers_and_Vaccuums__c': "", #5
                'Aftermarket_and_Service__c': ""#6
            })
            recalculate_button = page.locator("(//button[contains(text(), 'Recalculate')])[last()]")
            recalculate_button.click()
        elif itteration == 3:
            sf.product2.update(product_record['Id'], {
                'FS_Curtis_Product_Division__c': divisions_apis[3],
                'FS_Curtis_Policy_Product_Type__c': type
            })

            sf.account.update(community_account_record['Id'], {
                'Toledo_Tools__c': "", #0
                'Reciprocating_Compressors__c': "",  #1
                'Small_Oil_Flooded_Rotary_Compressors__c': "",  #2
                'Large_Oil_Flooded_Rotary_Compressors__c': community_rank, #3
                'Oil_Free_Compressors__c': "",#4
                'Blowers_and_Vaccuums__c': "", #5
                'Aftermarket_and_Service__c': ""#6
            })


            sf.account.update(core_account_record['Id'], {
                'Toledo_Tools__c': "", #0
                'Reciprocating_Compressors__c': "",  #1
                'Small_Oil_Flooded_Rotary_Compressors__c': "",  #2
                'Large_Oil_Flooded_Rotary_Compressors__c': core_rank, #3
                'Oil_Free_Compressors__c': "",#4
                'Blowers_and_Vaccuums__c': "", #5
                'Aftermarket_and_Service__c': ""#6
            })
            recalculate_button = page.locator("(//button[contains(text(), 'Recalculate')])[last()]")
            recalculate_button.click()
        elif itteration == 4:
            sf.product2.update(product_record['Id'], {
                'FS_Curtis_Product_Division__c': divisions_apis[4],
                'FS_Curtis_Policy_Product_Type__c': type
            })


            sf.account.update(community_account_record['Id'], {
                'Toledo_Tools__c': "", #0
                'Reciprocating_Compressors__c': "",  #1
                'Small_Oil_Flooded_Rotary_Compressors__c': "",  #2
                'Large_Oil_Flooded_Rotary_Compressors__c': "", #3
                'Oil_Free_Compressors__c': community_rank,#4
                'Blowers_and_Vaccuums__c': "", #5
                'Aftermarket_and_Service__c': ""#6
            })

            sf.account.update(core_account_record['Id'], {
                'Toledo_Tools__c': "", #0
                'Reciprocating_Compressors__c': "",  #1
                'Small_Oil_Flooded_Rotary_Compressors__c': "",  #2
                'Large_Oil_Flooded_Rotary_Compressors__c': "", #3
                'Oil_Free_Compressors__c': core_rank,#4
                'Blowers_and_Vaccuums__c': "", #5
                'Aftermarket_and_Service__c': ""#6
            })
            recalculate_button = page.locator("(//button[contains(text(), 'Recalculate')])[last()]")
            recalculate_button.click()
        elif itteration == 5:
            sf.product2.update(product_record['Id'], {
                'FS_Curtis_Product_Division__c': divisions_apis[5],
                'FS_Curtis_Policy_Product_Type__c': type
            })
            sf.account.update(community_account_record['Id'], {
                'Toledo_Tools__c': "", #0
                'Reciprocating_Compressors__c': "",  #1
                'Small_Oil_Flooded_Rotary_Compressors__c': "",  #2
                'Large_Oil_Flooded_Rotary_Compressors__c': "", #3
                'Oil_Free_Compressors__c': "",#4
                'Blowers_and_Vaccuums__c': community_rank, #5
                'Aftermarket_and_Service__c': ""#6
            })

            sf.account.update(core_account_record['Id'], {
                'Toledo_Tools__c': "", #0
                'Reciprocating_Compressors__c': "",  #1
                'Small_Oil_Flooded_Rotary_Compressors__c': "",  #2
                'Large_Oil_Flooded_Rotary_Compressors__c': "", #3
                'Oil_Free_Compressors__c': "",#4
                'Blowers_and_Vaccuums__c': core_rank, #5
                'Aftermarket_and_Service__c': ""#6
            })
            recalculate_button = page.locator("(//button[contains(text(), 'Recalculate')])[last()]")
            recalculate_button.click()

        elif itteration == 6:
            sf.product2.update(product_record['Id'], {
                'FS_Curtis_Product_Division__c': divisions_apis[6],
                'FS_Curtis_Policy_Product_Type__c': type
            })
            sf.account.update(community_account_record['Id'], {
                'Toledo_Tools__c': "", #0
                'Reciprocating_Compressors__c': "",  #1
                'Small_Oil_Flooded_Rotary_Compressors__c': "",  #2
                'Large_Oil_Flooded_Rotary_Compressors__c': "", #3
                'Oil_Free_Compressors__c': "",#4
                'Blowers_and_Vaccuums__c': "", #5
                'Aftermarket_and_Service__c': community_rank#6
            })
            sf.account.update(core_account_record['Id'], {
                'Toledo_Tools__c': "", #0
                'Reciprocating_Compressors__c': "",  #1
                'Small_Oil_Flooded_Rotary_Compressors__c': "",  #2
                'Large_Oil_Flooded_Rotary_Compressors__c': "", #3
                'Oil_Free_Compressors__c': "",#4
                'Blowers_and_Vaccuums__c': "", #5
                'Aftermarket_and_Service__c': core_rank#6
            })
            recalculate_button = page.locator("(//button[contains(text(), 'Recalculate')])[last()]")
            recalculate_button.click()

# Start
if __name__ == "__main__":
    unique_number = 33 
    run_current_tasks(unique_number)