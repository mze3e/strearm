import names
import random
from random_address import real_random_address
import barnum
from faker import Faker

company_types_for_barnum = ['Corporation'
,'Incorporated'
,'Inc'
,'Co'
,'Industries'
,'LLC'
,'Limited'
,'Group'
,'Organization'
,'Agency'
,'International']

fname,lname = barnum.create_name()
full_name = lname+', '+fname
random_address = real_random_address()
if random_address['address2'] == '':
    address = random_address['address1']
else:
    address = random_address['address1']+', '+random_address['address2']
city = random_address['city']
state = random_address['state']
postal_code = random_address['postalCode']
lat = random_address['coordinates']['lat']
lng = random_address['coordinates']['lng']
fax =  barnum.create_phone(postal_code)
phone =  barnum.create_phone(postal_code)
email = barnum.create_email(name=(fname, lname))
birthday = barnum.create_birthday()
fake_ip = Faker()
ip_address_v4 = fake_ip.ipv4()
ip_address_v6 = fake_ip.ipv6()
cc_number = barnum.create_cc_number('visa') #('mastercard', 'visa', 'discover', 'amex')
expiry = barnum.create_date(max_years_future=3)
password = barnum.create_pw()


print(fname, lname)
print(phone)
print(fax)
print(address)
print(city)
print(state)
print(postal_code)
print(lat)
print(lng)
print("Born on {0:%m/%d/%Y}".format(birthday))
print(email)
print(ip_address_v4)
print(ip_address_v6)
print(cc_number)

print("{0:%m/%y}".format(expiry))
print("Password: {0:s}".format(password))
print(barnum.create_company_name('Generic')) # LawFirm
print(barnum.create_job_title())



import cv2
import random_face

engine = random_face.get_engine()
face = engine.get_random_face()
cv2.imshow("face", face)
cv2.waitKey()
