s = 7 * "8"
sp = [ ]

while '2222' in s or '8888' in s:
    if '2222' in s:
     s = s.replace ('2222','88')
     sp.append (s)
    else:
     s = s.replace ('8888','22')
     sp.append (s)
     print (s, len (sp))