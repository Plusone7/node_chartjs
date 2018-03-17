import re
phoneNumberRexgex = re.compile(r'(\d\d\d)-(\d\d\d)-(\d\d\d\d)')
mo = phoneNumberRexgex.search('My phone number is 415-534-4142.')
print('phone number found: '+mo.group(0))
print('mo.group(1): '+mo.group(1))
print('mo.group(2): '+mo.group(2))
print('mo.group(3): '+mo.group(3))
print (mo.groups())

#\( ******  \)
areaPhoneNumberRexgex = re.compile(r'(\(\d\d\d\))(\d\d\d-\d\d\d\d)')
number = areaPhoneNumberRexgex.search('(455)123-1333')
print('phone number found: '+number.group(0))