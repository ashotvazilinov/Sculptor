from simple_salesforce import Salesforce, SalesforceLogin, SalesforceError
from datetime import datetime
import random
import time
from playwright.sync_api import sync_playwright, expect, Page

USERNAME='serge@twistellar.com.sculptorqa'
PASSWORD='2K23workhard!'
SECURITE_TOKEN='LdBcgrnZfVf4sL0PU3TzqXX0A'
DOMAIN='test' 
SITE_URL = f'https://{DOMAIN}.salesforce.com/'
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
def Main_product_option_set_true():
    Bundle_Full_name = ["ZZZ - 001 Test Bundle Created 2026-03-14_19-30-46",
                         "ZZZ - 002 Test Bundle Created 2026-03-14_19-30-46"]
    Feature_first_name = "test Number two" #do i need that?
    for x in Bundle_Full_name:
        print(f"\n=== Processing bundle mask: {x} ===")
        bundles = sf.query( f"SELECT Id, Name FROM Product2 WHERE Name = '{x}' and RecordType.name = 'Product Bundle' and IsActive = true")
        for bundle in bundles["records"]:
            bundle_id = bundle["Id"]
            option_result = sf.query(f"""
            SELECT
                name,
                id, SCLP__Product__r.name, SCLP__Feature__r.name, FS_Curtis_Bundle_Main_Product__c
            FROM
                SCLP__ProductOption__c
            WHERE
                SCLP__Feature__r.SCLP__Order__c = 1
                AND SCLP__Bundle__c = '{bundle_id}'
            """)
            option_name = option_result["records"][0]['SCLP__Product__r']['Name']
            feature_name = option_result["records"][0]['SCLP__Feature__r']['Name']
            print(option_name[0:2].lower())
            option_name_lower_two_first_letters = option_name[0:2].lower()
            print(feature_name[0:2].lower())
            feature_name_lower_two_first_letters = feature_name[0:2].lower()
            if option_name_lower_two_first_letters == feature_name_lower_two_first_letters:
                sf.SCLP__ProductOption__c.update(
                    option_result["records"][0]['Id'],
                    {
                        'FS_Curtis_Bundle_Main_Product__c': True
                    }

                )
# Main_product_option_set_true()
def set_product_lenght():
    Bundle_Full_name = ["ZZZ - 001 Test Bundle Created 2026-03-14_19-30-46",
                        "ZZZ - 002 Test Bundle Created 2026-03-14_19-30-46"]
    length_number = 3
    for x in Bundle_Full_name:
        print(f"\n=== Processing bundle mask: {x} ===")
        bundles = sf.query( f"SELECT Id, Name FROM Product2 WHERE Name = '{x}' and RecordType.name = 'Product Bundle' and IsActive = true")
        for bundle in bundles["records"]:
            bundle_id = bundle["Id"]
            option_result = sf.query(f"""
            SELECT
                name,
                id, SCLP__Product__r.name, SCLP__Feature__r.name, FS_Curtis_Bundle_Main_Product__c, SCLP__Product__c,
                SCLP__Product__r.FS_Curtis_Bundle_Optional_Code_Length__c
            FROM
                SCLP__ProductOption__c
            WHERE
                FS_Curtis_Bundle_Main_Product__c = true
                AND SCLP__Bundle__c = '{bundle_id}'
            """)
            print(option_result['records'][0]['SCLP__Product__r']['Name'])
            if option_result['records'][0]['FS_Curtis_Bundle_Main_Product__c'] == True and option_result['records'][0]['SCLP__Product__r']['FS_Curtis_Bundle_Optional_Code_Length__c'] == None:
                sf.Product2.update(
                    option_result["records"][0]['SCLP__Product__c'],
                    {
                        'FS_Curtis_Bundle_Optional_Code_Length__c': f'{length_number}'
                    })
                print(f'the product {option_result['records'][0]['SCLP__Product__r']['Name']} lenght is set to {length_number}')
# set_product_lenght()
def set_product_option_addition_and_location():
    Bundle_Full_name = ["ZZZ - 001 Test Bundle Created 2026-03-14_19-30-46",
                        "ZZZ - 002 Test Bundle Created 2026-03-14_19-30-46"]
    product_codes = ['SO-001', 'SO-003']
    feature_name = 'Feature Number One'
    code_addition = 9
    code_location = 5
    for x in Bundle_Full_name:
        print(f"\n=== Processing bundle mask: {x} ===")
        bundles = sf.query( f"SELECT Id, Name FROM Product2 WHERE Name = '{x}' and RecordType.name = 'Product Bundle' and IsActive = true")
        for bundle in bundles["records"]:
            bundle_id = bundle["Id"]
            for code in product_codes:
                option_result = sf.query(f"""
                SELECT
                    Id,
                    Name,
                    SCLP__Bundle__r.name,
                    SCLP__Product__r.name,
                    FS_Curtis_Bundle_Main_Product__c,
                    SCLP__Product__r.FS_Curtis_Bundle_Optional_Code_Length__c,
                    SCLP__Product__r.ProductCode, FS_Curtis_Dynamic_Code_Addition__c, FS_Curtis_Dynamic_Code_Location__c 
                FROM
                    SCLP__ProductOption__c
                WHERE
                    SCLP__Bundle__c = '{bundle_id}'
                    AND SCLP__Feature__r.name = '{feature_name}'
                    and SCLP__Product__r.ProductCode = '{code}'
                """)
                print(option_result['records'][0]['SCLP__Product__r']['Name'])
                sf.SCLP__ProductOption__c.update(
                    option_result["records"][0]['Id'],
                    {
                        'FS_Curtis_Dynamic_Code_Addition__c': f'{code_addition}',
                        'FS_Curtis_Dynamic_Code_Location__c': f'{code_location}'
                    })
                print(f'the product {option_result['records'][0]['SCLP__Product__r']['Name']} code Addition and location  is set to {code_addition} and {code_location}')

# set_product_option_addition_and_location()
def create_codes_combination_records_for_one():
    Bundle_Full_name = ["ZZZ - 001 Test Bundle Created 2026-03-14_19-30-46",
                        "ZZZ - 002 Test Bundle Created 2026-03-14_19-30-46"]
    product_codes = ['SO-001']
    Code_sequence__for_one = 'SPC'
    for x in Bundle_Full_name:
        print(f"\n=== Processing bundle mask: {x} ===")
        bundles = sf.query( f"SELECT Id, Name FROM Product2 WHERE Name = '{x}' and RecordType.name = 'Product Bundle' and IsActive = true")
        for bundle in bundles["records"]:
            bundle_id = bundle["Id"]
            for code in product_codes:
                option_result_for_one_product = sf.query(f"""
                SELECT
                    Id,
                    Name,
                    SCLP__Bundle__r.name, SCLP__Bundle__c,
                    SCLP__Product__r.name, SCLP__Product__c,
                    FS_Curtis_Bundle_Main_Product__c,
                    SCLP__Product__r.FS_Curtis_Bundle_Optional_Code_Length__c,
                    SCLP__Product__r.ProductCode, FS_Curtis_Dynamic_Code_Addition__c, FS_Curtis_Dynamic_Code_Location__c 
                FROM
                    SCLP__ProductOption__c
                WHERE
                    SCLP__Bundle__c = '{bundle_id}'
                    and SCLP__Product__r.ProductCode = '{code}'
                """)
                print(option_result_for_one_product['records'][0]['SCLP__Product__r']['Name'])
                try:
                    sf.FS_Curtis_Optional_Codes_Combination__c.create({
                            'Product1__c': f'{option_result_for_one_product['records'][0]['SCLP__Product__c']}',
                            'Bundle__c': f'{option_result_for_one_product['records'][0]['SCLP__Bundle__c']}',
                            'Code_sequence__c': f'{Code_sequence__for_one}'
                        })
                    print(f'123')
                except SalesforceError as e:
                    "FIELD_CUSTOM_VALIDATION_EXCEPTION" in str(e)
                    print('such a combination already exists')
create_codes_combination_records_for_one()
def create_codes_combination_records_for_two():
    Bundle_Full_name = ["ZZZ - 001 Test Bundle Created 2026-03-14_19-30-46",
                        "ZZZ - 002 Test Bundle Created 2026-03-14_19-30-46"]
    product_codes = ['SO-001', 'SO-003']
    Code_sequence__for_two = 'FPC'
    for x in Bundle_Full_name:
        print(f"\n=== Processing bundle mask: {x} ===")
        bundles = sf.query( f"SELECT Id, Name FROM Product2 WHERE Name = '{x}' and RecordType.name = 'Product Bundle' and IsActive = true")
        for bundle in bundles["records"]:
            bundle_id = bundle["Id"]
            option_result_for_two_options = sf.query(f"""
            SELECT
                Id,
                Name,
                SCLP__Bundle__r.name, SCLP__Product__c,
                SCLP__Product__r.name, SCLP__Bundle__c,
                FS_Curtis_Bundle_Main_Product__c,
                SCLP__Product__r.FS_Curtis_Bundle_Optional_Code_Length__c,
                SCLP__Product__r.ProductCode, FS_Curtis_Dynamic_Code_Addition__c, FS_Curtis_Dynamic_Code_Location__c 
            FROM
                SCLP__ProductOption__c
            WHERE
                SCLP__Bundle__c = '{bundle_id}'
                and (SCLP__Product__r.ProductCode = '{product_codes[0]}'
                or SCLP__Product__r.ProductCode = '{product_codes[1]}')
            """)
            print(option_result_for_two_options['records'][0]['SCLP__Product__c'])
            print(option_result_for_two_options['records'][1]['SCLP__Product__c'])
            try:

                sf.FS_Curtis_Optional_Codes_Combination__c.create({
                            'Product1__c': f'{option_result_for_two_options['records'][0]['SCLP__Product__c']}',
                            'Product2__c': f'{option_result_for_two_options['records'][1]['SCLP__Product__c']}',
                            'Bundle__c': f'{option_result_for_two_options['records'][0]['SCLP__Bundle__c']}',
                            'Code_sequence__c': f'{Code_sequence__for_two}'
                    })
                print(f'123')
            except SalesforceError as e:
                "FIELD_CUSTOM_VALIDATION_EXCEPTION" in str(e)
                print('such a combination already exists')
create_codes_combination_records_for_two()