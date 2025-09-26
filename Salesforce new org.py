from simple_salesforce import Salesforce, SalesforceLogin, SFType
from datetime import datetime
import time

session_id, instance = SalesforceLogin(
    # username='testin1g1233211234@gmail.com', #орг Артема
    # password='fsad534fsd',
    # security_token='eoVSG7DvEoLvOZxBzmBIlczL',
    # domain='test'
    username='test-vaslhuo2vcxg@example.com', #орг Димы
    password='fyiv0%czSxeac',
    # security_token='eoVSG7DvEoLvOZxBzmBIlczL',
    domain='test'
)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
print(timestamp)
sf = Salesforce(instance=instance, session_id=session_id)
print("Connected!")
# for element in dir(sf):
#     if not element.startswith('_'):
#         if isinstance(getattr(sf, element), str):
#             print('Poperty Name: {0} ; vale {1}'. format(element, getattr(sf, element)))

def create_products_and_pricebook_entries(sf):
    for i in range(1, 9): 
        product_name = f"Test Product {i}"
        existing_product  = sf.query(f"SELECT Id FROM Product2 WHERE Name = '{product_name}'")
        

        if existing_product.get('records'):
            print(f"Product '{product_name}' already exists. Skip creation.")
            continue
        
        product = sf.Product2.create({
            'Name': product_name,
            'IsActive': True
        })

        # Get standard PB id
        pricebook_id = None
        pricebook_entries = sf.query("SELECT Id, Name FROM Pricebook2 WHERE IsStandard = TRUE")
        for entry in pricebook_entries['records']:
            if entry['Name'] == 'Standard Price Book':
                pricebook_id = entry['Id']
                break

        if not pricebook_id:
            print("Standard Price Book not found!")
            continue

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

    print("Products and Pricebook Entries created successfully!")

def delete_test_product_salesforce(sf):
    print("Start Product Deleting...")
    for i in range(1, 6):
        query = f"SELECT Name, Id FROM Product2 WHERE Name = 'Test Product {i}'"
        results = sf.query(query) 
        while results.get('records'):
            for record in results['records']:
                product_id = record['Id']
                product_name = record['Name']

                try:
                    sf.Product2.delete(product_id) 
                    print(f"product Deleted '{product_name}' с ID {product_id}")
                except Exception as e:
                    print(f"Error deleting '{product_name}': {e}")

            if results.get('nextRecordsUrl'):
                results = sf.query_more(results['nextRecordsUrl'], True)
            else:
                break

    print("All product are deleted.")

def Standard_PriceBook_activation(sf):
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
def create_account(sf):
    print('Start creating account')
    abc = "select name, id from account where name = 'test account'"
    

    
    results = sf.query(abc)
    

    if results.get('records') and len(results['records']) > 0:
        print ('test account already exists')
    else:
        sf.account.create({'Name': 'Test Account'})
        print('test account is created')        

def create_opportunity(sf):
    print('Start creating Opportunity')
    Standard_Price_book_query = "select name, id from pricebook2 where name = 'Standard Price Book'"
    SPB_results = sf.query(Standard_Price_book_query)
    if SPB_results.get('records'):
        for PB in SPB_results['records']:
            SB_name = PB['Name']
            SPB_id = PB['Id']

            print(f"found {SB_name} with id: {SPB_id}")

    account_query = "select name, id from account where name = 'test account'"
    acc_results = sf.query(account_query)
    if acc_results.get('records'):
        for Accs in acc_results['records']:
            Acc_name = Accs['Name']
            Acc_id = Accs['Id']
            print(f'Account found with the name {Acc_name} with id: {Acc_id}')

    print('now it\'s about opportunity')
    opp = "select name, id from opportunity where name = 'test opportunity'"
    
    opp_results = sf.query(opp)

    

    if opp_results.get('records') and len(opp_results['records']) > 0:
        print ('test opportunity already exists')
    else:
        sf.opportunity.create({
            'Name': 'Test Opportunity',
            'CloseDate': '2025-09-04',
            'StageName': 'Qualification',
            'Pricebook2Id': SPB_id,
            'AccountId': Acc_id
            })
        print('test opportunity is created')          

def create_Quote(sf):
    print('Start creating Quote')
    Standard_Price_book_query = "select name, id from pricebook2 where name = 'Standard Price Book'"
    SPB_results = sf.query(Standard_Price_book_query)
    if SPB_results.get('records'):
        for PB in SPB_results['records']:
            SPB_name = PB['Name']
            SPB_id = PB['Id']

            print(f"found {SPB_name} with id: {SPB_id}")

    account_query = "select name, id from account where name = 'test account'"
    acc_results = sf.query(account_query)
    if acc_results.get('records'):
        for Accs in acc_results['records']:
            Acc_name = Accs['Name']
            Acc_id = Accs['Id']
            print(f'Account found with the name {Acc_name} with id: {Acc_id}')

    print('now it\'s about opportunity')
    opp = "select name, id from opportunity where name = 'test opportunity'"
    
    opp_results = sf.query(opp)

    

    if opp_results.get('records') and len(opp_results['records']) > 0:
        print ('test opportunity already exists')
    else:
        sf.opportunity.create({
            'Name': 'Test Opportunity',
            'CloseDate': '2025-09-04',
            'StageName': 'Qualification',
            'Pricebook2Id': SPB_id,
            'AccountId': Acc_id
            })
        print('test opportunity is created')          
    
    opp_query = "select name, id from opportunity where name like 'test opportunity%'"
    opp_results = sf.query(opp_query)
    if opp_results.get('records'):
        for opps in opp_results['records']:
            Opp_name = opps['Name']
            Opp_id = opps['Id']
            print(f'Opportunity found with the name {Opp_name} with id: {Opp_id}')

    print('now it\'s about opportunity')

    quote = "select name, id from sclp__quote__c where name like 'test quote%'"
    quote_result = sf.query(quote)

    if quote_result.get('records') and len(quote_result['records']) > 0:
        print ('test quote already exists')
    else:
        sf.sclp__quote__c.create({
            'Name': f'Test Quote Created {timestamp}',
            'SCLP__Pricebook__c': SPB_id,
            'SCLP__Account__c': Acc_id,
            'SCLP__Opportunity__c': Opp_id
            })
    existing_quote = f"select name, id from sclp__quote__c where name like 'test quote created {timestamp}'"
    existing_quote_result = sf.query(existing_quote)
    if existing_quote_result.get('records'):
        for q in existing_quote_result['records']:
            print(f"Quote '{q['Name']}' with ID {q['Id']} is created")
    else:
        print("No quotes found")
    
def just_test(sf):
    sf.product2.create({
        'Name': 'test pr',
        'IsActive': True
    })
    print('created')

    query = sf.query("select name, id, IsActive  from Product2 where name = 'test pr'")
    if query.get('records'):
        for i in query['records']:
            id_for_products = i['Id']
            sf.product2.delete(id_for_products)
    print('deleted')
            

def delete_all_quotes(sf):
    quotes_query = sf.query("select id from sclp__quote__c")
    while quotes_query.get('records'):
        for record in quotes_query['records']:
            sf.sclp__quote__c.delete(record['Id'])

def create_bundle(sf):
    print('Start Bundle creation')
    bundle_query_result = sf.query("select name, id from product2 where name like 'Test Bundle created%'")
    if len(bundle_query_result.get('records', [])) >= 1:
        print('Bundle already created')
    else:
        print('bundle to be created')
        Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
        rt_id = Rt_bundle_in_qurey['records'][0]['Id']
        print(f"Bundle Record Type id is {rt_id}")
        sf.product2.create({
            'Name': f'Test Bundle Created {timestamp}',
            'RecordTypeId': f'{rt_id}',
            'IsActive': 'true'
        })
        created_bundle_id = sf.query("select name, id from product2 where name like 'Test Bundle created%'")['records'][0]['Id']
        print(f'New ID of bundle is {created_bundle_id}\n Now lets create Features')

        sf.SCLP__ProductFeature__c.create({
            'Name': 'We are number one',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'true',
            'SCLP__Order__c': '1',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'false'
        })
        sf.SCLP__ProductFeature__c.create({
            'Name': 'Number two',
            'SCLP__HasGroup__c': 'false',
            'SCLP__Multiple__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': created_bundle_id,
            'SCLP__Required__c': 'true'
        })
        first_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 1 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'first feature id is {first_feature_id}')
        second_feature_id = sf.query(f"select id from SCLP__ProductFeature__c where SCLP__Order__c = 2 and SCLP__Product__c = '{created_bundle_id}'")['records'][0]['Id']
        print(f'second feature id is {second_feature_id}\n Now lets create options')
        product1_id = sf.query(f"select id from product2 where name = 'Test Product 1'")['records'][0]['Id']
        product2_id = sf.query(f"select id from product2 where name = 'Test Product 2'")['records'][0]['Id']
        product3_id = sf.query(f"select id from product2 where name = 'Test Product 3'")['records'][0]['Id']
        product4_id = sf.query(f"select id from product2 where name = 'Test Product 4'")['records'][0]['Id']
        product5_id = sf.query(f"select id from product2 where name = 'Test Product 5'")['records'][0]['Id']
        product6_id = sf.query(f"select id from product2 where name = 'Test Product 6'")['records'][0]['Id']
        product7_id = sf.query(f"select id from product2 where name = 'Test Product 7'")['records'][0]['Id']
        product8_id = sf.query(f"select id from product2 where name = 'Test Product 8'")['records'][0]['Id']


        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product1_id,
            'SCLP__ChildRequired__c': 'true'
        })
        option1_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 1'")['records'][0]['Id']

        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__ChildRequired__c': 'false',
            'SCLP__DefaultOption__c': 'false',
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product2_id,
            'SCLP__MasterOption__c': option1_id 
        })
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': first_feature_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product3_id
        })
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': second_feature_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product4_id
        })
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Feature__c': second_feature_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product5_id,
            'SCLP__DefaultOption__c': 'true'
        })
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product6_id,
            'SCLP__DefaultOption__c': 'true'
        })
        print('option 6 created')
        option6_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 6'")['records'][0]['Id']
        print('query for 6 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '1',
            'SCLP__Product__c': product7_id,
            'SCLP__DefaultOption__c': 'true',
            'SCLP__MasterOption__c': option6_id
        })
        print('option 7 created')
        option7_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 7'")['records'][0]['Id']
        print('query for 7 worked out')
        sf.SCLP__ProductOption__c.create({
            'SCLP__BundleQuantity__c': '1',
            'SCLP__Bundle__c': created_bundle_id,
            'SCLP__Order__c': '2',
            'SCLP__Product__c': product8_id,
            'SCLP__DefaultOption__c': 'false',
        })
        print('option 8 created')




def delete_bundle(sf):
    print('Start Bundle deletion')


    options = sf.query("SELECT Id, SCLP__Product__r.Name, SCLP__Bundle__r.Name FROM SCLP__ProductOption__c WHERE SCLP__Bundle__r.name LIKE 'Test Bundle created%' ORDER BY SCLP__Product__r.name DESC")
    
    for o in options['records']:
        try:
            sf.SCLP__ProductOption__c.delete(o['Id'])
            product_name = o.get('SCLP__Product__r', {}).get('Name', 'N/A')
            print(f"Deleted option for product: {product_name} with Id {o['Id']}")
        except Exception as e:
            product_name = o.get('SCLP__Product__r', {}).get('Name', 'N/A')
            print(f"Failed to delete option for product {product_name} ({o['Id']}): {e}")

    bundles = sf.query("SELECT Name, Id FROM Product2 WHERE Name LIKE 'Test Bundle created%'")
    if bundles['records']:
        for b in bundles['records']:
            try:
                sf.Product2.delete(b['Id'])
                print(f"Deleted bundle: {b['Name']} ({b['Id']})")
            except Exception as e:
                print(f"Error deleting bundle: {e}")
    else:
        print("No bundles to delete")

    


# create_products_and_pricebook_entries(sf)
# print("Product added ended")
# delete_test_product_salesforce(sf)
# print("products deleted")
# Standard_PriceBook_activation(sf)
# print('PB ended')
# create_account(sf)
# print('account ended')
# create_opportunity(sf)
# print('Opportunity ended')
# create_Quote(sf)
# print('Quote ended')
# # just_test(sf)
# # print('done')
# # delete_all_quotes(sf)
# # print('all quotes deleted')
delete_bundle(sf)
print('Bundle deleted')
create_bundle(sf)
print("bundle ended")