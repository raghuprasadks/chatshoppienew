import os
import json
from watson_developer_cloud import DiscoveryV1

discovery = DiscoveryV1(
    version="2018-10-15",
    iam_apikey="fNRl9bmiLGsAMEgV1Kq57bZ90N5SIvZDsXkKo6F3r58Y",
    url= "https://gateway-syd.watsonplatform.net/discovery/api"
)

with open(os.path.join(os.getcwd(), r'C:\Users\Anup\Chatshoppie_Dev','Disctest')) as fileinfo:

    add_doc = discovery.add_document('84dcebca-5543-4177-9c2a-4dc0687212dd', '39238ec1-0d1f-42eb-8b2e-bc08187cc536', file=fileinfo).get_result()

print(json.dumps(add_doc, indent=2)) 