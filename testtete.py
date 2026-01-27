from simple_salesforce import Salesforce, SalesforceLogin, SalesforceError
from datetime import datetime
import random
import time
from playwright.sync_api import sync_playwright, expect, Page
from playwright_utils import *

USERNAME='serge@twistellar.com.sculptorqa'
PASSWORD='2K23workhard!'
SECURITE_TOKEN='EeIdYKjLdwQVsQFuEryL87e7g'
DOMAIN='test' 

session_id, instance = SalesforceLogin(

    username=USERNAME, 
    password=PASSWORD,
    security_token=SECURITE_TOKEN,
    domain=DOMAIN 
)
sf = Salesforce(instance=instance, session_id=session_id)
print("Connected!")
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
timestamp_for_SF_date = datetime.now().strftime("%Y-%m-%d")
timestamp_for_SF_date_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0000")
timestamp_for_SF_time = datetime.now().strftime("%H:%M:%S.000Z")
print(timestamp)
RECORDS_QTY = 10
def Delete_product_test_004 (sf):
    Bundle_first_name = ["WWW"]
    Bundle_second_name = ["003"]
    # Feature_Name_moved_to = "Feature Number One"
    Product_name = "Test Product 004 test test test test test test test test test test test test test"

    for i in Bundle_first_name:

        for x in Bundle_second_name:
            print(f"\n=== Processing bundle mask: {i} - {x} ===")

            bundles = sf.query(
                f"SELECT Id, Name FROM Product2 WHERE Name like '{i} - {x}%' and RecordType.name = 'Product Bundle'"
            )

            for bundle in bundles["records"]:

                bundle_id = bundle["Id"] #take bundle id
                print(f"▶ Bundle found: {bundle['Name']} ({bundle_id})")
                option_result = sf.query(
                    f"""
                    SELECT Id, SCLP__Product__r.Name
                    FROM SCLP__ProductOption__c
                    WHERE SCLP__Product__r.name = '{Product_name}'
                    AND SCLP__Bundle__c = '{bundle_id}'
                    """
                ) #take option that needs to be moved
                option_id = option_result["records"][0]["Id"] #take option's id
                print(f"✔ Option found: {option_result['records'][0]["SCLP__Product__r"]["Name"]} ({option_id})")

                option_feature = sf.query(
                    f"""
                    SELECT Id, SCLP__Feature__c, SCLP__Order__c
                    FROM SCLP__ProductOption__c
                    WHERE SCLP__Bundle__c = '{bundle_id}'
                    """
                ) #take feature's options order and feature id
                
                if not option_feature["records"]:
                    continue
                old_feature_result = sf.query(
                    f"""
                    SELECT Id, SCLP__Product__r.Name, SCLP__Feature__c, SCLP__Feature__r.Name
                    FROM SCLP__ProductOption__c
                    WHERE SCLP__Product__r.name = '{Product_name}'
                    AND SCLP__Bundle__c = '{bundle_id}'
                    """
                )
                old_feature_id = old_feature_result['records'][0]['SCLP__Feature__c']
                # print(old_feature_result['records'][0]['SCLP__Feature__c'])
                # print(old_feature_result['records'][0]['SCLP__Feature__r']["Name"])
                sf.SCLP__ProductOption__c.delete(option_id)
                Qty_of_options_in_old_result = sf.query(
                    f"""
                    SELECT Id, SCLP__Product__r.name 
                    from SCLP__ProductOption__c 
                    where SCLP__Feature__c = '{old_feature_id}'
                    AND SCLP__Bundle__c = '{bundle_id}'
                    """)
                print(len(Qty_of_options_in_old_result['records']))
                print(f'This is an old Feature ID: {old_feature_id}')
                if len(Qty_of_options_in_old_result['records']) == 0:
                    sf.SCLP__ProductFeature__c.delete(old_feature_id)
Delete_product_test_004(sf)    
