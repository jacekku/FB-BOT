import requests
from bs4 import BeautifulSoup
import re

def get_power():
    r=requests.get("https://powerlisting.fandom.com/wiki/special:random")
    soup = BeautifulSoup(r.text, 'html.parser')
    p=soup.p
    h1=soup.h1
    return str(r.url+"\n*"+h1.text+"*\n"+p.text)


print(get_power())
print 