from simple_salesforce import Salesforce, SalesforceLogin, SalesforceError, SalesforceMalformedRequest
from datetime import datetime
import random
import time
import config
from playwright.sync_api import sync_playwright, expect, Page
from concurrent.futures import ThreadPoolExecutor, as_completed

USERNAME='test-zw54isibqvak@example.com'
PASSWORD='ttyk|ate6Dnpw'
SECURITE_TOKEN='VSu5W89l5JnP1XjQ2rlXYrSS'
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

RECORDS_QTY = 400
def permission_set_creation():
    # 1. Create Permission Set
    perm_set_data = {
        "Name": "SO_Sculptor_permission_set",
        "Label": "SO Sculptor Permission Set",
        "Description": "SO Sculptor Permission Set created with Python because I can",
        "LicenseId": None  # if you want to assign a licence, you can fill it
    }

    try:
        sf.PermissionSet.create(perm_set_data) #creating perm set
        print('Permission Set is created')
    except SalesforceError as e:
        "DUPLICATE_DEVELOPER_NAME" in str(e)
        print('There is already the SO Sculptor Permission Set')
        
    permission_set_id = sf.query("SELECT Id FROM PermissionSet WHERE Name = 'SO_Sculptor_permission_set'")["records"][0]["Id"] #get Permission Set ID
    # print(sf.query("SELECT Id FROM PermissionSet WHERE Name = 'SO_Sculptor_permission_set'"))
    if permission_set_id == None:
        print('No Permission Set Id is taken')
        raise
    else:
        print(f"✅ Permission Set 'SO Sculptor Permission Set' is created (Id: {permission_set_id})")

    # 2. Taking active Users
    users = sf.query("SELECT Id, Name FROM User WHERE IsActive = true and (Email like '%twistellar%' or LastName like '%site%')")['records']
    print(f"👥 Active Users QTY is: {len(users)}")

    # 3. Assigning permission sets to all users
    assigned_users = 0
    not_assigned_users = 0
    for u in users:
        try:
            sf.PermissionSetAssignment.create({
                "AssigneeId": u["Id"],            # to whom
                "PermissionSetId": permission_set_id  # what is assigned
            })
            print(f"✅ Assigned to User {u['Name']} ({u['Id']})")
            assigned_users += 1
        except Exception as e:
            print(f"⚠️ Error assigning {u['Name']}: {e}")
            not_assigned_users += 1

    if not_assigned_users == 0:
        print(f"🎉 {assigned_users} users are assigned Permission Set 'SO Sculptor Permission Set'")
    else:
        print(f"🤢 {not_assigned_users} users are NOT assigned Permission Set 'SO Sculptor Permission Set'")

def create_fields():
    try: 
        object_name = ['Product2', 'SCLP__Quote__c', 'SCLP__QuoteLineItem__c']
        ps_query = "SELECT Id FROM PermissionSet WHERE Name = 'SO_Sculptor_permission_set'"
        ps_result = sf.query(ps_query)
        permission_set_id = ps_result['records'][0]['Id']
        print(f"✅ Found Permission Set 'test' (Id: {permission_set_id})")
        for x in object_name:
            print(f'Start creating {x} fields')

            
        #'''autonumber'''
            try:
                autonumber_field_metadata = {
                'FullName': f'{x}.test_Auto_Number__c',
                'Metadata': {
                    'label': 'Test Auto Number',
                    'type': 'AutoNumber',
                    'displayFormat': 'Python-{0000}',
                    'startingNumber': 1,
                    'description': 'Field created with Python',
                    # 'updateExistingRecords': True
                }
            }

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=autonumber_field_metadata)
                print(f"✅ AutoNumber field created for {x}!")
                print(f"Result is: {result}")

                Autonumber_field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Auto_Number__c',
                    'PermissionsRead': True,
                }

                result = sf.FieldPermissions.create(Autonumber_field_perm_data)
                print("✅ Auto Number is added for read Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
                #except ind
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Auto Number field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise
        #'''Formula'''
            try:
                if x == 'Product2':
                    formula_field_metadata = {
                        "FullName": f"{x}.test_Formula__c",
                        "Metadata": {
                            "label": "Test Formula",
                            "type": "Number",
                            "precision": 18,
                            "scale": 0,
                            "formula": 'VALUE(RIGHT(Name, LEN(Name) - FIND("Test Product ", Name) - 12))',         
                            "description": "Number field that shows Test Product's number"
                        }
                    }
                else:
                    formula_field_metadata = {
                        "FullName": f"{x}.test_Formula__c",
                        "Metadata": {
                            "label": "Test Formula",
                            "type": "Number",
                            "precision": 18,
                            "scale": 0,
                            "formula": '1',        
                            "description": "just one"
                            }}

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=formula_field_metadata)
                print("✅ Formula field created")
                print(result)
                formula_field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Formula__c',
                    'PermissionsRead': True,
                }

                result = sf.FieldPermissions.create(formula_field_perm_data)
                print("✅ Formula is added for read Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Formula field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise
        #'''checkbox'''
            try:
                checkbox_field_metadata = {
                    'FullName': f'{x}.test_Checkbox__c',
                    'Metadata': {
                        'label': 'Test Checkbox',
                        'type': 'Checkbox',
                        'defaultValue': False,
                        'description': 'Field created with Python'
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=checkbox_field_metadata)
                print(f"✅ Field checkbox is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Checkbox__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Checkbox is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Checkbox field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise
        #'''Currency'''
            try:
                currency_field_metadata = {
                    'FullName': f'{x}.test_Currency__c',
                    'Metadata': {
                        "label": "Test Currency",
                        "type": "Currency",
                        "precision": 18,
                        "scale": 2,
                        "description": "Description Test currency"
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=currency_field_metadata)
                print(f"✅ Field currency is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Currency__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Currency is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Currency field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise

        #'''Date'''
            try:
                Date_field_metadata = {
                    'FullName': f'{x}.test_Date__c',
                    'Metadata': {
                        "label": "Test Date",
                        "type": "Date",
                        "description": "Description Test Date"
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Date_field_metadata)
                print(f"✅ Field Date is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Date__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Date is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Date field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise  
        #'''DateTime'''
            try:
                DateTime_field_metadata = {
                    'FullName': f'{x}.test_DateTime__c',
                    'Metadata': {
                        "label": "Test DateTime",
                        "type": "DateTime",
                        "description": "Description Test DateTime"
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=DateTime_field_metadata)
                print(f"✅ Field DateTime is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_DateTime__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ DateTime is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Date Time field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise

        #'''Email'''
            try:
                Email_field_metadata = {
                    'FullName': f'{x}.test_Email__c',
                    'Metadata': {
                        "label": "Test Email",
                        "type": "Email",
                        "description": "Description Test Email",
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Email_field_metadata)
                print(f"✅ Field Email is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Email__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Email is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Email field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise
            
        #'''Number'''
            try:
                Number_field_metadata = {
                    'FullName': f'{x}.test_Number__c',
                    'Metadata': {
                        "label": "Test Number",
                        "type": "Number",
                        "precision": 18,
                        "scale": 2,
                        "description": "Description Test Number"
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Number_field_metadata)
                print(f"✅ Field Number is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Number__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Number is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Number field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise
        #'''Percent'''
            try:
                Percent_field_metadata = {
                    'FullName': f'{x}.test_Percent__c',
                    'Metadata': {
                        "label": "Test Percent",
                        "type": "Percent",
                        "precision": 18,
                        "scale": 2,
                        "description": "Description Test Percent"
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Percent_field_metadata)
                print(f"✅ Field Percent is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Percent__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Percent is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Percent field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise

        #'''Phone'''
            try:
                Phone_field_metadata = {
                    'FullName': f'{x}.test_Phone__c',
                    'Metadata': {
                        "label": "Test Phone",
                        "type": "Phone",
                        "description": "Description Test Phone"
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Phone_field_metadata)
                print(f"✅ Field Phone is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Phone__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Phone is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Phone field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise
        #'''Picklist'''
            try:
                Picklist_field_metadata = {
                    'FullName': f'{x}.test_Picklist__c',
                    'Metadata': {
                        "label": "Test Picklist",
                        "type": "Picklist",
                        "description": "Description Test Picklist",
                        'valueSet': {
                            'valueSetDefinition': {
                                'sorted': False,
                                'value': [
                                    {'fullName': '1', 'default': False, 'label': '1'},
                                    {'fullName': '2', 'default': False, 'label': '2'},
                                    {'fullName': '3', 'default': False, 'label': '3'}
                                ]
                            },
                            'restricted': True
                        
                    }
                }}
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Picklist_field_metadata)
                print(f"✅ Field Picklist is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Picklist__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Picklist is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Picklist field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise

        #'''Multi Picklist'''
            try:
                Multi_Picklist_field_metadata = {
                    'FullName': f'{x}.test_Multi_Picklist__c',
                    'Metadata': {
                        "label": "Test Multi Picklist",
                        "type": "MultiselectPicklist",
                        'required': False,
                        'visibleLines': 5,
                        "description": "Description Test Multi Picklist",
                        'valueSet': {
                            'valueSetDefinition': {
                                'sorted': False,
                                'value': [
                                    {'fullName': 'one', 'default': False, 'label': 'one'},
                                    {'fullName': 'two', 'default': False, 'label': 'two'},
                                    {'fullName': 'three', 'default': False, 'label': 'three'}
                                ]
                            },
                            'restricted': True
                        
                    }
                }}
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Multi_Picklist_field_metadata)
                print(f"✅ Field Multi Picklist is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Multi_Picklist__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Multi Picklist is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Multi Picklist field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise
        #'''Text'''
            try:
                Text_field_metadata = {
                    'FullName': f'{x}.test_Text__c',
                    'Metadata': {
                        'label': 'Test Text',
                        'length': 255,
                        'type': 'Text',
                        "description": "Description Test Text"
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Text_field_metadata)
                print(f"✅ Field Text is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Text__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Text is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Text field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise
        #'''Text_Area'''
            try:
                Text_Area_field_metadata = {
                    'FullName': f'{x}.test_Text_Area__c',
                    'Metadata': {
                        'label': 'Test Text Area',
                        'type': 'TextArea',
                        "description": "Description Test Text Area"
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Text_Area_field_metadata)
                print(f"✅ Field Text Area is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Text_Area__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Text Area is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Text Area field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise
        #'''Text_Area_Long'''
            try:
                Text_Area_Long_field_metadata = {
                    'FullName': f'{x}.test_Text_Area_Long__c',
                    'Metadata': {
                        'label': 'Test Text Area Long',
                        'type': 'LongTextArea',
                        'length': 32768,
                        'visibleLines': 25,
                        "description": "Description Test Text Area_Long"
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Text_Area_Long_field_metadata)
                print(f"✅ Field Text Area_Long is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Text_Area_Long__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Text Area_Long is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Text Area_Long field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise
        #'''Text_Area_Rich'''
            try:
                Text_Area_Rich_field_metadata = {
                    'FullName': f'{x}.test_Text_Area_Rich__c',
                    'Metadata': {
                        'label': 'Test Text Area Rich',
                        'type': 'Html',
                        'length': 32768,
                        'visibleLines': 10,
                        "description": "Description Test Text Area_Rich"
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Text_Area_Rich_field_metadata)
                print(f"✅ Field Text Area_Rich is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Text_Area_Rich__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Text Area_Rich is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Text Area_Rich field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise
        #'''Time'''
            try:
                Time_field_metadata = {
                    'FullName': f'{x}.test_Time__c',
                    'Metadata': {
                        'label': 'Test Time',
                        'type': 'Time',
                        "description": "Description Test Time"
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Time_field_metadata)
                print(f"✅ Field Time is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Time__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Text Time is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Text Time field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise
        #'''URL'''
            try:
                URL_field_metadata = {
                    'FullName': f'{x}.test_URL__c',
                    'Metadata': {
                        'label': 'Test URL',
                        'type': 'Url',
                        "description": "Description Test URL"
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=URL_field_metadata)
                print(f"✅ Field URL is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_URL__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Text URL is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Text URL field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise
    except SalesforceError as e:
        "INVALID_TYPE" in str(e)
        print("no SCLP__")
        ps_query = "SELECT Id FROM PermissionSet WHERE Name = 'SO_Sculptor_permission_set'"
        ps_result = sf.query(ps_query)
        permission_set_id = ps_result['records'][0]['Id']
        print(f"✅ Found Permission Set 'test' (Id: {permission_set_id})")
        object_name = ['Product2', 'Quote__c', 'QuoteLineItem__c']
        for x in object_name:
            print(f'Start creating {x} fields')

            
        #'''autonumber'''
            try:
                autonumber_field_metadata = {
                'FullName': f'{x}.test_Auto_Number__c',
                'Metadata': {
                    'label': 'Test Auto Number',
                    'type': 'AutoNumber',
                    'displayFormat': 'Python-{0000}',
                    'startingNumber': 1,
                    'description': 'Field created with Python',
                    # 'updateExistingRecords': True
                }
            }

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=autonumber_field_metadata)
                print(f"✅ AutoNumber field created for {x}!")
                print(f"Result is: {result}")

                Autonumber_field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Auto_Number__c',
                    'PermissionsRead': True,
                }

                result = sf.FieldPermissions.create(Autonumber_field_perm_data)
                print("✅ Auto Number is added for read Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
                #except ind
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Auto Number field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise
        #'''Formula'''
            try:
                if x == 'Product2':
                    formula_field_metadata = {
                        "FullName": f"{x}.test_Formula__c",
                        "Metadata": {
                            "label": "Test Formula",
                            "type": "Number",
                            "precision": 18,
                            "scale": 0,
                            "formula": 'VALUE(RIGHT(Name, LEN(Name) - FIND("Test Product ", Name) - 12))',         
                            "description": "Number field that shows Test Product's number"
                        }
                    }
                else:
                    formula_field_metadata = {
                        "FullName": f"{x}.test_Formula__c",
                        "Metadata": {
                            "label": "Test Formula",
                            "type": "Number",
                            "precision": 18,
                            "scale": 0,
                            "formula": '1',        
                            "description": "just one"
                            }}

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=formula_field_metadata)
                print("✅ Formula field created")
                print(result)
                formula_field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Formula__c',
                    'PermissionsRead': True,
                }

                result = sf.FieldPermissions.create(formula_field_perm_data)
                print("✅ Formula is added for read Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Formula field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise
        #'''checkbox'''
            try:
                checkbox_field_metadata = {
                    'FullName': f'{x}.test_Checkbox__c',
                    'Metadata': {
                        'label': 'Test Checkbox',
                        'type': 'Checkbox',
                        'defaultValue': False,
                        'description': 'Field created with Python'
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=checkbox_field_metadata)
                print(f"✅ Field checkbox is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Checkbox__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Checkbox is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Checkbox field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise
        #'''Currency'''
            try:
                currency_field_metadata = {
                    'FullName': f'{x}.test_Currency__c',
                    'Metadata': {
                        "label": "Test Currency",
                        "type": "Currency",
                        "precision": 18,
                        "scale": 2,
                        "description": "Description Test currency"
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=currency_field_metadata)
                print(f"✅ Field currency is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Currency__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Currency is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Currency field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise

        #'''Date'''
            try:
                Date_field_metadata = {
                    'FullName': f'{x}.test_Date__c',
                    'Metadata': {
                        "label": "Test Date",
                        "type": "Date",
                        "description": "Description Test Date"
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Date_field_metadata)
                print(f"✅ Field Date is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Date__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Date is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Date field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise  
        #'''DateTime'''
            try:
                DateTime_field_metadata = {
                    'FullName': f'{x}.test_DateTime__c',
                    'Metadata': {
                        "label": "Test DateTime",
                        "type": "DateTime",
                        "description": "Description Test DateTime"
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=DateTime_field_metadata)
                print(f"✅ Field DateTime is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_DateTime__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ DateTime is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Date Time field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise

        #'''Email'''
            try:
                Email_field_metadata = {
                    'FullName': f'{x}.test_Email__c',
                    'Metadata': {
                        "label": "Test Email",
                        "type": "Email",
                        "description": "Description Test Email",
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Email_field_metadata)
                print(f"✅ Field Email is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Email__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Email is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Email field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise
            
        #'''Number'''
            try:
                Number_field_metadata = {
                    'FullName': f'{x}.test_Number__c',
                    'Metadata': {
                        "label": "Test Number",
                        "type": "Number",
                        "precision": 18,
                        "scale": 2,
                        "description": "Description Test Number"
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Number_field_metadata)
                print(f"✅ Field Number is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Number__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Number is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Number field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise
        #'''Percent'''
            try:
                Percent_field_metadata = {
                    'FullName': f'{x}.test_Percent__c',
                    'Metadata': {
                        "label": "Test Percent",
                        "type": "Percent",
                        "precision": 18,
                        "scale": 2,
                        "description": "Description Test Percent"
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Percent_field_metadata)
                print(f"✅ Field Percent is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Percent__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Percent is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Percent field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise

        #'''Phone'''
            try:
                Phone_field_metadata = {
                    'FullName': f'{x}.test_Phone__c',
                    'Metadata': {
                        "label": "Test Phone",
                        "type": "Phone",
                        "description": "Description Test Phone"
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Phone_field_metadata)
                print(f"✅ Field Phone is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Phone__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Phone is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Phone field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise
        #'''Picklist'''
            try:
                Picklist_field_metadata = {
                    'FullName': f'{x}.test_Picklist__c',
                    'Metadata': {
                        "label": "Test Picklist",
                        "type": "Picklist",
                        "description": "Description Test Picklist",
                        'valueSet': {
                            'valueSetDefinition': {
                                'sorted': False,
                                'value': [
                                    {'fullName': '1', 'default': False, 'label': '1'},
                                    {'fullName': '2', 'default': False, 'label': '2'},
                                    {'fullName': '3', 'default': False, 'label': '3'}
                                ]
                            },
                            'restricted': True
                        
                    }
                }}
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Picklist_field_metadata)
                print(f"✅ Field Picklist is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Picklist__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Picklist is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Picklist field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise

        #'''Multi Picklist'''
            try:
                Multi_Picklist_field_metadata = {
                    'FullName': f'{x}.test_Multi_Picklist__c',
                    'Metadata': {
                        "label": "Test Multi Picklist",
                        "type": "MultiselectPicklist",
                        'required': False,
                        'visibleLines': 5,
                        "description": "Description Test Multi Picklist",
                        'valueSet': {
                            'valueSetDefinition': {
                                'sorted': False,
                                'value': [
                                    {'fullName': 'one', 'default': False, 'label': 'one'},
                                    {'fullName': 'two', 'default': False, 'label': 'two'},
                                    {'fullName': 'three', 'default': False, 'label': 'three'}
                                ]
                            },
                            'restricted': True
                        
                    }
                }}
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Multi_Picklist_field_metadata)
                print(f"✅ Field Multi Picklist is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Multi_Picklist__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Multi Picklist is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Multi Picklist field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise
        #'''Text'''
            try:
                Text_field_metadata = {
                    'FullName': f'{x}.test_Text__c',
                    'Metadata': {
                        'label': 'Test Text',
                        'length': 255,
                        'type': 'Text',
                        "description": "Description Test Text"
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Text_field_metadata)
                print(f"✅ Field Text is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Text__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Text is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Text field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise
        #'''Text_Area'''
            try:
                Text_Area_field_metadata = {
                    'FullName': f'{x}.test_Text_Area__c',
                    'Metadata': {
                        'label': 'Test Text Area',
                        'type': 'TextArea',
                        "description": "Description Test Text Area"
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Text_Area_field_metadata)
                print(f"✅ Field Text Area is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Text_Area__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Text Area is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Text Area field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise
        #'''Text_Area_Long'''
            try:
                Text_Area_Long_field_metadata = {
                    'FullName': f'{x}.test_Text_Area_Long__c',
                    'Metadata': {
                        'label': 'Test Text Area Long',
                        'type': 'LongTextArea',
                        'length': 32768,
                        'visibleLines': 25,
                        "description": "Description Test Text Area_Long"
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Text_Area_Long_field_metadata)
                print(f"✅ Field Text Area_Long is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Text_Area_Long__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Text Area_Long is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Text Area_Long field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise
        #'''Text_Area_Rich'''
            try:
                Text_Area_Rich_field_metadata = {
                    'FullName': f'{x}.test_Text_Area_Rich__c',
                    'Metadata': {
                        'label': 'Test Text Area Rich',
                        'type': 'Html',
                        'length': 32768,
                        'visibleLines': 10,
                        "description": "Description Test Text Area_Rich"
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Text_Area_Rich_field_metadata)
                print(f"✅ Field Text Area_Rich is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Text_Area_Rich__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Text Area_Rich is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Text Area_Rich field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise
        #'''Time'''
            try:
                Time_field_metadata = {
                    'FullName': f'{x}.test_Time__c',
                    'Metadata': {
                        'label': 'Test Time',
                        'type': 'Time',
                        "description": "Description Test Time"
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Time_field_metadata)
                print(f"✅ Field Time is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_Time__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Text Time is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Text Time field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise
        #'''URL'''
            try:
                URL_field_metadata = {
                    'FullName': f'{x}.test_URL__c',
                    'Metadata': {
                        'label': 'Test URL',
                        'type': 'Url',
                        "description": "Description Test URL"
                    }
                }
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=URL_field_metadata)
                print(f"✅ Field URL is created for {x}!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'{x}',
                    'Field': f'{x}.test_URL__c',
                    'PermissionsRead': True,
                    'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Text URL is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Text URL field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise

        
def create_products_and_pricebook_entries():

    pricebook = sf.query("SELECT Id FROM Pricebook2 WHERE name = 'Standard Price Book'")
    if not pricebook['records']:
        print("Standard Price Book not found!")
        raise

    pricebook_id = pricebook['records'][0]['Id']

    def worker(i):

        product_name = f"Test Product {i:03d}"

        existing_product = sf.query(
            f"SELECT Id FROM Product2 WHERE Name = '{product_name}'"
        )

        if existing_product['records']:
            print(f"{product_name} exists")
            return

        if i != 4:
            product = sf.Product2.create({
                'Name': product_name,
                'IsActive': True, 
                'Description': f'This is a test description for Product {i:03d}', 
                'ProductCode': f'SO-{i:03d}', 
                'test_Checkbox__c': random.choice([True, False]), 
                'test_Currency__c': i*0.3, 
                'test_Date__c': '1997-10-06', 
                'test_DateTime__c': '1997-10-06T18:05:43.000+0000', 
                'test_Email__c': f'test{i:03d}@test.test', 
                'test_Number__c': i*0.4, 
                'test_Percent__c': i*0.2, 
                'test_Phone__c': random.randint(10000000, 99999999), 
                'test_Picklist__c': random.randrange(1, 4), 
                'test_Multi_Picklist__c': random.choice(['one', 'two', 'three', 'two;three', 'one;three', 'one;two;three']), 
                'test_Text__c': f'Test Text {i:03d}', 
                'test_Text_Area__c': f'Test Text Area {i:03d}', 
                'test_Text_Area_Long__c': f'Test Text Area Long {i:03d}', 
                'test_Text_Area_Rich__c': f'<p>Test Text Rich {i:03d}</p>', 
                'test_Time__c': '15:16:08.000Z', 
                'test_URL__c': 'www.youtube.com'
            })
        else:
                product = sf.Product2.create({
                'Name': f'{product_name} test test test test test test test test test test test test test',
                'IsActive': True, 
                'Description': f'This is a test description for Product {i:03d}', 
                'ProductCode': f'SO-{i:03d}', 
                'test_Checkbox__c': random.choice([True, False]), 
                'test_Currency__c': i*0.3, 
                'test_Date__c': '1997-10-06', 
                'test_DateTime__c': '1997-10-06T18:05:43.000+0000', 
                'test_Email__c': f'test{i:03d}@test.test', 
                'test_Number__c': i*0.4, 
                'test_Percent__c': i*0.2, 
                'test_Phone__c': random.randint(10000000, 99999999), 
                'test_Picklist__c': random.randrange(1, 4), 
                'test_Multi_Picklist__c': random.choice(['one', 'two', 'three', 'two;three', 'one;three', 'one;two;three']), 
                'test_Text__c': f'Test Text {i:03d}', 
                'test_Text_Area__c': f'Test Text Area {i:03d}', 
                'test_Text_Area_Long__c': f'Test Text Area Long {i:03d}', 
                'test_Text_Area_Rich__c': f'<p>Test Text Rich {i:03d}</p>', 
                'test_Time__c': '15:16:08.000Z', 
                'test_URL__c': 'www.youtube.com',
                'SCLPCE__ManualCostForCommunity__c': True
            })
        price = i * 100

        existing_entry = sf.query(
            f"SELECT Id FROM PricebookEntry "
            f"WHERE Pricebook2Id = '{pricebook_id}' "
            f"AND Product2Id = '{product['id']}'"
        )

        if not existing_entry['records']:
            sf.PricebookEntry.create({
                'Pricebook2Id': pricebook_id,
                'Product2Id': product['id'],
                'UnitPrice': price,
                'IsActive': True
            })

        print(f"{product_name} DONE")

    with ThreadPoolExecutor(max_workers=25) as executor:
        futures = [
            executor.submit(worker, i)
            for i in range(1, RECORDS_QTY)
        ]

        for f in as_completed(futures):
            f.result()

def delete_test_product_salesforce():
    print("Start Product Deleting...")
    def worker(i):
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
    with ThreadPoolExecutor(max_workers=25) as executor:
        futures = [
            executor.submit(worker, i)
            for i in range(1, RECORDS_QTY)
        ]

        for f in as_completed(futures):
            f.result()


    print("All product are deleted.")

def Standard_PriceBook_activation():
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
def create_account():
    print('Start creating account')
    account_created = "select name, id from account where name like 'test account created %'"
    

    
    results = sf.query(account_created)
    

    if results.get('records') and len(results['records']) > 0:
        print ('test account already exists')
    else:
        sf.account.create({
            'Name': f'Test Account created {timestamp}',
            # 'OwnerId': '005QI00000GeYzRYAV'
            })
        print('test account is created') 
    sf.contact.create({
        'FirstName': 'Test First Name',
        'LastName': f'Test Last Name Created {timestamp}',
        'AccountId': sf.query(f"select id from account where name = 'Test Account created {timestamp}'")['records'][0]['Id'],
        # 'OwnerId': '005QI00000GeYzRYAV'
    })
    print('test contant is created')
    contact_query = f"SELECT Id, FirstName, LastName from Contact where LastName like 'Test Last Name Created {timestamp}'"
    print(f"test contant {sf.query(contact_query)['records'][0]['LastName']} is created")
def create_opportunity():
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
            'AccountId': Acc_id,
            # 'OwnerId': '005QI00000GeYzRYAV'
            })
        print('test opportunity is created')          

def create_Quote():
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

def delete_all_quotes():
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
        
def create_big_bundle():
    print('Start Bundle creation')
    bundle_query_result = sf.query(f"select name, id from product2 where name like 'Big Test Bundle Created%'")
    if len(bundle_query_result.get('records')) >= 1:
        print('Bundle already created')
    else:
        print('bundle to be created')
        Rt_bundle_in_qurey = sf.query("SELECT Id, Name, SObjectType FROM RecordType WHERE SObjectType = 'Product2' AND Name = 'Product Bundle'")
        rt_id = Rt_bundle_in_qurey['records'][0]['Id']
        print(f"Bundle Record Type id is {rt_id}")
        sf.product2.create({
            'Name': f'Big Test Bundle Created {timestamp}',
            'RecordTypeId': rt_id,
            'IsActive': 'true'
        })
        print('Bundle is created')
        created_bundle_id = sf.query(f"select name, id from product2 where name = 'Big Test Bundle Created {timestamp}'")['records'][0]['Id']
        print(f'New ID of bundle is {created_bundle_id}\n Now lets create Features')
        try:
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
            def worker(z):
                try:
                    sf.SCLP__ProductOption__c.create({
                    'SCLP__BundleQuantity__c': '1',
                    'SCLP__Bundle__c': created_bundle_id,
                    'SCLP__Order__c': z,
                    'SCLP__Product__c':  sf.query(f"select id from product2 where name = 'Test Product {z:03d}'")['records'][0]['Id'],
                    'SCLP__DefaultOption__c': 'false',
                    'SCLP__Tip__c': f'Tip test {z:03d}'
                    })
                    print(f'option {z:03d} created')
                except Exception as e:
                    print(f'Error in option {z:03d}: {e}')


            with ThreadPoolExecutor(max_workers=25) as executor:
                futures = [executor.submit(worker, z) for z in range(9, RECORDS_QTY)]

                for f in as_completed(futures):
                    f.result()
    

                    


            # for i in range(9, RECORDS_QTY):
            #     sf.SCLP__ProductOption__c.create({
            #     'SCLP__BundleQuantity__c': '1',
            #     'SCLP__Bundle__c': created_bundle_id,
            #     'SCLP__Order__c': i,
            #     'SCLP__Product__c':  sf.query(f"select id from product2 where name = 'Test Product {i:03d}'")['records'][0]['Id'],
            #     'SCLP__DefaultOption__c': 'false',
            #     'SCLP__Tip__c': f'Tip test {i:03d}'
            #     })
            #     print(f'option {i:03d} created')



        except SalesforceError as e:
            "INVALID_TYPE" in str(e)
            print("no SCLP__")
            sf.ProductFeature__c.create({
                'Name': 'Feature Number One',
                'HasGroup__c': 'false',
                'Multiple__c': 'true',
                'Order__c': '1',
                'Product__c': created_bundle_id,
                'Required__c': 'false',
                'Tip__c': 'Feature Number One tip'
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
            product1_id = sf.query(f"select id from product2 where name = 'Test Product 001'")['records'][0]['Id']
            product2_id = sf.query(f"select id from product2 where name = 'Test Product 002'")['records'][0]['Id']
            product3_id = sf.query(f"select id from product2 where name = 'Test Product 003'")['records'][0]['Id']
            product4_id = sf.query(f"select id from product2 where name like 'Test Product 004%'")['records'][0]['Id']
            product5_id = sf.query(f"select id from product2 where name = 'Test Product 005'")['records'][0]['Id']
            product6_id = sf.query(f"select id from product2 where name = 'Test Product 006'")['records'][0]['Id']
            product7_id = sf.query(f"select id from product2 where name = 'Test Product 007'")['records'][0]['Id']
            product8_id = sf.query(f"select id from product2 where name = 'Test Product 008'")['records'][0]['Id']

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
            option1_id = sf.query(f"select id from ProductOption__c where Product__r.name = 'Test Product 001' and Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
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
            option6_id = sf.query(f"select id from ProductOption__c where Product__r.name = 'Test Product 006' and Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
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
            def worker(z):
                try:
                    sf.ProductOption__c.create({
                    'BundleQuantity__c': '1',
                    'Bundle__c': created_bundle_id,
                    'Order__c': z,
                    'Product__c':  sf.query(f"select id from product2 where name = 'Test Product {z:03d}'")['records'][0]['Id'],
                    'DefaultOption__c': 'false',
                    'Tip__c': f'Tip test {z:03d}'
                    })
                    print(f'option {z:03d} created')
                except Exception as e:
                    print(f'Error in option {z:03d}: {e}')


            with ThreadPoolExecutor(max_workers=25) as executor:
                futures = [executor.submit(worker, z) for z in range(9, RECORDS_QTY)]

                for f in as_completed(futures):
                    f.result()
            # for i in range(9, RECORDS_QTY):
            #     sf.ProductOption__c.create({
            #     'BundleQuantity__c': '1',
            #     'Bundle__c': created_bundle_id,
            #     'Order__c': i,
            #     'Product__c':  sf.query(f"select id from product2 where name = 'Test Product {i:03d}'")['records'][0]['Id'],
            #     'DefaultOption__c': 'false',
            #     'Tip__c': f'Tip test {i:03d}'
            #       })
            #     print(f'option {i:03d} created')

def create_normal_bundle():
    print('Start Bundle creation')
    bundle_query_result = sf.query(f"select name, id from product2 where name like 'Test Bundle Created%'")
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
        created_bundle_id = sf.query(f"select name, id from product2 where name = 'Test Bundle Created {timestamp}'")['records'][0]['Id']
        print(f'New ID of bundle is {created_bundle_id}\n Now lets create Features')
        try:
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

        except SalesforceError as e:
            "INVALID_TYPE" in str(e)
            print("no SCLP__")
            sf.ProductFeature__c.create({
                'Name': 'Feature Number One',
                'HasGroup__c': 'false',
                'Multiple__c': 'true',
                'Order__c': '1',
                'Product__c': created_bundle_id,
                'Required__c': 'false',
                'Tip__c': 'Feature Number One tip'
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
            product1_id = sf.query(f"select id from product2 where name = 'Test Product 001'")['records'][0]['Id']
            product2_id = sf.query(f"select id from product2 where name = 'Test Product 002'")['records'][0]['Id']
            product3_id = sf.query(f"select id from product2 where name = 'Test Product 003'")['records'][0]['Id']
            product4_id = sf.query(f"select id from product2 where name like 'Test Product 004%'")['records'][0]['Id']
            product5_id = sf.query(f"select id from product2 where name = 'Test Product 005'")['records'][0]['Id']
            product6_id = sf.query(f"select id from product2 where name = 'Test Product 006'")['records'][0]['Id']
            product7_id = sf.query(f"select id from product2 where name = 'Test Product 007'")['records'][0]['Id']
            product8_id = sf.query(f"select id from product2 where name = 'Test Product 008'")['records'][0]['Id']

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
            option1_id = sf.query(f"select id from ProductOption__c where Product__r.name = 'Test Product 001' and Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
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
            option6_id = sf.query(f"select id from ProductOption__c where Product__r.name = 'Test Product 006' and Bundle__c = '{created_bundle_id}'")['records'][0]['Id']
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


def delete_bundle():
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

def Community_Cost_Price_enabling():
    print('Now its about Cost Price')
    try:
        try:
            record = sf.query("SELECT Id FROM SCLP__ProductCostPrice__c LIMIT 1")['records'][0]
            print(record)
            sf.SCLP__ProductCostPrice__c.update(record['Id'], {
                'SCLPCE__CommunityCostPriceEnabled__c': True
            })
            print("Updated successfully!")

        except IndexError:
            print("No SCLP__ProductCostPrice__c records found (empty result set)")
            # create reateken INVALID_FIELD
            try:
                sf.SCLP__ProductCostPrice__c.create({
                    'SCLPCE__CommunityCostPriceEnabled__c': True
                })
                print("Created successfully with namespaced field")
            except SalesforceMalformedRequest as e:
                if "INVALID_FIELD" in str(e):
                    sf.SCLP__ProductCostPrice__c.create({
                        'CommunityCostPriceEnabled__c': True
                    })
                    print("Created successfully with local field")
                else:
                    raise

        except SalesforceError as e:
            msg = str(e)
            if "INVALID_FIELD" in msg:
                print("Field mismatch, retrying with local field")
                sf.SCLP__ProductCostPrice__c.create({
                    'CommunityCostPriceEnabled__c': True
                })
                print("Created successfully!")
            else:
                raise

    except SalesforceError as e:
        "INVALID_TYPE" in str(e)
        print("no SCLP__")
        try:
            try:
                record = sf.query("SELECT Id FROM ProductCostPrice__c LIMIT 1")['records'][0]
                print(record)
                sf.ProductCostPrice__c.update(record['Id'], {
                    'SCLPCE__CommunityCostPriceEnabled__c': True
                })
                print("Updated successfully!")

            except IndexError:
                print("No ProductCostPrice__c records found (empty result set)")
                # create reateken INVALID_FIELD
                try:
                    sf.ProductCostPrice__c.create({
                        'SCLPCE__CommunityCostPriceEnabled__c': True
                    })
                    print("Created successfully with namespaced field")
                except SalesforceMalformedRequest as e:
                    if "INVALID_FIELD" in str(e):
                        sf.ProductCostPrice__c.create({
                            'CommunityCostPriceEnabled__c': True
                        })
                        print("Created successfully with local field")
                    else:
                        raise

            except SalesforceError as e:
                msg = str(e)
                if "INVALID_FIELD" in msg:
                    print("Field mismatch, retrying with local field")
                    sf.ProductCostPrice__c.create({
                        'CommunityCostPriceEnabled__c': True
                    })
                    print("Created successfully!")
                else:
                    raise

        except SalesforceError as e:
            try:
                record = sf.query("SELECT Id FROM ProductCostPrice__c LIMIT 1")['records'][0]
                print(record)
                sf.ProductCostPrice__c.update(record['Id'], {
                    'CommunityCostPriceEnabled__c': True
                })
                print("Updated successfully!")
            except IndexError:
                print("No ProductCostPrice__c records found.")
                sf.ProductCostPrice__c.create({
                    'CommunityCostPriceEnabled__c': True
                })
                print("Created successfully!")        
def create_multiple_quotes_core():
    print('Start creating Multiple Quotes')
    Standard_Price_book_query = sf.query("select name, id from pricebook2 where name = 'Standard Price Book'")['records'][0]
    print(f"pricebook {Standard_Price_book_query['Name']} with id {Standard_Price_book_query['Id']} is found")
    account_query = sf.query("select name, id from account where name like 'test account created %'")['records'][0]
    print(f"account {account_query['Name']} with id {account_query['Id']} is found")
    opp = sf.query("select name, id from opportunity where name like 'test opportunity created %'")['records'][0]
    print(f"opportunity {opp['Name']} with id {opp['Id']} is found")    
    print('queries ended')
    try:
        sf.SCLP__Quote__c.create({'Name': f'001 Test Quote Core Created {timestamp}',
                'SCLP__Opportunity__c': opp['Id'],
                'SCLP__Pricebook__c': Standard_Price_book_query['Id'],
                'SCLP__Account__c': account_query['Id'],
                # 'SCLP__Account__c': '001In00000BR0MAIA1',
                'test_Checkbox__c': random.choice([True, False]),
                'test_Currency__c': 1*0.3,
                'test_Date__c': '1997-10-06',
                'test_DateTime__c': '1997-10-06T18:18:43.000+0000',
                'test_Email__c': f'test001@test.test',
                'test_Number__c': 1*0.4,
                'test_Percent__c': 1*0.2,
                'test_Phone__c': random.randint(10000000, 99999999), 
                'test_Picklist__c': random.randrange(1, 4),
                'test_Multi_Picklist__c': random.choice(['one', 'two', 'three', 'two;three', 'one;three', 'one;two;three']),
                'test_Text__c': f'Test Text 001',
                'test_Text_Area__c': f'Test Text Area 001',
                'test_Text_Area_Long__c': f'Test Text Area Long 001',
                'test_Text_Area_Rich__c': f'<p>Test Text Rich 001</p>',
                'test_Time__c': '15:16:08.000Z',
                'test_URL__c': 'www.youtube.com',
                'SCLP__DescriptionHeader__c': "<p>{!test_Auto_Number__c}</p><p> {!test_Checkbox__c} </p><p>{!test_Currency__c}</p><p>{!test_Date__c}</p><p>{!test_DateTime__c}</p><p>{!test_Email__c}</p><p>{!test_formula__c}</p><p>{!test_Multi_Picklist__c}</p><p>{!test_Number__c}</p><p>{!test_Percent__c}</p><p>{!test_Phone__c}</p><p>{!test_Picklist__c}</p><p>{!test_Text__c}</p><p>{!test_Text_Area__c}</p><p>{!test_Text_Area_Long__c}</p><p>{!test_Text_Area_Rich__c}</p><p>{!test_Time__c}</p><p>{!test_URL__c}</p>",
                'SCLP__DescriptionFooter__c': "<p>{!test_Auto_Number__c}</p><p> {!test_Checkbox__c} </p><p>{!test_Currency__c}</p><p>{!test_Date__c}</p><p>{!test_DateTime__c}</p><p>{!test_Email__c}</p><p>{!test_formula__c}</p><p>{!test_Multi_Picklist__c}</p><p>{!test_Number__c}</p><p>{!test_Percent__c}</p><p>{!test_Phone__c}</p><p>{!test_Picklist__c}</p><p>{!test_Text__c}</p><p>{!test_Text_Area__c}</p><p>{!test_Text_Area_Long__c}</p><p>{!test_Text_Area_Rich__c}</p><p>{!test_Time__c}</p><p>{!test_URL__c}</p>"
                })['id']
        use_sclp = True
        print('Quote is created for SCLP')
    except SalesforceError as e:
        if "NOT_FOUND" in str(e):
            print(f'No SCLP')
            use_sclp = False
        else:
            raise
    def worker(z):
        try:
            if use_sclp:
                new_timestamp = timestamp

                sf.sclp__quote__c.create({
                    'Name': f'{z:03d} Test Quote Core Created {timestamp}',
                    'SCLP__Opportunity__c': opp['Id'],
                    'SCLP__Pricebook__c': Standard_Price_book_query['Id'],
                    'SCLP__Account__c': account_query['Id'],
                    # 'OwnerId': '005In000001jl0ZIAQ',
                    'test_Checkbox__c': random.choice([True, False]),
                    'test_Currency__c': z*0.3,
                    'test_Date__c': '1997-10-06',
                    'test_DateTime__c': '1997-10-06T18:18:43.000+0000',
                    'test_Email__c': f'test{z:03d}@test.test',
                    'test_Number__c': z*0.4,
                    'test_Percent__c': z*0.2,
                    'test_Phone__c': random.randint(10000000, 99999999), 
                    'test_Picklist__c': random.randrange(1, 4),
                    'test_Multi_Picklist__c': random.choice(['one', 'two', 'three', 'two;three', 'one;three', 'one;two;three']),
                    'test_Text__c': f'Test Text {z:03d}',
                    'test_Text_Area__c': f'Test Text Area {z:03d}',
                    'test_Text_Area_Long__c': f'Test Text Area Long {z:03d}',
                    'test_Text_Area_Rich__c': f'<p>Test Text Rich {z:03d}</p>',
                    'test_Time__c': '15:16:08.000Z',
                    'test_URL__c': 'www.youtube.com',
                    'SCLP__DescriptionHeader__c': "<p>{!test_Auto_Number__c}</p><p> {!test_Checkbox__c} </p><p>{!test_Currency__c}</p><p>{!test_Date__c}</p><p>{!test_DateTime__c}</p><p>{!test_Email__c}</p><p>{!test_formula__c}</p><p>{!test_Multi_Picklist__c}</p><p>{!test_Number__c}</p><p>{!test_Percent__c}</p><p>{!test_Phone__c}</p><p>{!test_Picklist__c}</p><p>{!test_Text__c}</p><p>{!test_Text_Area__c}</p><p>{!test_Text_Area_Long__c}</p><p>{!test_Text_Area_Rich__c}</p><p>{!test_Time__c}</p><p>{!test_URL__c}</p>",
                    'SCLP__DescriptionFooter__c': "<p>{!test_Auto_Number__c}</p><p> {!test_Checkbox__c} </p><p>{!test_Currency__c}</p><p>{!test_Date__c}</p><p>{!test_DateTime__c}</p><p>{!test_Email__c}</p><p>{!test_formula__c}</p><p>{!test_Multi_Picklist__c}</p><p>{!test_Number__c}</p><p>{!test_Percent__c}</p><p>{!test_Phone__c}</p><p>{!test_Picklist__c}</p><p>{!test_Text__c}</p><p>{!test_Text_Area__c}</p><p>{!test_Text_Area_Long__c}</p><p>{!test_Text_Area_Rich__c}</p><p>{!test_Time__c}</p><p>{!test_URL__c}</p>"


                    })
                print(f'Quote number Core {z:03d} is created')
            else:
                new_timestamp = timestamp

                sf.quote__c.create({
                    'Name': f'{z:03d} Test Quote Core Created {new_timestamp}',
                    'Opportunity__c': opp['Id'],
                    'Pricebook__c': Standard_Price_book_query['Id'],
                    'Account__c': account_query['Id'],
                    'test_Checkbox__c': random.choice([True, False]),
                    'test_Currency__c': z*0.3,
                    'test_Date__c': '1997-10-06',
                    'test_DateTime__c': '1997-10-06T18:18:43.000+0000',
                    'test_Email__c': f'test{z:03d}@test.test',
                    'test_Number__c': z*0.4,
                    'test_Percent__c': z*0.2,
                    'test_Phone__c': random.randint(10000000, 99999999), 
                    'test_Picklist__c': random.randrange(1, 4),
                    'test_Multi_Picklist__c': random.choice(['one', 'two', 'three', 'two;three', 'one;three', 'one;two;three']),
                    'test_Text__c': f'Test Text {z:03d}',
                    'test_Text_Area__c': f'Test Text Area {z:03d}',
                    'test_Text_Area_Long__c': f'Test Text Area Long {z:03d}',
                    'test_Text_Area_Rich__c': f'<p>Test Text Rich {z:03d}</p>',
                    'test_Time__c': '15:16:08.000Z',
                    'test_URL__c': 'www.youtube.com',
                    'DescriptionHeader__c': "<p>{!test_Auto_Number__c}</p><p> {!test_Checkbox__c} </p><p>{!test_Currency__c}</p><p>{!test_Date__c}</p><p>{!test_DateTime__c}</p><p>{!test_Email__c}</p><p>{!test_formula__c}</p><p>{!test_Multi_Picklist__c}</p><p>{!test_Number__c}</p><p>{!test_Percent__c}</p><p>{!test_Phone__c}</p><p>{!test_Picklist__c}</p><p>{!test_Text__c}</p><p>{!test_Text_Area__c}</p><p>{!test_Text_Area_Long__c}</p><p>{!test_Text_Area_Rich__c}</p><p>{!test_Time__c}</p><p>{!test_URL__c}</p>",
                    'DescriptionFooter__c': "<p>{!test_Auto_Number__c}</p><p> {!test_Checkbox__c} </p><p>{!test_Currency__c}</p><p>{!test_Date__c}</p><p>{!test_DateTime__c}</p><p>{!test_Email__c}</p><p>{!test_formula__c}</p><p>{!test_Multi_Picklist__c}</p><p>{!test_Number__c}</p><p>{!test_Percent__c}</p><p>{!test_Phone__c}</p><p>{!test_Picklist__c}</p><p>{!test_Text__c}</p><p>{!test_Text_Area__c}</p><p>{!test_Text_Area_Long__c}</p><p>{!test_Text_Area_Rich__c}</p><p>{!test_Time__c}</p><p>{!test_URL__c}</p>"


                    })
                print(f'Quote number Core {z:03d} is created')

        except Exception as e:
            print(f'Error in Quote {z:03d}: {e}')
    with ThreadPoolExecutor(max_workers=25) as executor:
        futures = [executor.submit(worker, z) for z in range(1, RECORDS_QTY)]

        for f in as_completed(futures):
            f.result()

def create_multiple_quotes_community_no_opportunities():
    print('Start creating Multiple Quotes')
    Standard_Price_book_query = sf.query("select name, id from pricebook2 where name = 'Standard Price Book'")['records'][0]
    print(f"pricebook {Standard_Price_book_query['Name']} with id {Standard_Price_book_query['Id']} is found")
    account_query = sf.query("select name, id from account where name = 'Partner Account'")['records'][0]
    print(f"account {account_query['Name']} with id {account_query['Id']} is found")
    opp = sf.query("select name, id from opportunity where name like 'test opportunity created %'")['records'][0]
    owner = sf.query("SELECT Id, Name from user where ContactId !=null and name = 'One Partner'")['records'][0]['Id']
    print(f"opportunity {opp['Name']} with id {opp['Id']} is found")    
    print('queries ended')
    try:
        sf.SCLP__Quote__c.create({'Name': f'001 Test Quote Community Created {timestamp}',
                # 'SCLP__Opportunity__c': opp['Id'],
                'OwnerId': owner,
                'SCLP__Pricebook__c': Standard_Price_book_query['Id'],
                'SCLP__Account__c': account_query['Id'],
                'test_Checkbox__c': random.choice([True, False]),
                'test_Currency__c': 1*0.3,
                'test_Date__c': '1997-10-06',
                'test_DateTime__c': '1997-10-06T18:18:43.000+0000',
                'test_Email__c': f'test001@test.test',
                'test_Number__c': 1*0.4,
                'test_Percent__c': 1*0.2,
                'test_Phone__c': random.randint(10000000, 99999999), 
                'test_Picklist__c': random.randrange(1, 4),
                'test_Multi_Picklist__c': random.choice(['one', 'two', 'three', 'two;three', 'one;three', 'one;two;three']),
                'test_Text__c': f'Test Text 001',
                'test_Text_Area__c': f'Test Text Area 001',
                'test_Text_Area_Long__c': f'Test Text Area Long 001',
                'test_Text_Area_Rich__c': f'<p>Test Text Rich 001</p>',
                'test_Time__c': '15:16:08.000Z',
                'test_URL__c': 'www.youtube.com',
                'SCLP__DescriptionHeader__c': "<p>{!test_Auto_Number__c}</p><p> {!test_Checkbox__c} </p><p>{!test_Currency__c}</p><p>{!test_Date__c}</p><p>{!test_DateTime__c}</p><p>{!test_Email__c}</p><p>{!test_formula__c}</p><p>{!test_Multi_Picklist__c}</p><p>{!test_Number__c}</p><p>{!test_Percent__c}</p><p>{!test_Phone__c}</p><p>{!test_Picklist__c}</p><p>{!test_Text__c}</p><p>{!test_Text_Area__c}</p><p>{!test_Text_Area_Long__c}</p><p>{!test_Text_Area_Rich__c}</p><p>{!test_Time__c}</p><p>{!test_URL__c}</p>",
                'SCLP__DescriptionFooter__c': "<p>{!test_Auto_Number__c}</p><p> {!test_Checkbox__c} </p><p>{!test_Currency__c}</p><p>{!test_Date__c}</p><p>{!test_DateTime__c}</p><p>{!test_Email__c}</p><p>{!test_formula__c}</p><p>{!test_Multi_Picklist__c}</p><p>{!test_Number__c}</p><p>{!test_Percent__c}</p><p>{!test_Phone__c}</p><p>{!test_Picklist__c}</p><p>{!test_Text__c}</p><p>{!test_Text_Area__c}</p><p>{!test_Text_Area_Long__c}</p><p>{!test_Text_Area_Rich__c}</p><p>{!test_Time__c}</p><p>{!test_URL__c}</p>"
                })['id']
        use_sclp = True
        print('Quote is created for SCLP')
    except SalesforceError as e:
        if "NOT_FOUND" in str(e):
            print(f'No SCLP')
            use_sclp = False
        else:
            raise
    def worker(z):
        try:
            if use_sclp:
                new_timestamp = timestamp

                sf.sclp__quote__c.create({
                    # 'SCLP__Opportunity__c': opp['Id'],
                    'OwnerId': owner,
                    'Name': f'{z:03d} Test Quote Community Created {timestamp}',
                    'SCLP__Pricebook__c': Standard_Price_book_query['Id'],
                    'SCLP__Account__c': account_query['Id'],
                    'test_Checkbox__c': random.choice([True, False]),
                    'test_Currency__c': z*0.3,
                    'test_Date__c': '1997-10-06',
                    'test_DateTime__c': '1997-10-06T18:18:43.000+0000',
                    'test_Email__c': f'test{z:03d}@test.test',
                    'test_Number__c': z*0.4,
                    'test_Percent__c': z*0.2,
                    'test_Phone__c': random.randint(10000000, 99999999), 
                    'test_Picklist__c': random.randrange(1, 4),
                    'test_Multi_Picklist__c': random.choice(['one', 'two', 'three', 'two;three', 'one;three', 'one;two;three']),
                    'test_Text__c': f'Test Text {z:03d}',
                    'test_Text_Area__c': f'Test Text Area {z:03d}',
                    'test_Text_Area_Long__c': f'Test Text Area Long {z:03d}',
                    'test_Text_Area_Rich__c': f'<p>Test Text Rich {z:03d}</p>',
                    'test_Time__c': '15:16:08.000Z',
                    'test_URL__c': 'www.youtube.com',
                    'SCLP__DescriptionHeader__c': "<p>{!test_Auto_Number__c}</p><p> {!test_Checkbox__c} </p><p>{!test_Currency__c}</p><p>{!test_Date__c}</p><p>{!test_DateTime__c}</p><p>{!test_Email__c}</p><p>{!test_formula__c}</p><p>{!test_Multi_Picklist__c}</p><p>{!test_Number__c}</p><p>{!test_Percent__c}</p><p>{!test_Phone__c}</p><p>{!test_Picklist__c}</p><p>{!test_Text__c}</p><p>{!test_Text_Area__c}</p><p>{!test_Text_Area_Long__c}</p><p>{!test_Text_Area_Rich__c}</p><p>{!test_Time__c}</p><p>{!test_URL__c}</p>",
                    'SCLP__DescriptionFooter__c': "<p>{!test_Auto_Number__c}</p><p> {!test_Checkbox__c} </p><p>{!test_Currency__c}</p><p>{!test_Date__c}</p><p>{!test_DateTime__c}</p><p>{!test_Email__c}</p><p>{!test_formula__c}</p><p>{!test_Multi_Picklist__c}</p><p>{!test_Number__c}</p><p>{!test_Percent__c}</p><p>{!test_Phone__c}</p><p>{!test_Picklist__c}</p><p>{!test_Text__c}</p><p>{!test_Text_Area__c}</p><p>{!test_Text_Area_Long__c}</p><p>{!test_Text_Area_Rich__c}</p><p>{!test_Time__c}</p><p>{!test_URL__c}</p>"


                    })
                print(f'Quote number Community {z:03d} is created')
            else:
                new_timestamp = timestamp

                sf.quote__c.create({
                    # 'Opportunity__c': opp['Id'],
                    'Name': f'{z:03d} Test Quote Community Created {new_timestamp}',
                    'Pricebook__c': Standard_Price_book_query['Id'],
                    'Account__c': account_query['Id'],
                    'test_Checkbox__c': random.choice([True, False]),
                    'test_Currency__c': z*0.3,
                    'test_Date__c': '1997-10-06',
                    'test_DateTime__c': '1997-10-06T18:18:43.000+0000',
                    'test_Email__c': f'test{z:03d}@test.test',
                    'test_Number__c': z*0.4,
                    'test_Percent__c': z*0.2,
                    'test_Phone__c': random.randint(10000000, 99999999), 
                    'test_Picklist__c': random.randrange(1, 4),
                    'test_Multi_Picklist__c': random.choice(['one', 'two', 'three', 'two;three', 'one;three', 'one;two;three']),
                    'test_Text__c': f'Test Text {z:03d}',
                    'test_Text_Area__c': f'Test Text Area {z:03d}',
                    'test_Text_Area_Long__c': f'Test Text Area Long {z:03d}',
                    'test_Text_Area_Rich__c': f'<p>Test Text Rich {z:03d}</p>',
                    'test_Time__c': '15:16:08.000Z',
                    'test_URL__c': 'www.youtube.com',
                    'DescriptionHeader__c': "<p>{!test_Auto_Number__c}</p><p> {!test_Checkbox__c} </p><p>{!test_Currency__c}</p><p>{!test_Date__c}</p><p>{!test_DateTime__c}</p><p>{!test_Email__c}</p><p>{!test_formula__c}</p><p>{!test_Multi_Picklist__c}</p><p>{!test_Number__c}</p><p>{!test_Percent__c}</p><p>{!test_Phone__c}</p><p>{!test_Picklist__c}</p><p>{!test_Text__c}</p><p>{!test_Text_Area__c}</p><p>{!test_Text_Area_Long__c}</p><p>{!test_Text_Area_Rich__c}</p><p>{!test_Time__c}</p><p>{!test_URL__c}</p>",
                    'DescriptionFooter__c': "<p>{!test_Auto_Number__c}</p><p> {!test_Checkbox__c} </p><p>{!test_Currency__c}</p><p>{!test_Date__c}</p><p>{!test_DateTime__c}</p><p>{!test_Email__c}</p><p>{!test_formula__c}</p><p>{!test_Multi_Picklist__c}</p><p>{!test_Number__c}</p><p>{!test_Percent__c}</p><p>{!test_Phone__c}</p><p>{!test_Picklist__c}</p><p>{!test_Text__c}</p><p>{!test_Text_Area__c}</p><p>{!test_Text_Area_Long__c}</p><p>{!test_Text_Area_Rich__c}</p><p>{!test_Time__c}</p><p>{!test_URL__c}</p>"


                    })
                print(f'Quote number Community {z:03d} is created')

        except Exception as e:
            print(f'Error in Quote {z:03d}: {e}')
    with ThreadPoolExecutor(max_workers=25) as executor:
        futures = [executor.submit(worker, z) for z in range(1, RECORDS_QTY)]

        for f in as_completed(futures):
            f.result()

def create_blocks():
    try:
        for i in range(1, 6):
            sf.SCLP__SculptorPDFTemplateBlock__c.create({
            'Name': f'{i:03d} Test Block {timestamp}',
            'SCLP__IsActive__c': True,
            'SCLP__Content__c': (
                f'<p>Test Content for Block {i:03d}</p>'
                '<p>{!test_Auto_Number__c}</p>'
                '<p>{!test_Checkbox__c}</p>'
                '<p>{!test_Currency__c}</p>'
                '<p>{!test_Date__c}</p>'
                '<p>{!test_DateTime__c}</p>'
                '<p>{!test_Email__c}</p>'
                '<p>{!test_formula__c}</p>'
                '<p>{!test_Multi_Picklist__c}</p>'
                '<p>{!test_Number__c}</p>'
                '<p>{!test_Percent__c}</p>'
                '<p>{!test_Phone__c}</p>'
                '<p>{!test_Picklist__c}</p>'
                '<p>{!test_Text__c}</p>'
                '<p>{!test_Text_Area__c}</p>'
                '<p>{!test_Text_Area_Long__c}</p>'
                '<p>{!test_Text_Area_Rich__c}</p>'
                '<p>{!test_Time__c}</p>'
                '<p>{!test_URL__c}</p>'
            )
            # 'OwnerId': '005QI00000GeYzRYAV'

            })
            print(f'Block number {i:03d} is created')

    except SalesforceError as e:
        "INVALID_TYPE" in str(e)
        print("no SCLP__")
        for i in range(1, 6):
            sf.SculptorPDFTemplateBlock__c.create({
            'Name': f'{i:03d} Test Block {timestamp}',
            'IsActive__c': True,
            'Content__c': (
                f'<p>Test Content for Block {i:03d}</p>'
                '<p>{!test_Auto_Number__c}</p>'
                '<p>{!test_Checkbox__c}</p>'
                '<p>{!test_Currency__c}</p>'
                '<p>{!test_Date__c}</p>'
                '<p>{!test_DateTime__c}</p>'
                '<p>{!test_Email__c}</p>'
                '<p>{!test_formula__c}</p>'
                '<p>{!test_Multi_Picklist__c}</p>'
                '<p>{!test_Number__c}</p>'
                '<p>{!test_Percent__c}</p>'
                '<p>{!test_Phone__c}</p>'
                '<p>{!test_Picklist__c}</p>'
                '<p>{!test_Text__c}</p>'
                '<p>{!test_Text_Area__c}</p>'
                '<p>{!test_Text_Area_Long__c}</p>'
                '<p>{!test_Text_Area_Rich__c}</p>'
                '<p>{!test_Time__c}</p>'
                '<p>{!test_URL__c}</p>'
            )
            })
            print(f'Block number {i:03d} is created')
            


def create_Pricing_Rule():
    Is_Active = False



    try:
        folders = sf.query("select name, id from SCLP__RuleFolder__c where name = 'SO Test Rules'")
        if folders['records']:
            folder = folders['records'][0]['Id']
        else:
            folder = sf.SCLP__RuleFolder__c.create({
                'Name': 'SO Test Rules'
            })['id']
        sf.SCLP__Rule__c.create({'Name': f'001 Test Rule Number {timestamp}',
                    'SCLP__Active__c': Is_Active,
                    'SCLP__ExecutionOrder__c': 1
                        })['id']
        use_sclp = True
        print('Rule is created for SCLP')
    except SalesforceError as e:
        if "NOT_FOUND" in str(e):
            print(f'No SCLP')
            folders = sf.query("select name, id from RuleFolder__c where name = 'SO Test Rules'")
            if folders['records']:
                folder = folders['records'][0]['Id']
            else:
                folder = sf.RuleFolder__c.create({
                    'Name': 'SO Test Rules'
                })['id']

    
            use_sclp = False
        else:
            raise

    def worker(z):
        try:
            if use_sclp:
                existing = sf.query(
                    f"select id from SCLP__Rule__c "
                    f"where name like '{z:03d} Test Rule Number%'"
                )

                if existing['records']:
                    print(f'Rule {z:03d} already exists')
                    return

                rule_id = sf.SCLP__Rule__c.create({
                    'Name': f'{z:03d} Test Rule Number {timestamp}',
                    'SCLP__Active__c': Is_Active,
                    'SCLP__ExecutionOrder__c': z,
                    'SCLP__RuleFolder__c': folder
                })['id']

                sf.SCLP__RuleAction__c.create({
                    'Name': 'Make a line absolute discount',
                    'SCLP__Action__c': '=',
                    'SCLP__Calc__c': f"- {z:03d}",
                    'SCLP__Order__c': 1,
                    'SCLP__SourceField__c': 'SCLP__OriginalPrice__c',
                    'SCLP__SourceObject__c': 'QuoteLineItem__c',
                    'SCLP__TargetField__c': 'SCLP__RulePrice__c',
                    'SCLP__TargetObject__c': 'QuoteLineItem__c',
                    'SCLP__Rule__c': rule_id,
                    'SCLP__ExtendedValue__c': """{"ranges":{"bounds":[],"prices":[100]},"pricingMethod":null,"notification":{}}""",
                    'SCLP__Type__c': 'EDITING',
                })

                sf.SCLP__RuleCondition__c.create({
                    'SCLP__Rule__c': rule_id,
                    'SCLP__Operator__c': 'CONTAINS',
                    'SCLP__TargetField__c': 'Name',
                    'SCLP__TargetObject__c': 'Account',
                    'SCLP__Type__c': 'FIELD',
                    'SCLP__Value__c': 'partner',
                    'SCLP__Not__c': False
                })

            else:
                existing = sf.query(
                    f"select id from Rule__c "
                    f"where name like '{z:03d} Test Rule Number%'"
                )

                if existing['records']:
                    print(f'Rule {z:03d} already exists')
                    return

                rule_id = sf.Rule__c.create({
                    'Name': f'{z:03d} Test Rule Number {timestamp}',
                    'Active__c': Is_Active,
                    'ExecutionOrder__c': z,
                    'RuleFolder__c': folder
                })['id']

                sf.RuleAction__c.create({
                    'Name': 'Make a line absolute discount',
                    'Action__c': '=',
                    'Calc__c': f"- {z:03d}",
                    'Order__c': 1,
                    'SourceField__c': 'OriginalPrice__c',
                    'SourceObject__c': 'QuoteLineItem__c',
                    'TargetField__c': 'RulePrice__c',
                    'TargetObject__c': 'QuoteLineItem__c',
                    'Rule__c': rule_id,
                    'ExtendedValue__c': """{"ranges":{"bounds":[],"prices":[100]},"pricingMethod":null,"notification":{}}""",
                    'Type__c': 'EDITING',
                })

                sf.RuleCondition__c.create({
                    'Rule__c': rule_id,
                    'Operator__c': 'CONTAINS',
                    'TargetField__c': 'Name',
                    'TargetObject__c': 'Account',
                    'Type__c': 'FIELD',
                    'Value__c': 'partner',
                    'Not__c': False
                })

            print(f'Rule {z:03d} DONE')

        except Exception as e:
            print(f'Error in rule {z:03d}: {e}')


    with ThreadPoolExecutor(max_workers=25) as executor:
        futures = [executor.submit(worker, z) for z in range(1, RECORDS_QTY)]

        for f in as_completed(futures):
            f.result()
        
def delete_all_records(object_name):
    print(f"Deleting all records from {object_name}")

    results = sf.query(f"SELECT Id, Name FROM {object_name}")

    records = results['records']

    def worker(record):
        try:
            getattr(sf, object_name).delete(record['Id'])
            print(f"Deleted {record['Name']} ({record['Id']})")
        except Exception as e:
            print(f"Error deleting {record['Name']}: {e}")

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(worker, record)
            for record in records
        ]

        for f in as_completed(futures):
            f.result()

def test():
    print('1')

def Quote_Vat():
    ps_result = sf.query("SELECT Id FROM PermissionSet WHERE Name = 'SO_Sculptor_permission_set'")
    permission_set_id = ps_result['records'][0]['Id']
    print(f"✅ Found Permission Set 'test' (Id: {permission_set_id})")
    try:
        print(f'Start creating Vat field for SCLP__Quote__c object')
        try:
            Vat_Percent_field_metadata = {
                'FullName': 'SCLP__Quote__c.VAT_Percent__c',
                'Metadata': {
                    "label": "VAT Percent",
                    "type": "Percent",
                    "precision": 18,
                    "scale": 2,
                    "description": "VAT for taxes"
                }
            }
            

            result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Vat_Percent_field_metadata)
            print(f"✅ Field Percent is created for SCLP__Quote__c!")
            print(f"Result: {result}")

            field_perm_data = {
                'ParentId': permission_set_id,
                'SobjectType': f'SCLP__Quote__c',
                'Field': f'SCLP__Quote__c.VAT_Percent__c',
                'PermissionsRead': True,
                'PermissionsEdit': True
            }

            result = sf.FieldPermissions.create(field_perm_data)
            print("✅ Vat is added for read/edit Permission Set 'SO Sculptor Permission Set'")
            print(f"Result: {result}")
        except SalesforceError as e:
            error_text = str(e)

            if "DUPLICATE_DEVELOPER_NAME" in error_text:
                print("👌 Vat Percent field already exists")
            elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                print("❌ Missing required parameter")
                raise  
            else:
                print(f"⚠️ Unhandled Salesforce error: {error_text}")
                raise
        #Tax amount
        try:
            Tax_Amount_field_metadata = {
            "FullName": "SCLP__Quote__c.Tax_Amount__c",
            "Metadata": {
                "label": "Tax Amount",
                "type": "Currency",
                "precision": 18,
                "scale": 2,
                "formula": 'SCLP__TotalAmount__c * VAT_Percent__c',         
                "description": "Tax Amount for taxes",
                "formulaTreatBlanksAs": "BlankAsZero"
            }}
                    
            

            result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Tax_Amount_field_metadata)
            print(f"✅ Tax Amount is created!")
            print(f"Result: {result}")

            field_perm_data = {
                'ParentId': permission_set_id,
                'SobjectType': f'SCLP__Quote__c',
                'Field': f'SCLP__Quote__c.Tax_Amount__c',
                'PermissionsRead': True,
                # 'PermissionsEdit': True
            }

            result = sf.FieldPermissions.create(field_perm_data)
            print("✅ Tax Amount is added for read Permission Set 'SO Sculptor Permission Set'")
            print(f"Result: {result}")
        except SalesforceError as e:
            error_text = str(e)

            if "DUPLICATE_DEVELOPER_NAME" in error_text:
                print("👌 Tax Amount field already exists")
            elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                print("❌ Missing required parameter")
                raise  
            else:
                print(f"⚠️ Unhandled Salesforce error: {error_text}")
                raise
        #Total With Tax
        try:
            Total_With_tax_field_metadata = {
            "FullName": "SCLP__Quote__c.Total_With_Tax__c",
            "Metadata": {
                "label": "Total With Tax",
                "type": "Currency",
                "precision": 18,
                "scale": 2,
                "formula": 'SCLP__TotalAmount__c + (SCLP__TotalAmount__c * VAT_Percent__c)',         
                "description": "Total With Tax for taxes",
                "formulaTreatBlanksAs": "BlankAsZero"
            }}
                    
            

            result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Total_With_tax_field_metadata)
            print(f"✅ Total With Tax is created!")
            print(f"Result: {result}")

            field_perm_data = {
                'ParentId': permission_set_id,
                'SobjectType': f'SCLP__Quote__c',
                'Field': f'SCLP__Quote__c.Total_With_Tax__c',
                'PermissionsRead': True,
                # 'PermissionsEdit': True
            }

            result = sf.FieldPermissions.create(field_perm_data)
            print("✅ Total With Tax is added for read/edit Permission Set 'SO Sculptor Permission Set'")
            print(f"Result: {result}")
        except SalesforceError as e:
            error_text = str(e)

            if "DUPLICATE_DEVELOPER_NAME" in error_text:
                print("👌 Total With Tax field already exists")
            elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                print("❌ Missing required parameter")
                raise  
            else:
                print(f"⚠️ Unhandled Salesforce error: {error_text}")
                raise
        print("➡ Creating record inside Custom Settings...")
    #custom settings
        try:
            setting_record = {
                'Name': 'Default',
                'SCLP__QuoteTaxFieldLabel__c': 'VAT %',
                'SCLP__QuoteTaxPercentField__c': 'VAT_Percent__c ',
                'SCLP__QuoteTotalWithTax__c': 'Total_With_Tax__c '


            }

            result = sf.SCLP__SculptorTaxSettings__c.create(setting_record)

            print("✅ Quote VAT is set")
            print(result)

        except SalesforceError as e:
            error_text = str(e)

            if "DUPLICATE_VALUE" in error_text:
                print("👌 Custom Setting already exist field already exists")
            elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                print("❌ Missing required parameter")
                raise  
            else:
                print(f"⚠️ Unhandled Salesforce error: {error_text}")
                raise
    except SalesforceError as e:
        "INVALID_TYPE" in str(e)
        print("no SCLP__")
        print(f'Start creating Vat field for Quote__c object')
        try:
            Vat_Percent_field_metadata = {
                'FullName': 'Quote__c.VAT_Percent__c',
                'Metadata': {
                    "label": "VAT Percent",
                    "type": "Percent",
                    "precision": 18,
                    "scale": 2,
                    "description": "VAT for taxes"
                }
            }
            

            result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Vat_Percent_field_metadata)
            print(f"✅ Field Percent is created for Quote__c!")
            print(f"Result: {result}")

            field_perm_data = {
                'ParentId': permission_set_id,
                'SobjectType': f'Quote__c',
                'Field': f'Quote__c.VAT_Percent__c',
                'PermissionsRead': True,
                'PermissionsEdit': True
            }

            result = sf.FieldPermissions.create(field_perm_data)
            print("✅ Vat is added for read/edit Permission Set 'SO Sculptor Permission Set'")
            print(f"Result: {result}")
        except SalesforceError as e:
            error_text = str(e)

            if "DUPLICATE_DEVELOPER_NAME" in error_text:
                print("👌 Vat Percent field already exists")
            elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                print("❌ Missing required parameter")
                raise  
            else:
                print(f"⚠️ Unhandled Salesforce error: {error_text}")
                raise
        #Tax amount
        try:
            Tax_Amount_field_metadata = {
            "FullName": "Quote__c.Tax_Amount__c",
            "Metadata": {
                "label": "Tax Amount",
                "type": "Currency",
                "precision": 18,
                "scale": 2,
                "formula": 'TotalAmount__c * VAT_Percent__c',         
                "description": "Tax Amount for taxes",
                "formulaTreatBlanksAs": "BlankAsZero"
            }}
                    
            

            result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Tax_Amount_field_metadata)
            print(f"✅ Tax Amount is created!")
            print(f"Result: {result}")

            field_perm_data = {
                'ParentId': permission_set_id,
                'SobjectType': f'Quote__c',
                'Field': f'Quote__c.Tax_Amount__c',
                'PermissionsRead': True,
                # 'PermissionsEdit': True
            }

            result = sf.FieldPermissions.create(field_perm_data)
            print("✅ Tax Amount is added for read Permission Set 'SO Sculptor Permission Set'")
            print(f"Result: {result}")
        except SalesforceError as e:
            error_text = str(e)

            if "DUPLICATE_DEVELOPER_NAME" in error_text:
                print("👌 Tax Amount field already exists")
            elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                print("❌ Missing required parameter")
                raise  
            else:
                print(f"⚠️ Unhandled Salesforce error: {error_text}")
                raise
        #Total With Tax
        try:
            Total_With_tax_field_metadata = {
            "FullName": "Quote__c.Total_With_Tax__c",
            "Metadata": {
                "label": "Total With Tax",
                "type": "Currency",
                "precision": 18,
                "scale": 2,
                "formula": 'TotalAmount__c + (TotalAmount__c * VAT_Percent__c)',         
                "description": "Total With Tax for taxes",
                "formulaTreatBlanksAs": "BlankAsZero"
            }}
                    
            

            result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Total_With_tax_field_metadata)
            print(f"✅ Total With Tax is created!")
            print(f"Result: {result}")

            field_perm_data = {
                'ParentId': permission_set_id,
                'SobjectType': f'Quote__c',
                'Field': f'Quote__c.Total_With_Tax__c',
                'PermissionsRead': True,
                # 'PermissionsEdit': True
            }

            result = sf.FieldPermissions.create(field_perm_data)
            print("✅ Total With Tax is added for read/edit Permission Set 'SO Sculptor Permission Set'")
            print(f"Result: {result}")
        except SalesforceError as e:
            error_text = str(e)

            if "DUPLICATE_DEVELOPER_NAME" in error_text:
                print("👌 Total With Tax field already exists")
            elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                print("❌ Missing required parameter")
                raise  
            else:
                print(f"⚠️ Unhandled Salesforce error: {error_text}")
                raise
        print("➡ Creating record inside Custom Settings...")
    #custom settings
        try:
            setting_record = {
                'Name': 'Default',
                'QuoteTaxFieldLabel__c': 'VAT %',
                'QuoteTaxPercentField__c': 'VAT_Percent__c ',
                'QuoteTotalWithTax__c': 'Total_With_Tax__c '


            }

            result = sf.SculptorTaxSettings__c.create(setting_record)

            print("✅ Quote VAT is set")
            print(result)

        except SalesforceError as e:
            error_text = str(e)

            if "DUPLICATE_VALUE" in error_text:
                print("👌 Custom Setting already exist field already exists")
            elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                print("❌ Missing required parameter")
                raise  
            else:
                print(f"⚠️ Unhandled Salesforce error: {error_text}")
                raise
def QLI_Vat():
    ps_result = sf.query("SELECT Id FROM PermissionSet WHERE Name = 'SO_Sculptor_permission_set'")
    permission_set_id = ps_result['records'][0]['Id']
    print(f"✅ Found Permission Set 'SO_Sculptor_permission_set' (Id: {permission_set_id})")
    try:
        print(f'Start creating Vat field for SCLP__QuoteLineItem__c object')
        #vat percent
        try:
            Vat_Percent_field_metadata = {
                'FullName': 'SCLP__QuoteLineItem__c.VAT_Percent__c',
                'Metadata': {
                    "label": "VAT Percent",
                    "type": "Percent",
                    "precision": 18,
                    "scale": 2,
                    "description": "VAT for taxes for QLI"
                }
            }
            

            result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Vat_Percent_field_metadata)
            print(f"✅ Field Percent is created for SCLP__QuoteLineItem__c!")
            print(f"Result: {result}")

            field_perm_data = {
                'ParentId': permission_set_id,
                'SobjectType': f'SCLP__QuoteLineItem__c',
                'Field': f'SCLP__QuoteLineItem__c.VAT_Percent__c',
                'PermissionsRead': True,
                'PermissionsEdit': True
            }

            result = sf.FieldPermissions.create(field_perm_data)
            print("✅ Percent is added for read/edit Permission Set 'SO Sculptor Permission Set'")
            print(f"Result: {result}")
        except SalesforceError as e:
            error_text = str(e)

            if "DUPLICATE_DEVELOPER_NAME" in error_text:
                print("👌 Vat Percent field already exists")
            elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                print("❌ Missing required parameter")
                raise  
            else:
                print(f"⚠️ Unhandled Salesforce error: {error_text}")
                raise
    #QLI Label
        try:
            QLI_Label_field_metadata = {
                'FullName': 'SCLP__QuoteLineItem__c.QLI_Label__c',
                'Metadata': {
                    'label': 'QLI Label',
                    'length': 255,
                    'type': 'Text',
                    "description": "Quote Line Item Label for taxes"
                }
            }
            

            result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=QLI_Label_field_metadata)
            print(f"✅ Label is created for SCLP__QuoteLineItem__c!")
            print(f"Result: {result}")

            field_perm_data = {
                'ParentId': permission_set_id,
                'SobjectType': f'SCLP__QuoteLineItem__c',
                'Field': f'SCLP__QuoteLineItem__c.QLI_Label__c',
                'PermissionsRead': True,
                'PermissionsEdit': True
            }

            result = sf.FieldPermissions.create(field_perm_data)
            print("✅ Label is added for read/edit Permission Set 'SO Sculptor Permission Set'")
            print(f"Result: {result}")
        except SalesforceError as e:
            error_text = str(e)

            if "DUPLICATE_DEVELOPER_NAME" in error_text:
                print("👌 Label field already exists")
            elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                print("❌ Missing required parameter")
                raise  
            else:
                print(f"⚠️ Unhandled Salesforce error: {error_text}")
                raise
    #Tax Amount Formula
        try:
            Tax_Amount_Formula_field_metadata = {
            "FullName": "SCLP__QuoteLineItem__c.Tax_Amount_Formula__c",
            "Metadata": {
                "label": "Tax Amount Formula",
                "type": "Currency",
                "precision": 18,
                "scale": 2,
                "formula": 'SCLP__CustomerPrice__c * Vat_Percent__c',         
                "description": "Tax Amount formula for QLI",
                "formulaTreatBlanksAs": "BlankAsZero"
            }}
            
            

            result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Tax_Amount_Formula_field_metadata)
            print(f"✅ Label is created for SCLP__QuoteLineItem__c!")
            print(f"Result: {result}")

            field_perm_data = {
                'ParentId': permission_set_id,
                'SobjectType': f'SCLP__QuoteLineItem__c',
                'Field': f'SCLP__QuoteLineItem__c.Tax_Amount_Formula__c',
                'PermissionsRead': True,
                # 'PermissionsEdit': True
            }

            result = sf.FieldPermissions.create(field_perm_data)
            print("✅ Tax Amount formula is added for read/edit Permission Set 'SO Sculptor Permission Set'")
            print(f"Result: {result}")
        except SalesforceError as e:
            error_text = str(e)

            if "DUPLICATE_DEVELOPER_NAME" in error_text:
                print("👌 Tax Amount formula field already exists")
            elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                print("❌ Missing required parameter")
                raise  
            else:
                print(f"⚠️ Unhandled Salesforce error: {error_text}")
                raise
    #Total With Tax
        try:
            Total_With_tax_field_metadata = {
            "FullName": "SCLP__QuoteLineItem__c.Total_With_Tax__c",
            "Metadata": {
                "label": "Total With Tax",
                "type": "Currency",
                "precision": 18,
                "scale": 2,
                "formula": 'SCLP__CustomerPrice__c + Tax_Amount_Formula__c',         
                "description": "Total With Tax for taxes",
                "formulaTreatBlanksAs": "BlankAsZero"
            }}
                    
            

            result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Total_With_tax_field_metadata)
            print(f"✅ Total With Tax is created!")
            print(f"Result: {result}")

            field_perm_data = {
                'ParentId': permission_set_id,
                'SobjectType': f'SCLP__QuoteLineItem__c',
                'Field': f'SCLP__QuoteLineItem__c.Total_With_Tax__c',
                'PermissionsRead': True,
                # 'PermissionsEdit': True
            }

            result = sf.FieldPermissions.create(field_perm_data)
            print("✅ Total With Tax is added for read Permission Set 'SO Sculptor Permission Set'")
            print(f"Result: {result}")
        except SalesforceError as e:
            error_text = str(e)

            if "DUPLICATE_DEVELOPER_NAME" in error_text:
                print("👌 Total With Tax field already exists")
            elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                print("❌ Missing required parameter")
                raise  
            else:
                print(f"⚠️ Unhandled Salesforce error: {error_text}")
                raise

    #Rollup summary next step
        try:
            Taxes_rollup_field_metadata = {
            "FullName": "SCLP__Quote__c.Total_of_VATs__c",
            "Metadata": {
                "label": "Total of VATs",
                "type": "Summary",
                "summaryForeignKey": "SCLP__QuoteLineItem__c.SCLP__Quote__c",
                "description": "Total of vats for taxes",
                "summarizedField" : "SCLP__QuoteLineItem__c.Total_With_Tax__c",
                "summaryOperation": "SUM"
            }}
            
            

            result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Taxes_rollup_field_metadata)
            print(f"✅ Rollup is created for SCLP__Quote__c!")
            print(f"Result: {result}")

            field_perm_data = {
                'ParentId': permission_set_id,
                'SobjectType': f'SCLP__Quote__c',
                'Field': f'SCLP__Quote__c.Total_of_VATs__c',
                'PermissionsRead': True,
                # 'PermissionsEdit': True
            }

            result = sf.FieldPermissions.create(field_perm_data)
            print("✅ Rollup is added for read Permission Set 'SO Sculptor Permission Set'")
            print(f"Result: {result}")
        except SalesforceError as e:
            error_text = str(e)

            if "DUPLICATE_DEVELOPER_NAME" in error_text:
                print("👌 Rollup field already exists")
            elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                print("❌ Missing required parameter")
                raise  
            else:
                print(f"⚠️ Unhandled Salesforce error: {error_text}")
                raise
            #Total With Tax
            try:
                Total_With_tax_field_with_rollup_metadata = {
                "FullName": "SCLP__Quote__c.Total_With_Tax_with_rollup__c",
                "Metadata": {
                    "label": "Total With Tax with rollup",
                    "type": "Currency",
                    "precision": 18,
                    "scale": 2,
                    "formula": 'SCLP__TotalAmount__c + (SCLP__TotalAmount__c * VAT_Percent__c) + Total_of_VATs__c',         
                    "description": "Total With Tax with rollup for taxes",
                    "formulaTreatBlanksAs": "BlankAsZero"
                }}
                        
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Total_With_tax_field_with_rollup_metadata)
                print(f"✅ Total With Tax is created!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'SCLP__Quote__c',
                    'Field': f'SCLP__Quote__c.Total_With_Tax_with_rollup__c',
                    'PermissionsRead': True,
                    # 'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Total With Tax with rollup is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Total With Tax with rollup field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise

    #custom setting update
        print("➡ Creating Custom Setting record...")

        setting_record = {
            'Name': 'Default',
            'SCLP__QuoteTotalWithTax__c': 'Total_With_Tax_with_rollup__c',
            'SCLP__LineItemTaxFieldLabel__c': 'QLI VAT',
            'SCLP__LineItemTaxAmountField__c': 'Tax_Amount__c',
            'SCLP__LineItemTaxPercentField__c': 'VAT_Percent__c',
            'SCLP__LineItemTotalWithTax__c': 'Total_With_Tax__c'
        }

        try:
            result = sf.SCLP__SculptorTaxSettings__c.create(setting_record)
            print("🆕 Custom Setting created")
            print(result)

        except SalesforceError as e:
            err = str(e)
            print(f"⚠ Create failed: {err}")
            print("➡ Trying to update...")


            existing = sf.query("""
                SELECT Id 
                FROM SCLP__SculptorTaxSettings__c 
                WHERE Name = 'Default'
                LIMIT 1
            """)

            if existing['totalSize'] == 0:
                raise Exception("❌ Record not found to update")

            rec_id = existing['records'][0]['Id']

            sf.SCLP__SculptorTaxSettings__c.update(rec_id, setting_record)

            print("♻ Custom Setting updated")


    #adding VAT to Quote Builder
        with sync_playwright() as p:
        # Connect to the existing browser instance
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()  # Using the first context
            page = context.new_page()  # Taking the first tab

            page.goto(SITE_URL)
            username_input = page.locator('input[id="username"]')
            password_input = page.locator('input[id="password"]')
            username_input.fill(USERNAME)
            password_input.fill(PASSWORD)
            page.press('input[id="password"]', 'Enter')


            page.wait_for_selector('button[title="App Launcher"]', state='visible')
            time.sleep(1)
            page.click('button[title="App Launcher"]')

            page.fill('input.slds-input[placeholder="Search apps and items..."]', 'Sculptor CPQ')
            page.wait_for_selector('text="Sculptor CPQ"', state='visible')
            time.sleep(1)
            page.click('text="Sculptor CPQ"')

            Sculptor_settings_tab = ('//span[contains(text(), "Sculptor Settings")]')
            Fields_and_layouts = ('//a[contains(text(), "Fields and Layouts")]')
            Sculptor_settings_QLI_VAT = ("//div[@role='group' and .//*[text()='Quote Builder Fields']]//*[text()='VAT Percent']") # ('//div[normalize-space(text())="Sidebar Product Fields"]/ancestor::div[contains(@part, "dual-listbox")]//span[text()="Active"]')
            Sculptor_settings_QLI_VAT_move_right = ("//div[text()='Quote Builder Fields']//following::button[contains(@title, 'Move')][1]")
            
            Sculptor_settings_Quote_VAT = ("//div[@role='group' and .//*[text()='Quote Fields for Quote Details']]//*[text()='VAT Percent']") # ('//div[normalize-space(text())="Sidebar Product Fields"]/ancestor::div[contains(@part, "dual-listbox")]//span[text()="Active"]')
            Sculptor_settings_Quote_VAT_move_right = ("//div[text()='Quote Fields for Quote Details']//following::button[contains(@title, 'Move')][1]")
            
            Sculptor_settings_Save_Success_message = ("//*[text()='Configurations successfully updated']")
            Save_Button = ("(//button[contains(text(), 'Save')])[last()]")
            page.wait_for_selector(Sculptor_settings_tab, state='visible')
            page.click(Sculptor_settings_tab)

            page.wait_for_selector(Fields_and_layouts, state='visible')
            page.click(Fields_and_layouts)
            
            page.wait_for_selector(Sculptor_settings_QLI_VAT, state='visible')
            page.click(Sculptor_settings_QLI_VAT)

            page.wait_for_selector(Sculptor_settings_QLI_VAT_move_right, state='visible')
            page.click(Sculptor_settings_QLI_VAT_move_right)

            page.wait_for_selector(Sculptor_settings_Quote_VAT, state='visible')
            page.click(Sculptor_settings_Quote_VAT)
            page.wait_for_selector(Sculptor_settings_Quote_VAT_move_right, state='visible')
            page.click(Sculptor_settings_Quote_VAT_move_right)

            page.wait_for_selector(Save_Button, state='visible')
            page.click(Save_Button)

            page.wait_for_selector(Sculptor_settings_Save_Success_message, state='visible')
    except SalesforceError as e:
        "INVALID_TYPE" in str(e)
        print("no SCLP__")
        print(f'Start creating Vat field for QuoteLineItem__c object')
        #vat percent
        try:
            Vat_Percent_field_metadata = {
                'FullName': 'QuoteLineItem__c.VAT_Percent__c',
                'Metadata': {
                    "label": "VAT Percent",
                    "type": "Percent",
                    "precision": 18,
                    "scale": 2,
                    "description": "VAT for taxes for QLI"
                }
            }
            

            result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Vat_Percent_field_metadata)
            print(f"✅ Field Percent is created for QuoteLineItem__c!")
            print(f"Result: {result}")

            field_perm_data = {
                'ParentId': permission_set_id,
                'SobjectType': f'QuoteLineItem__c',
                'Field': f'QuoteLineItem__c.VAT_Percent__c',
                'PermissionsRead': True,
                'PermissionsEdit': True
            }

            result = sf.FieldPermissions.create(field_perm_data)
            print("✅ Percent is added for read/edit Permission Set 'SO Sculptor Permission Set'")
            print(f"Result: {result}")
        except SalesforceError as e:
            error_text = str(e)

            if "DUPLICATE_DEVELOPER_NAME" in error_text:
                print("👌 Vat Percent field already exists")
            elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                print("❌ Missing required parameter")
                raise  
            else:
                print(f"⚠️ Unhandled Salesforce error: {error_text}")
                raise
    #QLI Label
        try:
            QLI_Label_field_metadata = {
                'FullName': 'QuoteLineItem__c.QLI_Label__c',
                'Metadata': {
                    'label': 'QLI Label',
                    'length': 255,
                    'type': 'Text',
                    "description": "Quote Line Item Label for taxes"
                }
            }
            

            result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=QLI_Label_field_metadata)
            print(f"✅ Label is created for QuoteLineItem__c!")
            print(f"Result: {result}")

            field_perm_data = {
                'ParentId': permission_set_id,
                'SobjectType': f'QuoteLineItem__c',
                'Field': f'QuoteLineItem__c.QLI_Label__c',
                'PermissionsRead': True,
                'PermissionsEdit': True
            }

            result = sf.FieldPermissions.create(field_perm_data)
            print("✅ Label is added for read/edit Permission Set 'SO Sculptor Permission Set'")
            print(f"Result: {result}")
        except SalesforceError as e:
            error_text = str(e)

            if "DUPLICATE_DEVELOPER_NAME" in error_text:
                print("👌 Label field already exists")
            elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                print("❌ Missing required parameter")
                raise  
            else:
                print(f"⚠️ Unhandled Salesforce error: {error_text}")
                raise
    #Tax Amount Formula
        try:
            Tax_Amount_Formula_field_metadata = {
            "FullName": "QuoteLineItem__c.Tax_Amount_Formula__c",
            "Metadata": {
                "label": "Tax Amount Formula",
                "type": "Currency",
                "precision": 18,
                "scale": 2,
                "formula": 'CustomerPrice__c * Vat_Percent__c',         
                "description": "Tax Amount formula for QLI",
                "formulaTreatBlanksAs": "BlankAsZero"
            }}
            
            

            result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Tax_Amount_Formula_field_metadata)
            print(f"✅ Label is created for QuoteLineItem__c!")
            print(f"Result: {result}")

            field_perm_data = {
                'ParentId': permission_set_id,
                'SobjectType': f'QuoteLineItem__c',
                'Field': f'QuoteLineItem__c.Tax_Amount_Formula__c',
                'PermissionsRead': True,
                # 'PermissionsEdit': True
            }

            result = sf.FieldPermissions.create(field_perm_data)
            print("✅ Tax Amount formula is added for read/edit Permission Set 'SO Sculptor Permission Set'")
            print(f"Result: {result}")
        except SalesforceError as e:
            error_text = str(e)

            if "DUPLICATE_DEVELOPER_NAME" in error_text:
                print("👌 Tax Amount formula field already exists")
            elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                print("❌ Missing required parameter")
                raise  
            else:
                print(f"⚠️ Unhandled Salesforce error: {error_text}")
                raise
    #Total With Tax
        try:
            Total_With_tax_field_metadata = {
            "FullName": "QuoteLineItem__c.Total_With_Tax__c",
            "Metadata": {
                "label": "Total With Tax",
                "type": "Currency",
                "precision": 18,
                "scale": 2,
                "formula": 'CustomerPrice__c + Tax_Amount_Formula__c',         
                "description": "Total With Tax for taxes",
                "formulaTreatBlanksAs": "BlankAsZero"
            }}
                    
            

            result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Total_With_tax_field_metadata)
            print(f"✅ Total With Tax is created!")
            print(f"Result: {result}")

            field_perm_data = {
                'ParentId': permission_set_id,
                'SobjectType': f'QuoteLineItem__c',
                'Field': f'QuoteLineItem__c.Total_With_Tax__c',
                'PermissionsRead': True,
                # 'PermissionsEdit': True
            }

            result = sf.FieldPermissions.create(field_perm_data)
            print("✅ Total With Tax is added for read Permission Set 'SO Sculptor Permission Set'")
            print(f"Result: {result}")
        except SalesforceError as e:
            error_text = str(e)

            if "DUPLICATE_DEVELOPER_NAME" in error_text:
                print("👌 Total With Tax field already exists")
            elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                print("❌ Missing required parameter")
                raise  
            else:
                print(f"⚠️ Unhandled Salesforce error: {error_text}")
                raise

    #Rollup summary next step
        try:
            Taxes_rollup_field_metadata = {
            "FullName": "Quote__c.Total_of_VATs__c",
            "Metadata": {
                "label": "Total of VATs",
                "type": "Summary",
                "summaryForeignKey": "QuoteLineItem__c.Quote__c",
                "description": "Total of vats for taxes",
                "summarizedField" : "QuoteLineItem__c.Total_With_Tax__c",
                "summaryOperation": "SUM"
            }}
            
            

            result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Taxes_rollup_field_metadata)
            print(f"✅ Rollup is created for Quote__c!")
            print(f"Result: {result}")

            field_perm_data = {
                'ParentId': permission_set_id,
                'SobjectType': f'Quote__c',
                'Field': f'Quote__c.Total_of_VATs__c',
                'PermissionsRead': True,
                # 'PermissionsEdit': True
            }

            result = sf.FieldPermissions.create(field_perm_data)
            print("✅ Rollup is added for read Permission Set 'SO Sculptor Permission Set'")
            print(f"Result: {result}")
        except SalesforceError as e:
            error_text = str(e)

            if "DUPLICATE_DEVELOPER_NAME" in error_text:
                print("👌 Rollup field already exists")
            elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                print("❌ Missing required parameter")
                raise  
            else:
                print(f"⚠️ Unhandled Salesforce error: {error_text}")
                raise
            #Total With Tax
            try:
                Total_With_tax_field_with_rollup_metadata = {
                "FullName": "Quote__c.Total_With_Tax_with_rollup__c",
                "Metadata": {
                    "label": "Total With Tax with rollup",
                    "type": "Currency",
                    "precision": 18,
                    "scale": 2,
                    "formula": 'TotalAmount__c + (TotalAmount__c * VAT_Percent__c) + Total_of_VATs__c',         
                    "description": "Total With Tax with rollup for taxes",
                    "formulaTreatBlanksAs": "BlankAsZero"
                }}
                        
                

                result = sf.toolingexecute('sobjects/CustomField/', method='POST', data=Total_With_tax_field_with_rollup_metadata)
                print(f"✅ Total With Tax is created!")
                print(f"Result: {result}")

                field_perm_data = {
                    'ParentId': permission_set_id,
                    'SobjectType': f'Quote__c',
                    'Field': f'Quote__c.Total_With_Tax_with_rollup__c',
                    'PermissionsRead': True,
                    # 'PermissionsEdit': True
                }

                result = sf.FieldPermissions.create(field_perm_data)
                print("✅ Total With Tax with rollup is added for read/edit Permission Set 'SO Sculptor Permission Set'")
                print(f"Result: {result}")
            except SalesforceError as e:
                error_text = str(e)

                if "DUPLICATE_DEVELOPER_NAME" in error_text:
                    print("👌 Total With Tax with rollup field already exists")
                elif "FIELD_INTEGRITY_EXCEPTION" in error_text:
                    print("❌ Missing required parameter")
                    raise  
                else:
                    print(f"⚠️ Unhandled Salesforce error: {error_text}")
                    raise

    #custom setting update
        print("➡ Creating Custom Setting record...")

        setting_record = {
            'Name': 'Default',
            'QuoteTotalWithTax__c': 'Total_With_Tax_with_rollup__c',
            'LineItemTaxFieldLabel__c': 'QLI VAT',
            'LineItemTaxAmountField__c': 'Tax_Amount__c',
            'LineItemTaxPercentField__c': 'VAT_Percent__c',
            'LineItemTotalWithTax__c': 'Total_With_Tax__c'
        }

        try:
            result = sf.SculptorTaxSettings__c.create(setting_record)
            print("🆕 Custom Setting created")
            print(result)

        except SalesforceError as e:
            err = str(e)
            print(f"⚠ Create failed: {err}")
            print("➡ Trying to update...")


            existing = sf.query("""
                SELECT Id 
                FROM SculptorTaxSettings__c 
                WHERE Name = 'Default'
                LIMIT 1
            """)

            if existing['totalSize'] == 0:
                raise Exception("❌ Record not found to update")

            rec_id = existing['records'][0]['Id']

            sf.SculptorTaxSettings__c.update(rec_id, setting_record)

            print("♻ Custom Setting updated")


    #adding VAT to Quote Builder
        with sync_playwright() as p:
        # Connect to the existing browser instance
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()  # Using the first context
            page = context.new_page()  # Taking the first tab

            page.goto(SITE_URL)
            username_input = page.locator('input[id="username"]')
            password_input = page.locator('input[id="password"]')
            username_input.fill(USERNAME)
            password_input.fill(PASSWORD)
            page.press('input[id="password"]', 'Enter')


            page.wait_for_selector('button[title="App Launcher"]', state='visible')
            time.sleep(1)
            page.click('button[title="App Launcher"]')

            page.fill('input.slds-input[placeholder="Search apps and items..."]', 'Sculptor CPQ')
            page.wait_for_selector('text="Sculptor CPQ"', state='visible')
            time.sleep(1)
            page.click('text="Sculptor CPQ"')

            Sculptor_settings_tab = ('//span[contains(text(), "Sculptor Settings")]')
            Fields_and_layouts = ('//a[contains(text(), "Fields and Layouts")]')
            Sculptor_settings_QLI_VAT = ("//div[@role='group' and .//*[text()='Quote Builder Fields']]//*[text()='VAT Percent']") # ('//div[normalize-space(text())="Sidebar Product Fields"]/ancestor::div[contains(@part, "dual-listbox")]//span[text()="Active"]')
            Sculptor_settings_QLI_VAT_move_right = ("//div[text()='Quote Builder Fields']//following::button[contains(@title, 'Move')][1]")
            
            Sculptor_settings_Quote_VAT = ("//div[@role='group' and .//*[text()='Quote Fields for Quote Details']]//*[text()='VAT Percent']") # ('//div[normalize-space(text())="Sidebar Product Fields"]/ancestor::div[contains(@part, "dual-listbox")]//span[text()="Active"]')
            Sculptor_settings_Quote_VAT_move_right = ("//div[text()='Quote Fields for Quote Details']//following::button[contains(@title, 'Move')][1]")
            
            Sculptor_settings_Save_Success_message = ("//*[text()='Configurations successfully updated']")
            Save_Button = ("(//button[contains(text(), 'Save')])[last()]")
            page.wait_for_selector(Sculptor_settings_tab, state='visible')
            page.click(Sculptor_settings_tab)

            page.wait_for_selector(Fields_and_layouts, state='visible')
            page.click(Fields_and_layouts)
            
            page.wait_for_selector(Sculptor_settings_QLI_VAT, state='visible')
            page.click(Sculptor_settings_QLI_VAT)

            page.wait_for_selector(Sculptor_settings_QLI_VAT_move_right, state='visible')
            page.click(Sculptor_settings_QLI_VAT_move_right)

            page.wait_for_selector(Sculptor_settings_Quote_VAT, state='visible')
            page.click(Sculptor_settings_Quote_VAT)
            page.wait_for_selector(Sculptor_settings_Quote_VAT_move_right, state='visible')
            page.click(Sculptor_settings_Quote_VAT_move_right)

            page.wait_for_selector(Save_Button, state='visible')
            page.click(Save_Button)

            page.wait_for_selector(Sculptor_settings_Save_Success_message, state='visible')
   

def test():
    result = sf.query("""SELECT Id, Name, test_Checkbox__c, test_Text__c, test_Number__c 
                      from Quote__c 
                      where name like '%65%'""")

    IDs = [record["Id"] for record in result["records"]]
    print(IDs)
    # IDs = ['a0AC1000002bwS5MAI', 'a0AC1000002bwVKMAY']
    for i in IDs:
        sf.Quote__c.update(i, {'test_Number__c': 123})
        print(f'the product with id {i} is updated')

# permission_set_creation()
# print('Permission set ended')
# create_fields()
# print('Product fields ended')
# create_products_and_pricebook_entries()
# print("Product added ended")
# delete_test_product_salesforce()
# print("products deleted")
# Standard_PriceBook_activation()
# print('PB ended')
# create_account()
# print('account ended')
# create_opportunity()
# print('Opportunity ended')
# # create_Quote()
# # print('Quote ended')
# # delete_all_quotes()
# # print('all quotes deleted')
# delete_bundle()
# print('Bundle deleted')
# create_big_bundle()
# print("big bundle ended")
# create_normal_bundle()
# print("normal bundle ended")
# Community_Cost_Price_enabling()
# print('Cost Price enabled')
# create_multiple_quotes_core()  
# print('Multiple Quotes core created')
# create_multiple_quotes_community_no_opportunities()  
# print('Multiple Quotes for community created')
# create_blocks()
# print('create_blocks ended')
create_Pricing_Rule()
print('create Pricing Rule ended')
# delete_all_records('sclp__rule__c')
# print('all records deleted')
# Quote_Vat()
# print('Quote VAT is set')
# QLI_Vat()
# print('QLI vat ended')
# test()
# print('test')