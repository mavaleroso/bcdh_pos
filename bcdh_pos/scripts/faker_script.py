from faker import Faker
from main.models import Location, Generic, SubGeneric, Unit,Company,ClientType,Brand, ItemType, Discounts, SystemConfiguration, Clients, UserDetails, RoleDetails
import numpy as np
import random
import datetime

fake = Faker()
Faker.seed(313)

generic_name = ['Oxytocin','Co-amoxiclav','Clindamycin','Docusate Sodium','Paracetamol/Orphenadrine Tablet','BUDESONIDE',
                'CEFUROXIME','FEBUXOSTAT','Aluminum/magnesium/Semiticone','AMLODIPINE','Amoxicillin','CEFIXIME','CITIRIZINE',
                'MEtronidazole','Multivitamins/Buclizine','Multivitamins/Zinc','Hexaminine']

sub_generic_name = ['GYNE-TOCIN/AMBTOCYN','EUROCLAV/XOVAX','INDIMAX','IRWAX','NEOTIC','ORPHEN PLUS',
                'MEDCORT','JAZCEF','FEBUNAZ','Alsium','AMLO-10','Altomox','CEFTRI',
                'ALTOXIME','ALLERCEF','Aldazole','Appetal']

unit_name = ['Box','Pack','Bottle']
item_type = ['Medicine','Supply']
company_name = ['CMN PHARMA INC.','ALL BIO PHARMA','ALTOMED PHARMACEUTICALS INC.','D & G PHARMA','DEMS TRADING','GEN PHARMA DIST.CO.','ECE MARKETING']
company_code = ['CPI', 'ABP', 'API','DGP','DT','GPDC','EM']
status = ['Active','Inactive']
brand_name = ['Paracetamol','Biogesic','Calpol','Neozep','Solmux']
client_type = ['Walk-in','Out-patient','In-patient']
discount = ['PWD','Senior Citizen','OPD','Corporators','Special']
discount_percentage = [20,20,6,20,0]
fixed_amount = [False,False,False,False,True] 


clients_name = ['Reymark','Jonas','Marwen','Alexis']
middle_name = ['N','A','A','B']
last_name = ['Valdehueza','Docdoc','Valeroso','Villanueva']


client_type_id = ['1','2','3','1']
sub_generic_id = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17']

role_details = ['Admin','Inventory Staff','Management','Sales Staff']



active = True
possible_status = ['published','drafs']

for gen in generic_name: 
    gen_val = Generic(name=gen,is_active = active)
    gen_val.save()

# for sub_gen in sub_generic_name: 
#     sub_gen_val = SubGeneric(name=sub_gen,is_active = active)
#     sub_gen_val.save()

for i in range(len(sub_generic_name)):
    sub_gen_val = SubGeneric(name=sub_generic_name[i],is_active = active,generic_id = sub_generic_id[i])
    sub_gen_val.save()

for unit in unit_name:
    unit_val = Unit(name=unit)
    unit_val.save()

for itemtype in item_type:
    item_val = ItemType(name=itemtype)
    item_val.save()

for client in client_type:
    client_val = ClientType(name=client)
    client_val.save()

for i in range(len(company_name)):
    com_val = Company(name=company_name[i],code = company_code[i],address =fake.unique.address(),remarks =company_name[i])
    com_val.save()

# for company in company_name:
#     com_val = Company(name=company,code=fake.sbn9(),address =fake.unique.address(),remarks =company,  created_at = fake.date_time(), updated_at =fake.date_time())
#     com_val.save()

for brand in brand_name:
    brand_val = Brand(name=brand)
    brand_val.save()

for i in range(len(discount)):
    discount_val = Discounts(name=discount[i],percentage = discount_percentage[i],is_fixed_amount =fixed_amount[i])
    discount_val.save()

# custom 
for i in range(20):
    location_db = Location(name=fake.address())
    location_db.save()
    
for i in range(len(clients_name)):
    db_cl = Clients(first_name=clients_name[i],middle_name = middle_name[i],last_name =last_name[i],birthdate =datetime.date.today(),sex="Male",address=fake.unique.address(),occupation=fake.address(),client_type_id =client_type_id[i] )
    db_cl.save()
    
for roles in role_details:
    role = RoleDetails(role_name=roles)
    role.save()


system_configuration_db = SystemConfiguration(name='Bayugan City Doctors Hospital', inventory_code='23-05-00000', transaction_code = '23-05-00000', year='2023')
system_configuration_db.save()

userdb = UserDetails(middle_name='Vilanueva', sex = 'Male', address='J.P. Rizal', position ='CMT II', role_id = '1', user_id = '1')
userdb.save()



