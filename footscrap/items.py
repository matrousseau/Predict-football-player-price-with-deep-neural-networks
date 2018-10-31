some_list = '\r\n\t\t\t\t\t\t\t\t\t27 oct. 1984\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(33)\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t'

delr= some_list.replace("\r", "")
delt = delr.replace("\t", "")
deln = delt.replace("\n", "")

print (deln)