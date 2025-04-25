from simple_salesforce import Salesforce
import config

# Подключение к Salesforce
sf = Salesforce(username=config.LOGIN, password=config.PASSWORD, security_token=config.SECURITY_TOKEN)

# Функция для удаления продуктов
def delete_products():
    for i in range (1, 6):
        results = sf.query(f"SELECT Name, Id FROM Product2 WHERE Name = 'Test Product to be deleted {i}'")

        while results:
            # Если есть записи, пытаемся удалить их
            if 'records' in results and len(results['records']) > 0:
                for record in results['records']:
                    product_id = record['Id']
                    product_name = record['Name']
                    
                    try:
                        # Удаляем продукт
                        sf.Product2.delete(product_id)
                        print(f"Product '{product_name}' with ID {product_id} has been deleted.")
                    except Exception as e:
                        print(f"An error occurred while deleting the product '{product_name}': {e}")

            # Проверяем, есть ли следующая страница данных
            if results.get('nextRecordsUrl'):
                results = sf.query_more(results['nextRecordsUrl'], True)
                print("Next page of results:", results)
            else:
                break  # Если нет следующей страницы, завершаем цикл

# Вызываем функцию для удаления продуктов


def create_products_and_pricebook_entries():
    for i in range(1, 6):  # Цикл для создания 5 продуктов
        product_name = f"Test Product to be deleted {i}"

        # Создаем продукт
        product = sf.Product2.create({
            'Name': product_name,
            'IsActive': True
        })

        # Получаем Id стандартного прайсбука
        pricebook_id = None
        pricebook_entries = sf.query("SELECT Id, Name FROM Pricebook2 WHERE IsStandard = TRUE")
        for entry in pricebook_entries['records']:
            if entry['Name'] == 'Standard Price Book':
                pricebook_id = entry['Id']
                break

        if not pricebook_id:
            print("Standard Price Book not found!")
            continue

        # Задаем цену для текущего продукта (1, 2, 3, 4, 5)
        price = i  

        # Проверяем, существует ли уже запись для данного продукта и прайсбука
        existing_entry = sf.query(f"SELECT Id FROM PricebookEntry WHERE Pricebook2Id = '{pricebook_id}' AND Product2Id = '{product['id']}'")
        if existing_entry['totalSize'] == 0:
            # Если записи нет, создаем новую
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

# Вызываем функцию для создания продуктов и привязки к прайсбуку
create_products_and_pricebook_entries()
# delete_products()
# delete_opportunity()