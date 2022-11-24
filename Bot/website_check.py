import urllib.request
def checkSite(site):
    try:
        urllib.request.urlopen(str(site)).getcode()==200 
        return "Site online" 
    except: 
        return "Site not reachable..."