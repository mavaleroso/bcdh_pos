from faker import Faker
from main.models import Location, Generic, SubGeneric, Unit, Company, ClientType, Brand, ItemType, Discounts
import numpy as np
import random

fake = Faker()
Faker.seed(313)

generic_name = ['Oxytocin', 'Co-amoxiclav', 'Clindamycin', 'Docusate Sodium', 'Paracetamol/Orphenadrine Tablet', 'BUDESONIDE',
                'CEFUROXIME', 'FEBUXOSTAT', 'Aluminum/magnesium/Semiticone', 'AMLODIPINE', 'Amoxicillin', 'CEFIXIME', 'CITIRIZINE',
                'MEtronidazole', 'Multivitamins/Buclizine']

sub_generic_name = ['GYNE-TOCIN/AMBTOCYN', 'EUROCLAV/XOVAX', 'INDIMAX', 'IRWAX', 'NEOTIC', 'ORPHEN PLUS',
                    'MEDCORT', 'JAZCEF', 'FEBUNAZ', 'Alsium', 'AMLO-10', 'Altomox', 'CEFTRI',
                    'ALTOXIME', 'ALLERCEF', 'Aldazole', 'Appetal']

unit_name = ['Box', 'Pack', 'Bottle']
item_type = ['Medicine', 'Supply']
company_name = ['CMN PHARMA INC.', 'ALL BIO PHARMA', 'ALTOMED PHARMACEUTICALS INC.',
                'D & G PHARMA', 'DEMS TRADING', 'GEN PHARMA DIST.CO.', 'ECE MARKETING']
brand_name = ['Paracetamol', 'Biogesic', 'Calpol', 'Neozep', 'Solmux']
client_type = ['Walk-in', 'Out-patient', 'In-patient']
discount = ['PWD', 'Senior Citizen', 'OPD', 'Corporators', 'Special']
location_sample = ['Main', 'Emergency', 'Others']
discount_percentage = [20, 20, 6, 20, 0]
fixed_amount = [False, False, False, False, True]


active = True
possible_status = ['published', 'drafs']

for gen in generic_name:
    gen_val = Generic(name=gen, is_active=active,
                      created_at=fake.date_time(), updated_at=fake.date_time())
    gen_val.save()

for sub_gen in sub_generic_name:
    sub_gen_val = SubGeneric(name=sub_gen, is_active=active,
                             created_at=fake.date_time(), updated_at=fake.date_time())
    sub_gen_val.save()

for unit in unit_name:
    unit_val = Unit(name=unit, created_at=fake.date_time(),
                    updated_at=fake.date_time())
    unit_val.save()

for itemtype in item_type:
    item_val = ItemType(
        name=itemtype, created_at=fake.date_time(), updated_at=fake.date_time())
    item_val.save()

for client in client_type:
    client_val = ClientType(
        name=client, created_at=fake.date_time(), updated_at=fake.date_time())
    client_val.save()

for company in company_name:
    com_val = Company(name=company, code=fake.sbn9(), address=fake.unique.address(
    ), remarks=company,  created_at=fake.date_time(), updated_at=fake.date_time())
    com_val.save()

for brand in brand_name:
    brand_val = Brand(name=brand, created_at=fake.date_time(),
                      updated_at=fake.date_time())
    brand_val.save()

for i in range(len(discount)):
    discount_val = Discounts(name=discount[i], percentage=discount_percentage[i],
                             is_fixed_amount=fixed_amount[i], created_at=fake.date_time(), updated_at=fake.date_time())
    discount_val.save()

# custom

for i in range(len(location_sample)):
    location_db = Location(
        name=location_sample[i], created_at=fake.date_time(), updated_at=fake.date_time())
    location_db.save()
