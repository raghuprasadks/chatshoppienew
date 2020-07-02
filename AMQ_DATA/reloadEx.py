import os
import sys
import importlib
import static
import templates
import subprocess   
import json
import random

from cloudant.result import Result, ResultByKey
from cloudant.query import Query


from flask import Flask,render_template,request,session,current_app,redirect,url_for,jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,TextField,FormField
from wtforms.validators import InputRequired,Email,Length
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager,login_user,logout_user,login_required,current_user,UserMixin

from flask_socketio import SocketIO,emit
from flask_principal import Principal,Identity,AnonymousIdentity,identity_changed
import wtforms_json
from send_email import send_email
import html
import requests
from bs4 import BeautifulSoup
import re
import urllib3
from threading import Thread

from flask_mail import Mail,Message

from itsdangerous import URLSafeTimedSerializer


from email.mime.text import MIMEText
import smtplib

#to_reload=False


#from requests_html import HTMLSession

#import aiohttp
#import asyncio
#import async_timeout
#new
#loop=asyncio.get_event_loop()


# new
#async def fetch(url):

 #   async with aiohttp.ClientSession() as session, async_timeout.timeout(10):
  #      async with session.get(url) as response:
   #         return await response.text()

#def fight(resp):

 #   return "Please work"

#print (c)

#html.escape('x > 2 && x < 7')

from cloudant.client import Cloudant

client=Cloudant.iam("9da704c7-f678-4c15-a485-67404a35e77b-bluemix","PaXGKKmDQ7iAv27crY--ek4hpJtChRZvoYkKu1886LfL",connect=True)
#Connect to the account and establish a session cookie
client.connect()
session=client.session()

db=client['amq']

if db.exists():

    print ("connected to db")

result_collection = Result(db.all_docs)



sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(),'..'))


from run import WatsonEnv

async_mode="threading"
app = Flask(__name__, static_url_path='',template_folder='templates')

# Generate your SECRET KEY with os.random and paste it on to your ssecure code
#http://flask.pocco.org/docs --quickstart and sessions
#check python tutorial doc


app.config['SECRET_KEY']={b'&\xc1\x04\xe8\xf1.\xa9\xac.\xd17\x9f\xa8d\xa6\x9d'}

s=URLSafeTimedSerializer('Thisisasecret!')



Bootstrap(app)

wtforms_json.init()
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
app.config["WTF_CSRF_ENABLED"]=False



socketio=SocketIO(app,async_mode=async_mode)

thread = None
namespace ='/AMQ'  

#zohoemail

#def __init__(self,email_):


 #   self.email_=email_

mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USERNAME']='anupg76@gmail.com'
app.config['MAIL_PASSWORD']='Shiva@76'
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USE_SSL']=False
mail=Mail(app)

class RegisterForm(FlaskForm):

    name = TextField(('Name'),validators=[InputRequired(),Length(min=2, max=15)])
    email = StringField('Email',validators=[InputRequired(),Email(message='Invalid Email'),Length(max=100)])
    password = PasswordField('Password',validators=[InputRequired(),Length(min=5, max=80)])
    shopping_cart = TextField()

class LoginForm(FlaskForm):

    email = StringField('Email',validators=[InputRequired(),Email(message='Invalid Email'),Length(max=50)])
    password = PasswordField('Password',validators=[InputRequired(),Length(min=5, max=80)])
    remember = BooleanField('Remember me')
    
def unescape(s):

        s=s.replace("&lt;","<")
        s=s.replace("&gt;",">")
        s=s.replace("&amp;","&")

        return s   

class WebSocketSender:

    ''' Wrap send_message with a class to use with watson.handle_conversation()
    This is one implementation of UI. Slack integration is another
    '''

    def __init__(self):

        pass

    def send_message(self,message):
        ''' Function to send a message to the web ui via Flask Socket IO'''
        lines=message.split('\n')
        for line in lines:
            image = None
            
            
            if 'pict' in line:
             
                line, http_tail = line.split('http',1)
                image = 'http'+ http_tail
                 
                
            if 'rover.ebay.com' in line:
                line,http_tail=line.split('http',1)
                image=unescape('http'+http_tail)

                 
                


            emit('my_response',{'data':line.strip(),'image':image})
    
    
    
   
    def get_user_json(self,user_id):
        ''' Get user information from user_id
        :param str user_id:user ID to look up
        ''' 
        #form=RegisterForm()

        #first impl of web-ui user is just user_id, for now

        return{'user':{'profile':{
               'name':user_id,
               #'last_name':user_id,
               'email':user_id,
        }}} 


sender=WebSocketSender()


#@app.route('/my-link/')




#def add_to_shopping_cart():
    #user_doc=find_doc('customer','email')

    
  
    #client.connect()

    #current_doc=client['amq'][user_doc['_id']]


    #session=HTMLSession()
    #session.browser

   

    #resp=session.get("http://localhost:5000/signin")

 #   resp=loop.run_until_complete(asyncio.gather(fetch("http://localhost:5000/signin")))

    #resp.html.render()

    #resp.html.html



    #t= Thread(target=resp)
    #t.start()

    #http=urllib3.PoolManager()

    #url="http://localhost:5000/signin"

    #response=http.request('GET',url)

    #print (response.status)

    #soup=BeautifulSoup(resp.html.html,"html.parser")

    #print (soup)

  #  print ("ok")

    #r=requests.get("https://www.bbc.com/")
    #c=r.content

    #soup=BeautifulSoup(c,"html.parser")

    #item=soup.find_all('img')
    #item=soup.find_all("div",{"class":"bot_message"})

    #print (item)
    #print ("done")

    #

    #for item in all:

     #   print (item.find_all("a")[0].text)
    #item=all[15].find_all("a").text

   
    
        #current_doc['shopping_cart'].append(customer_str)
    #current_doc['shopping_cart'].append(item)
    #current_doc.save()

    


   # return fight(resp)

 

#def find_doc(customer,email):

    
 #   selector={

  #      'type':'customer',
        
        
   # }
       
    #query=Query(db,selector=selector)

    #for doc in query()['docs']:

     #   return doc

    #return None

#def clearing_shopping_cart(self):

 #  self.context['shopping_cart']=''
  # self.context['cart_item']=''





@app.route("/")

def index():

    ''' Render wos Web ui
        The  Web UI interacts with Python via Flask SocketIO
        and uses HTML/CSS/JS for formatting
    '''
    
    return render_template ("index.html", async_mode=async_mode)


@app.route('/signup',methods=['GET','POST'])

def signup():

    form = RegisterForm()

    

    if form.validate_on_submit():


        #return '<h1>' + form.name.data + '' + form.email.data + '' + form.password.data + '</h1>'
        hashed_password = generate_password_hash(form.password.data,method='sha256')
       
        customer={

            '_id': form.email.data,
            'type':'customer',
            'name':form.name.data,
            'email':form.email.data,
            'shopping_cart':[],   
            'password':hashed_password

        }

        key = customer['email']
        token=s.dumps(key,salt='email-confirm')

        new_doc=db.create_document(customer)
        #zoho email
        
        msg=Message('Chatshoppie',sender='anupg76@gmail.com', recipients=[key])
        link=url_for('confirm_email',token=token, _external=True)
        msg.subject="Account Activation Email from Chatshoppie.com"
        msg.body="Congratulations... you have now registered for Chatshoppie.com, the one stop shop for all Shopping. It's as easy as Chating..." 'Please click on the link {}'.format(link)
        mail.send(msg)  
        return '<h1> the email you entered is {} </h1>'.format(key)

        if new_doc.exists():

           print ('created document')
           return redirect(url_for("signin"))
           
          
          
    return render_template("register.html",async_mode=async_mode,form=form)


@app.route('/confirm_email/<token>')

def confirm_email(token):

    

    key=s.loads(token,salt='email-confirm',max_age=3600)
    

    return render_template("signin.html",async_mode=async_mode)


    


@app.route("/signin",methods=['POST','GET'])
#check for password mapping
def signin():

    form = LoginForm()

    result_collection = Result(db.all_docs,include_docs=True)

    us=format(result_collection[0])

   
    print ("retrieved first record:\n{0}\n".format(result_collection[0]))

    hashed_password = generate_password_hash(form.password.data,method='sha256')
    if form.validate_on_submit():

        customer={

            '_id': form.email.data,
            'type':'customer',
            'email':form.email.data,
            'password':hashed_password,
            'shopping_cart':[]
            

        }

        query=Query(db,selector=customer)

        
        #for doc in query()['docs']:
        #return redirect(url_for('signin'))
        return render_template("login.html")

                       
        
        #if check_password_hash(password,form.password.data):

            #return redirect(url_for('register'))

        
          # return '<h1> valid username and Password </h>'


        #return None


    return render_template("signin.html",async_mode=async_mode,form=form)



user={

        #'_id': form.email.data,
        'type':'customer',
        #'email':form.email.data
    }





@app.route('/logout')

def logout():

    logout_user()

    
    return redirect(url_for('signin'))

@app.route('/refresh')




def refresh():

    #global to_reload
    #to_reload=True
    #async_mode="threading"
    exec(open("app.py").read())
    

    
    #return render_template('login.html')
    #return app

#class AppReloader(object):
##
 #   def __init__(self,create_app):

  #      self.create_app=create_app
   #     self.app=create_app()

    #def get_application(self):

     #   global to_reload
      #  if to_reload:

       #     self.app=self.create_app()
        #    to_reload=False

        #return self.app

    #def __call__(self,create_app):

     #   app=self.get_application()

      #  return app



   


@socketio.on('my_event',namespace=namespace)

def do_message(message):

    ''' this is the message from web ui user'''

    if not watson:

        #report incomplete setup

        sender.send_message("Sorry. The AMQ onlinestore is closed(failed to initialise)")

    elif message['data']:

        # send message to AMQ onlinestore and start a conversation loop
        message=message['data']

        watson.handle_conversation(message,sender,user)

@socketio.on('connect',namespace=namespace)
def do_connect():
    '''on web ui connect do something here'''

    #on web ui send a generic greeting vis flask SocketIO
    #uncomment for debugging. Not great for normal use case
    #emit('my_reponse',{'data':'Hello!'})

    pass

@socketio.on('disconnect',namespace=namespace)

def do_disconnect():
    '''On disconnect, print to stdout. Just FYI'''

    print ('Client Disconnected')

#This script is intended to run from the command line
port = os.getenv('PORT', '5000')

#application=AppReloader(app)

if __name__ == '__main__':
    
    #Initialise the store with its bluemix services for the web ui
    watson=WatsonEnv.get_AMQ_online_store()

    
    

    socketio.run(app,host='0.0.0.0',port=int(port),debug=True)
    

        















