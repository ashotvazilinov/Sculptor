from simple_salesforce import Salesforce, SalesforceLogin, SalesforceError
from datetime import datetime

session_id, instance = SalesforceLogin(

    username='test-cgvyjwv2fuev@example.com', 
    password='[admufwjcI7jd',
    security_token='iFSgmj5ero4xMjk5U9PGYHT2',
    domain='test' 
)
sf = Salesforce(instance=instance, session_id=session_id)
print("Connected!")
# git add .

# git commit -m "changed smth"

# git push origin HEAD:main

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
print(timestamp)

# for element in dir(sf):
#     if not element.startswith('_'):
#         if isinstance(getattr(sf, element), str):
#             print('Poperty Name: {0} ; vale {1}'. format(element, getattr(sf, element)))
product_qty = 10
def create_products_and_pricebook_entries(sf):
    for i in range(1, product_qty): 
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
    for i in range(1, product_qty):
        query = f"SELECT Name, Id FROM Product2 WHERE Name = 'Test Product {i}'"
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
    account_created = "select name, id from account where name like 'test account created %'"
    

    
    results = sf.query(account_created)
    

    if results.get('records') and len(results['records']) > 0:
        print ('test account already exists')
    else:
        sf.account.create({'Name': f'Test Account created {timestamp}'})
        print('test account is created') 
    sf.contact.create({
        'FirstName': 'Test First Name',
        'LastName': f'Test Last Name Created {timestamp}',
        'AccountId': sf.query(f"select id from account where name = 'Test Account created {timestamp}'")['records'][0]['Id']    
        #'Product__c':  sf.query(f"select id from product2 where name = 'Test Product {i}'")['records'][0]['Id'],
    })
    print('test contact is created')
    contact_query = f"SELECT Id, FirstName, LastName from Contact where LastName like 'Test Last Name Created {timestamp}'"
    print(f"test contact {sf.query(contact_query)['records'][0]['LastName']} is created")
def create_opportunity(sf):
    print('Start creating Opportunity')
    Standard_Price_book_query = "select name, id from pricebook2 where name = 'Standard Price Book'"
    SPB_results = sf.query(Standard_Price_book_query)
    if SPB_results.get('records'):
        for PB in SPB_results['records']:
            SB_name = PB['Name']
            SPB_id = PB['Id']

            print(f"found {SB_name} with id: {SPB_id}")

    account_query = "select name, id from account where name like 'test account created %'"
    acc_results = sf.query(account_query)
    if acc_results.get('records'):
        for Accs in acc_results['records']:
            Acc_name = Accs['Name']
            Acc_id = Accs['Id']
            print(f'Account found with the name {Acc_name} with id: {Acc_id}')

    print('now it\'s about opportunity')
    opp = "select name, id from opportunity where name like 'test opportunity created%'"
    
    opp_results = sf.query(opp)

    

    if opp_results.get('records') and len(opp_results['records']) > 0:
        print ('test opportunity already exists')
    else:
        sf.opportunity.create({
            'Name': f'Test Opportunity created {timestamp}',
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

    account_query = "select name, id from account where name like 'test account created %'"
    acc_results = sf.query(account_query)
    if acc_results.get('records'):
        for Accs in acc_results['records']:
            Acc_name = Accs['Name']
            Acc_id = Accs['Id']
            print(f'Account found with the name {Acc_name} with id: {Acc_id}')

    print('now it\'s about opportunity')
    opp = "select name, id from opportunity where name like 'test opportunity created %'"
    
    opp_results = sf.query(opp)

    

    if opp_results.get('records') and len(opp_results['records']) > 0:
        print ('test opportunity already exists')
    else:
        sf.opportunity.create({
            'Name': f'Test Opportunity Created {timestamp}',
            'CloseDate': '2025-09-04',
            'StageName': 'Qualification',
            'Pricebook2Id': SPB_id,
            'AccountId': Acc_id
            })
        print('test opportunity is created')          
    
    opp_query = "select name, id from opportunity where name like 'test opportunity created %'"
    opp_results = sf.query(opp_query)
    if opp_results.get('records'):
        for opps in opp_results['records']:
            Opp_name = opps['Name']
            Opp_id = opps['Id']
            print(f'Opportunity found with the name {Opp_name} with id: {Opp_id}')

    print('now it\'s about opportunity')

    try:
        quote = "select name, id from sclp__quote__c where name like 'test quote created%'"
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
    except SalesforceError as e:
        "INVALID_TYPE" in str(e)
        print("no SCLP__")
        quote = "select name, id from quote__c where name like 'test quote created %' AND (NOT Name LIKE '%number%')"
        quote_result = sf.query(quote)

        if quote_result.get('records') and len(quote_result['records']) > 0:
            print ('test quote already exists')
        else:
            sf.quote__c.create({
                'Name': f'Test Quote Created {timestamp}',
                'Pricebook__c': SPB_id,
                'Account__c': Acc_id,
                'Opportunity__c': Opp_id
                })
        existing_quote = f"select name, id from quote__c where name like 'test quote created {timestamp}'"
        existing_quote_result = sf.query(existing_quote)
        if existing_quote_result.get('records'):
            for q in existing_quote_result['records']:
                print(f"Quote '{q['Name']}' with ID {q['Id']} is created")
        else:
            print("No quotes found")

    
            

def delete_all_quotes(sf):
    try:
        quotes_query = sf.query("select id, name from sclp__quote__c")
        while quotes_query.get('records'):
            for record in quotes_query['records']:
                sf.sclp__quote__c.delete(record['Id'])
                print(f"Deleted quote with ID: {record['Id']} with name {record['Name']}")
                quotes_query = sf.query("select id from sclp__quote__c where isDeleted = false")
    except SalesforceError as e:
        "INVALID_TYPE" in str(e)
        print("no SCLP__")
        quotes_query = sf.query("select id, name from quote__c")
        while quotes_query.get('records'):
            for record in quotes_query['records']:
                sf.quote__c.delete(record['Id'])
                print(f"Deleted quote with ID: {record['Id']} with name {record['Name']}")
                quotes_query = sf.query("select id from quote__c where isDeleted = false")
        
def create_bundle(sf):
    print('Start Bundle creation')
    bundle_query_result = sf.query("select name, id from product2 where name like 'Test Bundle created%'")
    if len(bundle_query_result.get('records')) >= 1:
        print('Bundle already created')
    else:
        print('bundle to be created')
        Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
        rt_id = Rt_bundle_in_qurey['records'][0]['Id']
        print(f"Bundle Record Type id is {rt_id}")
        sf.product2.create({
            'Name': f'Test Bundle Created {timestamp}',
            'RecordTypeId': rt_id,
            'IsActive': 'true'
        })
        created_bundle_id = sf.query("select name, id from product2 where name like 'Test Bundle created%'")['records'][0]['Id']
        print(f'New ID of bundle is {created_bundle_id}\n Now lets create Features')
        try:
            sf.SCLP__ProductFeature__c.create({
                'Name': 'We are number one',
                'SCLP__HasGroup__c': 'false',
                'SCLP__Multiple__c': 'true',
                'SCLP__Order__c': '1',
                'SCLP__Product__c': created_bundle_id,
                'SCLP__Required__c': 'false',
                'SCLP__Tip__c': 'https://www.youtube.com/watch?v=PfYnvDL0Qcw&list=RDPfYnvDL0Qcw'
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
                'SCLP__ChildRequired__c': 'true',
                'SCLP__Tip__c': 'Tip test 1',
                'SCLP__HideInQuote__c': True
            })
            option1_id = sf.query(f"select id from SCLP__ProductOption__c where SCLP__Product__r.name = 'Test Product 1'")['records'][0]['Id']
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
            sf.SCLP__ProductOption__c.create({
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__Feature__c': second_feature_id,
                'SCLP__Order__c': '2',
                'SCLP__Product__c': product5_id,
                'SCLP__DefaultOption__c': 'true',
                'SCLP__Tip__c': 'Tip test 5'
            })
            print('Options 5 is created')

            sf.SCLP__ProductOption__c.create({
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__Order__c': '1',
                'SCLP__Product__c': product6_id,
                'SCLP__DefaultOption__c': 'true',
                'SCLP__Tip__c': 'Tip test 6'
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
            for i in range(9, product_qty):
                sf.SCLP__ProductOption__c.create({
                'SCLP__BundleQuantity__c': '1',
                'SCLP__Bundle__c': created_bundle_id,
                'SCLP__Order__c': i,
                'SCLP__Product__c':  sf.query(f"select id from product2 where name = 'Test Product {i}'")['records'][0]['Id'],
                'SCLP__DefaultOption__c': 'false',
                'SCLP__Tip__c': f'Tip test {i}'
                })
                print(f'option {i} created')

        except SalesforceError as e:
            "INVALID_TYPE" in str(e)
            print("no SCLP__")
            sf.ProductFeature__c.create({
                'Name': 'We are number one',
                'HasGroup__c': 'false',
                'Multiple__c': 'true',
                'Order__c': '1',
                'Product__c': created_bundle_id,
                'Required__c': 'false',
                'Tip__c': 'https://www.youtube.com/watch?v=PfYnvDL0Qcw&list=RDPfYnvDL0Qcw'
            })
            first_feature_id = sf.query(f"select id from ProductFeature__c where Order__c = 1 and Product__c = '{created_bundle_id}'")['records'][0]['Id']
            print(f'first feature id is {first_feature_id}')
            sf.ProductFeature__c.create({
                'Name': 'Number two',
                'HasGroup__c': 'false',
                'Multiple__c': 'false',
                'Order__c': '2',
                'Product__c': created_bundle_id,
                'Required__c': 'true',
                'Tip__c': 'Feature Number two tip'
            })

            second_feature_id = sf.query(f"select id from ProductFeature__c where Order__c = 2 and Product__c = '{created_bundle_id}'")['records'][0]['Id']
            print(f'second feature id is {second_feature_id}\n Now lets create options')
            product1_id = sf.query(f"select id from product2 where name = 'Test Product 1'")['records'][0]['Id']
            product2_id = sf.query(f"select id from product2 where name = 'Test Product 2'")['records'][0]['Id']
            product3_id = sf.query(f"select id from product2 where name = 'Test Product 3'")['records'][0]['Id']
            product4_id = sf.query(f"select id from product2 where name = 'Test Product 4'")['records'][0]['Id']
            product5_id = sf.query(f"select id from product2 where name = 'Test Product 5'")['records'][0]['Id']
            product6_id = sf.query(f"select id from product2 where name = 'Test Product 6'")['records'][0]['Id']
            product7_id = sf.query(f"select id from product2 where name = 'Test Product 7'")['records'][0]['Id']
            product8_id = sf.query(f"select id from product2 where name = 'Test Product 8'")['records'][0]['Id']

            sf.ProductOption__c.create({
                'BundleQuantity__c': '1',
                'Bundle__c': created_bundle_id,
                'DefaultOption__c': 'false',
                'Feature__c': first_feature_id,
                'Order__c': '1',
                'Product__c': product1_id,
                'ChildRequired__c': 'true',
                'Tip__c': 'Tip test 1',
                'HideInQuote__c': True
            })
            option1_id = sf.query(f"select id from ProductOption__c where Product__r.name = 'Test Product 1'")['records'][0]['Id']
            print('Options 1 is created')
            sf.ProductOption__c.create({
                'BundleQuantity__c': '1',
                'Bundle__c': created_bundle_id,
                'ChildRequired__c': 'false',
                'DefaultOption__c': 'false',
                'Order__c': '2',
                'Product__c': product2_id,
                'MasterOption__c': option1_id,
                'Tip__c': 'Tip test 2',
                'HideInQuote__c': True
            })
            print('Options 2 is created')

            sf.ProductOption__c.create({
                'BundleQuantity__c': '1',
                'Bundle__c': created_bundle_id,
                'Feature__c': first_feature_id,
                'Order__c': '2',
                'Product__c': product3_id,
                'Tip__c': 'Tip test 3'
            })
            print('Options 3 is created')

            sf.ProductOption__c.create({
                'BundleQuantity__c': '1',
                'Bundle__c': created_bundle_id,
                'Feature__c': second_feature_id,
                'Order__c': '1',
                'Product__c': product4_id,
                'Tip__c': 'Tip test 4'
            })
            print('Options 4 is created')
            sf.ProductOption__c.create({
                'BundleQuantity__c': '1',
                'Bundle__c': created_bundle_id,
                'Feature__c': second_feature_id,
                'Order__c': '2',
                'Product__c': product5_id,
                'DefaultOption__c': 'true',
                'Tip__c': 'Tip test 5'
            })
            print('Options 5 is created')

            sf.ProductOption__c.create({
                'BundleQuantity__c': '1',
                'Bundle__c': created_bundle_id,
                'Order__c': '1',
                'Product__c': product6_id,
                'DefaultOption__c': 'true',
                'Tip__c': 'Tip test 6'
            })
            print('option 6 created')
            option6_id = sf.query(f"select id from ProductOption__c where Product__r.name = 'Test Product 6'")['records'][0]['Id']
            print('query for 6 worked out')
            sf.ProductOption__c.create({
                'BundleQuantity__c': '1',
                'Bundle__c': created_bundle_id,
                'Order__c': '1',
                'Product__c': product7_id,
                'DefaultOption__c': 'true',
                'MasterOption__c': option6_id,
                'Tip__c': 'Tip test 7',
                'BundleQuantity__c': ''
            })
            print('option 7 created')
            print('query for 7 worked out')
            sf.ProductOption__c.create({
                'BundleQuantity__c': '1',
                'Bundle__c': created_bundle_id,
                'Order__c': '2',
                'Product__c': product8_id,
                'DefaultOption__c': 'false',
                'Tip__c': 'Tip test 8'
            })
            print('option 8 created')
            for i in range(9, product_qty):
                sf.ProductOption__c.create({
                'BundleQuantity__c': '1',
                'Bundle__c': created_bundle_id,
                'Order__c': i,
                'Product__c':  sf.query(f"select id from product2 where name = 'Test Product {i}'")['records'][0]['Id'],
                'DefaultOption__c': 'false',
                'Tip__c': f'Tip test {i}'
                  })
                print(f'option {i} created')

def delete_bundle(sf):
    print('Start Bundle deletion')

    try:
        options = sf.query("SELECT Id, SCLP__Product__r.Name, SCLP__Bundle__r.Name FROM SCLP__ProductOption__c WHERE SCLP__Bundle__r.name LIKE 'Test Bundle created%' ORDER BY SCLP__Product__r.name DESC")
        
        for o in options['records']:
            try:
                sf.SCLP__ProductOption__c.delete(o['Id'])
                product_name = o['SCLP__Product__r']['Name']
                print(f"Deleted option for product: {product_name} (ID: {o['Id']})")
            except Exception as e:
                product_name = o['SCLP__Product__r']['Name']
                print(f"Failed to delete option for product {product_name} (ID: {o['Id']}): {e}")

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
    except SalesforceError as e:
        "INVALID_TYPE" in str(e)
        print("no SCLP__")
        options = sf.query("SELECT Id, Product__r.Name, Bundle__r.Name FROM ProductOption__c WHERE Bundle__r.name LIKE 'Test Bundle created%' ORDER BY Product__r.name DESC")
        
        for o in options['records']:
            try:
                sf.ProductOption__c.delete(o['Id'])
                product_name = o['Product__r']['Name']
                print(f"Deleted option for product: {product_name} (ID: {o['Id']})")
            except Exception as e:
                product_name = o['Product__r']['Name']
                print(f"Failed to delete option for product {product_name} (ID: {o['Id']}): {e}")

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

def Community_Cost_Price_enabling(sf):
    print('Now its about Cost Price')
    try:
        record = sf.query("SELECT Id FROM SCLP__ProductCostPrice__c LIMIT 1")['records'][0]
        print(record)
        sf.SCLP__ProductCostPrice__c.update(record['Id'], {
            'CommunityCostPriceEnabled__c': True
        })
        print("Updated successfully!")
    except SalesforceError as e:
        "INVALID_TYPE" in str(e)
        print("no SCLP__")
        record = sf.query("SELECT Id FROM ProductCostPrice__c LIMIT 1")['records'][0]
        print(record)
        sf.ProductCostPrice__c.update(record['Id'], {
            'CommunityCostPriceEnabled__c': True
        })
        print("Updated successfully!")
def create_multiple_quotes(sf):
    print('Start creating Multiple Quotes')
    Standard_Price_book_query = sf.query("select name, id from pricebook2 where name = 'Standard Price Book'")['records'][0]
    print(f"pricebook {Standard_Price_book_query['Name']} with id {Standard_Price_book_query['Id']} is found")
    account_query = sf.query("select name, id from account where name like 'test account created %'")['records'][0]
    # opp = sf.query("select name, id from opportunity where name like 'test opportunity created %'")['records'][0]
    print('queries ended')
    try:
        for i in range(1, product_qty):
            sf.sclp__quote__c.create({
                'Name': f'Test Quote Created Number {i} {timestamp}',
                # 'SCLP__Opportunity__c': opp['Id'],
                'SCLP__Pricebook__c': Standard_Price_book_query['Id'],
                'SCLP__Account__c': account_query['Id'],
                'OwnerId': '005RR00000FyXgxYAF'


                })
            print(f'Quote number {i} is created')
    except SalesforceError as e:
        "INVALID_TYPE" in str(e)
        print("no SCLP__")
        for i in range(1, product_qty):
            sf.quote__c.create({
                'Name': f'Test Quote Created Number {i} {timestamp}',
                # 'Opportunity__c': opp['Id'],
                'Pricebook__c': Standard_Price_book_query['Id'],
                'Account__c': account_query['Id'],


                })
            print(f'Quote number {i} is created')



def create_test_acc_field(sf):
    field_metadata = {
        'FullName': 'Account.Test_acc__c',
        'Metadata': {
            'label': 'Test acc 3',
            'length': 255,
            'type': 'Text',
            'description': 'Тестовое поле созданное через Tooling API'
        }
    }
    

    result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=field_metadata)
    print("✅ Поле Test_acc успешно создано на объекте Account!")
    print(f"Результат: {result}")


# create_products_and_pricebook_entries(sf)
# print("Product added ended")
# # # # delete_test_product_salesforce(sf)
# # # # print("products deleted")
# Standard_PriceBook_activation(sf)
# print('PB ended')
# create_account(sf)
# print('account ended')
# create_opportunity(sf)
# print('Opportunity ended')
# create_Quote(sf)
# print('Quote ended')
# delete_all_quotes(sf)
# print('all quotes deleted')
# delete_bundle(sf)
# print('Bundle deleted')
create_bundle(sf)
print("bundle ended")
# Community_Cost_Price_enabling(sf)
# print('Cost Price enabled')
# create_multiple_quotes(sf)
# print('Multiple Quotes created')
# create_test_acc_field(sf)
# print('field ended')