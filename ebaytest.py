import json
import requests

searches = []

with open (r"C:\Users\Anup\OneDrive\Chatshoppie_dev\ebay_search_test.txt", "r") as searchfile:
  
    searches = searchfile.readlines()
    
  
for item in searches:
    search = item.split(',')[0]
  
  
    url=('http://svcs.ebay.com/services/search/FindingService/v1\
?SECURITY-APPNAME=Automati-Askmanyq-PRD-f43ce4284-a0bada92\
&OPERATION-NAME=findItemsByKeywords\
&SERVICE-VERSION=1.0.0\
&RESPONSE-DATA-FORMAT=JSON\
&REST-PAYLOAD\
&GLOBAL-ID=EBAY-AU\
&affiliate.trackingId=5338413822\
&affiliate.networkId=9\
&affiliate.customId=CS0714\
&itemFilter(0).name=Condition\
&itemFilter(0).value=New\
&itemFilter(1).paramName=Currency\
&itemFilter(1).paramValue=AUD\
&itemFilter(2).name=MinPrice\
&itemFilter(2).value=0\
&itemFilter(3).name=MaxPrice\
&itemFilter(3).value=50\
&apectFilter.aspectName=Buying Format\
&aspectFilter.aspectValueName=Buy It Now\
&aspectFilter.aspectName=Style\
&aspectFilter.aspectValueName=Trench Coat\
&aspectFilter.aspectName=Colour\
&aspectFilter.aspectValueName=Red\
&keywords='+ item)
    
    url=url.replace(" ","%20")
    
    apiResult = requests.get(url)
    parsedoc = apiResult.json()
  
    #print (parsedoc)
  

    for item in (parsedoc["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]):
        Productname=item["title"][0]
        Producturl=item["viewItemURL"][0]
        Imageurl=item["galleryURL"][0]

        condition=item['condition'][0]['conditionDisplayName'][0]
        price=item['sellingStatus'][0]["convertedCurrentPrice"][0]['__value__']

    

    
        print(Productname +" "+Producturl +" "+Imageurl+price+" "+condition)




  #print(parsedoc)






