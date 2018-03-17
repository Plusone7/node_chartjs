
import re
heroRegex = re.compile(r'Batman|Tina Fey')
mo1 = heroRegex.search('Batman and Tina Fey.')
print(mo1.group()) # Batman 

mo2 = heroRegex.search('Tina Fey and Batman.')
print(mo2.group()) # Tina Fey

regex = re.compile(r'Bat(man|mobile|bat)')
mo = regex.search('Batmobile lost a wheel')
print(mo.group())
print(mo.group(1))