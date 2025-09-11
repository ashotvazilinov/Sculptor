from simple_salesforce import Salesforce, SalesforceLogin, SFType
from datetime import datetime

session_id, instance = SalesforceLogin(
    username='test-yehcwneensgt@example.com',
    password='&ua5zlfhpgOmk',
    # security_token='тут_нужен_токен_если_IP_не_разрешен',
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
    for i in range(1, 6): 
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
        price = i  

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
            'Name': f'Test Quote {timestamp}',
            'SCLP__Pricebook__c': SPB_id,
            'SCLP__Account__c': Acc_id,
            'SCLP__Opportunity__c': Opp_id
            })
    existing_quote = f"select name, id from sclp__quote__c where name like 'test quote {timestamp}'"
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
            

create_products_and_pricebook_entries(sf)
print("Product added ended")
# delete_test_product_salesforce(sf)
# print("products deleted")
Standard_PriceBook_activation(sf)
print('PB ended')
create_account(sf)
print('account ended')
create_opportunity(sf)
print('Opportunity ended')
create_Quote(sf)
print('Quote ended')
just_test(sf)
print('done')
