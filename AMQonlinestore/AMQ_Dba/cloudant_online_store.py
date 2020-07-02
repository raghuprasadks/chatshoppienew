import logging
import os
import sys
from cloudant.query import Query
from flask_wtf import FlaskForm
import requests

#from app import RegisterForm,LoginForm,signup
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,TextField,FormField
from wtforms.validators import InputRequired,Email,Length
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager,login_user,logout_user,login_required,current_user,UserMixin
#from app import signin
#from flask_socketio import SocketIO,emit
import wtforms_json
#from app import nm
#from app.signin import nm
from cloudant.client import Cloudant

#client=Cloudant.iam("9da704c7-f678-4c15-a485-67404a35e77b-bluemix","PaXGKKmDQ7iAv27crY--ek4hpJtChRZvoYkKu1886LfL",connect=True)
       #Connect to the account and establish a session cookie
#client.connect()
#session=client.session()

#db=client['amq']
#changing databse to test which has partition instead of amq

#if db.exists():

 #   print ("connected to cloudant")

logging.basicConfig(level=logging.DEBUG)
LOG=logging.getLogger(__name__)


class RegisterForm(FlaskForm):

    name = TextField(('Name'),validators=[InputRequired(),Length(min=2, max=15)])
    email = StringField('Email',validators=[InputRequired(),Email(message='Invalid Email'),Length(max=50)])
    password = PasswordField('Password',validators=[InputRequired(),Length(min=5, max=80)])
    shopping_cart = TextField()
  

class LoginForm(FlaskForm):

    name = TextField(('Name'),validators=[InputRequired(),Length(min=2, max=15)])
    email = StringField('Email',validators=[InputRequired(),Email(message='Invalid Email'),Length(max=50)])

def test():

    form=LoginForm()
    eme=form.email.data
    print (eme)

    print("excellent")
class CloudantOnlineStore(object):

    def __init__(self,client,db_name):
        '''Creates a new instance of Cloudonlinestore
        :param Object client: instance of to cloudant client to connect to
        :param str db_name: name of the database to use
        '''

        self.client=client
        self.db_name=db_name

    def init(self):
        ''' Creates and initialises the database
        '''
        try:
            self.client.connect()
            LOG.info("Getting Database")

            if self.db_name not in self.client.all_dbs():
                LOG.info('Creating Database{}...'.format(self.db_name))
                self.client.create_database(self.db_name)
            else:
                LOG.info('Database{}exists.'.format(self.db_name))

        finally:

            self.client.disconnect()

    # user

    def add_customer_obj(self,customer,email,doc):

        

        '''Adds a new customer to DB unless they already exists

        :param str email: ID of the customer(email address)
        :param str first_name: first name of the customer
        :param str last_name: last name of the customer
        :param list shopping_cart: items in customers shopping cart
        '''

      

        customer_doc={
                'type':'customer',
                'email':customer.email,
                'name':customer.name,
                #'last_name':customer.last_name,
                'shopping_cart':customer.shopping_cart,
                
                    
        }

        self.add_doc_if_not_exists(doc,customer,email)

    def find_customer(self,email):

        '''Finds the customer based on the specified customerStr in CLoudant
        :param str customer_str: customer(email_addr)
        :returns: document with cust info
        :rtype: dict
        '''

        return self.find_doc('customer','email')

    def find_name(self,name):

        fv=open(r'C:\Users\Anup\OneDrive\Chatshoppie_linux_production\em.txt','r')
        em=fv.read()
        print(em)
        
        url="https://9da704c7-f678-4c15-a485-67404a35e77b-bluemix.cloudant.com/amq/"
        final_url=f'{url}{em}'
        res1=requests.get(final_url,auth=requests.auth.HTTPBasicAuth('9da704c7-f678-4c15-a485-67404a35e77b-bluemix', '7861ebf41a6e5276cb08fb17e1da9dc5fc39cdc397dfc39959a9e4f584c697a5'))
        print (res1)
        
        #res1=requests.get('https://9da704c7-f678-4c15-a485-67404a35e77b-bluemix.cloudant.com/amq/_all_docs?include_docs=true',auth=requests.auth.HTTPBasicAuth('9da704c7-f678-4c15-a485-67404a35e77b-bluemix', '7861ebf41a6e5276cb08fb17e1da9dc5fc39cdc397dfc39959a9e4f584c697a5'))
        #print (res1)
    
        dice=res1.json()
        print (dice)

    
    #same FOR loop logic for add to cart

        #for e in dice['rows']:

      #  name=dice['name']
       # print (name)

            #
       # print ("for name")
        return name

        #res1=requests.get('https://9da704c7-f678-4c15-a485-67404a35e77b-bluemix.cloudant.com/amq/_all_docs?include_docs=true',auth=requests.auth.HTTPBasicAuth('9da704c7-f678-4c15-a485-67404a35e77b-bluemix', '7861ebf41a6e5276cb08fb17e1da9dc5fc39cdc397dfc39959a9e4f584c697a5'))
        #print (res1)
    
        #dicn=res1.json()
        #print (dicn)

    
    #same FOR loop logic for add to cart

        #for n in dicn['rows']:

         #   name=n['doc']['name']
          #  print (name)
           # print ("for name")

        #if signin==name:

        #return name
        
       # name=dicn['rows'][1]['doc']['name']
        
       # return customer
        

        
        #print (name)


        #doc=self.find_customer(email)

        #return name

    


        #doc=self.find_customer(email)

        #return shoppingcart
    
    def list_shopping_cart(self,customer_str):

        ''' Getting shopping cart info for the customer.
        :param str customer_str: customer(email addr)
        :returns:shopping cart
        :rtype:list
        '''
        
        fv=open(r'C:\Users\Anup\OneDrive\Chatshoppie_linux_production\em.txt','r')
        em=fv.read()
        print(em)

        #client.connect()

        url="https://9da704c7-f678-4c15-a485-67404a35e77b-bluemix.cloudant.com/amq/"
        final_url=f'{url}{em}'
        res1=requests.get(final_url,auth=requests.auth.HTTPBasicAuth('9da704c7-f678-4c15-a485-67404a35e77b-bluemix', '7861ebf41a6e5276cb08fb17e1da9dc5fc39cdc397dfc39959a9e4f584c697a5'))
        print (res1)
        
        #res1=requests.get('https://9da704c7-f678-4c15-a485-67404a35e77b-bluemix.cloudant.com/amq/_all_docs?include_docs=true',auth=requests.auth.HTTPBasicAuth('9da704c7-f678-4c15-a485-67404a35e77b-bluemix', '7861ebf41a6e5276cb08fb17e1da9dc5fc39cdc397dfc39959a9e4f584c697a5'))
        #print (res1)
    
       # dice=res1.json()
       # print (dice)

    
    #same FOR loop logic for add to cart

        #for e in dice['rows']:

        #shopping_cart=dice['shopping_cart']
        #print (shopping_cart)

            #
        #print ("for shopping cart")
        #return shopping_cart
        #res1=requests.get('https://9da704c7-f678-4c15-a485-67404a35e77b-bluemix.cloudant.com/amq/_all_docs?include_docs=true',auth=requests.auth.HTTPBasicAuth('9da704c7-f678-4c15-a485-67404a35e77b-bluemix', '7861ebf41a6e5276cb08fb17e1da9dc5fc39cdc397dfc39959a9e4f584c697a5'))
        #print (res1)
    
        #dics=res1.json()
        #print (dics)

    
        doc = self.find_customer(customer_str)
        #if doc:
        #    return doc['shopping_cart']
        return doc  # None
            


    #def add_to_shopping_cart(self,customer_str,item):   

     #   '''Adds item to shopping cart for customer

      #  :param str customer_str:customer(email addr)
       # :param str item:item to add

        #'''
        #user_doc=self.find_doc('customer','email')

        #try:
         #   self.client.connect()
         #   current_doc=self.client['amq'][user_doc['_id']]
         #   if current_doc:
         #      current_doc['shopping_cart'].append(item)
         #      current_doc.save()
        #except Exception:
         #   LOG.exception("Cloudant DB exception")

        #finally:
         #   self.client.disconnect()


    def delete_item_shopping_cart(self,customer_str,item):

        ''' Deletes item from shopping cart for customer.
        :param str customer_str: The customer specified by user
        :param str item: item to delete
        '''

        user_doc=self.find_doc('customer','email')

        try:
            self.client.connect()
         #   current_doc=self.client[self.db_name][user_doc['_id']]

          #  if current_doc:
           #     if item in current_doc['shopping_cart']:
            #        current_doc['shopping_cart'].remove(item)
             #       current_doc.save()

        except Exception:

            LOG.exception("Cloudant DB Exception:")

        finally:
            self.client.disconnect()


    def find_doc(self,customer,email):

        
        ''' Finds a doc in cloudantDB
        :param str doc_type : document type stored in Cloudant
        :param str property_name: property name to search for
        :param str proprty_value:value that should match for the specified property name
        :returns: doc from query or none
        :rtype:dict or none
        '''
        #client=Cloudant.iam("9da704c7-f678-4c15-a485-67404a35e77b-bluemix","PaXGKKmDQ7iAv27crY--ek4hpJtChRZvoYkKu1886LfL",connect=True)
        #client.connect()
        #session=client.session() 
        #print (session) 

        fv=open(r'C:\Users\Anup\OneDrive\Chatshoppie_linux_production\em.txt','r')
        em=fv.read()
        print(em)
        print ("great")

        #client.connect()
        
        #session=client.session()

        #print (session)
        print("connected new user")

        url="https://9da704c7-f678-4c15-a485-67404a35e77b-bluemix.cloudant.com/amq/"
        final_url=f'{url}{em}'
        res1=requests.get(final_url,auth=requests.auth.HTTPBasicAuth('9da704c7-f678-4c15-a485-67404a35e77b-bluemix', '7861ebf41a6e5276cb08fb17e1da9dc5fc39cdc397dfc39959a9e4f584c697a5'),timeout=10)
        print (res1)
        
        #res1=requests.get('https://9da704c7-f678-4c15-a485-67404a35e77b-bluemix.cloudant.com/amq/_all_docs?include_docs=true',auth=requests.auth.HTTPBasicAuth('9da704c7-f678-4c15-a485-67404a35e77b-bluemix', '7861ebf41a6e5276cb08fb17e1da9dc5fc39cdc397dfc39959a9e4f584c697a5'))
        #print (res1)
    
      #  dice=res1.json()
       # print (dice)

    
    #same FOR loop logic for add to cart

        #for e in dice['rows']:

        #email=dice['email']
        #print (email)

            #
        #print ("for email")
        return email


        #email=dict['rows'][1]['doc']['email']
        #name=dict['rows'][1]['doc']['name']
        #shopping_cart=dict['rows'][1]['doc']['shopping_cart']
        
       # return customer
        #

       
        

                
        #try:

         #   self.client.connect()
          #  db=self.client['amq']
           # selector={
            #       '_id':{'$gt':0},
             #      'type':'customer'
                  
            #}
            #query=Query(db,selector=selector)
            #for doc in query()['docs']:
             #   return doc
            #return None

        #except Exception:

         #   LOG.exception("Cloudant DB exception")

        #finally:

         #   self.client.disconnect()

    

    def add_doc_if_not_exists(self,doc,customer,email):
        ''' Adds a new doc to cloudant if a doc with the same value for unique_property_name 
        does not exist.
        :param dict doc: document to add
        :param str unique_property_name: name of the property used to search for an existing document
        (value will be extracted from the doc)
        '''
        form=RegisterForm

        doc_type=doc['customer']
        property_value=doc['email']

        existing_doc=self.find_doc(customer,email)

        if existing_doc is not None:
            LOG.debug('Existing{} doc where {}={}:\n{}'.format(customer,email,property_value,existing_doc))
        else:
            LOG.debug('Creating {} doc where {}={}'.format(customer,email,property_value))

            try:

                self.client.connect()
                db=self.client['amq']
                db.create_document(doc)

            except Exception:

                LOG.exception("Cloudant DB Exception:")
            
            finally:

                self.client.disconnect()


    @staticmethod
    def optimize_cloudant_url(url):
  

            '''
            if the URL is in the pattern
            https://username:password@*-bluemix.cloudant.com
            then strip out the username and password to make it py3.6 friendly.
            ie.: https://*-bluemix.cloudant.com

            :param url: Cloudant URL to optimise
            :return: URL with out redundant user:pass@
            '''
            safe_url=''
            if url and len(url)>0:
                url_fragments=url.split("@")

                if len(url_fragments)==2:
                    safe_url='https://'+url_fragments.pop()
                    LOG.info("New Cloudant URL: {}".format(safe_url))
                else:
                    LOG.exception("Malformed Cloudant URL: %s"% url)

            else:

                LOG.exception("URL not found")

            return safe_url
            






































