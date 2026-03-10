import random
products = ['Green Ear Cushions for T-Earbuds 21;200;;TECG21',
'Designer Box for T-Phone 21;150;;TDBTP21',
'T-Phone 21 128 GB;1500;Latest generation of smartphones, offering OLED displays, 5G connectivity, the T14 chip for better performance, improved cameras.;TP12821',
'Black Silicone Case for T-Phone 21;150;The silky, soft-touch finish of the silicone exterior feels great in your hand.;TSCB21',
'Green Silicone Case for T-Phone 21;250;The silky, soft-touch finish of the silicone exterior feels great in your hand.;TSCG21',
'Black Ear Cushions for T-Earbuds 21;200;;TECB21',
'Repair Insurance T2000;2000;The service provides the ability to repair malfunctions of a smartphone, tablet and headphones.;TRI200021',
'Memory Card 512 GB;30;An electronic data storage device used for storing digital information, typically using flash memory.;TMC51221',
'Box for T-Earbuds 21;50;;TBTE21',
'Designer Box for T-Earbuds 21;125;;TDBTE21',
'Headphones with 3.5 mm Plug;80;;TH21',
'20W USB-C Charger;100;20W USB‑C Charger offers fast, efficient charging at home, in the office, or on the go.;TC21',
'T-Band 21;500;Fitnes-band, that incorporates fitness tracking, health-oriented capabilities, integrates with Android, iOS and other products and services.;TB21',
'T-Earbuds 21;300;Wireless Bluetooth earbuds.;TE21',
'Box for T-Phone 21;50;;TBTP21',
'Repair Insurance T1000;1000;The service provides the ability to repair malfunctions of a smartphone or tablet.;TRI100021',
'Repair Insurance T300;300;The service provides the ability to repair malfunctions of a smartphone or tablet.;TRI30021',
'T-Phone 21 512 GB;2000;Latest generation of smartphones, offering OLED displays, 5G connectivity, the T14 chip for better performance, improved cameras.;TP51221',]

product_name = products[0].split(';')[0]
product_price = float(products[0].split(';')[1])
product_description = products[0].split(';')[2]
product_code = products[0].split(';')[3]
new_price = (float(products[0].split(';')[1]))*random.choice([0.5, 1.5])
# print(product_name)
# print(product_price)
# print(product_description)
# print(product_code)
print(new_price)

