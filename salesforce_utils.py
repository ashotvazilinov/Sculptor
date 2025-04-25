from simple_salesforce import Salesforce
import config

def connect_to_salesforce():
    """ Connecting to the Salesforce API. """
    return Salesforce(username=config.LOGIN, password=config.PASSWORD, security_token=config.SECURITY_TOKEN)

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


