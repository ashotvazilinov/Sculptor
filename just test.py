import config
from simple_salesforce import Salesforce

sf = Salesforce(
    username= config.LOGIN,
    password= config.PASSWORD,
    security_token=config.SECURITY_TOKEN,
    domain='login'
)

query = "select name, id from Product2 where name = 'Test Product'"
result = sf.query(query)

for product in result['records']:
    sf.Product2.delete(product['Id'])
    print(f"Удалено: {product['Id']}")

