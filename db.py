from werkzeug.security import generate_password_hash
import logging
from user import User

from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey

logging.basicConfig(level=logging.DEBUG)
LOG=logging.getLogger(__name__)


# Useful variables
serviceUsername = "9da704c7-f678-4c15-a485-67404a35e77b-bluemix"
servicePassword = "7861ebf41a6e5276cb08fb17e1da9dc5fc39cdc397dfc39959a9e4f584c697a5"
serviceURL = "https://9da704c7-f678-4c15-a485-67404a35e77b-bluemix:7861ebf41a6e5276cb08fb17e1da9dc5fc39cdc397dfc39959a9e4f584c697a5@9da704c7-f678-4c15-a485-67404a35e77b-bluemix.cloudant.com"

# This is the name of the database we are working with.
databaseName = "amq"
print ("===\n")

# Use the IBM Cloudant library to create an IBM Cloudant client.
client = Cloudant(serviceUsername, servicePassword, url=serviceURL)

# Connect to the server
client.connect()

myDatabaseDemo = client.create_database(databaseName)

# Check that the database now exists.
if myDatabaseDemo.exists():
    print ("'{0}' successfully created.\n".format(databaseName))

# Space out the results.
print ("----\n")



def save_user(username, email,mobile,password):
#we need to add password

    password_hash = generate_password_hash(password)
    #users_collection.insert_one({'_id': username, 'email': email, 'password': password_hash})
    isUserExists = False
    try:
        jsonDocument = {
            "name": username,
            "email": email,
            "mobile": mobile,
            "password": password_hash
        }
        
        print('get user :::',email)
        email = email.strip()
        if(isUserExistsByEmail(email)== None):
        #if(get_user(username)== None):
            print('User does not exists')
        
        # Create a document using the Database API.
            newDocument = myDatabaseDemo.create_document(jsonDocument)
        
        # Check that the document exists in the database.
            if newDocument.exists():
                print ("Document '{0}' successfully created.".format(email))
                print("Data committed")
        else:
            print('user  exits')
            isUserExists = True
    except Exception as e:
        print(e)
        return 'There was an issue in registering'
    return isUserExists

def forgot_password(email,password):
#we need to add password
    password_hash = generate_password_hash(password)
    result_collection = Result(myDatabaseDemo.all_docs, include_docs=True)
    user_data={}
    isUserPresent=False
    for record in result_collection:
        print('##Record## :: ')
        print (record)
        print(type(record))
        print (' email value :get ::',record.get('doc').get('email'))
        doc=record.get('doc')
        
        if(doc.get('email')==email):
            print('document retrived ## ',doc)
            id =doc['_id']
            print('id ## ',id)
            my_document = myDatabaseDemo[id]
            my_document['password']=password_hash
            my_document.save()
            user_data=my_document
    
    return User(user_data['name'],user_data['mobile'],user_data['email'], user_data['password']) if user_data else None


def get_user(username):
    #user_data = users_collection.find_one({'_id': username})
    print('get_user',username)
    user_data={}
    
    result_collection = Result(myDatabaseDemo.all_docs, include_docs=True)
    #result_collection = Result(myDatabaseDemo.all_docs)
    print ("Retrieved  document:",result_collection)
    print ("Retrieved minimal document:\n{0}\n".format(result_collection[0]))
    pasword_collection=''
    current_user={}
    isUserPresent=False
    for record in result_collection:
        print (record)
        print(type(record))
        print (' name value :get ::',record.get('doc').get('name'))
        doc=record.get('doc')
        
        if(doc.get('name')==username):
            pasword_collection=doc.get('password')
            user_data = doc
            isUserPresent=True
        
   
    #return User(user_data['name'],user_data['mobile'],user_data['email']) if user_data else None
    return User(user_data['name'],user_data['mobile'],user_data['email'], user_data['password']) if user_data else None

def get_userByEmail(email):
    #user_data = users_collection.find_one({'_id': username})
    print('get_user by email ##',email)
    user_data={}
    email = email.strip()
    print('Email ::##',email)
    
    result_collection = Result(myDatabaseDemo.all_docs, include_docs=True)
    #result_collection = Result(myDatabaseDemo.all_docs)
    print ("Retrieved  document:",result_collection)
    print ("Retrieved minimal document:\n{0}\n".format(result_collection[0]))
    pasword_collection=''
    current_user={}
    isUserPresent=False
    for record in result_collection:
        print (record)
        print(type(record))
        print (' name value :get ::',record.get('doc').get('email'))
        doc=record.get('doc')
        
        if(doc.get('email').strip()==email):
            print('user by email found ## ##')
            pasword_collection=doc.get('password')
            user_data = doc
            isUserPresent=True
        
   
    #return User(user_data['name'],user_data['mobile'],user_data['email']) if user_data else None
    return User(user_data['name'],user_data['mobile'],user_data['email'], user_data['password']) if user_data else None


def isUserExistsByEmail(email):
    email = email.strip()
    print("isUserExists ::###",email)
    #user_data = users_collection.find_one({'_id': username})
    #print('get_user',email)
    user_data={}
    
    result_collection = Result(myDatabaseDemo.all_docs, include_docs=True)
    #result_collection = Result(myDatabaseDemo.all_docs)
    print ("Retrieved  document:",result_collection)
    print ("Retrieved minimal document:\n{0}\n".format(result_collection[0]))
    pasword_collection=''
    current_user={}
    isUserPresent=False
    for record in result_collection:
        print (record)
        print(type(record))
        print (' email value :get ::',record.get('doc').get('email'))
        doc=record.get('doc')
        
        if(doc.get('email')==email):
            pasword_collection=doc.get('password')
            user_data = doc
            isUserPresent=True
        
   
    #return User(user_data['name'],user_data['mobile'],user_data['email']) if user_data else None
    return User(user_data['name'],user_data['mobile'],user_data['email'], user_data['password']) if user_data else None