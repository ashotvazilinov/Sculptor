import config
from simple_salesforce import Salesforce
import html_elements
sf = Salesforce(
    username= config.LOGIN,
    password= config.PASSWORD,
    security_token=config.SECURITY_TOKEN,
    domain='login'
)

soql = "select name, id from Product2 where name = 'Test Product'"
result = sf.query(soql)

for one_product in result['records']:
    sf.Product2.delete(one_product['Id'])
    print(f"Удалено: {one_product['Id']}")

