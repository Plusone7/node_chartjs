
# -*- coding: <encoding UTF-8> -*-
# python3 googleMapSearch.py "whatever you want to search address"

import webbrowser,sys,pyperclip
if len(sys.argv)>1:
    #get address from command line
    address = ''.join(sys.argv[1:])
    print(address)
else:
    #get address from clipboard
    address = pyperclip.paste()
    print(address)
webbrowser.open('https://www.google.com/maps/place/'+address)
#mapit 870 Valencia St,San Francisco,CA 94110
