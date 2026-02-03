from simple_salesforce import Salesforce, SalesforceLogin, SalesforceError
from datetime import datetime
import random
import time
from playwright.sync_api import sync_playwright, expect, Page
from old_playwright_utils import *

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
def Factory_Options_renaming(sf):
    # Iteration_order = 0 

    Bundle_first_name = ["WWW", "YYY"]
    Bundle_second_name = ["001", "003"]
    Full_name = ["WWW - 001", "WWW - 002"]
    Old_Feature_Name = "Number two"
    New_Feature_Name = "Testing number two"
    # for i in Bundle_first_name:

    for x in Full_name:
        print(f"\n=== Processing bundle mask: {x} ===")
        bundles = sf.query(
            f"SELECT Id, Name FROM Product2 WHERE Name like '{x}%' and RecordType.name = 'Product Bundle'"
        )

        for bundle in bundles["records"]:

            bundle_id = bundle["Id"]

            feature_result = sf.query(
                f"""
                SELECT Id, Name
                FROM SCLP__ProductFeature__c
                WHERE Name LIKE '%{Old_Feature_Name}%'
                AND SCLP__Product__c = '{bundle_id}'
                """
            )

            for feature in feature_result["records"]:
                sf.SCLP__ProductFeature__c.update(feature["Id"], {'Name': New_Feature_Name})
            #     new_feature_result = sf.query(
            #     f"""
            #     SELECT Id, Name
            #     FROM SCLP__ProductFeature__c
            #     WHERE Name LIKE '%Number two%'
            #     AND SCLP__Product__c = '{bundle_id}'
            #     """
            # )
                # Name_of_new_feature = new_feature_result["records"][0]["Name"]

                # Iteration_order += 1
                # print(feature["Id"], feature["Name"], "was and became", Name_of_new_feature,  Iteration_order)
# Factory_Options_renaming(sf)
def Move_iCommand (sf):
    Bundle_first_name = ["ZZZ", "YYY"]
    Bundle_second_name = ["002", "003"]
    Full_name = ["WWW - 001", "WWW - 002"]
    Feature_Name_moved_to = "Feature Number One"
    Product_name = "Test Product 004 test test test test test test test test test test test test test"


    for x in Full_name:
        print(f"\n=== Processing bundle mask: {x} ===")

        bundles = sf.query(
            f"SELECT Id, Name FROM Product2 WHERE Name like '{x}%' and RecordType.name = 'Product Bundle'"
        )

        for bundle in bundles["records"]:

            bundle_id = bundle["Id"] #take bundle id
            bundle_name = bundle["Name"]
            print(f"▶ Bundle found: {bundle['Name']} ({bundle_id})")
            option_result = sf.query(
                f"""
                SELECT Id, SCLP__Product__r.Name
                FROM SCLP__ProductOption__c
                WHERE SCLP__Product__r.name = '{Product_name}'
                AND SCLP__Bundle__c = '{bundle_id}'
                """
            ) #take option that needs to be moved
            if not option_result["records"]:
                print("❌ Option not found")
                continue
            else:
                option_id = option_result["records"][0]["Id"] #take option's id
                print(f"✔ Option found: {option_result['records'][0]["SCLP__Product__r"]["Name"]} ({option_id})")


            factory_option_feature = sf.query(
                f"""
                SELECT Id, SCLP__Feature__c, SCLP__Order__c
                FROM SCLP__ProductOption__c
                WHERE SCLP__Feature__r.Name LIKE '%{Feature_Name_moved_to}%'
                AND SCLP__Bundle__c = '{bundle_id}'
                """
            ) #take feature's options order and feature id
            
            if not factory_option_feature["records"]:
                continue
            # max_order_integer = factory_option_feature["records"][0]["SCLP__Order__c"]
            # print(f'order is {max_order_integer}')
            feature_id = factory_option_feature["records"][0]["SCLP__Feature__c"]
            orders = [
                rec["SCLP__Order__c"]
                for rec in factory_option_feature["records"]
                if rec.get("SCLP__Order__c") is not None
            ] #take max order of options from the feature to move to

            max_order = max(orders) if orders else 0
            next_order = max_order + 1
            old_feature_result = sf.query(
                f"""
                SELECT Id, SCLP__Product__r.Name, SCLP__Feature__c, SCLP__Feature__r.Name
                FROM SCLP__ProductOption__c
                WHERE SCLP__Product__r.name = '{Product_name}'
                AND SCLP__Bundle__c = '{bundle_id}'
                """
            )
            old_feature_id = old_feature_result['records'][0]['SCLP__Feature__c']
            old_feature_name = old_feature_result['records'][0]['SCLP__Feature__r']['Name']
            # print(old_feature_result['records'][0]['SCLP__Feature__c'])
            # print(old_feature_result['records'][0]['SCLP__Feature__r']["Name"])
            sf.SCLP__ProductOption__c.update(
                option_id,
                {
                    # "SCLP__Feature__c": feature_id,
                    "SCLP__Order__c": next_order
                }
            )
            sf.SCLP__ProductOption__c.update(
                option_id,
                {
                    "SCLP__Feature__c": feature_id,
                    # "SCLP__Order__c": next_order
                }
            )
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
                print(f'Feature {old_feature_name} is deleted from bundle {bundle_name}')
# Move_iCommand(sf)    
def delete_product_from_bundle(sf):
    Bundle_first_name = ["YYY"]
    Bundle_second_name = ["002"]
    Full_name = ["WWW - 001", "WWW - 002"]

    # Feature_Name_moved_to = "Feature Number One"
    Product_name = "Test Product 004 test test test test test test test test test test test test test"


    for x in Full_name:
        print(f"\n=== Processing bundle mask: {x} ===")

        bundles = sf.query(
            f"SELECT Id, Name FROM Product2 WHERE Name like '{x}%' and RecordType.name = 'Product Bundle'"
        )

        for bundle in bundles["records"]:

            bundle_id = bundle["Id"] #take bundle id
            bundle_name = bundle["Name"]
            print(f"▶ Bundle found: {bundle['Name']} ({bundle_id})")
            option_result = sf.query(
                f"""
                SELECT Id, SCLP__Product__r.Name
                FROM SCLP__ProductOption__c
                WHERE SCLP__Product__r.name = '{Product_name}'
                AND SCLP__Bundle__c = '{bundle_id}'
                """
            ) #take option that needs to be removed
            option_id = option_result["records"][0]["Id"] #take option's id
            if not option_result["records"]:
                print("❌ Option not found")
                continue
            else:
                print(f"✔ Option found: {option_result['records'][0]["SCLP__Product__r"]["Name"]} ({option_id})")

            # factory_option_feature = sf.query(
            #     f"""
            #     SELECT Id, SCLP__Feature__c, SCLP__Order__c
            #     FROM SCLP__ProductOption__c
            #     WHERE SCLP__Feature__r.Name LIKE '%{Feature_Name_moved_to}%'
            #     AND SCLP__Bundle__c = '{bundle_id}'
            #     """
            # ) #take feature's options order and feature id
            
            # if not factory_option_feature["records"]:
            #     continue
            # max_order_integer = factory_option_feature["records"][0]["SCLP__Order__c"]
            # print(f'order is {max_order_integer}')
            # feature_id = factory_option_feature["records"][0]["SCLP__Feature__c"]
            # orders = [
            #     rec["SCLP__Order__c"]
            #     for rec in factory_option_feature["records"]
            #     if rec.get("SCLP__Order__c") is not None
            # ] #take max order of options from the feature to move to

            # max_order = max(orders) if orders else 0
            # next_order = max_order + 1
            old_feature_result = sf.query(
                f"""
                SELECT Id, SCLP__Product__r.Name, SCLP__Feature__c, SCLP__Feature__r.Name
                FROM SCLP__ProductOption__c
                WHERE Id = '{option_id}'
                """
            )
            old_feature_id = old_feature_result['records'][0]['SCLP__Feature__c']
            old_feature_name = old_feature_result['records'][0]['SCLP__Feature__r']['Name']
            # print(old_feature_result['records'][0]['SCLP__Feature__c'])
            # print(old_feature_result['records'][0]['SCLP__Feature__r']["Name"])
            sf.SCLP__ProductOption__c.delete(
                option_id                )
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
                print(f'Feature {old_feature_name} is deleted from bundle {bundle_name}')
            # Created_single_QLIs = sf.query(
            #     f"""
            #     SELECT
            #         Id, Name, SCLP__Product__r.name, SCLP__BundleLineItem__c, SCLP__ProductOption__c
            #     FROM
            #         SCLP__QuoteLineItem__c
            #     WHERE
            #         LastModifiedDate = today
            #         and LastModifiedBy.name = 'Serge Koczanowski'
            #         AND SCLP__ProductOption__c = NULL
            #         and SCLP__Product__r.name = '{Product_name}'
            #     """)
            
            # if not Created_single_QLIs["records"]:
            #     print("❌ QLI not found")
            #     continue
            # else:
            #     print(f'Newly created QLI is found{Created_single_QLIs['records'][0]['SCLP__Product__r']['Name']}')

            # QLIs_Id = Created_single_QLIs['records'][0]['Id']
            # sf.SCLP__QuoteLineItem__c.delete(QLIs_Id)
            # print('The QLI is delted')
# delete_product_from_bundle(sf)

def delete_feature_from_bundle(sf):
    Bundle_first_name = ["YYY"]
    Bundle_second_name = ["002"]
    Full_name = ["ZZZ - 003", "WWW - 002"]

    # Feature_Name_moved_to = "Feature Number One"
    Feature_name = "Number two"


    for x in Full_name:
        print(f"\n=== Processing bundle mask: {x} ===")

        bundles = sf.query(
            f"SELECT Id, Name FROM Product2 WHERE Name like '{x}%' and RecordType.name = 'Product Bundle'"
        )

        for bundle in bundles["records"]:

            bundle_id = bundle["Id"] #take bundle id
            bundle_name = bundle["Name"]
            print(f"▶ Bundle found: {bundle['Name']} ({bundle_id})")
            feature_result = sf.query(
                f"""
                SELECT Id, Name
                FROM SCLP__ProductFeature__c
                WHERE name = '{Feature_name}'
                AND SCLP__Product__c = '{bundle_id}'
                """
            ) #take feature that needs to be removed
            if not feature_result["records"]:
                print("❌ feature not found")
                continue

            feature = feature_result["records"][0]
            feature_id = feature["Id"]

            print(f"✔ feature found: {feature['Name']} ({feature_id})")

            sf.SCLP__ProductFeature__c.delete(feature_id)
# delete_feature_from_bundle(sf)


def create_products_and_pricebook_entries(sf):
    for i in range(1, RECORDS_QTY): 
        product_name = f"Test Product {i:03d}"
        existing_product  = sf.query(f"SELECT Id FROM Product2 WHERE Name = '{product_name}'")
        

        if existing_product.get('records'):
            print(f"Product '{product_name}' already exists. Skip creation.")
            continue
        
        if i != 4:
            product = sf.Product2.create({
                'Name': f'{product_name}',
                'IsActive': True,
                'Description': f'This is a test description for Product {i:03d}',
                'ProductCode': f'SO-{i:03d}',
                'Brand__c': 'FS-Curtis'
            })
        else:
            try:
                product = sf.Product2.create({
                    'Name': f'{product_name} test test test test test test test test test test test test test',
                    'IsActive': True,
                    'SCLPCE__ManualCostForCommunity__c': True,
                    'Brand__c': 'FS-Curtis'

                })
            except IndexError:
                print("No SCLP__.")
                product = sf.Product2.create({
                    'Name': product_name,
                    'IsActive': True,
                    'ManualCostForCommunity__c': True,
                    # 'Description': f'This is a test description for Product {i:03d}',
                    # 'ProductCode': f'SO-{i:03d}'
                    })
            except SalesforceError as e:
                "INVALID_TYPE" in str(e)
                print('No such field as ManualCostForCommunity__c')
                product = sf.Product2.create({
                    'Name': f'{product_name} test test test test test test test test test test test test test',
                    'IsActive': True,
                    # 'Description': f'This is a test description for Product {i:03d}',
                    # 'ProductCode': f'SO-{i:03d}',
                })

        # Get standard PB id
        pricebook_id = None
        pricebook_entries = sf.query("SELECT Id, Name FROM Pricebook2 WHERE IsStandard = TRUE")
        pricebook_sculptor_entries = sf.query("SELECT Id, Name FROM Pricebook2 WHERE Name = 'FS-Curtis Sculptor'")

        for entry in pricebook_entries['records']:
            if entry['Name'] == 'Standard Price Book':
                pricebook_id = entry['Id']
                break
        for sculptor_entry in pricebook_sculptor_entries['records']:
            if sculptor_entry['Name'] == 'FS-Curtis Sculptor':
                pricebook_sculptor_id = sculptor_entry['Id']
                break
        


        # set price for the current product (1, 2, 3, 4, 5)
        price = i * 100

        # check if there is a record of the for the product and PB
        existing_entry = sf.query(f"SELECT Id FROM PricebookEntry WHERE Pricebook2Id = '{pricebook_id}' AND Product2Id = '{product['id']}'")
        if existing_entry['totalSize'] == 0:
            # If there is no record we create one
            sf.PricebookEntry.create({
                'Pricebook2Id': pricebook_id,
                'Product2Id': product['id'],
                'UnitPrice': price,
                'IsActive': True
            })
            print(f"PricebookEntry created for {product_name} with price {price}")
        else:
            print(f"PricebookEntry for {product_name} already exists.")
        existing_entry = sf.query(f"SELECT Id FROM PricebookEntry WHERE Pricebook2Id = '{pricebook_sculptor_id}' AND Product2Id = '{product['id']}'")
        if existing_entry['totalSize'] == 0:
            # If there is no record we create one
            sf.PricebookEntry.create({
                'Pricebook2Id': pricebook_sculptor_id,
                'Product2Id': product['id'],
                'UnitPrice': price,
                'IsActive': True
            })
            print(f"PricebookEntry created for {product_name} with price {price}")
        else:
            print(f"PricebookEntry for {product_name} already exists.")

    print("Products and Pricebook Entries created successfully!")
def delete_test_product_salesforce(sf):
    print("Start Product Deleting...")
    for i in range(1, RECORDS_QTY):
        query = f"SELECT Name, Id FROM Product2 WHERE Name like 'Test Product {i:03d}%'"
        results = sf.query(query) 
        while results.get('records'):
            for record in results['records']:
                product_id = record['Id']
                product_name = record['Name']

                try:
                    sf.Product2.delete(product_id) 
                    print(f"product Deleted '{product_name}' with ID {product_id}")
                except Exception as e:
                    print(f"Error deleting '{product_name}': {e}")

            if results.get('nextRecordsUrl'):
                results = sf.query_more(results['nextRecordsUrl'], True)
            else:
                break

    print("All product are deleted.")

def create_bundle_WWW_001_1(sf): #1
    print('Start Bundle 1')
    bundle_query_result = sf.query(f"select name, id from product2 where name like 'WWW - 001 Test Bundle Created%' and Description = 'Test 1'" )
    if len(bundle_query_result.get('records')) >= 1:
        print('Bundle already created')
    else:
        print('bundle to be created')
        Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
        rt_id = Rt_bundle_in_qurey['records'][0]['Id']
        print(f"Bundle Record Type id is {rt_id}")
        sf.product2.create({
            'Name': f'WWW - 001 Test Bundle Created {timestamp}',
            'RecordTypeId': rt_id,
            'IsActive': 'true',
            'Brand__c': 'FS-Curtis',
            'Description': "Test 1",
            'Sculptor_CPQ_Product__c': True,
            'ProductCode': 'Test Product Code',
        })
        created_bundle_id = sf.query(f"select name, id from product2 where name = 'WWW - 001 Test Bundle Created {timestamp}' and Description = 'Test 1'")['records'][0]['Id']
        print(f'New ID of bundle is {created_bundle_id}\n Now lets create Features')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Feature Number One',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'true',
            'SCLP__Order__c': '1',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            'SCLP__Tip__c': 'Feature Number One tip'
        })
        first_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 1 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'first feature id is {first_feature_id}')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Number two',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'true',
            'SCLP__Tip__c': 'Feature Number two tip'
        })

        second_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 2 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'second feature id is {second_feature_id}\n Now lets create options')
        product1_id = sf.query(f"select id from product2 where name = 'Test Product 001'")['records'][0]['Id']
        product2_id = sf.query(f"select id from product2 where name = 'Test Product 002'")['records'][0]['Id']
        product3_id = sf.query(f"select id from product2 where name = 'Test Product 003'")['records'][0]['Id']
        product4_id = sf.query(f"select id from product2 where name like 'Test Product 004%'")['records'][0]['Id']
        product5_id = sf.query(f"select id from product2 where name = 'Test Product 005'")['records'][0]['Id']
        product6_id = sf.query(f"select id from product2 where name = 'Test Product 006'")['records'][0]['Id']
        product7_id = sf.query(f"select id from product2 where name = 'Test Product 007'")['records'][0]['Id']
        product8_id = sf.query(f"select id from product2 where name = 'Test Product 008'")['records'][0]['Id']


        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product1_id,
            'SCLP__ChildRequired__c': 'true',
            'SCLP__Tip__c': 'Tip test 1',
            'SCLP__HideInQuote__c': True
        })
        option1_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 001' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('Options 1 is created')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__ChildRequired__c': 'false',
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product2_id,
            'SCLP__MasterOption__c': option1_id,
            'SCLP__Tip__c': 'Tip test 2',
            'SCLP__HideInQuote__c': True
        })
        print('Options 2 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product3_id,
            'SCLP__Tip__c': 'Tip test 3'
        })
        print('Options 3 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': second_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product4_id,
            'SCLP__Tip__c': 'Tip test 4'
        })
        print('Options 4 is created')
        # sf.SCLP__ProductOption__c.create({
        #     'SCLP__BundleQuantity__c': '1',
        #     'SCLP__Bundle__c': created_bundle_id,
        #     'SCLP__Feature__c': second_feature_id,
        #     'SCLP__Order__c': '2',
        #     'SCLP__Product__c': product5_id,
        #     'SCLP__DefaultOption__c': 'true',
        #     'SCLP__Tip__c': 'Tip test 5'
        # })
        # print('Options 5 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product6_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__Tip__c': 'Tip test 6'
        })
        print('option 6 created')
        option6_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 006' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('query for 6 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product7_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__MasterOption__c': option6_id,
            'SCLP__Tip__c': 'Tip test 7',
            'SCLP__BundleQuantity__c': ''
        })
        print('option 7 created')
        print('query for 7 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product8_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Tip__c': 'Tip test 8'
        })
        print('option 8 created')
def create_bundle_WWW_002_1(sf): #2
    print('Start Bundle creation 2')
    bundle_query_result = sf.query(f"select name, id from product2 where name like 'WWW - 002 Test Bundle Created%' and Description = 'Test 1'")
    if len(bundle_query_result.get('records')) >= 1:
        print('Bundle already created')
    else:
        print('bundle to be created')
        Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
        rt_id = Rt_bundle_in_qurey['records'][0]['Id']
        print(f"Bundle Record Type id is {rt_id}")
        sf.product2.create({
            'Name': f'WWW - 002 Test Bundle Created {timestamp}',
            'RecordTypeId': rt_id,
            'IsActive': 'true',
            'Brand__c': 'FS-Curtis',
            'Description': "Test 1",
            'Sculptor_CPQ_Product__c': True,
            'ProductCode': 'Test Product Code'

        })
        created_bundle_id = sf.query(f"select name, id from product2 where name = 'WWW - 002 Test Bundle Created {timestamp}' and Description = 'Test 1'")['records'][0]['Id']
        print(f'New ID of bundle is {created_bundle_id}\n Now lets create Features')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Feature Number One',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'true',
            'SCLP__Order__c': '1',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            'SCLP__Tip__c': 'Feature Number One tip'
        })
        first_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 1 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'first feature id is {first_feature_id}')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Number two',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'true',
            'SCLP__Tip__c': 'Feature Number two tip'
        })

        second_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 2 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'second feature id is {second_feature_id}\n Now lets create options')
        product1_id = sf.query(f"select id from product2 where name = 'Test Product 001'")['records'][0]['Id']
        product2_id = sf.query(f"select id from product2 where name = 'Test Product 002'")['records'][0]['Id']
        product3_id = sf.query(f"select id from product2 where name = 'Test Product 003'")['records'][0]['Id']
        product4_id = sf.query(f"select id from product2 where name like 'Test Product 004%'")['records'][0]['Id']
        product5_id = sf.query(f"select id from product2 where name = 'Test Product 005'")['records'][0]['Id']
        product6_id = sf.query(f"select id from product2 where name = 'Test Product 006'")['records'][0]['Id']
        product7_id = sf.query(f"select id from product2 where name = 'Test Product 007'")['records'][0]['Id']
        product8_id = sf.query(f"select id from product2 where name = 'Test Product 008'")['records'][0]['Id']


        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product1_id,
            'SCLP__ChildRequired__c': 'true',
            'SCLP__Tip__c': 'Tip test 1',
            'SCLP__HideInQuote__c': True
        })
        option1_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 001' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('Options 1 is created')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__ChildRequired__c': 'false',
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product2_id,
            'SCLP__MasterOption__c': option1_id,
            'SCLP__Tip__c': 'Tip test 2',
            'SCLP__HideInQuote__c': True
        })
        print('Options 2 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product3_id,
            'SCLP__Tip__c': 'Tip test 3'
        })
        print('Options 3 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': second_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product4_id,
            'SCLP__Tip__c': 'Tip test 4'
        })
        print('Options 4 is created')
        # sf.SCLP__ProductOption__c.create({
        #     'SCLP__BundleQuantity__c': '1',
        #     'SCLP__Bundle__c': created_bundle_id,
        #     'SCLP__Feature__c': second_feature_id,
        #     'SCLP__Order__c': '2',
        #     'SCLP__Product__c': product5_id,
        #     'SCLP__DefaultOption__c': 'true',
        #     'SCLP__Tip__c': 'Tip test 5'
        # })
        # print('Options 5 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product6_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__Tip__c': 'Tip test 6'
        })
        print('option 6 created')
        option6_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 006' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('query for 6 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product7_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__MasterOption__c': option6_id,
            'SCLP__Tip__c': 'Tip test 7',
            'SCLP__BundleQuantity__c': ''
        })
        print('option 7 created')
        print('query for 7 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product8_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Tip__c': 'Tip test 8'
        })
        print('option 8 created')
def create_bundle_WWW_003_1(sf): #3
    print('Start Bundle creation 3')
    bundle_query_result = sf.query(f"select name, id from product2 where name like 'WWW - 003 Test Bundle Created%' and Description = 'Test 1'")
    if len(bundle_query_result.get('records')) >= 1:
        print('Bundle already created')
    else:
        print('bundle to be created')
        Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
        rt_id = Rt_bundle_in_qurey['records'][0]['Id']
        print(f"Bundle Record Type id is {rt_id}")
        sf.product2.create({
            'Name': f'WWW - 003 Test Bundle Created {timestamp}',
            'RecordTypeId': rt_id,
            'IsActive': 'true',
            'Brand__c': 'FS-Curtis',
            'Description': "Test 1",
            'Sculptor_CPQ_Product__c': True,
            'ProductCode': 'Test Product Code'

        })
        created_bundle_id = sf.query(f"select name, id from product2 where name = 'WWW - 003 Test Bundle Created {timestamp}' and Description = 'Test 1'")['records'][0]['Id']
        print(f'New ID of bundle is {created_bundle_id}\n Now lets create Features')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Feature Number One',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'true',
            'SCLP__Order__c': '1',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            'SCLP__Tip__c': 'Feature Number One tip'
        })
        first_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 1 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'first feature id is {first_feature_id}')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Number two',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'true',
            'SCLP__Tip__c': 'Feature Number two tip'
        })

        second_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 2 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'second feature id is {second_feature_id}\n Now lets create options')
        product1_id = sf.query(f"select id from product2 where name = 'Test Product 001'")['records'][0]['Id']
        product2_id = sf.query(f"select id from product2 where name = 'Test Product 002'")['records'][0]['Id']
        product3_id = sf.query(f"select id from product2 where name = 'Test Product 003'")['records'][0]['Id']
        product4_id = sf.query(f"select id from product2 where name like 'Test Product 004%'")['records'][0]['Id']
        product5_id = sf.query(f"select id from product2 where name = 'Test Product 005'")['records'][0]['Id']
        product6_id = sf.query(f"select id from product2 where name = 'Test Product 006'")['records'][0]['Id']
        product7_id = sf.query(f"select id from product2 where name = 'Test Product 007'")['records'][0]['Id']
        product8_id = sf.query(f"select id from product2 where name = 'Test Product 008'")['records'][0]['Id']


        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product1_id,
            'SCLP__ChildRequired__c': 'true',
            'SCLP__Tip__c': 'Tip test 1',
            'SCLP__HideInQuote__c': True
        })
        option1_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 001' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('Options 1 is created')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__ChildRequired__c': 'false',
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product2_id,
            'SCLP__MasterOption__c': option1_id,
            'SCLP__Tip__c': 'Tip test 2',
            'SCLP__HideInQuote__c': True
        })
        print('Options 2 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product3_id,
            'SCLP__Tip__c': 'Tip test 3'
        })
        print('Options 3 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': second_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product4_id,
            'SCLP__Tip__c': 'Tip test 4'
        })
        print('Options 4 is created')
        # sf.SCLP__ProductOption__c.create({
        #     'SCLP__BundleQuantity__c': '1',
        #     'SCLP__Bundle__c': created_bundle_id,
        #     'SCLP__Feature__c': second_feature_id,
        #     'SCLP__Order__c': '2',
        #     'SCLP__Product__c': product5_id,
        #     'SCLP__DefaultOption__c': 'true',
        #     'SCLP__Tip__c': 'Tip test 5'
        # })
        # print('Options 5 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product6_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__Tip__c': 'Tip test 6'
        })
        print('option 6 created')
        option6_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 006' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('query for 6 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product7_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__MasterOption__c': option6_id,
            'SCLP__Tip__c': 'Tip test 7',
            'SCLP__BundleQuantity__c': ''
        })
        print('option 7 created')
        print('query for 7 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product8_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Tip__c': 'Tip test 8'
        })
        print('option 8 created')
def create_bundle_YYY_001_1(sf): #4
    print('Start Bundle creation 4')
    bundle_query_result = sf.query(f"select name, id from product2 where name like 'YYY - 001 Test Bundle Created%' and Description = 'Test 1'")
    if len(bundle_query_result.get('records')) >= 1:
        print('Bundle already created')
    else:
        print('bundle to be created')
        Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
        rt_id = Rt_bundle_in_qurey['records'][0]['Id']
        print(f"Bundle Record Type id is {rt_id}")
        sf.product2.create({
            'Name': f'YYY - 001 Test Bundle Created {timestamp}',
            'RecordTypeId': rt_id,
            'IsActive': 'true',
            'Brand__c': 'FS-Curtis',
            'Description': "Test 1",
            'Sculptor_CPQ_Product__c': True,
            'ProductCode': 'Test Product Code'

        })
        created_bundle_id = sf.query(f"select name, id from product2 where name = 'YYY - 001 Test Bundle Created {timestamp}' and Description = 'Test 1'")['records'][0]['Id']
        print(f'New ID of bundle is {created_bundle_id}\n Now lets create Features')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Feature Number One',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'true',
            'SCLP__Order__c': '1',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            'SCLP__Tip__c': 'Feature Number One tip'
        })
        first_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 1 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'first feature id is {first_feature_id}')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Number two',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'true',
            'SCLP__Tip__c': 'Feature Number two tip'
        })

        second_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 2 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'second feature id is {second_feature_id}\n Now lets create options')
        product1_id = sf.query(f"select id from product2 where name = 'Test Product 001'")['records'][0]['Id']
        product2_id = sf.query(f"select id from product2 where name = 'Test Product 002'")['records'][0]['Id']
        product3_id = sf.query(f"select id from product2 where name = 'Test Product 003'")['records'][0]['Id']
        product4_id = sf.query(f"select id from product2 where name like 'Test Product 004%'")['records'][0]['Id']
        product5_id = sf.query(f"select id from product2 where name = 'Test Product 005'")['records'][0]['Id']
        product6_id = sf.query(f"select id from product2 where name = 'Test Product 006'")['records'][0]['Id']
        product7_id = sf.query(f"select id from product2 where name = 'Test Product 007'")['records'][0]['Id']
        product8_id = sf.query(f"select id from product2 where name = 'Test Product 008'")['records'][0]['Id']


        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product1_id,
            'SCLP__ChildRequired__c': 'true',
            'SCLP__Tip__c': 'Tip test 1',
            'SCLP__HideInQuote__c': True
        })
        option1_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 001' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('Options 1 is created')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__ChildRequired__c': 'false',
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product2_id,
            'SCLP__MasterOption__c': option1_id,
            'SCLP__Tip__c': 'Tip test 2',
            'SCLP__HideInQuote__c': True
        })
        print('Options 2 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product3_id,
            'SCLP__Tip__c': 'Tip test 3'
        })
        print('Options 3 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': second_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product4_id,
            'SCLP__Tip__c': 'Tip test 4'
        })
        print('Options 4 is created')
        # sf.SCLP__ProductOption__c.create({
        #     'SCLP__BundleQuantity__c': '1',
        #     'SCLP__Bundle__c': created_bundle_id,
        #     'SCLP__Feature__c': second_feature_id,
        #     'SCLP__Order__c': '2',
        #     'SCLP__Product__c': product5_id,
        #     'SCLP__DefaultOption__c': 'true',
        #     'SCLP__Tip__c': 'Tip test 5'
        # })
        # print('Options 5 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product6_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__Tip__c': 'Tip test 6'
        })
        print('option 6 created')
        option6_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 006' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('query for 6 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product7_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__MasterOption__c': option6_id,
            'SCLP__Tip__c': 'Tip test 7',
            'SCLP__BundleQuantity__c': ''
        })
        print('option 7 created')
        print('query for 7 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product8_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Tip__c': 'Tip test 8'
        })
        print('option 8 created')
def create_bundle_YYY_002_1(sf): #5
    print('Start Bundle creation 5')
    bundle_query_result = sf.query(f"select name, id from product2 where name like 'YYY - 002 Test Bundle Created%' and Description = 'Test 1'")
    if len(bundle_query_result.get('records')) >= 1:
        print('Bundle already created')
    else:
        print('bundle to be created')
        Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
        rt_id = Rt_bundle_in_qurey['records'][0]['Id']
        print(f"Bundle Record Type id is {rt_id}")
        sf.product2.create({
            'Name': f'YYY - 002 Test Bundle Created {timestamp}',
            'RecordTypeId': rt_id,
            'IsActive': 'true',
            'Brand__c': 'FS-Curtis',
            'Description': "Test 1",
            'Sculptor_CPQ_Product__c': True,
            'ProductCode': 'Test Product Code'

        })
        created_bundle_id = sf.query(f"select name, id from product2 where name = 'YYY - 002 Test Bundle Created {timestamp}' and Description = 'Test 1'")['records'][0]['Id']
        print(f'New ID of bundle is {created_bundle_id}\n Now lets create Features')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Feature Number One',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'true',
            'SCLP__Order__c': '1',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            'SCLP__Tip__c': 'Feature Number One tip'
        })
        first_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 1 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'first feature id is {first_feature_id}')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Number two',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'true',
            'SCLP__Tip__c': 'Feature Number two tip'
        })

        second_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 2 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'second feature id is {second_feature_id}\n Now lets create options')
        product1_id = sf.query(f"select id from product2 where name = 'Test Product 001'")['records'][0]['Id']
        product2_id = sf.query(f"select id from product2 where name = 'Test Product 002'")['records'][0]['Id']
        product3_id = sf.query(f"select id from product2 where name = 'Test Product 003'")['records'][0]['Id']
        product4_id = sf.query(f"select id from product2 where name like 'Test Product 004%'")['records'][0]['Id']
        product5_id = sf.query(f"select id from product2 where name = 'Test Product 005'")['records'][0]['Id']
        product6_id = sf.query(f"select id from product2 where name = 'Test Product 006'")['records'][0]['Id']
        product7_id = sf.query(f"select id from product2 where name = 'Test Product 007'")['records'][0]['Id']
        product8_id = sf.query(f"select id from product2 where name = 'Test Product 008'")['records'][0]['Id']


        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product1_id,
            'SCLP__ChildRequired__c': 'true',
            'SCLP__Tip__c': 'Tip test 1',
            'SCLP__HideInQuote__c': True
        })
        option1_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 001' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('Options 1 is created')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__ChildRequired__c': 'false',
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product2_id,
            'SCLP__MasterOption__c': option1_id,
            'SCLP__Tip__c': 'Tip test 2',
            'SCLP__HideInQuote__c': True
        })
        print('Options 2 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product3_id,
            'SCLP__Tip__c': 'Tip test 3'
        })
        print('Options 3 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': second_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product4_id,
            'SCLP__Tip__c': 'Tip test 4'
        })
        print('Options 4 is created')
        # sf.SCLP__ProductOption__c.create({
        #     'SCLP__BundleQuantity__c': '1',
        #     'SCLP__Bundle__c': created_bundle_id,
        #     'SCLP__Feature__c': second_feature_id,
        #     'SCLP__Order__c': '2',
        #     'SCLP__Product__c': product5_id,
        #     'SCLP__DefaultOption__c': 'true',
        #     'SCLP__Tip__c': 'Tip test 5'
        # })
        # print('Options 5 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product6_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__Tip__c': 'Tip test 6'
        })
        print('option 6 created')
        option6_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 006' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('query for 6 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product7_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__MasterOption__c': option6_id,
            'SCLP__Tip__c': 'Tip test 7',
            'SCLP__BundleQuantity__c': ''
        })
        print('option 7 created')
        print('query for 7 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product8_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Tip__c': 'Tip test 8'
        })
        print('option 8 created')
def create_bundle_YYY_003_1(sf): #6
    print('Start Bundle creation 6')
    bundle_query_result = sf.query(f"select name, id from product2 where name like 'YYY - 003 Test Bundle Created%' and Description = 'Test 1'")
    if len(bundle_query_result.get('records')) >= 1:
        print('Bundle already created')
    else:
        print('bundle to be created')
        Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
        rt_id = Rt_bundle_in_qurey['records'][0]['Id']
        print(f"Bundle Record Type id is {rt_id}")
        sf.product2.create({
            'Name': f'YYY - 003 Test Bundle Created {timestamp}',
            'RecordTypeId': rt_id,
            'IsActive': 'true',
            'Brand__c': 'FS-Curtis',
            'Description': "Test 1",
            'Sculptor_CPQ_Product__c': True,
            'ProductCode': 'Test Product Code'

        })
        created_bundle_id = sf.query(f"select name, id from product2 where name = 'YYY - 003 Test Bundle Created {timestamp}' and Description = 'Test 1'")['records'][0]['Id']
        print(f'New ID of bundle is {created_bundle_id}\n Now lets create Features')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Feature Number One',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'true',
            'SCLP__Order__c': '1',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            'SCLP__Tip__c': 'Feature Number One tip'
        })
        first_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 1 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'first feature id is {first_feature_id}')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Number two',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'true',
            'SCLP__Tip__c': 'Feature Number two tip'
        })

        second_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 2 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'second feature id is {second_feature_id}\n Now lets create options')
        product1_id = sf.query(f"select id from product2 where name = 'Test Product 001'")['records'][0]['Id']
        product2_id = sf.query(f"select id from product2 where name = 'Test Product 002'")['records'][0]['Id']
        product3_id = sf.query(f"select id from product2 where name = 'Test Product 003'")['records'][0]['Id']
        product4_id = sf.query(f"select id from product2 where name like 'Test Product 004%'")['records'][0]['Id']
        product5_id = sf.query(f"select id from product2 where name = 'Test Product 005'")['records'][0]['Id']
        product6_id = sf.query(f"select id from product2 where name = 'Test Product 006'")['records'][0]['Id']
        product7_id = sf.query(f"select id from product2 where name = 'Test Product 007'")['records'][0]['Id']
        product8_id = sf.query(f"select id from product2 where name = 'Test Product 008'")['records'][0]['Id']


        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product1_id,
            'SCLP__ChildRequired__c': 'true',
            'SCLP__Tip__c': 'Tip test 1',
            'SCLP__HideInQuote__c': True
        })
        option1_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 001' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('Options 1 is created')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__ChildRequired__c': 'false',
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product2_id,
            'SCLP__MasterOption__c': option1_id,
            'SCLP__Tip__c': 'Tip test 2',
            'SCLP__HideInQuote__c': True
        })
        print('Options 2 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product3_id,
            'SCLP__Tip__c': 'Tip test 3'
        })
        print('Options 3 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': second_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product4_id,
            'SCLP__Tip__c': 'Tip test 4'
        })
        print('Options 4 is created')
        # sf.SCLP__ProductOption__c.create({
        #     'SCLP__BundleQuantity__c': '1',
        #     'SCLP__Bundle__c': created_bundle_id,
        #     'SCLP__Feature__c': second_feature_id,
        #     'SCLP__Order__c': '2',
        #     'SCLP__Product__c': product5_id,
        #     'SCLP__DefaultOption__c': 'true',
        #     'SCLP__Tip__c': 'Tip test 5'
        # })
        # print('Options 5 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product6_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__Tip__c': 'Tip test 6'
        })
        print('option 6 created')
        option6_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 006' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('query for 6 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product7_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__MasterOption__c': option6_id,
            'SCLP__Tip__c': 'Tip test 7',
            'SCLP__BundleQuantity__c': ''
        })
        print('option 7 created')
        print('query for 7 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product8_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Tip__c': 'Tip test 8'
        })
        print('option 8 created')
def create_bundle_ZZZ_001_1(sf): #7
    print('Start Bundle creation 7')
    bundle_query_result = sf.query(f"select name, id from product2 where name like 'ZZZ - 001 Test Bundle Created%' and Description = 'Test 1'")
    if len(bundle_query_result.get('records')) >= 1:
        print('Bundle already created')
    else:
        print('bundle to be created')
        Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
        rt_id = Rt_bundle_in_qurey['records'][0]['Id']
        print(f"Bundle Record Type id is {rt_id}")
        sf.product2.create({
            'Name': f'ZZZ - 001 Test Bundle Created {timestamp}',
            'RecordTypeId': rt_id,
            'IsActive': 'true',
            'Brand__c': 'FS-Curtis',
            'Description': "Test 1",
            'Sculptor_CPQ_Product__c': True,
            'ProductCode': 'Test Product Code'

        })
        created_bundle_id = sf.query(f"select name, id from product2 where name = 'ZZZ - 001 Test Bundle Created {timestamp}' and Description = 'Test 1'")['records'][0]['Id']
        print(f'New ID of bundle is {created_bundle_id}\n Now lets create Features')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Feature Number One',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'true',
            'SCLP__Order__c': '1',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            'SCLP__Tip__c': 'Feature Number One tip'
        })
        first_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 1 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'first feature id is {first_feature_id}')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Number two',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'true',
            'SCLP__Tip__c': 'Feature Number two tip'
        })

        second_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 2 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'second feature id is {second_feature_id}\n Now lets create options')
        product1_id = sf.query(f"select id from product2 where name = 'Test Product 001'")['records'][0]['Id']
        product2_id = sf.query(f"select id from product2 where name = 'Test Product 002'")['records'][0]['Id']
        product3_id = sf.query(f"select id from product2 where name = 'Test Product 003'")['records'][0]['Id']
        product4_id = sf.query(f"select id from product2 where name like 'Test Product 004%'")['records'][0]['Id']
        product5_id = sf.query(f"select id from product2 where name = 'Test Product 005'")['records'][0]['Id']
        product6_id = sf.query(f"select id from product2 where name = 'Test Product 006'")['records'][0]['Id']
        product7_id = sf.query(f"select id from product2 where name = 'Test Product 007'")['records'][0]['Id']
        product8_id = sf.query(f"select id from product2 where name = 'Test Product 008'")['records'][0]['Id']


        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product1_id,
            'SCLP__ChildRequired__c': 'true',
            'SCLP__Tip__c': 'Tip test 1',
            'SCLP__HideInQuote__c': True
        })
        option1_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 001' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('Options 1 is created')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__ChildRequired__c': 'false',
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product2_id,
            'SCLP__MasterOption__c': option1_id,
            'SCLP__Tip__c': 'Tip test 2',
            'SCLP__HideInQuote__c': True
        })
        print('Options 2 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product3_id,
            'SCLP__Tip__c': 'Tip test 3'
        })
        print('Options 3 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': second_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product4_id,
            'SCLP__Tip__c': 'Tip test 4'
        })
        print('Options 4 is created')
        # sf.SCLP__ProductOption__c.create({
        #     'SCLP__BundleQuantity__c': '1',
        #     'SCLP__Bundle__c': created_bundle_id,
        #     'SCLP__Feature__c': second_feature_id,
        #     'SCLP__Order__c': '2',
        #     'SCLP__Product__c': product5_id,
        #     'SCLP__DefaultOption__c': 'true',
        #     'SCLP__Tip__c': 'Tip test 5'
        # })
        # print('Options 5 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product6_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__Tip__c': 'Tip test 6'
        })
        print('option 6 created')
        option6_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 006' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('query for 6 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product7_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__MasterOption__c': option6_id,
            'SCLP__Tip__c': 'Tip test 7',
            'SCLP__BundleQuantity__c': ''
        })
        print('option 7 created')
        print('query for 7 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product8_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Tip__c': 'Tip test 8'
        })
        print('option 8 created')
def create_bundle_ZZZ_002_1(sf): #8
    print('Start Bundle creation 8')
    bundle_query_result = sf.query(f"select name, id from product2 where name like 'ZZZ - 002 Test Bundle Created%' and Description = 'Test 1'")
    if len(bundle_query_result.get('records')) >= 1:
        print('Bundle already created')
    else:
        print('bundle to be created')
        Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
        rt_id = Rt_bundle_in_qurey['records'][0]['Id']
        print(f"Bundle Record Type id is {rt_id}")
        sf.product2.create({
            'Name': f'ZZZ - 002 Test Bundle Created {timestamp}',
            'RecordTypeId': rt_id,
            'IsActive': 'true',
            'Brand__c': 'FS-Curtis',
            'Description': "Test 1",
            'Sculptor_CPQ_Product__c': True,
            'ProductCode': 'Test Product Code'

        })
        created_bundle_id = sf.query(f"select name, id from product2 where name = 'ZZZ - 002 Test Bundle Created {timestamp}' and Description = 'Test 1'")['records'][0]['Id']
        print(f'New ID of bundle is {created_bundle_id}\n Now lets create Features')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Feature Number One',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'true',
            'SCLP__Order__c': '1',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            'SCLP__Tip__c': 'Feature Number One tip'
        })
        first_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 1 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'first feature id is {first_feature_id}')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Number two',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'true',
            'SCLP__Tip__c': 'Feature Number two tip'
        })

        second_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 2 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'second feature id is {second_feature_id}\n Now lets create options')
        product1_id = sf.query(f"select id from product2 where name = 'Test Product 001'")['records'][0]['Id']
        product2_id = sf.query(f"select id from product2 where name = 'Test Product 002'")['records'][0]['Id']
        product3_id = sf.query(f"select id from product2 where name = 'Test Product 003'")['records'][0]['Id']
        product4_id = sf.query(f"select id from product2 where name like 'Test Product 004%'")['records'][0]['Id']
        product5_id = sf.query(f"select id from product2 where name = 'Test Product 005'")['records'][0]['Id']
        product6_id = sf.query(f"select id from product2 where name = 'Test Product 006'")['records'][0]['Id']
        product7_id = sf.query(f"select id from product2 where name = 'Test Product 007'")['records'][0]['Id']
        product8_id = sf.query(f"select id from product2 where name = 'Test Product 008'")['records'][0]['Id']


        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product1_id,
            'SCLP__ChildRequired__c': 'true',
            'SCLP__Tip__c': 'Tip test 1',
            'SCLP__HideInQuote__c': True
        })
        option1_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 001' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('Options 1 is created')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__ChildRequired__c': 'false',
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product2_id,
            'SCLP__MasterOption__c': option1_id,
            'SCLP__Tip__c': 'Tip test 2',
            'SCLP__HideInQuote__c': True
        })
        print('Options 2 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product3_id,
            'SCLP__Tip__c': 'Tip test 3'
        })
        print('Options 3 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': second_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product4_id,
            'SCLP__Tip__c': 'Tip test 4'
        })
        print('Options 4 is created')
        # sf.SCLP__ProductOption__c.create({
        #     'SCLP__BundleQuantity__c': '1',
        #     'SCLP__Bundle__c': created_bundle_id,
        #     'SCLP__Feature__c': second_feature_id,
        #     'SCLP__Order__c': '2',
        #     'SCLP__Product__c': product5_id,
        #     'SCLP__DefaultOption__c': 'true',
        #     'SCLP__Tip__c': 'Tip test 5'
        # })
        # print('Options 5 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product6_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__Tip__c': 'Tip test 6'
        })
        print('option 6 created')
        option6_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 006' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('query for 6 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product7_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__MasterOption__c': option6_id,
            'SCLP__Tip__c': 'Tip test 7',
            'SCLP__BundleQuantity__c': ''
        })
        print('option 7 created')
        print('query for 7 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product8_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Tip__c': 'Tip test 8'
        })
        print('option 8 created')
def create_bundle_ZZZ_003_1(sf): #9
    print('Start Bundle creation 9')
    bundle_query_result = sf.query(f"select name, id from product2 where name like 'ZZZ - 003 Test Bundle Created%' and Description = 'Test 1'")
    if len(bundle_query_result.get('records')) >= 1:
        print('Bundle already created')
    else:
        print('bundle to be created')
        Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
        rt_id = Rt_bundle_in_qurey['records'][0]['Id']
        print(f"Bundle Record Type id is {rt_id}")
        sf.product2.create({
            'Name': f'ZZZ - 003 Test Bundle Created {timestamp}',
            'RecordTypeId': rt_id,
            'IsActive': 'true',
            'Brand__c': 'FS-Curtis',
            'Description': "Test 1",
            'Sculptor_CPQ_Product__c': True,
            'ProductCode': 'Test Product Code'

        })
        created_bundle_id = sf.query(f"select name, id from product2 where name = 'ZZZ - 003 Test Bundle Created {timestamp}' and Description = 'Test 1'")['records'][0]['Id']
        print(f'New ID of bundle is {created_bundle_id}\n Now lets create Features')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Feature Number One',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'true',
            'SCLP__Order__c': '1',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            'SCLP__Tip__c': 'Feature Number One tip'
        })
        first_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 1 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'first feature id is {first_feature_id}')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Number two',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'true',
            'SCLP__Tip__c': 'Feature Number two tip'
        })

        second_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 2 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'second feature id is {second_feature_id}\n Now lets create options')
        product1_id = sf.query(f"select id from product2 where name = 'Test Product 001'")['records'][0]['Id']
        product2_id = sf.query(f"select id from product2 where name = 'Test Product 002'")['records'][0]['Id']
        product3_id = sf.query(f"select id from product2 where name = 'Test Product 003'")['records'][0]['Id']
        product4_id = sf.query(f"select id from product2 where name like 'Test Product 004%'")['records'][0]['Id']
        product5_id = sf.query(f"select id from product2 where name = 'Test Product 005'")['records'][0]['Id']
        product6_id = sf.query(f"select id from product2 where name = 'Test Product 006'")['records'][0]['Id']
        product7_id = sf.query(f"select id from product2 where name = 'Test Product 007'")['records'][0]['Id']
        product8_id = sf.query(f"select id from product2 where name = 'Test Product 008'")['records'][0]['Id']


        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product1_id,
            'SCLP__ChildRequired__c': 'true',
            'SCLP__Tip__c': 'Tip test 1',
            'SCLP__HideInQuote__c': True
        })
        option1_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 001' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('Options 1 is created')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__ChildRequired__c': 'false',
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product2_id,
            'SCLP__MasterOption__c': option1_id,
            'SCLP__Tip__c': 'Tip test 2',
            'SCLP__HideInQuote__c': True
        })
        print('Options 2 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product3_id,
            'SCLP__Tip__c': 'Tip test 3'
        })
        print('Options 3 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': second_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product4_id,
            'SCLP__Tip__c': 'Tip test 4'
        })
        print('Options 4 is created')
        # sf.SCLP__ProductOption__c.create({
        #     'SCLP__BundleQuantity__c': '1',
        #     'SCLP__Bundle__c': created_bundle_id,
        #     'SCLP__Feature__c': second_feature_id,
        #     'SCLP__Order__c': '2',
        #     'SCLP__Product__c': product5_id,
        #     'SCLP__DefaultOption__c': 'true',
        #     'SCLP__Tip__c': 'Tip test 5'
        # })
        # print('Options 5 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product6_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__Tip__c': 'Tip test 6'
        })
        print('option 6 created')
        option6_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 006' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('query for 6 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product7_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__MasterOption__c': option6_id,
            'SCLP__Tip__c': 'Tip test 7',
            'SCLP__BundleQuantity__c': ''
        })
        print('option 7 created')
        print('query for 7 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product8_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Tip__c': 'Tip test 8'
        })
        print('option 8 created')
def create_bundle_WWW_001_2(sf): #10
    print('Start Bundle creation 10')
    bundle_query_result = sf.query(f"select name, id from product2 where name like 'WWW - 001 Test Bundle Created%' and Description = 'Test 2'" )
    if len(bundle_query_result.get('records')) >= 1:
        print('Bundle already created')
    else:
        print('bundle to be created')
        Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
        rt_id = Rt_bundle_in_qurey['records'][0]['Id']
        print(f"Bundle Record Type id is {rt_id}")
        sf.product2.create({
            'Name': f'WWW - 001 Test Bundle Created {timestamp}',
            'RecordTypeId': rt_id,
            'IsActive': 'true',
            'Brand__c': 'FS-Curtis',
            'Description': "Test 2",
            'Sculptor_CPQ_Product__c': True,
            'ProductCode': 'Test Product Code'
        })
        created_bundle_id = sf.query(f"select name, id from product2 where name = 'WWW - 001 Test Bundle Created {timestamp}' and Description = 'Test 2'")['records'][0]['Id']
        print(f'New ID of bundle is {created_bundle_id}\n Now lets create Features')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Feature Number One',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'true',
            'SCLP__Order__c': '1',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            'SCLP__Tip__c': 'Feature Number One tip'
        })
        first_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 1 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'first feature id is {first_feature_id}')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Number two',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'true',
            'SCLP__Tip__c': 'Feature Number two tip'
        })

        second_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 2 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'second feature id is {second_feature_id}\n Now lets create options')
        product1_id = sf.query(f"select id from product2 where name = 'Test Product 001'")['records'][0]['Id']
        product2_id = sf.query(f"select id from product2 where name = 'Test Product 002'")['records'][0]['Id']
        product3_id = sf.query(f"select id from product2 where name = 'Test Product 003'")['records'][0]['Id']
        product4_id = sf.query(f"select id from product2 where name like 'Test Product 004%'")['records'][0]['Id']
        product5_id = sf.query(f"select id from product2 where name = 'Test Product 005'")['records'][0]['Id']
        product6_id = sf.query(f"select id from product2 where name = 'Test Product 006'")['records'][0]['Id']
        product7_id = sf.query(f"select id from product2 where name = 'Test Product 007'")['records'][0]['Id']
        product8_id = sf.query(f"select id from product2 where name = 'Test Product 008'")['records'][0]['Id']


        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product1_id,
            'SCLP__ChildRequired__c': 'true',
            'SCLP__Tip__c': 'Tip test 1',
            'SCLP__HideInQuote__c': True
        })
        option1_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 001' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('Options 1 is created')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__ChildRequired__c': 'false',
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product2_id,
            'SCLP__MasterOption__c': option1_id,
            'SCLP__Tip__c': 'Tip test 2',
            'SCLP__HideInQuote__c': True
        })
        print('Options 2 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product3_id,
            'SCLP__Tip__c': 'Tip test 3'
        })
        print('Options 3 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': second_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product4_id,
            'SCLP__Tip__c': 'Tip test 4'
        })
        print('Options 4 is created')
        # sf.SCLP__ProductOption__c.create({
        #     'SCLP__BundleQuantity__c': '1',
        #     'SCLP__Bundle__c': created_bundle_id,
        #     'SCLP__Feature__c': second_feature_id,
        #     'SCLP__Order__c': '2',
        #     'SCLP__Product__c': product5_id,
        #     'SCLP__DefaultOption__c': 'true',
        #     'SCLP__Tip__c': 'Tip test 5'
        # })
        # print('Options 5 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product6_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__Tip__c': 'Tip test 6'
        })
        print('option 6 created')
        option6_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 006' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('query for 6 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product7_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__MasterOption__c': option6_id,
            'SCLP__Tip__c': 'Tip test 7',
            'SCLP__BundleQuantity__c': ''
        })
        print('option 7 created')
        print('query for 7 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product8_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Tip__c': 'Tip test 8'
        })
        print('option 8 created')
def create_bundle_WWW_002_2(sf): #11
    print('Start Bundle creation 11')
    bundle_query_result = sf.query(f"select name, id from product2 where name like 'WWW - 002 Test Bundle Created%' and Description = 'Test 2'")
    if len(bundle_query_result.get('records')) >= 1:
        print('Bundle already created')
    else:
        print('bundle to be created')
        Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
        rt_id = Rt_bundle_in_qurey['records'][0]['Id']
        print(f"Bundle Record Type id is {rt_id}")
        sf.product2.create({
            'Name': f'WWW - 002 Test Bundle Created {timestamp}',
            'RecordTypeId': rt_id,
            'IsActive': 'true',
            'Brand__c': 'FS-Curtis',
            'Description': "Test 2",
            'Sculptor_CPQ_Product__c': True,
            'ProductCode': 'Test Product Code'

        })
        created_bundle_id = sf.query(f"select name, id from product2 where name = 'WWW - 002 Test Bundle Created {timestamp}' and Description = 'Test 2'")['records'][0]['Id']
        print(f'New ID of bundle is {created_bundle_id}\n Now lets create Features')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Feature Number One',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'true',
            'SCLP__Order__c': '1',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            'SCLP__Tip__c': 'Feature Number One tip'
        })
        first_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 1 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'first feature id is {first_feature_id}')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Number two',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'true',
            'SCLP__Tip__c': 'Feature Number two tip'
        })

        second_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 2 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'second feature id is {second_feature_id}\n Now lets create options')
        product1_id = sf.query(f"select id from product2 where name = 'Test Product 001'")['records'][0]['Id']
        product2_id = sf.query(f"select id from product2 where name = 'Test Product 002'")['records'][0]['Id']
        product3_id = sf.query(f"select id from product2 where name = 'Test Product 003'")['records'][0]['Id']
        product4_id = sf.query(f"select id from product2 where name like 'Test Product 004%'")['records'][0]['Id']
        product5_id = sf.query(f"select id from product2 where name = 'Test Product 005'")['records'][0]['Id']
        product6_id = sf.query(f"select id from product2 where name = 'Test Product 006'")['records'][0]['Id']
        product7_id = sf.query(f"select id from product2 where name = 'Test Product 007'")['records'][0]['Id']
        product8_id = sf.query(f"select id from product2 where name = 'Test Product 008'")['records'][0]['Id']


        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product1_id,
            'SCLP__ChildRequired__c': 'true',
            'SCLP__Tip__c': 'Tip test 1',
            'SCLP__HideInQuote__c': True
        })
        option1_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 001' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('Options 1 is created')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__ChildRequired__c': 'false',
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product2_id,
            'SCLP__MasterOption__c': option1_id,
            'SCLP__Tip__c': 'Tip test 2',
            'SCLP__HideInQuote__c': True
        })
        print('Options 2 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product3_id,
            'SCLP__Tip__c': 'Tip test 3'
        })
        print('Options 3 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': second_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product4_id,
            'SCLP__Tip__c': 'Tip test 4'
        })
        print('Options 4 is created')
        # sf.SCLP__ProductOption__c.create({
        #     'SCLP__BundleQuantity__c': '1',
        #     'SCLP__Bundle__c': created_bundle_id,
        #     'SCLP__Feature__c': second_feature_id,
        #     'SCLP__Order__c': '2',
        #     'SCLP__Product__c': product5_id,
        #     'SCLP__DefaultOption__c': 'true',
        #     'SCLP__Tip__c': 'Tip test 5'
        # })
        # print('Options 5 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product6_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__Tip__c': 'Tip test 6'
        })
        print('option 6 created')
        option6_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 006' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('query for 6 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product7_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__MasterOption__c': option6_id,
            'SCLP__Tip__c': 'Tip test 7',
            'SCLP__BundleQuantity__c': ''
        })
        print('option 7 created')
        print('query for 7 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product8_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Tip__c': 'Tip test 8'
        })
        print('option 8 created')
def create_bundle_WWW_003_2(sf): #12
    print('Start Bundle creation 12')
    bundle_query_result = sf.query(f"select name, id from product2 where name like 'WWW - 003 Test Bundle Created%' and Description = 'Test 2'")
    if len(bundle_query_result.get('records')) >= 1:
        print('Bundle already created')
    else:
        print('bundle to be created')
        Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
        rt_id = Rt_bundle_in_qurey['records'][0]['Id']
        print(f"Bundle Record Type id is {rt_id}")
        sf.product2.create({
            'Name': f'WWW - 003 Test Bundle Created {timestamp}',
            'RecordTypeId': rt_id,
            'IsActive': 'true',
            'Brand__c': 'FS-Curtis',
            'Description': "Test 2",
            'Sculptor_CPQ_Product__c': True,
            'ProductCode': 'Test Product Code'

        })
        created_bundle_id = sf.query(f"select name, id from product2 where name = 'WWW - 003 Test Bundle Created {timestamp}' and Description = 'Test 2'")['records'][0]['Id']
        print(f'New ID of bundle is {created_bundle_id}\n Now lets create Features')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Feature Number One',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'true',
            'SCLP__Order__c': '1',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            'SCLP__Tip__c': 'Feature Number One tip'
        })
        first_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 1 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'first feature id is {first_feature_id}')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Number two',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'true',
            'SCLP__Tip__c': 'Feature Number two tip'
        })

        second_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 2 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'second feature id is {second_feature_id}\n Now lets create options')
        product1_id = sf.query(f"select id from product2 where name = 'Test Product 001'")['records'][0]['Id']
        product2_id = sf.query(f"select id from product2 where name = 'Test Product 002'")['records'][0]['Id']
        product3_id = sf.query(f"select id from product2 where name = 'Test Product 003'")['records'][0]['Id']
        product4_id = sf.query(f"select id from product2 where name like 'Test Product 004%'")['records'][0]['Id']
        product5_id = sf.query(f"select id from product2 where name = 'Test Product 005'")['records'][0]['Id']
        product6_id = sf.query(f"select id from product2 where name = 'Test Product 006'")['records'][0]['Id']
        product7_id = sf.query(f"select id from product2 where name = 'Test Product 007'")['records'][0]['Id']
        product8_id = sf.query(f"select id from product2 where name = 'Test Product 008'")['records'][0]['Id']


        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product1_id,
            'SCLP__ChildRequired__c': 'true',
            'SCLP__Tip__c': 'Tip test 1',
            'SCLP__HideInQuote__c': True
        })
        option1_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 001' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('Options 1 is created')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__ChildRequired__c': 'false',
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product2_id,
            'SCLP__MasterOption__c': option1_id,
            'SCLP__Tip__c': 'Tip test 2',
            'SCLP__HideInQuote__c': True
        })
        print('Options 2 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product3_id,
            'SCLP__Tip__c': 'Tip test 3'
        })
        print('Options 3 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': second_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product4_id,
            'SCLP__Tip__c': 'Tip test 4'
        })
        print('Options 4 is created')
        # sf.SCLP__ProductOption__c.create({
        #     'SCLP__BundleQuantity__c': '1',
        #     'SCLP__Bundle__c': created_bundle_id,
        #     'SCLP__Feature__c': second_feature_id,
        #     'SCLP__Order__c': '2',
        #     'SCLP__Product__c': product5_id,
        #     'SCLP__DefaultOption__c': 'true',
        #     'SCLP__Tip__c': 'Tip test 5'
        # })
        # print('Options 5 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product6_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__Tip__c': 'Tip test 6'
        })
        print('option 6 created')
        option6_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 006' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('query for 6 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product7_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__MasterOption__c': option6_id,
            'SCLP__Tip__c': 'Tip test 7',
            'SCLP__BundleQuantity__c': ''
        })
        print('option 7 created')
        print('query for 7 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product8_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Tip__c': 'Tip test 8'
        })
        print('option 8 created')
def create_bundle_ZZZ_001_2(sf): #13
    print('Start Bundle creation 13')
    bundle_query_result = sf.query(f"select name, id from product2 where name like 'ZZZ - 001 Test Bundle Created%' and Description = 'Test 2'")
    if len(bundle_query_result.get('records')) >= 1:
        print('Bundle already created')
    else:
        print('bundle to be created')
        Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
        rt_id = Rt_bundle_in_qurey['records'][0]['Id']
        print(f"Bundle Record Type id is {rt_id}")
        sf.product2.create({
            'Name': f'ZZZ - 001 Test Bundle Created {timestamp}',
            'RecordTypeId': rt_id,
            'IsActive': 'true',
            'Brand__c': 'FS-Curtis',
            'Description': "Test 2",
            'Sculptor_CPQ_Product__c': True,
            'ProductCode': 'Test Product Code'

        })
        created_bundle_id = sf.query(f"select name, id from product2 where name = 'ZZZ - 001 Test Bundle Created {timestamp}' and Description = 'Test 2'")['records'][0]['Id']
        print(f'New ID of bundle is {created_bundle_id}\n Now lets create Features')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Feature Number One',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'true',
            'SCLP__Order__c': '1',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            'SCLP__Tip__c': 'Feature Number One tip'
        })
        first_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 1 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'first feature id is {first_feature_id}')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Number two',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'true',
            'SCLP__Tip__c': 'Feature Number two tip'
        })

        second_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 2 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'second feature id is {second_feature_id}\n Now lets create options')
        product1_id = sf.query(f"select id from product2 where name = 'Test Product 001'")['records'][0]['Id']
        product2_id = sf.query(f"select id from product2 where name = 'Test Product 002'")['records'][0]['Id']
        product3_id = sf.query(f"select id from product2 where name = 'Test Product 003'")['records'][0]['Id']
        product4_id = sf.query(f"select id from product2 where name like 'Test Product 004%'")['records'][0]['Id']
        product5_id = sf.query(f"select id from product2 where name = 'Test Product 005'")['records'][0]['Id']
        product6_id = sf.query(f"select id from product2 where name = 'Test Product 006'")['records'][0]['Id']
        product7_id = sf.query(f"select id from product2 where name = 'Test Product 007'")['records'][0]['Id']
        product8_id = sf.query(f"select id from product2 where name = 'Test Product 008'")['records'][0]['Id']


        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product1_id,
            'SCLP__ChildRequired__c': 'true',
            'SCLP__Tip__c': 'Tip test 1',
            'SCLP__HideInQuote__c': True
        })
        option1_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 001' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('Options 1 is created')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__ChildRequired__c': 'false',
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product2_id,
            'SCLP__MasterOption__c': option1_id,
            'SCLP__Tip__c': 'Tip test 2',
            'SCLP__HideInQuote__c': True
        })
        print('Options 2 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product3_id,
            'SCLP__Tip__c': 'Tip test 3'
        })
        print('Options 3 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': second_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product4_id,
            'SCLP__Tip__c': 'Tip test 4'
        })
        print('Options 4 is created')
        # sf.SCLP__ProductOption__c.create({
        #     'SCLP__BundleQuantity__c': '1',
        #     'SCLP__Bundle__c': created_bundle_id,
        #     'SCLP__Feature__c': second_feature_id,
        #     'SCLP__Order__c': '2',
        #     'SCLP__Product__c': product5_id,
        #     'SCLP__DefaultOption__c': 'true',
        #     'SCLP__Tip__c': 'Tip test 5'
        # })
        # print('Options 5 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product6_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__Tip__c': 'Tip test 6'
        })
        print('option 6 created')
        option6_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 006' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('query for 6 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product7_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__MasterOption__c': option6_id,
            'SCLP__Tip__c': 'Tip test 7',
            'SCLP__BundleQuantity__c': ''
        })
        print('option 7 created')
        print('query for 7 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product8_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Tip__c': 'Tip test 8'
        })
        print('option 8 created')
def create_bundle_ZZZ_002_2(sf): #14
    print('Start Bundle creation 14')
    bundle_query_result = sf.query(f"select name, id from product2 where name like 'ZZZ - 002 Test Bundle Created%' and Description = 'Test 2'")
    if len(bundle_query_result.get('records')) >= 1:
        print('Bundle already created')
    else:
        print('bundle to be created')
        Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
        rt_id = Rt_bundle_in_qurey['records'][0]['Id']
        print(f"Bundle Record Type id is {rt_id}")
        sf.product2.create({
            'Name': f'ZZZ - 002 Test Bundle Created {timestamp}',
            'RecordTypeId': rt_id,
            'IsActive': 'true',
            'Brand__c': 'FS-Curtis',
            'Description': "Test 2",
            'Sculptor_CPQ_Product__c': True,
            'ProductCode': 'Test Product Code'

        })
        created_bundle_id = sf.query(f"select name, id from product2 where name = 'ZZZ - 002 Test Bundle Created {timestamp}' and Description = 'Test 2'")['records'][0]['Id']
        print(f'New ID of bundle is {created_bundle_id}\n Now lets create Features')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Feature Number One',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'true',
            'SCLP__Order__c': '1',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            'SCLP__Tip__c': 'Feature Number One tip'
        })
        first_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 1 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'first feature id is {first_feature_id}')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Number two',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'true',
            'SCLP__Tip__c': 'Feature Number two tip'
        })

        second_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 2 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'second feature id is {second_feature_id}\n Now lets create options')
        product1_id = sf.query(f"select id from product2 where name = 'Test Product 001'")['records'][0]['Id']
        product2_id = sf.query(f"select id from product2 where name = 'Test Product 002'")['records'][0]['Id']
        product3_id = sf.query(f"select id from product2 where name = 'Test Product 003'")['records'][0]['Id']
        product4_id = sf.query(f"select id from product2 where name like 'Test Product 004%'")['records'][0]['Id']
        product5_id = sf.query(f"select id from product2 where name = 'Test Product 005'")['records'][0]['Id']
        product6_id = sf.query(f"select id from product2 where name = 'Test Product 006'")['records'][0]['Id']
        product7_id = sf.query(f"select id from product2 where name = 'Test Product 007'")['records'][0]['Id']
        product8_id = sf.query(f"select id from product2 where name = 'Test Product 008'")['records'][0]['Id']


        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product1_id,
            'SCLP__ChildRequired__c': 'true',
            'SCLP__Tip__c': 'Tip test 1',
            'SCLP__HideInQuote__c': True
        })
        option1_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 001' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('Options 1 is created')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__ChildRequired__c': 'false',
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product2_id,
            'SCLP__MasterOption__c': option1_id,
            'SCLP__Tip__c': 'Tip test 2',
            'SCLP__HideInQuote__c': True
        })
        print('Options 2 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product3_id,
            'SCLP__Tip__c': 'Tip test 3'
        })
        print('Options 3 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': second_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product4_id,
            'SCLP__Tip__c': 'Tip test 4'
        })
        print('Options 4 is created')
        # sf.SCLP__ProductOption__c.create({
        #     'SCLP__BundleQuantity__c': '1',
        #     'SCLP__Bundle__c': created_bundle_id,
        #     'SCLP__Feature__c': second_feature_id,
        #     'SCLP__Order__c': '2',
        #     'SCLP__Product__c': product5_id,
        #     'SCLP__DefaultOption__c': 'true',
        #     'SCLP__Tip__c': 'Tip test 5'
        # })
        # print('Options 5 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product6_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__Tip__c': 'Tip test 6'
        })
        print('option 6 created')
        option6_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 006' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('query for 6 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product7_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__MasterOption__c': option6_id,
            'SCLP__Tip__c': 'Tip test 7',
            'SCLP__BundleQuantity__c': ''
        })
        print('option 7 created')
        print('query for 7 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product8_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Tip__c': 'Tip test 8'
        })
        print('option 8 created')
def create_bundle_ZZZ_003_2(sf): #15
    print('Start Bundle creation 15')
    bundle_query_result = sf.query(f"select name, id from product2 where name like 'ZZZ - 003 Test Bundle Created%' and Description = 'Test 2'")
    if len(bundle_query_result.get('records')) >= 1:
        print('Bundle already created')
    else:
        print('bundle to be created')
        Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
        rt_id = Rt_bundle_in_qurey['records'][0]['Id']
        print(f"Bundle Record Type id is {rt_id}")
        sf.product2.create({
            'Name': f'ZZZ - 003 Test Bundle Created {timestamp}',
            'RecordTypeId': rt_id,
            'IsActive': 'true',
            'Brand__c': 'FS-Curtis',
            'Description': "Test 2",
            'Sculptor_CPQ_Product__c': True,
            'ProductCode': 'Test Product Code'

        })
        created_bundle_id = sf.query(f"select name, id from product2 where name = 'ZZZ - 003 Test Bundle Created {timestamp}' and Description = 'Test 2'")['records'][0]['Id']
        print(f'New ID of bundle is {created_bundle_id}\n Now lets create Features')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Feature Number One',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'true',
            'SCLP__Order__c': '1',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            'SCLP__Tip__c': 'Feature Number One tip'
        })
        first_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 1 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'first feature id is {first_feature_id}')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Number two',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'true',
            'SCLP__Tip__c': 'Feature Number two tip'
        })

        second_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 2 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'second feature id is {second_feature_id}\n Now lets create options')
        product1_id = sf.query(f"select id from product2 where name = 'Test Product 001'")['records'][0]['Id']
        product2_id = sf.query(f"select id from product2 where name = 'Test Product 002'")['records'][0]['Id']
        product3_id = sf.query(f"select id from product2 where name = 'Test Product 003'")['records'][0]['Id']
        product4_id = sf.query(f"select id from product2 where name like 'Test Product 004%'")['records'][0]['Id']
        product5_id = sf.query(f"select id from product2 where name = 'Test Product 005'")['records'][0]['Id']
        product6_id = sf.query(f"select id from product2 where name = 'Test Product 006'")['records'][0]['Id']
        product7_id = sf.query(f"select id from product2 where name = 'Test Product 007'")['records'][0]['Id']
        product8_id = sf.query(f"select id from product2 where name = 'Test Product 008'")['records'][0]['Id']


        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product1_id,
            'SCLP__ChildRequired__c': 'true',
            'SCLP__Tip__c': 'Tip test 1',
            'SCLP__HideInQuote__c': True
        })
        option1_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 001' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('Options 1 is created')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__ChildRequired__c': 'false',
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product2_id,
            'SCLP__MasterOption__c': option1_id,
            'SCLP__Tip__c': 'Tip test 2',
            'SCLP__HideInQuote__c': True
        })
        print('Options 2 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product3_id,
            'SCLP__Tip__c': 'Tip test 3'
        })
        print('Options 3 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': second_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product4_id,
            'SCLP__Tip__c': 'Tip test 4'
        })
        print('Options 4 is created')
        # sf.SCLP__ProductOption__c.create({
        #     'SCLP__BundleQuantity__c': '1',
        #     'SCLP__Bundle__c': created_bundle_id,
        #     'SCLP__Feature__c': second_feature_id,
        #     'SCLP__Order__c': '2',
        #     'SCLP__Product__c': product5_id,
        #     'SCLP__DefaultOption__c': 'true',
        #     'SCLP__Tip__c': 'Tip test 5'
        # })
        # print('Options 5 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product6_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__Tip__c': 'Tip test 6'
        })
        print('option 6 created')
        option6_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 006' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('query for 6 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product7_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__MasterOption__c': option6_id,
            'SCLP__Tip__c': 'Tip test 7',
            'SCLP__BundleQuantity__c': ''
        })
        print('option 7 created')
        print('query for 7 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product8_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Tip__c': 'Tip test 8'
        })
        print('option 8 created')
def create_bundle_YYY_001_2(sf): #16
    print('Start Bundle creation 16')
    bundle_query_result = sf.query(f"select name, id from product2 where name like 'YYY - 001 Test Bundle Created%' and Description = 'Test 2'")
    if len(bundle_query_result.get('records')) >= 1:
        print('Bundle already created')
    else:
        print('bundle to be created')
        Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
        rt_id = Rt_bundle_in_qurey['records'][0]['Id']
        print(f"Bundle Record Type id is {rt_id}")
        sf.product2.create({
            'Name': f'YYY - 001 Test Bundle Created {timestamp}',
            'RecordTypeId': rt_id,
            'IsActive': 'true',
            'Brand__c': 'FS-Curtis',
            'Description': "Test 2",
            'Sculptor_CPQ_Product__c': True,
            'ProductCode': 'Test Product Code'

        })
        created_bundle_id = sf.query(f"select name, id from product2 where name = 'YYY - 001 Test Bundle Created {timestamp}' and Description = 'Test 2'")['records'][0]['Id']
        print(f'New ID of bundle is {created_bundle_id}\n Now lets create Features')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Feature Number One',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'true',
            'SCLP__Order__c': '1',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            'SCLP__Tip__c': 'Feature Number One tip'
        })
        first_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 1 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'first feature id is {first_feature_id}')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Number two',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'true',
            'SCLP__Tip__c': 'Feature Number two tip'
        })

        second_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 2 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'second feature id is {second_feature_id}\n Now lets create options')
        product1_id = sf.query(f"select id from product2 where name = 'Test Product 001'")['records'][0]['Id']
        product2_id = sf.query(f"select id from product2 where name = 'Test Product 002'")['records'][0]['Id']
        product3_id = sf.query(f"select id from product2 where name = 'Test Product 003'")['records'][0]['Id']
        product4_id = sf.query(f"select id from product2 where name like 'Test Product 004%'")['records'][0]['Id']
        product5_id = sf.query(f"select id from product2 where name = 'Test Product 005'")['records'][0]['Id']
        product6_id = sf.query(f"select id from product2 where name = 'Test Product 006'")['records'][0]['Id']
        product7_id = sf.query(f"select id from product2 where name = 'Test Product 007'")['records'][0]['Id']
        product8_id = sf.query(f"select id from product2 where name = 'Test Product 008'")['records'][0]['Id']


        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product1_id,
            'SCLP__ChildRequired__c': 'true',
            'SCLP__Tip__c': 'Tip test 1',
            'SCLP__HideInQuote__c': True
        })
        option1_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 001' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('Options 1 is created')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__ChildRequired__c': 'false',
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product2_id,
            'SCLP__MasterOption__c': option1_id,
            'SCLP__Tip__c': 'Tip test 2',
            'SCLP__HideInQuote__c': True
        })
        print('Options 2 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product3_id,
            'SCLP__Tip__c': 'Tip test 3'
        })
        print('Options 3 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': second_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product4_id,
            'SCLP__Tip__c': 'Tip test 4'
        })
        print('Options 4 is created')
        # sf.SCLP__ProductOption__c.create({
        #     'SCLP__BundleQuantity__c': '1',
        #     'SCLP__Bundle__c': created_bundle_id,
        #     'SCLP__Feature__c': second_feature_id,
        #     'SCLP__Order__c': '2',
        #     'SCLP__Product__c': product5_id,
        #     'SCLP__DefaultOption__c': 'true',
        #     'SCLP__Tip__c': 'Tip test 5'
        # })
        # print('Options 5 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product6_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__Tip__c': 'Tip test 6'
        })
        print('option 6 created')
        option6_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 006' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('query for 6 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product7_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__MasterOption__c': option6_id,
            'SCLP__Tip__c': 'Tip test 7',
            'SCLP__BundleQuantity__c': ''
        })
        print('option 7 created')
        print('query for 7 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product8_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Tip__c': 'Tip test 8'
        })
        print('option 8 created')
def create_bundle_YYY_002_2(sf): #17
    print('Start Bundle creation 17')
    bundle_query_result = sf.query(f"select name, id from product2 where name like 'YYY - 002 Test Bundle Created%' and Description = 'Test 2'")
    if len(bundle_query_result.get('records')) >= 1:
        print('Bundle already created')
    else:
        print('bundle to be created')
        Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
        rt_id = Rt_bundle_in_qurey['records'][0]['Id']
        print(f"Bundle Record Type id is {rt_id}")
        sf.product2.create({
            'Name': f'YYY - 002 Test Bundle Created {timestamp}',
            'RecordTypeId': rt_id,
            'IsActive': 'true',
            'Brand__c': 'FS-Curtis',
            'Description': "Test 2",
            'Sculptor_CPQ_Product__c': True,
            'ProductCode': 'Test Product Code'

        })
        created_bundle_id = sf.query(f"select name, id from product2 where name = 'YYY - 002 Test Bundle Created {timestamp}' and Description = 'Test 2'")['records'][0]['Id']
        print(f'New ID of bundle is {created_bundle_id}\n Now lets create Features')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Feature Number One',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'true',
            'SCLP__Order__c': '1',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            'SCLP__Tip__c': 'Feature Number One tip'
        })
        first_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 1 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'first feature id is {first_feature_id}')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Number two',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'true',
            'SCLP__Tip__c': 'Feature Number two tip'
        })

        second_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 2 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'second feature id is {second_feature_id}\n Now lets create options')
        product1_id = sf.query(f"select id from product2 where name = 'Test Product 001'")['records'][0]['Id']
        product2_id = sf.query(f"select id from product2 where name = 'Test Product 002'")['records'][0]['Id']
        product3_id = sf.query(f"select id from product2 where name = 'Test Product 003'")['records'][0]['Id']
        product4_id = sf.query(f"select id from product2 where name like 'Test Product 004%'")['records'][0]['Id']
        product5_id = sf.query(f"select id from product2 where name = 'Test Product 005'")['records'][0]['Id']
        product6_id = sf.query(f"select id from product2 where name = 'Test Product 006'")['records'][0]['Id']
        product7_id = sf.query(f"select id from product2 where name = 'Test Product 007'")['records'][0]['Id']
        product8_id = sf.query(f"select id from product2 where name = 'Test Product 008'")['records'][0]['Id']


        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product1_id,
            'SCLP__ChildRequired__c': 'true',
            'SCLP__Tip__c': 'Tip test 1',
            'SCLP__HideInQuote__c': True
        })
        option1_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 001' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('Options 1 is created')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__ChildRequired__c': 'false',
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product2_id,
            'SCLP__MasterOption__c': option1_id,
            'SCLP__Tip__c': 'Tip test 2',
            'SCLP__HideInQuote__c': True
        })
        print('Options 2 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product3_id,
            'SCLP__Tip__c': 'Tip test 3'
        })
        print('Options 3 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': second_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product4_id,
            'SCLP__Tip__c': 'Tip test 4'
        })
        print('Options 4 is created')
        # sf.SCLP__ProductOption__c.create({
        #     'SCLP__BundleQuantity__c': '1',
        #     'SCLP__Bundle__c': created_bundle_id,
        #     'SCLP__Feature__c': second_feature_id,
        #     'SCLP__Order__c': '2',
        #     'SCLP__Product__c': product5_id,
        #     'SCLP__DefaultOption__c': 'true',
        #     'SCLP__Tip__c': 'Tip test 5'
        # })
        # print('Options 5 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product6_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__Tip__c': 'Tip test 6'
        })
        print('option 6 created')
        option6_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 006' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('query for 6 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product7_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__MasterOption__c': option6_id,
            'SCLP__Tip__c': 'Tip test 7',
            'SCLP__BundleQuantity__c': ''
        })
        print('option 7 created')
        print('query for 7 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product8_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Tip__c': 'Tip test 8'
        })
        print('option 8 created')
def create_bundle_YYY_003_2(sf): #18
    print('Start Bundle creation 18')
    bundle_query_result = sf.query(f"select name, id from product2 where name like 'YYY - 003 Test Bundle Created%' and Description = 'Test 2'")
    if len(bundle_query_result.get('records')) >= 1:
        print('Bundle already created')
    else:
        print('bundle to be created')
        Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
        rt_id = Rt_bundle_in_qurey['records'][0]['Id']
        print(f"Bundle Record Type id is {rt_id}")
        sf.product2.create({
            'Name': f'YYY - 003 Test Bundle Created {timestamp}',
            'RecordTypeId': rt_id,
            'IsActive': 'true',
            'Brand__c': 'FS-Curtis',
            'Description': "Test 2",
            'Sculptor_CPQ_Product__c': True,
            'ProductCode': 'Test Product Code'

        })
        created_bundle_id = sf.query(f"select name, id from product2 where name = 'YYY - 003 Test Bundle Created {timestamp}' and Description = 'Test 2'")['records'][0]['Id']
        print(f'New ID of bundle is {created_bundle_id}\n Now lets create Features')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Feature Number One',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'true',
            'SCLP__Order__c': '1',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            'SCLP__Tip__c': 'Feature Number One tip'
        })
        first_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 1 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'first feature id is {first_feature_id}')
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Number two',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'true',
            'SCLP__Tip__c': 'Feature Number two tip'
        })

        second_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 2 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'second feature id is {second_feature_id}\n Now lets create options')
        product1_id = sf.query(f"select id from product2 where name = 'Test Product 001'")['records'][0]['Id']
        product2_id = sf.query(f"select id from product2 where name = 'Test Product 002'")['records'][0]['Id']
        product3_id = sf.query(f"select id from product2 where name = 'Test Product 003'")['records'][0]['Id']
        product4_id = sf.query(f"select id from product2 where name like 'Test Product 004%'")['records'][0]['Id']
        product5_id = sf.query(f"select id from product2 where name = 'Test Product 005'")['records'][0]['Id']
        product6_id = sf.query(f"select id from product2 where name = 'Test Product 006'")['records'][0]['Id']
        product7_id = sf.query(f"select id from product2 where name = 'Test Product 007'")['records'][0]['Id']
        product8_id = sf.query(f"select id from product2 where name = 'Test Product 008'")['records'][0]['Id']


        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product1_id,
            'SCLP__ChildRequired__c': 'true',
            'SCLP__Tip__c': 'Tip test 1',
            'SCLP__HideInQuote__c': True
        })
        option1_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 001' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('Options 1 is created')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__ChildRequired__c': 'false',
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product2_id,
            'SCLP__MasterOption__c': option1_id,
            'SCLP__Tip__c': 'Tip test 2',
            'SCLP__HideInQuote__c': True
        })
        print('Options 2 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product3_id,
            'SCLP__Tip__c': 'Tip test 3'
        })
        print('Options 3 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': second_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product4_id,
            'SCLP__Tip__c': 'Tip test 4'
        })
        print('Options 4 is created')
        # sf.SCLP__ProductOption__c.create({
        #     'SCLP__BundleQuantity__c': '1',
        #     'SCLP__Bundle__c': created_bundle_id,
        #     'SCLP__Feature__c': second_feature_id,
        #     'SCLP__Order__c': '2',
        #     'SCLP__Product__c': product5_id,
        #     'SCLP__DefaultOption__c': 'true',
        #     'SCLP__Tip__c': 'Tip test 5'
        # })
        # print('Options 5 is created')

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product6_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__Tip__c': 'Tip test 6'
        })
        print('option 6 created')
        option6_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 006' and SCLP__Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
        print('query for 6 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product7_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__MasterOption__c': option6_id,
            'SCLP__Tip__c': 'Tip test 7',
            'SCLP__BundleQuantity__c': ''
        })
        print('option 7 created')
        print('query for 7 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product8_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Tip__c': 'Tip test 8'
        })
        print('option 8 created')

def create_products_and_pricebook_entries(sf):
    for i in range(1, RECORDS_QTY): 
        product_name = f"Test Product {i:03d}"
        existing_product  = sf.query(f"SELECT Id FROM Product2 WHERE Name = '{product_name}'")
        

        if existing_product.get('records'):
            print(f"Product '{product_name}' already exists. Skip creation.")
            continue
        
        if i != 4:
            product = sf.Product2.create({
                'Name': f'{product_name}',
                'IsActive': True,
                'Description': f'This is a test description for Product {i:03d}',
                'ProductCode': f'SO-{i:03d}',
                'Brand__c': 'FS-Curtis'
            })
        else:
            try:
                product = sf.Product2.create({
                    'Name': f'{product_name} test test test test test test test test test test test test test',
                    'IsActive': True,
                    'SCLPCE__ManualCostForCommunity__c': True,
                    'Brand__c': 'FS-Curtis'

                })
            except IndexError:
                print("No SCLP__.")
                product = sf.Product2.create({
                    'Name': product_name,
                    'IsActive': True,
                    'ManualCostForCommunity__c': True,
                    # 'Description': f'This is a test description for Product {i:03d}',
                    # 'ProductCode': f'SO-{i:03d}'
                    })
            except SalesforceError as e:
                "INVALID_TYPE" in str(e)
                print('No such field as ManualCostForCommunity__c')
                product = sf.Product2.create({
                    'Name': f'{product_name} test test test test test test test test test test test test test',
                    'IsActive': True,
                    # 'Description': f'This is a test description for Product {i:03d}',
                    # 'ProductCode': f'SO-{i:03d}',
                })

        # Get standard PB id
        pricebook_id = None
        pricebook_entries = sf.query("SELECT Id, Name FROM Pricebook2 WHERE IsStandard = TRUE")
        pricebook_sculptor_entries = sf.query("SELECT Id, Name FROM Pricebook2 WHERE Name = 'FS-Curtis Sculptor'")

        for entry in pricebook_entries['records']:
            if entry['Name'] == 'Standard Price Book':
                pricebook_id = entry['Id']
                break
        for sculptor_entry in pricebook_sculptor_entries['records']:
            if sculptor_entry['Name'] == 'FS-Curtis Sculptor':
                pricebook_sculptor_id = sculptor_entry['Id']
                break
        


        # set price for the current product (1, 2, 3, 4, 5)
        price = i * 100

        # check if there is a record of the for the product and PB
        existing_entry = sf.query(f"SELECT Id FROM PricebookEntry WHERE Pricebook2Id = '{pricebook_id}' AND Product2Id = '{product['id']}'")
        if existing_entry['totalSize'] == 0:
            # If there is no record we create one
            sf.PricebookEntry.create({
                'Pricebook2Id': pricebook_id,
                'Product2Id': product['id'],
                'UnitPrice': price,
                'IsActive': True
            })
            print(f"PricebookEntry created for {product_name} with price {price}")
        else:
            print(f"PricebookEntry for {product_name} already exists.")
        existing_entry = sf.query(f"SELECT Id FROM PricebookEntry WHERE Pricebook2Id = '{pricebook_sculptor_id}' AND Product2Id = '{product['id']}'")
        if existing_entry['totalSize'] == 0:
            # If there is no record we create one
            sf.PricebookEntry.create({
                'Pricebook2Id': pricebook_sculptor_id,
                'Product2Id': product['id'],
                'UnitPrice': price,
                'IsActive': True
            })
            print(f"PricebookEntry created for {product_name} with price {price}")
        else:
            print(f"PricebookEntry for {product_name} already exists.")

    print("Products and Pricebook Entries created successfully!")
# create_products_and_pricebook_entries(sf)
def delete_test_product_salesforce(sf):
    print("Start Product Deleting...")
    for i in range(1, RECORDS_QTY):
        query = f"SELECT Name, Id FROM Product2 WHERE Name like 'Test Product {i:03d}%'"
        results = sf.query(query) 
        while results.get('records'):
            for record in results['records']:
                product_id = record['Id']
                product_name = record['Name']

                try:
                    sf.Product2.delete(product_id) 
                    print(f"product Deleted '{product_name}' with ID {product_id}")
                except Exception as e:
                    print(f"Error deleting '{product_name}': {e}")

            if results.get('nextRecordsUrl'):
                results = sf.query_more(results['nextRecordsUrl'], True)
            else:
                break

    print("All product are deleted.")
# delete_test_product_salesforce(sf)
def delete_bundle(sf):
    print('Start Bundle deletion')

    try:
        options = sf.query("SELECT Id, SCLP__Product__r.Name, SCLP__Bundle__r.Name FROM SCLP__ProductOption__c WHERE SCLP__Bundle__r.name LIKE '%Test Bundle Created%' ORDER BY SCLP__Product__r.name DESC")
        
        for o in options['records']:
            try:
                sf.SCLP__ProductOption__c.delete(o['Id'])
                product_name = o['SCLP__Product__r']['Name']
                print(f"Deleted option for product: {product_name} (ID: {o['Id']})")
            except Exception as e:
                product_name = o['SCLP__Product__r']['Name']
                print(f"Failed to delete option for product {product_name} (ID: {o['Id']}): {e}")

        bundles = sf.query(f"select name, id from product2 where name LIKE '%Test Bundle Created%'")
        if bundles['records']:
            for b in bundles['records']:
                try:
                    sf.Product2.delete(b['Id'])
                    print(f"Deleted bundle: {b['Name']} ({b['Id']})")
                except Exception as e:
                    print(f"Error deleting bundle: {e}")
        else:
            print("No bundles to delete")
    except SalesforceError as e:
        "INVALID_TYPE" in str(e)
        print("no SCLP__")
        options = sf.query("SELECT Id, Product__r.Name, Bundle__r.Name FROM ProductOption__c WHERE Bundle__r.name LIKE '%Test Bundle Created%' ORDER BY Product__r.name DESC")
        
        for o in options['records']:
            try:
                sf.ProductOption__c.delete(o['Id'])
                product_name = o['Product__r']['Name']
                print(f"Deleted option for product: {product_name} (ID: {o['Id']})")
            except Exception as e:
                product_name = o['Product__r']['Name']
                print(f"Failed to delete option for product {product_name} (ID: {o['Id']}): {e}")

        bundles = sf.query(f"select name, id from product2 where name LIKE '%Test Bundle Created%'")
        if bundles['records']:
            for b in bundles['records']:
                try:
                    sf.Product2.delete(b['Id'])
                    print(f"Deleted bundle: {b['Name']} ({b['Id']})")
                except Exception as e:
                    print(f"Error deleting bundle: {e}")
        else:
            print("No bundles to delete")
# delete_bundle(sf)

# create_bundle_WWW_001_1(sf)
# create_bundle_WWW_002_1(sf)
# create_bundle_WWW_003_1(sf)
# create_bundle_YYY_001_1(sf)
# create_bundle_YYY_002_1(sf)
# create_bundle_YYY_003_1(sf)
# create_bundle_ZZZ_001_1(sf)
# create_bundle_ZZZ_002_1(sf)
# create_bundle_ZZZ_003_1(sf)
# create_bundle_WWW_001_2(sf)
# create_bundle_WWW_002_2(sf)
# create_bundle_WWW_003_2(sf)
# create_bundle_ZZZ_001_2(sf)
# create_bundle_ZZZ_002_2(sf)
# create_bundle_ZZZ_003_2(sf)
# create_bundle_YYY_001_2(sf)
# create_bundle_YYY_002_2(sf)
# create_bundle_YYY_003_2(sf)