'''
Created on 29 Jan 2015

@author: chriseisbrown
'''
import re

p1 = re.compile('^\d{4} ([A-Z][a-z]{2}-[A-Z][a-z]{2})')
m1 = p1.match('2014 Mar-Apr')
thing0 = m1.group(0)
thing1 = m1.group(1)
#thing2 = m1.group(2)

p2 = re.compile('([A-Z][a-z]{2}-[A-Z][a-z]{2})')
m2 = p2.match('2014 Mar-Apr')
thing0 = m2.group(0)
thing1 = m2.group(1)
#thing2 = m2.group(2)

print thing0, thing1