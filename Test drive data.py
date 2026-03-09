from simple_salesforce import Salesforce, SalesforceLogin, SalesforceError, SalesforceMalformedRequest
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

USERNAME='test-uv4yfxsmdgrr@example.com'
PASSWORD='ia9%xlifpgaJa'
SECURITE_TOKEN='Z3rOUPyYw5eWOCcUkVOXdjOLX'
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

    products_for_td = ['Window cleaning standard',
            'Window cleaning exterior',
            'Microfibre pads',
            'Carpet cleaning',
            'NG floor cleaning system',
            'Indoor Cleaning Starter Set',
            'General cleaning',
            'Floor service',
            'Glass Cleaner',
            'Pure water cleaning system Filter-X',
            'Deep cleaning',
            'Indoor Cleaning Kit 100 Plus',
            'Cleaning interior glass',
            'Green Ear Cushions for T-Earbuds 21',
            'Designer Box for T-Phone 21',
            'T-Phone 21 128 GB',
            'Black Silicone Case for T-Phone 21',
            'Green Silicone Case for T-Phone 21',
            'Black Ear Cushions for T-Earbuds 21',
            'Repair Insurance T2000',
            'Memory Card 512 GB',
            'Box for T-Earbuds 21',
            'Designer Box for T-Earbuds 21',
            'Headphones with 3.5 mm Plug',
            '20W USB-C Charger',
            'T-Band 21',
            'T-Earbuds 21',
            'Box for T-Phone 21',
            'Repair Insurance T1000',
            'Repair Insurance T300',
            'T-Phone 21 512 GB',
            'T-Watch 21']
    product_prices = [0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                200,
                150,
                1500,
                150,
                250,
                200,
                2000,
                30,
                50,
                125,
                80,
                100,
                500,
                300,
                50,
                1000,
                300,
                2000,
                800]
    product_codes = ['WCR1',
        'WCCE',
        'SUPLL12',
        'CRP1',
        'NGFLOOR',
        'SUPLL35',
        'GCR1',
        'FLRC',
        'SUPPGL32',
        'PWSX20',
        'DPC1',
        'INDKIT100',
        'CIGL',
        'TECG21',
        'TDBTP21',
        'TP12821',
        'TSCB21',
        'TSCG21',
        'TECB21',
        'TRI200021',
        'TMC51221',
        'TBTE21',
        'TDBTE21',
        'TH21',
        'TC21',
        'TB21',
        'TE21',
        'TBTP21',
        'TRI100021',
        'TRI30021',
        'TP51221',
        'TW21']
    product_desciptions = ['For all kinds of residential windows, including standard windows, window seals, bay windows, skylights, and french doors',
        'All sorts of storefront windows, glass doors, exterior cleaning for high-rise buildings',
        '',
        'Steam cleaning and spot removal for both one-time and recurring services',
        'Includes S-Telescopic handle, Mop Pad holder & Cleaning Pad 40 cm, Tank 1.000 ml & colour coding rings',
        'Microfibre cleaning pad 27 cm PHH20 Pad holder 24 cm AFAET Thread adapter for Alu-Poles',
        'A general clean consists of the basic cleaning tasks that include sweeping, vacuuming, dusting, mopping, etc. This type of "surface" cleaning is performed more often to maintain cleanliness and hygiene',
        'Floor cleaning services include: Stripping and Waxing Tile & Grout Cleaning and Grout Colouring Sealing Scrubbing High speed burnishing',
        'Professional Glass Cleaner for glass, mirrors, and other waterproof surfaces',
        '',
        'Includes the “General cleaning” with detail emphasis and focus on build up, plus the following: light fixtures, moldings, woodwork, and window sills, baseboards, lamp and lampshades, furniture, light switch plates, countertops and backsplashes, mirrors, wastebaskets',
        'Handheld Unit 1 x Cleaning Liquid Pouch 2 x Microfibre Deep Cleaning TriPad* Easy-Click-Pole',
        'Cleaning and polishing glass, mirrors and other waterproof surfaces',
        '',
        '',
        'Latest generation of smartphones, offering OLED displays, 5G connectivity, the T14 chip for better performance, improved cameras.',
        'The silky, soft-touch finish of the silicone exterior feels great in your hand.',
        'The silky, soft-touch finish of the silicone exterior feels great in your hand.',
        '',
        'The service provides the ability to repair malfunctions of a smartphone, tablet and headphones.',
        'An electronic data storage device used for storing digital information, typically using flash memory.',
        '',
        '',
        '',
        '20W USB‑C Charger offers fast, efficient charging at home, in the office, or on the go.',
        'Fitnes-band, that incorporates fitness tracking, health-oriented capabilities, integrates with Android, iOS and other products and services.',
        'Wireless Bluetooth earbuds.',
        '',
        'The service provides the ability to repair malfunctions of a smartphone or tablet.',
        'The service provides the ability to repair malfunctions of a smartphone or tablet.',
        'Latest generation of smartphones, offering OLED displays, 5G connectivity, the T14 chip for better performance, improved cameras.',
        'Smartwatch, that incorporates fitness tracking, health-oriented capabilities, and wireless telecommunication, integrates only with Android OS.']
    Commercial_existing_entry = sf.query(
            f"SELECT Id FROM Pricebook2 WHERE Name = 'Commercial'"
        )['records'][0]['Id']

    if not Commercial_existing_entry:
        Commercial_existing_entry = sf.Pricebook2.create({
            'Name': 'Commercial',
            'IsActive': True
        })['id']
    commercial_name_and_price = ['Cleaning interior glass;32',
'Carpet cleaning;50',
'Floor service;30',
'Indoor Cleaning Starter Set;24',
'Deep cleaning;45',
'General cleaning;26',
'Indoor Cleaning Kit 100 Plus;28',
'Glass Cleaner;30',
'NG floor cleaning system;70',
'Pure water cleaning system Filter-X;120',
'Microfibre pads;2',
'Window cleaning standard;35',
'Window cleaning exterior;40',]
    
    Residential_existing_entry = sf.query(
            f"SELECT Id FROM Pricebook2 WHERE Name = 'Residential'"
        )['records'][0]['Id']

    if not Residential_existing_entry:
        Residential_existing_entry = sf.Pricebook2.create({
            'Name': 'Residential',
            'IsActive': True
        })['id']
    Residential_name_and_price = ['Microfibre pads;2.5',
'Indoor Cleaning Kit 100 Plus;28',
'Deep cleaning;50',
'Window cleaning standard;25',
'Carpet cleaning;45',
'Floor service;35',
'NG floor cleaning system;75',
'Indoor Cleaning Starter Set;26',
'Pure water cleaning system Filter-X;0',
'Window cleaning exterior;0',
'General cleaning;30',
'Glass Cleaner;30',]

    def worker1(i):
        product_name = products_for_td[i]
        product_price = product_prices[i]
        product_code = product_codes[i]
        product_desciption = product_desciptions[i]
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
            for i in range(len(products_for_td))
        ]

        for f in as_completed(futures):
            f.result()
    def worker2(i):
        product_name = commercial_name_and_price[i].split(';')[0]
        print(product_name)
        product_price = float(commercial_name_and_price[i].split(';')[1])
        products = sf.query(
            f"SELECT Id FROM Product2 WHERE Name = '{product_name}'"
        )

        if not products['records']:
            print(product_name, "NOT FOUND")
            return

        products_id = products['records'][0]['Id']
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
            for i in range(len(commercial_name_and_price))
        ]

        for f in as_completed(futures):
            f.result()
    def worker3(i):
        product_name = Residential_name_and_price[i].split(';')[0]
        print(product_name)
        product_price = float(Residential_name_and_price[i].split(';')[1])
        products = sf.query(
            f"SELECT Id FROM Product2 WHERE Name = '{product_name}'"
        )

        if not products['records']:
            print(product_name, "NOT FOUND")
            return

        products_id = products['records'][0]['Id']
        query = sf.query(
            f"SELECT Id FROM PricebookEntry WHERE Product2Id = '{products_id}' AND Pricebook2.Name = 'Residential'"
        )

        exist_pbe = query['records']

        if not exist_pbe:
            sf.PricebookEntry.create({
                'Pricebook2Id': Residential_existing_entry,
                'Product2Id': products_id,
                'UnitPrice': product_price,
                'IsActive': True
            })
        else:
            print(product_name, "exists")

    with ThreadPoolExecutor(max_workers=25) as executor:
        futures = [
            executor.submit(worker3, i)
            for i in range(len(Residential_name_and_price))
        ]

        for f in as_completed(futures):
            f.result()


def create_bundle():
    print('Start Bundle creation')
    smarphone_bundle_query_result = sf.query(f"select name, id from product2 where name like 'Smartphone Bundle Test'")
    if len(smarphone_bundle_query_result.get('records')) >= 1:
        print('Smartphone Bundle already created')
    else:
        print('Smartphone bundle to be created')
        Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
        rt_id = Rt_bundle_in_qurey['records'][0]['Id']
        print(f"Bundle Record Type id is {rt_id}")
        created_bundle_id = sf.product2.create({
            'Name': f'Smartphone Bundle Test',
            'RecordTypeId': rt_id,
            'IsActive': 'true'
        })
        created_bundle_id = sf.query(f"select name, id from product2 where name = 'Smartphone Bundle Test'")['records'][0]['Id']
        print(f'New ID of bundle is {created_bundle_id}\n Now lets create Features')

        try:
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

        except:
            pass      

# create_products()
# print('Product, Price Book and Price Book Entreis are created')
create_bundle()
print('Bundles are created')