# salesforce_utils.py
from simple_salesforce import Salesforce
import config

def connect_to_salesforce():
    """ Connecting to the Salesforce API. """
    return Salesforce(username=config.LOGIN, password=config.PASSWORD, security_token=config.SECURITY_TOKEN, domain=config.DOMAIN)
def delete_test_bundles_salesforce(sf, unique_number: int):
    """ Deletes test bundles from Salesforce. """
    print("Start Bundle Deleting...")

    query = f"SELECT Name, Id FROM Product2 WHERE Name = 'Test Bundle to be deleted {unique_number}'"
    results = sf.query(query) 

    while results.get('records'):
        for record in results['records']:
            product_id = record['Id']
            product_name = record['Name']

            try:
                sf.Product2.delete(product_id)
                print(f"Bundle is deleted '{product_name}' with ID {product_id}")
            except Exception as e:
                print(f"Error deleting '{product_name}': {e}")

        if results.get('nextRecordsUrl'):
            results = sf.query_more(results['nextRecordsUrl'], True)
        else:
            break

    print("All Bundles are deleted.")


def delete_test_opportunity_salesforce(sf, unique_number: int):
    print("Start Opportunity Deleting...")

    query = f"SELECT Name, Id FROM Opportunity WHERE Name = 'Test opportunity to be deleted {unique_number}'"
    results = sf.query(query)
    while results.get('records'):
        for record in results['records']:
            opportunity_id = record['Id']
            opportunity_name = record['Name']

            try:
                sf.Opportunity.delete(opportunity_id) 
                print(f"Opportunity Deleted '{opportunity_name}' с ID {opportunity_id}")
            except Exception as e:
                print(f"Error deleting '{opportunity_name}': {e}")

        if results.get('nextRecordsUrl'):
            results = sf.query_more(results['nextRecordsUrl'], True)
        else:
            break

    print("All Opportunities are deleted.")

def delete_test_quote_salesforce(sf, unique_number: int):
    print("Start Quote Deleting...")

    query = f"SELECT Name, Id FROM SCLP__Quote__c WHERE Name = 'Test quote to be deleted {unique_number}'"
    results = sf.query(query) 
    while results.get('records'):
        for record in results['records']:
            quote_id = record['Id']
            quote_name = record['Name']

            try:
                sf.SCLP__Quote__c.delete(quote_id) 
                print(f"Quote Deleted '{quote_name}' с ID {quote_id}")
            except Exception as e:
                print(f"Error deleting '{quote_name}': {e}")

        if results.get('nextRecordsUrl'):
            results = sf.query_more(results['nextRecordsUrl'], True)
        else:
            break

    print("All Quote are deleted.")

def create_products_and_pricebook_entries(sf, unique_number: int):
    for i in range(1, 5): 
        product_name = f"Test Product to be deleted {i}"
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

