import re
text = 'Why give us this if you don’t apply parking restrictions @TheBlock @Channel9 @gleneiracouncil #theblock #gleneiracouncil #pointless'
#Gleneiracouncil
#GlenEiraCouncil
#gleneiracouncil
#GLENEIRACOUNCIL
#gleneiracitycouncil
#@gleneiracitycouncil
#GlenEiraCityCouncil
#Gleneiracitycouncil
#@GlenEiraCityCouncil
#@gleneiracouncil

a = re.search('#Gleneiracouncil', text)
b = re.search('#gleneiracouncil', text)
c = re.search('#GlenEiraCouncil', text)
d = re.search('#GLENEIRACOUNCIL', text)
e = re.search('#gleneiracitycouncil', text)
f = re.search('@gleneiracitycouncil', text)
g = re.search('#GlenEiraCityCouncil', text)
h = re.search('#Gleneiracitycouncil', text)
i = re.search('@GlenEiraCityCouncil', text)
j = re.search('@gleneiracouncil', text)
if (((a is not None) or (b is not None) or (c is not None) or (d is not None) or (e is not None)
or (f is not None) or (g is not None) or (h is not None) or (i is not None) or (j is not None))is True):
    print(text)
else:
    print("wrong")


