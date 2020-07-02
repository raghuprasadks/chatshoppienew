import json
import logging
import os
import random
import re
import time
from watson_developer_cloud import AssistantV1
from watson_developer_cloud import DiscoveryV1

from user import User

from db import get_user, save_user

from flask_login import current_user


 
logging.basicConfig(level=logging.WARN)

LOG=logging.getLogger(__name__)

# limit the result count when calling discovery query
DISCOVERY_QUERY_COUNT=10

#limit more when formating and removing weak results
DISCOVERY_KEEP_COUNT=5

#Truncate the discovery text and we'l add ... if truncated
DISCOVERY_TRUNCATE=500

#Available DataSources for Discovery

DISCOVERY_EBAY_STORE="EBAY_STORE"
#DISCOVERY_AMAZON_STORE="AMAZON"


class OnlineStoreCustomer:

    def __init__(self, email=None,name=None):

        self.email=email
        self.name=current_user.username
        #self.last_name=last_name
   #     self.shopping_cart=shopping_cart

    def get_customer_dict(self):



     #   """Returns a dict in form usable by our cloudant
      #  :returns:customer dict of customer data
       # :rtype:dict
       # """

       #user==current_user.username


        #print (user)
      
        #print ("correct user")
        customer ={
        #    'type':'customer',
            # 'email':self.email,
             'name':self.name
            #'last_name':self.last_name,
            #'shopping_cart':self.shopping_cart

        }

        

        return customer

    #print ("really")
  

        
class AMQOnlineStore:

    #def __init__(self,assistant_client,discovery_client,cloudant_online_store,user):
    def __init__(self,assistant_client,discovery_client):
        print('AMQonlineStore inside init')
       
        #self.cloudant_user=current_user.username
        #specific for IBM Watson Assistant
        self.assistant_client=assistant_client
        self.workspace_id = self.setup_assistant_workspace(assistant_client,os.environ)

        #specific for IBM Cloudant NoSql database
      #  self.cloudant_online_store=cloudant_online_store

        #specific for IBM Watson Discovery Service
        self.discovery_client=discovery_client
        self.discovery_data_source=os.environ.get('DISCOVERY_DATA_SOURCE', DISCOVERY_EBAY_STORE)
     
        #self.user=current_user.username
        try:
             
           self.discovery_score_filter=float(os.environ.get(self.discovery_data_source + '_DISCO_SCORE_FILTER',0))
             
             #print (discovery_score_filter)

        except ValueError:

            LOG.debug(self.discovery_data_source + "__DISCO_SCORE_FILTER must"+"be a number between 0.0 and 1.0"+"Using default value of 0.0")
            self.discovery_score_filter=0.0
            pass
    
        self.discovery_environment_id,self.discovery_collection_id=(self.setup_discovery_collection(discovery_client,self.discovery_data_source,os.environ))

        self.context = {}
        self.customer=None
        self.response_tuple=None
        self.delay=0.5 #second
        response=self.assistant_client.message(
            workspace_id="33a981b1-6ce8-4143-a073-a901c5de9121",
            context=None).get_result()
        self.context = self.context_merge(self.context,response['context'])


    @staticmethod
    def setup_assistant_workspace(assistant_client,environ):
        print('setup assistant workspace')

        ''' :param assistant_client: Assistant service client
        :param object environ: runtime environment variables
        :return: ID of Assistant workspace
        :rtype:str
        :raise exception : when workspace in not found and cannot be created
        '''
       #Get the actual workspces

        workspaces=assistant_client.list_workspaces().get_result()['workspaces']

        env_workspace_id = environ.get('WORKSPACE_ID')

      
        if env_workspace_id:

            #optionally, we have an env var to give us a WORKSPACE_ID
            # if one was set in env, require that it is found

            LOG.debug("Using WORKSPACE_ID=%s" % env_workspace_id)

            for workspace in workspaces:

                if workspace['workspace_id']==env_workspace_id:

                   ret = env_workspace_id
                   break

            else:

                raise Exception("WORKSPACE_ID=%s is specified in a runtime environment variable, but that workspace doesnot exist." % env_workspace_id)

        else:
          
            #find it by name which we have already created

            name=environ.get('WORKSPACE_NAME', 'AMQ_master')

            for workspace in workspaces:
                if workspace['name']==name:
                    ret= workspace['workspace_id']
                    LOG.debug("Found WORKSPACE_ID=%(id)s using look up by"
                      "name=%(name)s"% {'id':ret, 'name': name})
                    break 
        
            else:
                # Not found, so create it.
                LOG.debug("Creating workspace from data/workspace.json...")
                workspace = AMQOnlineStore.get_workspace_json()
                created = assistant_client.create_workspace(
                    name,
                    "Assistant workspace created by Askmanyquestions.com",
                    workspace['language'],
                    intents=workspace['intents'],
                    entities=workspace['entities'],
                    dialog_nodes=workspace['dialog_nodes'],
                    counterexamples=workspace['counterexamples'],
                    metadata=workspace['metadata']).get_result()
                ret = created['workspace_id']
                LOG.debug("Created WORKSPACE_ID=%(id)s with "
                         "name=%(name)s" % {'id': ret, 'name': name})
       
        return ret


    @staticmethod
    def setup_discovery_collection(discovery_client,data_source,environ):
        print('setup_discovery_collection')
        ''' Ensure collection exists in Watson Discovery

        :param discovery_client:discovery service client
        :param str data_source: name of the discovery data source
        :param object environ: runtime environment variable
        :return: ID of Discovery environment and collection to use
        :rtype:str
        :raise Exception:  whne collection is not found and cannnot be created
       '''
       #if environment id exists ensure it is valid

        environment_id = environ.get('DISCOVERY_ENVIRONMENT_ID')

        if environment_id:
         try:
            LOG.debug("Using DISCOVERY_ENVIRONMENT_ID=%s" % environment_id)
            discovery_client.get_environment(environment_id)

         except Exception as e:
            print(e)
            raise Exception("Environment with DISCOVERY_ENVIRONMENT_ID=%s" "not found." % environment_id)

        else:

        # try to find environment name.

          name=environ.get('DISCOVERY_ENVIRONMENT_NAME','AMQ_Master')

          environments=discovery_client.list_environments().get_result()

          for environment in environments['environments']:

            if environment['name']==name:

                environment_id=environment['environment_id']

                LOG.debug("Found DISCOVERY_ENVIRONMENT_ID=%(id)s using"
                           "lookup by name=%(name)s" %
                           {'id':environment_id,'name':name})
         
                break

            elif not environment['read_only']:

                #last resort it to read only

                environment_id=environment['environment_id']


                # havenot coded for creating

          if not environment_id:
                # No existing environment found, so create it.
                # NOTE that the number of environments that can be created
                # under a trial Bluemix account is limited to one environment
                # per organization.
                try:
                    LOG.debug("Creating discovery environment...")
                    created = discovery_client.create_environment(
                        name,
                        "Discovery environment created by "
                        "AMQ_master.").get_result()
                    environment_id = created['environment_id']
                    LOG.debug("Created DISCOVERY_ENVIRONMENT_ID=%(id)s with "
                              "name=%(name)s" %
                              {'id': environment_id, 'name': name})
                except Exception as e:
                    raise Exception("Error creating Discovery "
                                    "Error: %s" % repr(e))

      #determine if collection exists

        collection_id=environ.get('DISCOVERY_COLLECTION_ID')

        if collection_id:
         try:
            LOG.debug("Using DISCOVERY_COLLECTION_ID=%s" % collection_id)
            discovery_client.get_collection(environment_id,collection_id)

            return environment_id,collection_id

         except Exception:
            raise Exception("Collection with DISCOVERY_COLLECTION_ID=%s"
                            "does not exist." % collection_id)
                 
        else:

           #Try to find collection by name.
           #  Search all connections
           #that exists in the discovery environment

           #Discovery Collection names

           ebay_collection_name="ebay_store"

            #filepath location to discovery file

           ebay_data_path= "AMQ_DATA/EBAY_STORE/"

           print (ebay_data_path)


           collections=discovery_client.list_collections(environment_id).get_result()['collections']

           for coll in collections:
               if ((data_source==DISCOVERY_EBAY_STORE and coll['name']==ebay_collection_name)):
                   return environment_id,coll['collection_id']


       #Doesnot exist so create it

        LOG.debug("Creating collection from datafiles")

        try:

            if data_source==DISCOVERY_EBAY_STORE:
                name= ebay_collection_name
                path= ebay_data_path

            if name:

                collection = discovery_client.create_collection(environment_id,name).get_result()

                #Add documents to collection

                if collection:
                    collection_id=collection['collection_id']

                    #with open(os.path.join(os.getcwd(),r'C:\Users\Anup\AMQ_Master\AMQ_DATA\AMQ_EBAY','kb3.json')) as fileinfo:

                      #print (fileinfo)

                     #  add_doc = discovery.add_document('84dcebca-5543-4177-9c2a-4dc0687212dd','d79b810d-d6ac-4941-8c29-bd1822e3e02e',file=fileinfo).get_result()
    
                    #print(json.dumps(add_doc,indent=2))

                    # mention file path- check discovery.py
                    for _, _, files in os.walk(path):

                        for fname in files:

                            if fname.endswith('.json'):

                                 with open(os.path.join(path, fname),'r') as f:

                                     data=f.read()

                                 discovery_client.add_document(environment_id,collection_id,file=data,filename=fname)

                         #       discovery_client.add_document('84dcebca-5543-4177-9c2a-4dc0687212dd','d79b810d-d6ac-4941-8c29-bd1822e3e02e',file=data,filename=fname)


        except Exception as e:

            raise Exception("Discovery Collection couldnot be found or created"
            
                            "Error:%s" % repr(e))
                            
                            
        if not collection_id:
            
            raise Exception("Discovery collection could not be found or created.")


        return environment_id, collection_id


    @staticmethod
    def get_workspace_json():

        with open ('AMQ_DATA/workspace.json') as workspace_file:

            workspace=json.load(workspace_file)

        return workspace

    def context_merge(self,dict1,dict2):

        '''combines 2 discts in to one for watson assistant context.

        common data in dict2 will override dict1

        :param dict dict1: original context dictionary

        :param dict dict2: new context dictionary -will override fields

        :returns new_dict for context

        :rtype is dict

        '''
        new_dict=dict1.copy()
            
        if dict2:

            new_dict.update(dict2)

        return new_dict

    
    
        
        
    def add_customer_to_context(self):

        ''' send customer info to watson using context.
        The customer data from UI is in cloudant DB, or has been added.
        Now add it to the context and pass it back to watson.
        '''

        #self.context=self.context_merge(self.context,self.customer.get_customer_dict())
        self.context=self.context_merge(self.context,self.customer.get_customer())

        

  

    def handle_discovery_query(self):

        ''' Take query string from Watson context  and send it to Discovery
        Discovery response will be merged in to context in order to allow it to be returned to watson.
        in the case where there is no Discovery client, a fake response will be returned, for testing purposes

        :return: False indicating no need for UI input, just return to watson

        :rtype: Bool

        '''

        query_string=self.context['discovery_string']
       # user_string=current_user.username
       # print (user_string)
       # user_string=self.context['user_string']

        if self.discovery_client:

            try:
               
             response=self.get_discovery_response(query_string)

            except Exception as e:

             response={'discovery_result': repr(e)}

       # else:

            #response=self.get_fake_discovery_response()


        self.context=self.context_merge(self.context,response)

        LOG.debug("watson_discovery:\n{}\ncontext:\n{}".format(response,self.context))

        # no need to user input return to watson dialogue

        return False

        
    def get_watson_response(self,message):
        print('get_watson_response :: ',message)

        '''Send text and context to watson and gets reply

         Message input is text, self.context is also added and sent to watson

         :param str message: text to sent to watson
         :returns: json dict from watson
         :rtype:dict

        '''

        #if user==current_user.username:
        
            #self.add_customer_to_context(user)

         #   print (user)
          #  print ("real user")
        

        response=self.assistant_client.message(


            workspace_id="33a981b1-6ce8-4143-a073-a901c5de9121",
            input ={'text':message},
            context =self.context)

        return response

  

    print ("anup3")
    @staticmethod
    def format_discovery_response(response,data_source):

        print ("format_discovery_response:::",data_source)
        '''Format data for Slack based on discovery datasource

        This method handles the different data source data and formats it specifically for Slack

        The following functions are specific to the data source that has been fed to watson discovery service
        
        We have currently one data source which is EBAY_STORE, which datasource is being used is specified in ".env" file by 
        setting the following key values:
        EBAY_STORE is datasource
        <datasource>_DISCO_COLLECTION_ID=<collection id of data source>
        <datasource>_DISCO_SCORE_FILTER=<float value between 0.0 and 1.0>
        DISCOVERY_DATA_SOURCE="<data source string name>"


        This pattern should be followed if additional data sources are added

        :param dict reponse: output from discovery
        :param string data_source :name of the discovery data source
        :returns cart_number, name,url,image of each item returned

        BUILD ALL BUSINESS RULES HERE...
        '''

        output = []

        if not response.get('results'):
            return output
        print ("anup4")

        def get_product_name(entry):

            ''' Pull product name from entry data for nice user display

            :param dict entry: output from Discovery
            :returns: name of product
            :rtype: str
            '''

            product_name=""

            if data_source == DISCOVERY_EBAY_STORE:

                #the product name is stored in title field.
                # Productname is fromm ebaytest.py

              if 'title' in entry:

                  product_name = entry['title']

            return product_name
            

        
        def get_product_url(entry):

            ''' Pull product url from entry data so user can navigate to product page

            :param dict entry: output from discovery
            :returns: url link to product description
            rtype:str
            '''
       
            product_url=""

            if data_source == DISCOVERY_EBAY_STORE:
                
                
              if 'product_page' in entry:

                  product_url=entry['product_page']

            return product_url



        def get_amazon_product_url(entry):

            ''' product url for AMAZON products'''

            amazon_product_url=""

            if data_source==DISCOVERY_EBAY_STORE:

                if 'amazon_prod_page' in entry:

                    amazon_product_url=entry['amazon_prod_page']
            
            return amazon_product_url


     

        def get_image_url(entry):

            ''' Pull product image url from entry data to allow pictures in slack

            :param dict entry: output from Discovery
            :returns: url link to product image
            :rtype:str

            '''

            image_url=""

            if data_source == DISCOVERY_EBAY_STORE:

               if 'image_url' in entry:

                   image_url = re.sub(r'scale\[[0-9]+\]','scale[50]',entry['image_url'])

            return image_url

        def get_amazon_accordion(entry):
            '''
            get amazon accordion
            '''

            amazon_accordion=""

            if data_source == DISCOVERY_EBAY_STORE:

                if 'amazonacc' in entry:

                    amazon_accordion=entry['amazonacc']

            return amazon_accordion


        def get_product_colour(entry):

            ''' get product colour
            '''

            product_colour=""

            if data_source == DISCOVERY_EBAY_STORE:

               if 'colour' in entry:

                   product_colour=entry['colour']

            return product_colour

        def get_product_size(entry):

            '''
            get product size
            '''

            product_size=""

            if data_source==DISCOVERY_EBAY_STORE:

               if 'size' in entry:

                   product_size=entry['size']

            return product_size
        

        def get_product_price(entry):

            '''
            get product price
            '''

            product_price=""
            
            if data_source==DISCOVERY_EBAY_STORE:

                if 'price' in entry:

                    product_price=entry['price']


            return product_price

        def get_product_price_category(entry):

            '''

            get price category less than 50, 50 to 100 , 100 to 250 and above 250

            '''

            product_price_category=""

            if data_source==DISCOVERY_EBAY_STORE:

                if 'pricecategory' in entry:

                    product_price_category = entry['pricecategory']

            return product_price_category


        
        def get_product_category(entry):

            '''
            get product category like womens dress, mens dress etc

            '''

            product_category=""

            if data_source==DISCOVERY_EBAY_STORE:

                if 'category' in entry:

                    product_category=entry['category']

                
            return product_category

        def get_product_sub_category(entry):

            '''

            get sub category like womens floral dresses, womens party dresses

            '''

            product_sub_category=""

            if data_source==DISCOVERY_EBAY_STORE:

                if 'subcategory' in entry:

                    product_sub_category=entry['subcategory']

            
            return product_sub_category

        def get_size_category(entry):

            '''

            get size category four, five
            
            '''

            size_category=""

            if data_source==DISCOVERY_EBAY_STORE:

                if 'sizecategory' in entry:

                    size_category=entry['sizecategory']

            return size_category

        def get_colour_category(entry):

            '''
                get colur category 1111 for black

            '''

            colour_category=""

            if data_source==DISCOVERY_EBAY_STORE:

                if 'colourcategory' in entry:

                    colour_category=entry['colourcategory']

            return colour_category


        def get_search(entry):

            '''
            search=true or false
            '''

            search_category=""

            if data_source==DISCOVERY_EBAY_STORE:

                if 'search' in entry:

                    search_category=entry['search']
                
            return search_category

        def get_sexcategory(entry):

            '''
            search for sex-male,female,kids etc
            '''

            sex_category=""

            if data_source==DISCOVERY_EBAY_STORE:

                if 'sexcategory' in entry:

                    sex_category=entry['sexcategory']

            return sex_category






        def slack_encode(input_text):
   
            ''' Removes <, &, > for Slack.

            :param str input_text: text to be cleaned for slack
            :returns: text without undesirable chars
            :rtype:str

            '''

            if not input_text:
                return input_text


            args = [('&','&amp;'), ('<','&lt;'), ('>','&alt;')]

            for from_to in args:

                input_text=input_text.replace(*from_to)
            
            return input_text


        results = response['results']

        cart_number=1

        for i in range(min(len(results),DISCOVERY_KEEP_COUNT)):

            result=results[i]

            product_data={

                "cart_number": str(cart_number),
                "name":slack_encode(get_product_name(result)),
                "purl":slack_encode(get_product_url(result)),
                "apurl":slack_encode(get_amazon_product_url(result)),
                "colour":slack_encode(get_product_colour(result)),
                "size":slack_encode(get_product_size(result)),
                "price":slack_encode(get_product_price(result)),
                "category":slack_encode(get_product_category(result)),
                "subcategory":slack_encode(get_product_sub_category(result)),
                "image":slack_encode(get_image_url(result)),
                "pcategory":slack_encode(get_product_price_category(result)),
                "scategory":slack_encode(get_size_category(result)),
                "ccategory":slack_encode(get_colour_category(result)),
                "search":slack_encode(get_search(result)),
                "xcategory":slack_encode(get_sexcategory(result)),
                "aaccordion":slack_encode(get_amazon_accordion(result)),
                
            }

            cart_number += 1
                
            output.append(product_data)

        return output

    
    def get_discovery_response(self,input_text):

        ''' call discovery with input_text and return formatted response
        Formatted response _tuple is saved for AMQ-online store to allow item to be easily added to the shopping cart

        Response is further formatted to be passed to UI
        :param str input_text : query to be used with Watson Discovey Service
        :returns: Discovery response in format for Watson Assistant
        :rtype:dict
        '''
        

        #http GET is in this format
        discovery_response=self.discovery_client.query(


            environment_id=self.discovery_environment_id,
            collection_id=self.discovery_collection_id,
            query=input_text,
            count=DISCOVERY_QUERY_COUNT
            #user=current_user.username
        ).get_result()

        

        #Watson discovery assigns a confidence level to each result
        #Based on data mix, we can assign a minimum tolerance value
        #in an attempt to filter out the 'weakest' results.

        if self.discovery_score_filter and 'results' in discovery_response:



            fr = [x for x in discovery_response['results'] if 'score' in x and x['score'] > self.discovery_score_filter]

            discovery_response['matching_results'] = len(fr)

            discovery_response['results'] = fr
            
        response=self.format_discovery_response(discovery_response,self.discovery_data_source)

        self.response_tuple = response

        fmt = "\n{cart_number}) {name}\n  {image} \n AUD->{price}  SIZE->{size}  COLOUR->{colour}  \n{purl} {apurl}\n {aaccordion}"

        

        print ("anup555")     
        
        formatted_response = "\n".join(fmt.format(**item) for item in response)

        return {'discovery_result': formatted_response}

        #return user

    

    

   

    def handle_message(self,message,sender):
        print('handle_message::',message,'sender :: ',sender)

        '''handler fr messages coming from Watson Assistant using context

        Field in context will trigger various actions in this application

        :param str message: text from UI
        :param object sender: sed for clients send_message implementation
        :returns: True if UI input is required, false if we want app processing and no input

        :rtypr: Bool

        '''
        #user=current_user.username

        #print (user)
        #print ("handle message user")
        watson_response=self.get_watson_response(message).get_result()
        LOG.debug("watson_response:\n{}\n".format(watson_response))

        if 'context' in watson_response:
            self.context=watson_response['context']
        sender.send_message("\n".join(watson_response['output']['text'])+"\n")

        
        if (self.context.get('discovery_string') and self.discovery_client):
            return self.handle_discovery_query()

        #if self.context.get('get_users')=='no':
         #   return False

        if self.context.get('get_input')=='no':
            return False

        return True

        

    #def get_customer(self,user,message,sender):
    def get_customer(self,user):

        
       # if self.context.get('get_users')=='yes':



        if user==current_user.username:

            print (user)
            print ("correct user")
            
        return user

    #def get_customers(self,user):


     #   customer={
            

      #      "user": current_user.username


       # }
        
        #m=customer.username

        #print (m)
        #print ("correct customers")
        #return customer
        


    def handle_conversation(self,message,sender,user):
        print('handle_conversation')

        ''' Handler of messages coming from user
        Loops when additional input is needed
        :param str message: text from UI
        :param sender: a sender implementation used for send_message
        :param str user: user ID
        '''

        #user=current_user.username

        #print (user)
        #print ("handle user")
       # if user and not self.customer:
        #    self.init_customer(sender,user)

        #get_users=self.get_customer(user)
        get_input=self.handle_message(message,sender)

        while not get_input:

            get_input=self.handle_message(message,sender)





            


        #get_users=self.handle_message(message,sender)
        
       # while not get_users:

        #    get_users=self.handle_message(message,sender)



        
        #while not get_input:

         #   get_input=self.handle_message(message,sender)


   # def run(self):

    #            ''' Main run loop of the application with a slack client

     #           '''
                #make sure DB exists
      #          self.cloudant_online_store.init()

       #         if self.slack_client and self.slack_client.rtm_connect():

        #            LOG.info("AMQ online store Bot is connected and running!")

         #           while True:

          #              slack_output=self.slack_client.rtm_read()
           #             if slack_output:
            #                LOG.debug("slack output\n:{}\n".format(slack_output))

             #           message,channel,user=self.parse_slack_output(slack_output)

              #          if message:

               #             LOG.debug("message:\n %s \n channel:\n %s \n" % (message,channel))

                #            if message and channel and 'unfurl' not in message:

                 #               sender=SlackSlender(self.slack_client,channel)

                  #              self.handle_conversation(message,sender,user)

                   #         time.sleep(self.delay)

                #else:

                 #   LOG.warning ("Connection failed.Invalid Slack Token  or Bot ID?")



















            
































            



            
















          










     

        
                                                 

            
            
                                               

        

        


                        
                        
                            
                            
                            








            
                           






        









            








    
    

























    
        
    













    
