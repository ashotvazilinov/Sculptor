from simple_salesforce import Salesforce, SalesforceLogin, SalesforceError, SalesforceMalformedRequest
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import random

USERNAME='sculptortso@twistellar.trail'
PASSWORD='WorkhardTSO2k26!'
SECURITE_TOKEN='UTwEmaQqXfdSL1bvJ9gvsvr4'
DOMAIN='login' 
SITE_URL = f'https://{DOMAIN}.salesforce.com/'
session_id, instance = SalesforceLogin(

    username=USERNAME, 
    password=PASSWORD,
    security_token=SECURITE_TOKEN,
    domain=DOMAIN 
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
def create_products():
    pricebook_id = sf.query("SELECT Id FROM Pricebook2 WHERE name = 'Standard Price Book'")['records'][0]['Id']
    if not pricebook_id:
        print("Standard Price Book not found!")
        raise
    print('Starting Standard Price Book activation')
    query = "select name, id from Pricebook2 where name = 'Standard Price book' and isactive = false"
    
    results = sf.query(query)

    if results.get('records'):

        for record in results['records']:
            product_id = record['Id']
            product_name = record['Name']
            print(f"Found Price Book: {product_name} (ID: {product_id})")

            sf.Pricebook2.update(product_id, {'IsActive': True})
            print(f"{product_name} is now active!")

    else:
        print("No inactive Standard Price Book found.")

    products = ['Green Ear Cushions for T-Earbuds 21;200;'';TECG21',
        'Designer Box for T-Phone 21;150;'';TDBTP21',
        'T-Phone 21 128 GB;1500;Latest generation of smartphones, offering OLED displays, 5G connectivity, the T14 chip for better performance, improved cameras.;TP12821',
        'Black Silicone Case for T-Phone 21;150;The silky, soft-touch finish of the silicone exterior feels great in your hand.;TSCB21',
        'Green Silicone Case for T-Phone 21;250;The silky, soft-touch finish of the silicone exterior feels great in your hand.;TSCG21',
        'Black Ear Cushions for T-Earbuds 21;200;'';TECB21',
        'Repair Insurance T2000;2000;The service provides the ability to repair malfunctions of a smartphone, tablet and headphones.;TRI200021',
        'Memory Card 512 GB;30;An electronic data storage device used for storing digital information, typically using flash memory.;TMC51221',
        'Box for T-Earbuds 21;50;'';TBTE21',
        'Designer Box for T-Earbuds 21;125;'';TDBTE21',
        'Headphones with 3.5 mm Plug;80;'';TH21',
        '20W USB-C Charger;100;20W USB‑C Charger offers fast, efficient charging at home, in the office, or on the go.;TC21',
        'T-Band 21;500;Fitnes-band, that incorporates fitness tracking, health-oriented capabilities, integrates with Android, iOS and other products and services.;TB21',
        'T-Earbuds 21;300;Wireless Bluetooth earbuds.;TE21',
        'Box for T-Phone 21;50;'';TBTP21',
        'Repair Insurance T1000;1000;The service provides the ability to repair malfunctions of a smartphone or tablet.;TRI100021',
        'Repair Insurance T300;300;The service provides the ability to repair malfunctions of a smartphone or tablet.;TRI30021',
        'T-Phone 21 512 GB;2000;Latest generation of smartphones, offering OLED displays, 5G connectivity, the T14 chip for better performance, improved cameras.;TP51221',
        'T-Watch 21;800;Smartwatch, that incorporates fitness tracking, health-oriented capabilities, and wireless telecommunication, integrates only with Android OS.;TW21',]
    Commercial_existing_entry = sf.query(
            f"SELECT Id FROM Pricebook2 WHERE Name = 'Commercial'"
        )

    if not Commercial_existing_entry['records']:
        Commercial_existing_entry = sf.Pricebook2.create({
            'Name': 'Commercial',
            'IsActive': True
        })['id']
    else:
        Commercial_existing_entry = Commercial_existing_entry['records'][0]['Id']

    def worker1(i):

        product_name = products[i].split(';')[0]
        product_price = float(products[i].split(';')[1])
        product_desciption = products[i].split(';')[2]
        product_code = products[i].split(';')[3]
        existing_product = sf.query(
            f"SELECT Id FROM Product2 WHERE Name = '{product_name}'"
        )

        if existing_product['records']:
            print(f"{product_name} exists")
            return


        products_id = sf.Product2.create({
            'Name': product_name,
            'IsActive': True, 
            'ProductCode': product_code,
            'Description': product_desciption
                })['id']
        
        sf.PricebookEntry.create({
            'Pricebook2Id': pricebook_id,
            'Product2Id': products_id,
            'UnitPrice': product_price,
            'IsActive': True
        })

    with ThreadPoolExecutor(max_workers=25) as executor:
        futures = [
            executor.submit(worker1, i)
            for i in range(len(products))
        ]

        for f in as_completed(futures):
            f.result()
    def worker2(i):
        product_name = products[i].split(';')[0]
        product_price = (float(products[i].split(';')[1]))*random.choice([0.5, 1.5])

        product = sf.query(
            f"SELECT Id FROM Product2 WHERE Name = '{product_name}'"
        )

        if not product['records']:
            print(product_name, "NOT FOUND")
            return

        products_id = product['records'][0]['Id']
        query = sf.query(
            f"SELECT Id FROM PricebookEntry WHERE Product2Id = '{products_id}' AND Pricebook2.Name = 'Commercial'"
        )

        exist_pbe = query['records']

        if not exist_pbe:
            sf.PricebookEntry.create({
                'Pricebook2Id': Commercial_existing_entry,
                'Product2Id': products_id,
                'UnitPrice': product_price,
                'IsActive': True
            })
        else:
            print(product_name, "exists")

    with ThreadPoolExecutor(max_workers=25) as executor:
        futures = [
            executor.submit(worker2, i)
            for i in range(len(products))
        ]

        for f in as_completed(futures):
            f.result()


def create_bundle():
    print('Start Bundle creation')
    Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
    rt_id = Rt_bundle_in_qurey['records'][0]['Id']
    print(f"Bundle Record Type id is {rt_id}")
    try:
        smarphone_bundle_query_result = sf.query(f"select name, id from product2 where name like 'Smartphone Bundle Test'")
        if len(smarphone_bundle_query_result.get('records')) >= 1:
            print('Smartphone Bundle already created')
        else:
            print('Smartphone bundle to be created')
            created_bundle_id = sf.product2.create({
                'Name': f'Smartphone Bundle Test',
                'RecordTypeId': rt_id,
                'IsActive': 'true'
            })

            created_bundle_id = sf.query(f"select name, id from product2 where name = 'Smartphone Bundle Test'")['records'][0]['Id']
            print(f'New ID of bundle is {created_bundle_id}\n Now lets create Features')

        
            MAIN_PRODUCT_feature_id = sf.SCLP__ProductFeature__c.create({
                'Name': 'MAIN PRODUCT',
                'SCLP__HasGroup__c': 'false',
                'SCLP__Multiple__c': 'false',
                'SCLP__Order__c': '1',
                'SCLP__Product__c': created_bundle_id,
                'SCLP__Required__c': 'false',
                # 'SCLP__Tip__c': 'Feature Number One tip'
            })['id']
            print(f'first feature id is {MAIN_PRODUCT_feature_id}')
            ACCESSORIES_feature_id = sf.SCLP__ProductFeature__c.create({
                'Name': 'ACCESSORIES',
                'SCLP__HasGroup__c': 'false',
                'SCLP__Multiple__c': 'true',
                'SCLP__Order__c': '2',
                'SCLP__Product__c': created_bundle_id,
                'SCLP__Required__c': 'false',
                # 'SCLP__Tip__c': 'Feature Number two tip'
            })['id']
            print(f'second feature id is {ACCESSORIES_feature_id}')
            box_feature_id = sf.SCLP__ProductFeature__c.create({
                'Name': 'BOX',
                'SCLP__HasGroup__c': 'false',
                'SCLP__Multiple__c': 'true',
                'SCLP__Order__c': '3',
                'SCLP__Product__c': created_bundle_id,
                'SCLP__Required__c': 'false',
                # 'SCLP__Tip__c': 'Feature Number two tip'
            })['id']  
            print(f'third feature id is {box_feature_id}')
            INSURANCE_feature_id = sf.SCLP__ProductFeature__c.create({
                'Name': 'INSURANCE',
                'SCLP__HasGroup__c': 'false',
                'SCLP__Multiple__c': 'false',
                'SCLP__Order__c': '4',
                'SCLP__Product__c': created_bundle_id,
                'SCLP__Required__c': 'false',
                # 'SCLP__Tip__c': 'Feature Number two tip'
            })['id']                       
            print(f'second feature id is {INSURANCE_feature_id}\n Now lets create options')


            sf.SCLP__ProductOption__c.create({
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__Feature__c': MAIN_PRODUCT_feature_id,
                'SCLP__Order__c': '1',
                'SCLP__Product__c': sf.query(f"select id from product2 where name = 'T-Phone 21 512 GB'")['records'][0]['Id'],
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Tip test 1',
                'SCLP__HideInQuote__c': False
            })['id']
            print("Options 'T-Phone 21 512 GB' is created")
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '2',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': MAIN_PRODUCT_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = 'T-Phone 21 128 GB'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                'SCLP__Tip__c': 'This is a preferable option',
                'SCLP__HideInQuote__c': False
            })
            print('Options T-Phone 21 128 GB is created')
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '1',
                'SCLP__BundleQuantity__c': '2',
                'SCLP__Feature__c': ACCESSORIES_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = 'Memory Card 512 GB'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'This is a preferable option',
                'SCLP__HideInQuote__c': False

            })
            print('Options Memory Card 512 GB is created')
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '2',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': ACCESSORIES_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = 'T-Watch 21'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'This is a preferable option',
                'SCLP__HideInQuote__c': False

            })
            print('Options Memory Card 512 GB is created')

            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '3',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': ACCESSORIES_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = 'Black Silicone Case for T-Phone 21'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'This is a preferable option',
                'SCLP__HideInQuote__c': False
            })
            print('Options Black Silicone Case for T-Phone 21 is created')

            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '4',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': ACCESSORIES_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '20W USB-C Charger'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                'SCLP__Tip__c': 'Compatible only with T-Phone 21',
                'SCLP__HideInQuote__c': False
            })
            print('Options 20W USB-C Charger is created')
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '5',
                'SCLP__BundleQuantity__c': '2',
                'SCLP__Feature__c': ACCESSORIES_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = 'Green Silicone Case for T-Phone 21'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Compatible only with T-Phone 21',
                'SCLP__HideInQuote__c': False
            })
            print('Options Green Silicone Case for T-Phone 21 is created')

            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '6',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': ACCESSORIES_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = 'T-Band 21'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Compatible only with T-Phone 21',
                'SCLP__HideInQuote__c': False
            })
            print('Options T-Band 21 is created')
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '1',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': box_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = 'Designer Box for T-Earbuds 21'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Compatible only with T-Phone 21',
                'SCLP__HideInQuote__c': False
            })
            print('Options Designer Box for T-Earbuds 21 is created')
            option = 'Designer Box for T-Phone 21'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '2',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': box_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Compatible only with T-Phone 21',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'Box for T-Earbuds 21'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '3',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': box_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Compatible only with T-Phone 21',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'Box for T-Phone 21'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '4',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': box_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Compatible only with T-Phone 21',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'Repair Insurance T2000'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '1',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': INSURANCE_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'Repair Insurance T1000'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '2',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': INSURANCE_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'Repair Insurance T300'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '3',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': INSURANCE_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'Green Silicone Case for T-Phone 21'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '4',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': INSURANCE_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')

        T_Earbuds_bundle_query_result = sf.query(f"select name, id from product2 where name like 'T-Earbuds Bundle'")
        if len(T_Earbuds_bundle_query_result.get('records')) >= 1:
            print('Smartphone Bundle already created')
        else:
            print('T-Earbuds Bundle to be created')
            Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
            rt_id = Rt_bundle_in_qurey['records'][0]['Id']
            print(f"Bundle Record Type id is {rt_id}")
            created_bundle_id = sf.product2.create({
                'Name': f'T-Earbuds Bundle',
                'RecordTypeId': rt_id,
                'IsActive': 'true'
            })
            created_bundle_id = sf.query(f"select name, id from product2 where name = 'T-Earbuds Bundle'")['records'][0]['Id']
            option = 'Box for T-Earbuds 21'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '1',
                'SCLP__BundleQuantity__c': '1',
                # 'SCLP__Feature__c': INSURANCE_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'Black Ear Cushions for T-Earbuds 21'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '2',
                'SCLP__BundleQuantity__c': '1',
                # 'SCLP__Feature__c': INSURANCE_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'Green Ear Cushions for T-Earbuds 21'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '3',
                'SCLP__BundleQuantity__c': '1',
                # 'SCLP__Feature__c': INSURANCE_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'T-Earbuds 21'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '4',
                'SCLP__BundleQuantity__c': '1',
                # 'SCLP__Feature__c': INSURANCE_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')

            option = 'Designer Box for T-Earbuds 21'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '5',
                'SCLP__BundleQuantity__c': '1',
                # 'SCLP__Feature__c': INSURANCE_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False,
                'SCLP__FixedPrice__c': True
            })
            print(f'Options {option} is created')

        T_Phone_128_gb_bundle_query_result = sf.query(f"select name, id from product2 where name like 'T-Phone 128 GB Bundle'")
        if len(T_Phone_128_gb_bundle_query_result.get('records')) >= 1:
            print('128gb Bundle already created')
        else:
            print('T-Earbuds Bundle to be created')
            Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
            rt_id = Rt_bundle_in_qurey['records'][0]['Id']
            print(f"Bundle Record Type id is {rt_id}")
            created_bundle_id = sf.product2.create({
                'Name': f'T-Phone 128 GB Bundle',
                'RecordTypeId': rt_id,
                'IsActive': 'true'
            })
            created_bundle_id = sf.query(f"select name, id from product2 where name = 'T-Phone 128 GB Bundle'")['records'][0]['Id']
            
            MAIN_PRODUCT_feature_id = sf.SCLP__ProductFeature__c.create({
            'Name': 'Main Test Product',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '1',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            # 'SCLP__Tip__c': 'Feature Number One tip'
            })['id']
            print(f'first feature id is {MAIN_PRODUCT_feature_id}')
            ACCESSORIES_feature_id = sf.SCLP__ProductFeature__c.create({
            'Name': 'ACCESSORIES',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'true',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            # 'SCLP__Tip__c': 'Feature Number One tip'
            })['id']
            print(f'first feature id is {ACCESSORIES_feature_id}')                
            BOX_feature_id = sf.SCLP__ProductFeature__c.create({
            'Name': 'BOX',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '3',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            # 'SCLP__Tip__c': 'Feature Number One tip'
            })['id']
            print(f'first feature id is {BOX_feature_id}')                
            Additiona_products_feature_id = sf.SCLP__ProductFeature__c.create({
            'Name': 'ADDITIONAL PRODUCTS',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '4',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            # 'SCLP__Tip__c': 'Feature Number One tip'
            })['id']
            print(f'first feature id is {Additiona_products_feature_id}')
        
            option = 'T-Phone 21 128 GB'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '1',
                'SCLP__BundleQuantity__c': '2',
                'SCLP__Feature__c': MAIN_PRODUCT_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'Green Silicone Case for T-Phone 21'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '1',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': ACCESSORIES_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'Headphones with 3.5 mm Plug'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '2',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': ACCESSORIES_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')

            option = 'Memory Card 512 GB'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '3',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': ACCESSORIES_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'Black Silicone Case for T-Phone 21'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '4',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': ACCESSORIES_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                'SCLP__Tip__c': "That's a preferred selection",
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = '20W USB-C Charger'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '5',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': ACCESSORIES_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'Box for T-Phone 21'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '1',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': BOX_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'Designer Box for T-Phone 21'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '2',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': BOX_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'T-Earbuds 21'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '1',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': Additiona_products_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'Designer Box for T-Earbuds 21'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '2',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': Additiona_products_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
#################
        T_Phone_128_gb_unconfigurable_bundle_query_result = sf.query(f"select name, id from product2 where name = 'T-Phone 128 GB with accesories'")
        if len(T_Phone_128_gb_unconfigurable_bundle_query_result.get('records')) >= 1:
            print('128gb Bundle already created')
        else:
            print('T-Earbuds Bundle to be created')
            Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
            rt_id = Rt_bundle_in_qurey['records'][0]['Id']
            print(f"Bundle Record Type id is {rt_id}")
            created_bundle_id = sf.product2.create({
                'Name': f'T-Phone 128 GB with accesories',
                'RecordTypeId': rt_id,
                'IsActive': 'true',
                'SCLP__Configurable__c': False
            })
            created_bundle_id = sf.query(f"select name, id from product2 where name = 'T-Phone 128 GB with accesories'")['records'][0]['Id']
            
            MAIN_PRODUCT_feature_id = sf.SCLP__ProductFeature__c.create({
            'Name': 'Main Test Product',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '1',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            # 'SCLP__Tip__c': 'Feature Number One tip'
            })['id']
            print(f'first feature id is {MAIN_PRODUCT_feature_id}')
            ACCESSORIES_feature_id = sf.SCLP__ProductFeature__c.create({
            'Name': 'ACCESSORIES',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'true',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            # 'SCLP__Tip__c': 'Feature Number One tip'
            })['id']
            print(f'first feature id is {ACCESSORIES_feature_id}')                
            Additiona_products_feature_id = sf.SCLP__ProductFeature__c.create({
            'Name': 'ADDITIONAL PRODUCTS',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '3',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            # 'SCLP__Tip__c': 'Feature Number One tip'
            })['id']
            print(f'first feature id is {Additiona_products_feature_id}')
        
            option = 'T-Phone 21 128 GB'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '1',
                'SCLP__BundleQuantity__c': '2',
                'SCLP__Feature__c': MAIN_PRODUCT_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'Green Silicone Case for T-Phone 21'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '1',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': ACCESSORIES_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'Headphones with 3.5 mm Plug'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '2',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': ACCESSORIES_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')

            option = 'Memory Card 512 GB'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '3',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': ACCESSORIES_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = '20W USB-C Charger'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '4',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': ACCESSORIES_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'T-Earbuds 21'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '1',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': Additiona_products_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
####################                
        t_phone_bundle_query_result = sf.query(f"select name, id from product2 where name like 'T-Phone Bundle'")
        if len(t_phone_bundle_query_result.get('records')) >= 1:
            print('T-Phone Bundle Bundle already created')
        else:
            print('T-Phone Bundle Bundle to be created')
            Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
            rt_id = Rt_bundle_in_qurey['records'][0]['Id']
            print(f"Bundle Record Type id is {rt_id}")
            created_bundle_id = sf.product2.create({
                'Name': f'T-Phone Bundle',
                'RecordTypeId': rt_id,
                'IsActive': 'true'
            })
            created_bundle_id = sf.query(f"select name, id from product2 where name = 'T-Phone Bundle'")['records'][0]['Id']
            
            MAIN_PRODUCT_feature_id = sf.SCLP__ProductFeature__c.create({
            'Name': 'MAIN PRODUCT',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '1',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            # 'SCLP__Tip__c': 'Feature Number One tip'
            })['id']
            print(f'first feature id is {MAIN_PRODUCT_feature_id}')
            ACCESSORIES_feature_id = sf.SCLP__ProductFeature__c.create({
            'Name': 'ACCESSORIES',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'true',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            # 'SCLP__Tip__c': 'Feature Number One tip'
            })['id']
            print(f'first feature id is {ACCESSORIES_feature_id}')                
            BOX_feature_id = sf.SCLP__ProductFeature__c.create({
            'Name': 'BOX',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '3',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            # 'SCLP__Tip__c': 'Feature Number One tip'
            })['id']
            print(f'first feature id is {BOX_feature_id}')                
            INSURANCE_feature_id = sf.SCLP__ProductFeature__c.create({
            'Name': 'Insurance',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '4',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false',
            # 'SCLP__Tip__c': 'Feature Number One tip'
            })['id']
            print(f'first feature id is {Additiona_products_feature_id}')
        
            option = 'T-Phone 21 128 GB'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '1',
                'SCLP__BundleQuantity__c': '2',
                'SCLP__Feature__c': MAIN_PRODUCT_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')                
            option = 'T-Phone 21 512 GB'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '2',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': MAIN_PRODUCT_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'Memory Card 512 GB'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '1',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': ACCESSORIES_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'Black Silicone Case for T-Phone 21'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '2',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': ACCESSORIES_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')

            option = 'Green Silicone Case for T-Phone 21'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '3',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': ACCESSORIES_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = '20W USB-C Charger'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '4',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': ACCESSORIES_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': "That's a preferred selection",
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'Headphones with 3.5 mm Plug'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '5',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': ACCESSORIES_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'Designer Box for T-Phone 21'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '1',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': BOX_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'Box for T-Phone 21'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '2',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': BOX_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'Repair Insurance T2000'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '1',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': INSURANCE_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'Repair Insurance T1000'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '2',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': INSURANCE_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')
            option = 'Repair Insurance T300'
            sf.SCLP__ProductOption__c.create({
                'SCLP__Order__c': '3',
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Feature__c': INSURANCE_feature_id,
                'SCLP__Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__DefaultOption__c': 'false',
                'SCLP__ChildRequired__c': 'false',
                # 'SCLP__Tip__c': 'Only in-store repair coverage',
                'SCLP__HideInQuote__c': False
            })
            print(f'Options {option} is created')

    except SalesforceError as e:
            "INVALID_TYPE" in str(e)
            print("no SCLP__")            
            smarphone_bundle_query_result = sf.query(f"select name, id from product2 where name like 'Smartphone Bundle Test'")
            if len(smarphone_bundle_query_result.get('records')) >= 1:
                print('Smartphone Bundle already created')
            else:
                print('Smartphone bundle to be created')
                created_bundle_id = sf.product2.create({
                    'Name': f'Smartphone Bundle Test',
                    'RecordTypeId': rt_id,
                    'IsActive': 'true'
                })

                created_bundle_id = sf.query(f"select name, id from product2 where name = 'Smartphone Bundle Test'")['records'][0]['Id']
                print(f'New ID of bundle is {created_bundle_id}\n Now lets create Features')

            
                MAIN_PRODUCT_feature_id = sf.ProductFeature__c.create({
                    'Name': 'MAIN PRODUCT',
                    'HasGroup__c': 'false',
                    'Multiple__c': 'false',
                    'Order__c': '1',
                    'Product__c': created_bundle_id,
                    'Required__c': 'false',
                    # 'Tip__c': 'Feature Number One tip'
                })['id']
                print(f'first feature id is {MAIN_PRODUCT_feature_id}')
                ACCESSORIES_feature_id = sf.ProductFeature__c.create({
                    'Name': 'ACCESSORIES',
                    'HasGroup__c': 'false',
                    'Multiple__c': 'true',
                    'Order__c': '2',
                    'Product__c': created_bundle_id,
                    'Required__c': 'false',
                    # 'Tip__c': 'Feature Number two tip'
                })['id']
                print(f'second feature id is {ACCESSORIES_feature_id}')
                box_feature_id = sf.ProductFeature__c.create({
                    'Name': 'BOX',
                    'HasGroup__c': 'false',
                    'Multiple__c': 'true',
                    'Order__c': '3',
                    'Product__c': created_bundle_id,
                    'Required__c': 'false',
                    # 'Tip__c': 'Feature Number two tip'
                })['id']  
                print(f'third feature id is {box_feature_id}')
                INSURANCE_feature_id = sf.ProductFeature__c.create({
                    'Name': 'INSURANCE',
                    'HasGroup__c': 'false',
                    'Multiple__c': 'false',
                    'Order__c': '4',
                    'Product__c': created_bundle_id,
                    'Required__c': 'false',
                    # 'Tip__c': 'Feature Number two tip'
                })['id']                       
                print(f'second feature id is {INSURANCE_feature_id}\n Now lets create options')


                sf.ProductOption__c.create({
                    'BundleQuantity__c': '1',
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'Feature__c': MAIN_PRODUCT_feature_id,
                    'Order__c': '1',
                    'Product__c': sf.query(f"select id from product2 where name = 'T-Phone 21 512 GB'")['records'][0]['Id'],
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Tip test 1',
                    'HideInQuote__c': False
                })['id']
                print("Options 'T-Phone 21 512 GB' is created")
                sf.ProductOption__c.create({
                    'Order__c': '2',
                    'BundleQuantity__c': '1',
                    'Feature__c': MAIN_PRODUCT_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = 'T-Phone 21 128 GB'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    'Tip__c': 'This is a preferable option',
                    'HideInQuote__c': False
                })
                print('Options T-Phone 21 128 GB is created')
                sf.ProductOption__c.create({
                    'Order__c': '1',
                    'BundleQuantity__c': '2',
                    'Feature__c': ACCESSORIES_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = 'Memory Card 512 GB'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'This is a preferable option',
                    'HideInQuote__c': False

                })
                print('Options Memory Card 512 GB is created')
                sf.ProductOption__c.create({
                    'Order__c': '2',
                    'BundleQuantity__c': '1',
                    'Feature__c': ACCESSORIES_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = 'T-Watch 21'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'This is a preferable option',
                    'HideInQuote__c': False

                })
                print('Options Memory Card 512 GB is created')

                sf.ProductOption__c.create({
                    'Order__c': '3',
                    'BundleQuantity__c': '1',
                    'Feature__c': ACCESSORIES_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = 'Black Silicone Case for T-Phone 21'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'This is a preferable option',
                    'HideInQuote__c': False
                })
                print('Options Black Silicone Case for T-Phone 21 is created')

                sf.ProductOption__c.create({
                    'Order__c': '4',
                    'BundleQuantity__c': '1',
                    'Feature__c': ACCESSORIES_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '20W USB-C Charger'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    'Tip__c': 'Compatible only with T-Phone 21',
                    'HideInQuote__c': False
                })
                print('Options 20W USB-C Charger is created')
                sf.ProductOption__c.create({
                    'Order__c': '5',
                    'BundleQuantity__c': '2',
                    'Feature__c': ACCESSORIES_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = 'Green Silicone Case for T-Phone 21'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Compatible only with T-Phone 21',
                    'HideInQuote__c': False
                })
                print('Options Green Silicone Case for T-Phone 21 is created')

                sf.ProductOption__c.create({
                    'Order__c': '6',
                    'BundleQuantity__c': '1',
                    'Feature__c': ACCESSORIES_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = 'T-Band 21'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Compatible only with T-Phone 21',
                    'HideInQuote__c': False
                })
                print('Options T-Band 21 is created')
                sf.ProductOption__c.create({
                    'Order__c': '1',
                    'BundleQuantity__c': '1',
                    'Feature__c': box_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = 'Designer Box for T-Earbuds 21'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Compatible only with T-Phone 21',
                    'HideInQuote__c': False
                })
                print('Options Designer Box for T-Earbuds 21 is created')
                option = 'Designer Box for T-Phone 21'
                sf.ProductOption__c.create({
                    'Order__c': '2',
                    'BundleQuantity__c': '1',
                    'Feature__c': box_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Compatible only with T-Phone 21',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'Box for T-Earbuds 21'
                sf.ProductOption__c.create({
                    'Order__c': '3',
                    'BundleQuantity__c': '1',
                    'Feature__c': box_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Compatible only with T-Phone 21',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'Box for T-Phone 21'
                sf.ProductOption__c.create({
                    'Order__c': '4',
                    'BundleQuantity__c': '1',
                    'Feature__c': box_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Compatible only with T-Phone 21',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'Repair Insurance T2000'
                sf.ProductOption__c.create({
                    'Order__c': '1',
                    'BundleQuantity__c': '1',
                    'Feature__c': INSURANCE_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'Repair Insurance T1000'
                sf.ProductOption__c.create({
                    'Order__c': '2',
                    'BundleQuantity__c': '1',
                    'Feature__c': INSURANCE_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'Repair Insurance T300'
                sf.ProductOption__c.create({
                    'Order__c': '3',
                    'BundleQuantity__c': '1',
                    'Feature__c': INSURANCE_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'Green Silicone Case for T-Phone 21'
                sf.ProductOption__c.create({
                    'Order__c': '4',
                    'BundleQuantity__c': '1',
                    'Feature__c': INSURANCE_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')

            T_Earbuds_bundle_query_result = sf.query(f"select name, id from product2 where name like 'T-Earbuds Bundle'")
            if len(T_Earbuds_bundle_query_result.get('records')) >= 1:
                print('Smartphone Bundle already created')
            else:
                print('T-Earbuds Bundle to be created')
                Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
                rt_id = Rt_bundle_in_qurey['records'][0]['Id']
                print(f"Bundle Record Type id is {rt_id}")
                created_bundle_id = sf.product2.create({
                    'Name': f'T-Earbuds Bundle',
                    'RecordTypeId': rt_id,
                    'IsActive': 'true'
                })
                created_bundle_id = sf.query(f"select name, id from product2 where name = 'T-Earbuds Bundle'")['records'][0]['Id']
                option = 'Box for T-Earbuds 21'
                sf.ProductOption__c.create({
                    'Order__c': '1',
                    'BundleQuantity__c': '1',
                    # 'Feature__c': INSURANCE_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'Black Ear Cushions for T-Earbuds 21'
                sf.ProductOption__c.create({
                    'Order__c': '2',
                    'BundleQuantity__c': '1',
                    # 'Feature__c': INSURANCE_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'Green Ear Cushions for T-Earbuds 21'
                sf.ProductOption__c.create({
                    'Order__c': '3',
                    'BundleQuantity__c': '1',
                    # 'Feature__c': INSURANCE_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'T-Earbuds 21'
                sf.ProductOption__c.create({
                    'Order__c': '4',
                    'BundleQuantity__c': '1',
                    # 'Feature__c': INSURANCE_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')

                option = 'Designer Box for T-Earbuds 21'
                sf.ProductOption__c.create({
                    'Order__c': '5',
                    'BundleQuantity__c': '1',
                    # 'Feature__c': INSURANCE_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False,
                    'FixedPrice__c': True
                })
                print(f'Options {option} is created')

            T_Phone_128_gb_bundle_query_result = sf.query(f"select name, id from product2 where name like 'T-Phone 128 GB Bundle'")
            if len(T_Phone_128_gb_bundle_query_result.get('records')) >= 1:
                print('128gb Bundle already created')
            else:
                print('T-Earbuds Bundle to be created')
                Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
                rt_id = Rt_bundle_in_qurey['records'][0]['Id']
                print(f"Bundle Record Type id is {rt_id}")
                created_bundle_id = sf.product2.create({
                    'Name': f'T-Phone 128 GB Bundle',
                    'RecordTypeId': rt_id,
                    'IsActive': 'true'
                })
                created_bundle_id = sf.query(f"select name, id from product2 where name = 'T-Phone 128 GB Bundle'")['records'][0]['Id']
                
                MAIN_PRODUCT_feature_id = sf.ProductFeature__c.create({
                'Name': 'Main Test Product',
                'HasGroup__c': 'false',
                'Multiple__c': 'false',
                'Order__c': '1',
                'Product__c': created_bundle_id,
                'Required__c': 'false',
                # 'Tip__c': 'Feature Number One tip'
                })['id']
                print(f'first feature id is {MAIN_PRODUCT_feature_id}')
                ACCESSORIES_feature_id = sf.ProductFeature__c.create({
                'Name': 'ACCESSORIES',
                'HasGroup__c': 'false',
                'Multiple__c': 'true',
                'Order__c': '2',
                'Product__c': created_bundle_id,
                'Required__c': 'false',
                # 'Tip__c': 'Feature Number One tip'
                })['id']
                print(f'first feature id is {ACCESSORIES_feature_id}')                
                BOX_feature_id = sf.ProductFeature__c.create({
                'Name': 'BOX',
                'HasGroup__c': 'false',
                'Multiple__c': 'false',
                'Order__c': '3',
                'Product__c': created_bundle_id,
                'Required__c': 'false',
                # 'Tip__c': 'Feature Number One tip'
                })['id']
                print(f'first feature id is {BOX_feature_id}')                
                Additiona_products_feature_id = sf.ProductFeature__c.create({
                'Name': 'ADDITIONAL PRODUCTS',
                'HasGroup__c': 'false',
                'Multiple__c': 'false',
                'Order__c': '4',
                'Product__c': created_bundle_id,
                'Required__c': 'false',
                # 'Tip__c': 'Feature Number One tip'
                })['id']
                print(f'first feature id is {Additiona_products_feature_id}')
            
                option = 'T-Phone 21 128 GB'
                sf.ProductOption__c.create({
                    'Order__c': '1',
                    'BundleQuantity__c': '2',
                    'Feature__c': MAIN_PRODUCT_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'Green Silicone Case for T-Phone 21'
                sf.ProductOption__c.create({
                    'Order__c': '1',
                    'BundleQuantity__c': '1',
                    'Feature__c': ACCESSORIES_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'Headphones with 3.5 mm Plug'
                sf.ProductOption__c.create({
                    'Order__c': '2',
                    'BundleQuantity__c': '1',
                    'Feature__c': ACCESSORIES_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')

                option = 'Memory Card 512 GB'
                sf.ProductOption__c.create({
                    'Order__c': '3',
                    'BundleQuantity__c': '1',
                    'Feature__c': ACCESSORIES_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'Black Silicone Case for T-Phone 21'
                sf.ProductOption__c.create({
                    'Order__c': '4',
                    'BundleQuantity__c': '1',
                    'Feature__c': ACCESSORIES_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    'Tip__c': "That's a preferred selection",
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = '20W USB-C Charger'
                sf.ProductOption__c.create({
                    'Order__c': '5',
                    'BundleQuantity__c': '1',
                    'Feature__c': ACCESSORIES_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'Box for T-Phone 21'
                sf.ProductOption__c.create({
                    'Order__c': '1',
                    'BundleQuantity__c': '1',
                    'Feature__c': BOX_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'Designer Box for T-Phone 21'
                sf.ProductOption__c.create({
                    'Order__c': '2',
                    'BundleQuantity__c': '1',
                    'Feature__c': BOX_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'T-Earbuds 21'
                sf.ProductOption__c.create({
                    'Order__c': '1',
                    'BundleQuantity__c': '1',
                    'Feature__c': Additiona_products_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'Designer Box for T-Earbuds 21'
                sf.ProductOption__c.create({
                    'Order__c': '2',
                    'BundleQuantity__c': '1',
                    'Feature__c': Additiona_products_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
    #################
            T_Phone_128_gb_unconfigurable_bundle_query_result = sf.query(f"select name, id from product2 where name = 'T-Phone 128 GB with accesories'")
            if len(T_Phone_128_gb_unconfigurable_bundle_query_result.get('records')) >= 1:
                print('128gb Bundle already created')
            else:
                print('T-Earbuds Bundle to be created')
                Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
                rt_id = Rt_bundle_in_qurey['records'][0]['Id']
                print(f"Bundle Record Type id is {rt_id}")
                created_bundle_id = sf.product2.create({
                    'Name': f'T-Phone 128 GB with accesories',
                    'RecordTypeId': rt_id,
                    'IsActive': 'true',
                    'Configurable__c': False
                })
                created_bundle_id = sf.query(f"select name, id from product2 where name = 'T-Phone 128 GB with accesories'")['records'][0]['Id']
                
                MAIN_PRODUCT_feature_id = sf.ProductFeature__c.create({
                'Name': 'Main Test Product',
                'HasGroup__c': 'false',
                'Multiple__c': 'false',
                'Order__c': '1',
                'Product__c': created_bundle_id,
                'Required__c': 'false',
                # 'Tip__c': 'Feature Number One tip'
                })['id']
                print(f'first feature id is {MAIN_PRODUCT_feature_id}')
                ACCESSORIES_feature_id = sf.ProductFeature__c.create({
                'Name': 'ACCESSORIES',
                'HasGroup__c': 'false',
                'Multiple__c': 'true',
                'Order__c': '2',
                'Product__c': created_bundle_id,
                'Required__c': 'false',
                # 'Tip__c': 'Feature Number One tip'
                })['id']
                print(f'first feature id is {ACCESSORIES_feature_id}')                
                Additiona_products_feature_id = sf.ProductFeature__c.create({
                'Name': 'ADDITIONAL PRODUCTS',
                'HasGroup__c': 'false',
                'Multiple__c': 'false',
                'Order__c': '3',
                'Product__c': created_bundle_id,
                'Required__c': 'false',
                # 'Tip__c': 'Feature Number One tip'
                })['id']
                print(f'first feature id is {Additiona_products_feature_id}')
            
                option = 'T-Phone 21 128 GB'
                sf.ProductOption__c.create({
                    'Order__c': '1',
                    'BundleQuantity__c': '2',
                    'Feature__c': MAIN_PRODUCT_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'Green Silicone Case for T-Phone 21'
                sf.ProductOption__c.create({
                    'Order__c': '1',
                    'BundleQuantity__c': '1',
                    'Feature__c': ACCESSORIES_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'Headphones with 3.5 mm Plug'
                sf.ProductOption__c.create({
                    'Order__c': '2',
                    'BundleQuantity__c': '1',
                    'Feature__c': ACCESSORIES_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')

                option = 'Memory Card 512 GB'
                sf.ProductOption__c.create({
                    'Order__c': '3',
                    'BundleQuantity__c': '1',
                    'Feature__c': ACCESSORIES_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = '20W USB-C Charger'
                sf.ProductOption__c.create({
                    'Order__c': '4',
                    'BundleQuantity__c': '1',
                    'Feature__c': ACCESSORIES_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'T-Earbuds 21'
                sf.ProductOption__c.create({
                    'Order__c': '1',
                    'BundleQuantity__c': '1',
                    'Feature__c': Additiona_products_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
    ####################                
            t_phone_bundle_query_result = sf.query(f"select name, id from product2 where name like 'T-Phone Bundle'")
            if len(t_phone_bundle_query_result.get('records')) >= 1:
                print('T-Phone Bundle Bundle already created')
            else:
                print('T-Phone Bundle Bundle to be created')
                Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
                rt_id = Rt_bundle_in_qurey['records'][0]['Id']
                print(f"Bundle Record Type id is {rt_id}")
                created_bundle_id = sf.product2.create({
                    'Name': f'T-Phone Bundle',
                    'RecordTypeId': rt_id,
                    'IsActive': 'true'
                })
                created_bundle_id = sf.query(f"select name, id from product2 where name = 'T-Phone Bundle'")['records'][0]['Id']
                
                MAIN_PRODUCT_feature_id = sf.ProductFeature__c.create({
                'Name': 'MAIN PRODUCT',
                'HasGroup__c': 'false',
                'Multiple__c': 'false',
                'Order__c': '1',
                'Product__c': created_bundle_id,
                'Required__c': 'false',
                # 'Tip__c': 'Feature Number One tip'
                })['id']
                print(f'first feature id is {MAIN_PRODUCT_feature_id}')
                ACCESSORIES_feature_id = sf.ProductFeature__c.create({
                'Name': 'ACCESSORIES',
                'HasGroup__c': 'false',
                'Multiple__c': 'true',
                'Order__c': '2',
                'Product__c': created_bundle_id,
                'Required__c': 'false',
                # 'Tip__c': 'Feature Number One tip'
                })['id']
                print(f'first feature id is {ACCESSORIES_feature_id}')                
                BOX_feature_id = sf.ProductFeature__c.create({
                'Name': 'BOX',
                'HasGroup__c': 'false',
                'Multiple__c': 'false',
                'Order__c': '3',
                'Product__c': created_bundle_id,
                'Required__c': 'false',
                # 'Tip__c': 'Feature Number One tip'
                })['id']
                print(f'first feature id is {BOX_feature_id}')                
                INSURANCE_feature_id = sf.ProductFeature__c.create({
                'Name': 'Insurance',
                'HasGroup__c': 'false',
                'Multiple__c': 'false',
                'Order__c': '4',
                'Product__c': created_bundle_id,
                'Required__c': 'false',
                # 'Tip__c': 'Feature Number One tip'
                })['id']
                print(f'first feature id is {Additiona_products_feature_id}')
            
                option = 'T-Phone 21 128 GB'
                sf.ProductOption__c.create({
                    'Order__c': '1',
                    'BundleQuantity__c': '2',
                    'Feature__c': MAIN_PRODUCT_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')                
                option = 'T-Phone 21 512 GB'
                sf.ProductOption__c.create({
                    'Order__c': '2',
                    'BundleQuantity__c': '1',
                    'Feature__c': MAIN_PRODUCT_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'Memory Card 512 GB'
                sf.ProductOption__c.create({
                    'Order__c': '1',
                    'BundleQuantity__c': '1',
                    'Feature__c': ACCESSORIES_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'Black Silicone Case for T-Phone 21'
                sf.ProductOption__c.create({
                    'Order__c': '2',
                    'BundleQuantity__c': '1',
                    'Feature__c': ACCESSORIES_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')

                option = 'Green Silicone Case for T-Phone 21'
                sf.ProductOption__c.create({
                    'Order__c': '3',
                    'BundleQuantity__c': '1',
                    'Feature__c': ACCESSORIES_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = '20W USB-C Charger'
                sf.ProductOption__c.create({
                    'Order__c': '4',
                    'BundleQuantity__c': '1',
                    'Feature__c': ACCESSORIES_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': "That's a preferred selection",
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'Headphones with 3.5 mm Plug'
                sf.ProductOption__c.create({
                    'Order__c': '5',
                    'BundleQuantity__c': '1',
                    'Feature__c': ACCESSORIES_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'Designer Box for T-Phone 21'
                sf.ProductOption__c.create({
                    'Order__c': '1',
                    'BundleQuantity__c': '1',
                    'Feature__c': BOX_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'Box for T-Phone 21'
                sf.ProductOption__c.create({
                    'Order__c': '2',
                    'BundleQuantity__c': '1',
                    'Feature__c': BOX_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'Repair Insurance T2000'
                sf.ProductOption__c.create({
                    'Order__c': '1',
                    'BundleQuantity__c': '1',
                    'Feature__c': INSURANCE_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'Repair Insurance T1000'
                sf.ProductOption__c.create({
                    'Order__c': '2',
                    'BundleQuantity__c': '1',
                    'Feature__c': INSURANCE_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')
                option = 'Repair Insurance T300'
                sf.ProductOption__c.create({
                    'Order__c': '3',
                    'BundleQuantity__c': '1',
                    'Feature__c': INSURANCE_feature_id,
                    'Product__c': sf.query(f"select id from product2 where name = '{option}'")['records'][0]['Id'],
                    'Bundle__c': created_bundle_id,
                    'DefaultOption__c': 'false',
                    'ChildRequired__c': 'false',
                    # 'Tip__c': 'Only in-store repair coverage',
                    'HideInQuote__c': False
                })
                print(f'Options {option} is created')

def create_account():
    print('Start creating account')
    account_created = "select name, id from account where name like 'BlueOcean Services'"



    results = sf.query(account_created)


    if results.get('records') and len(results['records']) > 0:
        print ('BlueOcean Services already exists')
    else:
        sf.account.create({
            'Name': f'BlueOcean Services',
            'BillingCity': 'Worthington',
            'BillingStreet': '2487  Old House Drive',
            # 'CleanStatus': 'Pending',
            # 'AccountNumber': '4'


            })
        print('BlueOcean Services account is created') 
    exist_contact_query = sf.query("SELECT Id, FirstName, LastName from Contact where Name like 'Timothy Davis'")
    if exist_contact_query['records']:
        print('Timothy Davis contact already exists')
    else:
        sf.contact.create({
            'FirstName': 'Timothy',
            'LastName': f'Davis',
            'AccountId': sf.query(f"select id from account where name = 'BlueOcean Services'")['records'][0]['Id'],
            # 'CleanStatus': 'Pending',
            'Email': 't.davist2121@gmail.com',
            'MailingCity': 'Binghamton',
            'MailingPostalCode': '13904',
            'MailingState': 'New York',
            'MailingStreet': '1252  Hinkle Deegan Lake Road',
            'Phone': '(212) 942-5611'
        })
    print('Timothy Davis contant is created')
    contact_query = f"SELECT Id, FirstName, LastName from Contact where Name like 'Timothy Davis'"
    print(f"Timothy Davis contant {sf.query(contact_query)['records'][0]['Id']} is created")
    print('Start creating EasyWay Education account')
    account_created = "select name, id from account where name like 'EasyWay Education'"



    results = sf.query(account_created)


    if results.get('records') and len(results['records']) > 0:
        print ('EasyWay Education  already exists')
    else:
        sf.account.create({
            'Name': f'EasyWay Education',
            'BillingCity': 'Secaucus',
            'BillingStreet': '2222  Goldleaf Lane',
            # 'CleanStatus': 'Pending',
            # 'AccountNumber': '5'


            })
        print('EasyWay Education account is created') 

def create_opportunity():
    print('Start creating Opportunity')
    Standard_Price_book_query = "select name, id from pricebook2 where name = 'Standard Price Book'"
    SPB_results = sf.query(Standard_Price_book_query)
    if SPB_results.get('records'):
        for PB in SPB_results['records']:
            SB_name = PB['Name']
            SPB_id = PB['Id']

            print(f"found {SB_name} with id: {SPB_id}")

    account_query = "select name, id from account where name like 'BlueOcean Services'"
    acc_results = sf.query(account_query)
    if acc_results.get('records'):
        for Accs in acc_results['records']:
            Acc_name = Accs['Name']
            Acc_id = Accs['Id']
            print(f'Account found with the name {Acc_name} with id: {Acc_id}')

    print('now it\'s about opportunity')
    opp = "select name, id from opportunity where name like 'T-Phone Box'"
    
    opp_results = sf.query(opp)

    

    if opp_results.get('records') and len(opp_results['records']) > 0:
        print ('T-Phone Box opportunity already exists')
    else:
        sf.opportunity.create({
            'Name': f'T-Phone Box',
            'CloseDate': '2025-09-04',
            'StageName': 'Needs Analysis',
            'Pricebook2Id': SPB_id,
            'AccountId': Acc_id,
            })
        print('test opportunity is created')          
    account_query = "select name, id from account where name like 'EasyWay Education'"
    acc_results = sf.query(account_query)
    if acc_results.get('records'):
        for Accs in acc_results['records']:
            Acc_name = Accs['Name']
            Acc_id = Accs['Id']
            print(f'Account found with the name {Acc_name} with id: {Acc_id}')

    print('now it\'s about opportunity')
    # opp = "select name, id from opportunity where name like 'Recurring Cleaning'"
    
    # opp_results = sf.query(opp)

    

    # if opp_results.get('records') and len(opp_results['records']) > 0:
    #     print ('Recurring Cleaning opportunity already exists')
    # else:
    #     sf.opportunity.create({
    #         'Name': f'Recurring Cleaning',
    #         'CloseDate': '2025-09-04',
    #         'StageName': 'Needs Analysis',
    #         'Pricebook2Id': SPB_id,
    #         'AccountId': Acc_id,
    #         })
    #     print('Recurring Cleaning opportunity is created')          

# create_products()
# print('Product, Price Book and Price Book Entreis are created')
create_bundle()
print('Bundles are created')
# create_account()
# print('Account created')
# create_opportunity()
# print('Opportunity created')