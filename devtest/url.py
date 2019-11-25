import urllib.request
PPUrlBraddon   = "http://59.167.251.106"
PPUrlGunghalin = "http://203.173.10.173"
rego='70'
x = urllib.request.urlopen('http://59.167.251.106/lpr/lpr.asp?rego="+rego')
print(x.read())


 
