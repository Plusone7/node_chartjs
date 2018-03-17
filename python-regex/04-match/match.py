import re

#可選擇性的比對

batRegex = re.compile(r'Bat(wo)?man')
mo1 = batRegex.search('The Adventures of Batman')
print(mo1.group()) # Batman
mo2 = batRegex.search('The Adventures of Batwoman')
print(mo2.group()) # Batwoman

phoneRegex = re.compile(r'(\d\d\d-)?\d\d\d-\d\d\d\d')
number = phoneRegex.search('123-1234')
print(number.group())
number2 = phoneRegex.search('000-123-1234')
print(number2.group())
