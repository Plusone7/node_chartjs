import re
phoneNumberRexgex = re.compile(r'\d\d\d-\d\d\d-\d\d\d\d')
#search()搜尋想要找的字串
# mo = phoneNumberRexgex.search('My phone number is 415-544-4242.')
# print('phone number found: '+mo.group())
urPhoneNumber = input()
scanPhoneNumber = phoneNumberRexgex.search(urPhoneNumber)
print('your phone number is :'+scanPhoneNumber.group())

# '\d' Matches any decimal digit; this is equivalent to the class [0-9].
# '\D' Matches any non-digit character; this is equivalent to the class [^0-9].
# '\s' Matches any whitespace character; this is equivalent to the class [ \t\n\r\f\v].
# '\S'Matches any non-whitespace character; this is equivalent to the class [^ \t\n\r\f\v].
# '\w'Matches any alphanumeric character; this is equivalent to the class [a-zA-Z0-9_].
# '\W'Matches any non-alphanumeric character; this is equivalent to the class [^a-zA-Z0-9_].