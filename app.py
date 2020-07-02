import eventlet
eventlet.monkey_patch(subprocess=True)
#from gevent import monkey
#monkey.patch_all(subprocess=True)

#import gevent

import os
import sys
import importlib
import static
import templates
import subprocess   
import json
import random
import requests
import urlparse2
import time
import hmac
#import pylint_flask
import functools



import redis

from python_path import PythonPath

from cloudant.result import Result, ResultByKey
from cloudant.query import Query,QueryResult

#from AMQonlinestore.AMQ_Dba import cloudant_online_store

#from AMQonlinestore.AMQ_onlinestore import AMQOnlineStore,OnlineStoreCustomer

#from AMQonlinestore.AMQ_Dba.cloudant_online_store import CloudantOnlineStore

#from AMQonlinestore.AMQ_Dba.cloudant_online_store import CloudantOnlineStore

#from gevent.pywsgi import WSGIServer

#from gevent.pywsgi import geventsocketio

#from AMQonlinestore.AMQ_onlinestore import OnlineStoreCustomer
from flask import Flask,render_template,request,session,current_app,redirect,url_for,jsonify,Response,flash,abort,Markup
#production
#from flask_uwsgi_websocket import geventWebSocket
#import socketio
#import asyncio
#import aiohttp
#from aiohttp import web
#import gunicorn
#PRODUCTION

from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm,Form
from wtforms import StringField,PasswordField,BooleanField,TextField,FormField,validators,ValidationError
#from wtforms.validators import InputRequired,Email,Length
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager,login_user,logout_user,login_required,current_user

from db import get_user, save_user,get_userByEmail,forgot_password

from passlib.handlers.sha2_crypt import sha256_crypt

from passlib import hash
#from flask import Flask

#from flask_socketio import SocketIO,emit
from flask_socketio import SocketIO,emit
# donot use gevent socket io as flask socketio 4 is linked to gevent

from flask_principal import Principal,Identity,AnonymousIdentity,identity_changed
import wtforms_json
from send_email import send_email
import html
import requests
from bs4 import BeautifulSoup
import re
import urllib3
from threading import Thread

from flask_session import Session
from datetime import timedelta


from time import sleep

from flask_mail import Mail,Message

from itsdangerous import URLSafeTimedSerializer


from email.mime.text import MIMEText
from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

import smtplib

from cloudant.client import Cloudant
from cloudant.design_document import DesignDocument

from flask_socketio import disconnect
import atexit
#from pathlib import PurePath

from threading import Lock

from flask_mail import Mail,Message
from email.mime.text import MIMEText
from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

import re

from flask import g

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(),'..'))

#from dotenv import load_dotenv
#load_dotenv(dotenv_path='OSS.env')

from run import WatsonEnv

#async_mode="threading"
async_mode= None
# change in to aiohttp

app = Flask(__name__, static_url_path='',template_folder='templates')

# Generate your SECRET KEY with os.random and paste it on to your ssecure code
#http://flask.pocco.org/docs --quickstart and sessions
#check python tutorial doc


#app.config['SECRET_KEY']={b'&\xc1\x04\xe8\xf1.\xa9\xac.\xd17\x9f\xa8d\xa6\x9d'}
app.config['SECRET_KEY']=b'&\xc1\x04\xe8\xf1.\xa9\xac.\xd17\x9f\xa8d\xa6\x9d'


s=URLSafeTimedSerializer('Thisisasecret!')

app.config['SESSION_TYPE']='filesystem'

Session(app)

 
Bootstrap(app)


wtforms_json.init()

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

app.config["WTF_CSRF_ENABLED"]=False


socketio=SocketIO(app,manage_session=True, engineio_logger=True)

#socketio.attach(app)
# change here 



thread = None
thread_lock=Lock()

namespace ='/AMQ'  



mail = Mail(app)

app.config['MAIL_SERVER']='smtp.zoho.eu'
app.config['MAIL_PORT']=587
app.config['MAIL_USERNAME']='admin@automationspectrum.com'
app.config['MAIL_PASSWORD']='Shiva@76'
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USE_SSL']=False
mail=Mail(app)



def validateEmail(form,field):
    print("ValidateEmail###")
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    regex1 = 'test' or 'sample' or 'dummy'
    if(not re.search(regex,field.data)):
        print('regex ##')       
        raise ValidationError('Incorrect Email')
    if(re.search(regex1,field.data)):
        print('regex1 ##')         
        raise ValidationError('Use Valid Email')
    

    print('validation successful')
    

class RegisterForm(Form):
    print('inside RegisterForm')
   
    name = StringField(('Name'),[validators.DataRequired(),validators.length(min=6,max=50)])
    #email = StringField('Email',[validators.DataRequired(),validators.email(),validators.length(min=6,max=50)])
    email = StringField('Email',[validators.InputRequired(),validateEmail])
    mobile = StringField('Mobile',[validators.DataRequired(),validators.length(min=10, max=14)])
    password = PasswordField('Password',[validators.DataRequired(),validators.length(min=8, max=15)])
    
    


class LoginForm(FlaskForm):

    #name = TextField(('Name'),[validators.DataRequired(),validators.length(min=2, max=15)])
    email = StringField('Email',[validators.DataRequired(),validators.email(),validators.length(min=6,max=50)])
    #mobile = TextField(('Mobile'),validators=[InputRequired(),Length(min=10, max=11)])
    password = PasswordField('Password',[validators.DataRequired(),validators.length(min=8, max=15)])
    
class ForgotPassword(Form):
    email = StringField('Email',[validators.DataRequired(),validators.email(),validators.length(min=6,max=50)])
    password = PasswordField('New Password',[validators.DataRequired(),validators.length(min=8, max=15)])
    
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
        print("app::send_message ::",message)
        ''' Function to send a message to the web ui via Flask Socket IO'''
        lines=message.split('\n')
        for line in lines:
            image = None
            #image1= None
            
            #ebay image
            if 'pict' in line:
             
                line, http_tail = line.split('http',1)
                print(http_tail)
                print("vgood")
                
                image = 'http'+ http_tail
                print(image)
                print("good")
           
            #ebay
            if 'rover.ebay.com' in line:
                line,http_tail=line.split('http',1)
                image=unescape('http'+http_tail)
            #amazon
            if 'www.amazon.com.au' in line:
                line,http_tail=line.split('http',1)
                image=unescape('http'+http_tail)

            
                


            emit('my_response',{'data':line.strip(),'image':image})
    
    
    
    


    #def get_user_json(self,user_id):
     #   ''' Get user information from user_id
      #  :param str user_id:user ID to look up
       # ''' 
       # #form=RegisterForm()

        #first impl of web-ui user is just user_id, for now
        #user=current_user.username
        #print (user)
        #print ("currentusernow")
        #user_id=current_user.username

        #print (user_id)
        #print ('jsonname')

        #return user_id
        #return user
        #return{'user':{'profile':{
         #      'name':current_user.username,
               #'last_name':user_id,
              # 'email':user_id,
        #}}} 

  


@app.route("/")

def index():

    ''' Render wos Web ui
        The  Web UI interacts with Python via Flask SocketIO
        and uses HTML/CSS/JS for formatting
    '''
    session['attempt'] = 5
    #return render_template ("index1.html", async_mode=socketio.async_mode)
    return render_template ("index1.html")


@app.route("/chatshoppie")
@login_required
def chatshoppie():
    print("chatshoppie ###")
    print("chatshoppie ###:: current_user ",current_user.username)
    if current_user.is_authenticated():
        print("user authenticated")
        pass

    return render_template("login2test.html")


@app.route('/signup',methods=['GET','POST'])

def signup():

    #if current_user.is_authenticated:


    form = RegisterForm()

    #if current_user.is_authenticated:

    #    return redirect(url_for('chatshoppie'))

    message =''

    if request.method=='POST' and form.validate_on_submit():

        username = str(request.form.get('name')).strip()
        email = str(request.form.get('email')).strip()
        mobile = str(request.form.get('mobile')).strip()
        password = str(request.form.get('password')).strip()

        print (username)
        print ("name")

       # username = username
        key = email
        token=s.dumps(key,salt='email-confirm')

        
        #zoho email
         
        try:
            isUserPresent = save_user(username, email,mobile,password)
            print('isuser present ',isUserPresent)
            
            if (isUserPresent):
                flash("**A User has already registered with this email",'danger')
                return redirect(url_for('signup'))
            else:
                msg=Message('Chatshoppie',sender='admin@automationspectrum.com', recipients=[key])
                link=url_for('confirm_email',token=token, _external=True)
                msg.subject="Account Confirmation Email from Chatshoppie.com"
         
                msg.html=render_template('/email.html',username=username,link=link,key=key)
        
        
                mail.send(msg)  
        
                return render_template("thankyou.html")

               

        except:
            print('exception ::')
            message = "User already exists!"
            flash("**Unable to register. Please contact Admin",'danger')


        
    
          
    #return render_template("register.html",async_mode=socketio.async_mode,form=form)
    return render_template("register.html",form=form)

@app.route('/confirm_email/<token>')

def confirm_email(token):

    

    key=s.loads(token,salt='email-confirm',max_age=3600)
    

    return render_template("login2test.html")

@app.route('/forgotpassword',methods=['GET','POST'])
def forgotpassword():

    print('Forgot password')
    form = ForgotPassword()
    if(request.method=='GET'):
        
        return render_template("forgotpassword.html",form=form)
    
    if request.method=='POST' and form.validate_on_submit():

        email = str(request.form.get('email')).strip()
        password = str(request.form.get('password')).strip()
        print('Email ::',email,' Password :: ',password)
        user = get_userByEmail(email)
        if (user==None):
            flash(u"**Invalid mailid.Please try again","error")
            return render_template("forgotpassword.html",form=form)
 
        else:
            print('update password')
            user = forgot_password(email,password)
            print('updated forgot password')
            if(user==None):
                flash(u"**Unable to change password.Please try again","error")
            else:
                flash(u"**Password changed successfully. Please login","success")
                return redirect(url_for('login'))
            
@app.route('/login', methods=['GET','POST'])

def login():
    print("inside login ###")
    form=LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('chatshoppie'))

    error = None;

    if request.method=='POST' and form.validate_on_submit():

        #username = request.form.get('name')
        email = str(request.form.get('email')).strip()
        print("email :## ",email)
        password_input = str(request.form.get('password')).strip()
        
        #user = get_user(username)

        #print('user:',email)
        user = get_userByEmail(email)
        print("user ##",user)
        print("user :password_input ##",password_input)

        if (user ==None):
            message = Markup('You have not registered yet.<br><a href="/signup">Click here to register</a>')
            flash(message, 'error')

        if user and user.check_password(password_input):
            print('user is found by email ::##')
            try:
                login_user(user,remember=True)
                #login_user(user,remember=True, duration=timedelta(days=5))
            except Exception as e:
                print('Exception ',e)
            #print("Before redirect ###:::currentuser ",current_user.username)
            #print("Before redirect ###:::currentuser::isAuthenticated ",current_user.is_authenticated)
            return redirect(url_for('chatshoppie'))

        else:
            print("Else ##")
            error = '**Incorrect login credentials'
            attempt= int(session.get('attempt'))
            attempt= attempt-1
            session['attempt']=attempt
            print('Attempt### ',attempt,flush=True)
            if attempt==1:
                client_ip= session.get('client_ip')
                flash('This is your last attempt, %s will be blocked for 24hr, Attempt %d of 5'  % (client_ip,attempt), 'error')
            if attempt==0:
                client_ip= session.get('client_ip')
                flash('Your account, %s is blocked. Contact Support for further details', 'error')
            else:
                flash(error,"error")

    if request.method=='GET':
        print("inside GET###")
        return render_template("signin.html",form=form)
    print("Before return###")
    return render_template("signin.html",form=form)


    


@login_manager.user_loader
def load_user(email):
    print('load user::', email)
    return get_userByEmail(email)



@app.route('/logout')
@login_required
def logout():
    print('logout')
    logout_user()
    #return redirect(url_for('home'))
    return render_template("index1.html")



@app.route("/documentation/")
#PR
#@websocket.route("/documentation/")
def documentation():

    #return render_template("documentation.html")
    #return render_template("accordion.html",async_mode=socketio.async_mode)
    return render_template("accordion.html")


@app.route("/privacypolicy/")
#PR
#@websocket.route("/privacypolicy/")
def privacypolicy():

    #return render_template("privacypolicy.html",async_mode=socketio.async_mode)
    return render_template("privacypolicy.html")


sender=WebSocketSender()

#user={
#    'type':'customer'
#}


@socketio.on('my_event',namespace=namespace)

#@websocket('my_event',namespace=namespace)

def do_message(message):

    ''' this is the message from web ui user''' 
    print('app::Do messaage::',message)
        
    if not watson:

        #report incomplete setup

        sender.send_message("Sorry. The AMQ onlinestore is closed(failed to initialise)")

    elif message['data']:

        # send message to AMQ onlinestore and start a conversation loop
        message=message['data']
               
        user=current_user.username
        print (user)
       
      
        print ("looking for this name")
       # f.close()

        watson.handle_conversation(message,sender,user)

        watson.get_customer(user)
        #watson.get_customers(user)
       # watson.add_customer_to_context()

@socketio.on('connect',namespace=namespace)
#@websocket('connect',namespace=namespace)
#@authenticated_only
def do_connect():

    socketio.emit('msg',{'msg':"good morning"})


    pass




def do_disconnect():
    '''On disconnect, print to stdout. Just FYI'''
    
    pass
    




#This script is intended to run from the command line
port = os.getenv('PORT', '5000')

#application=AppReloader(app)

if __name__ == '__main__':

    
    
    #Initialise the store with its bluemix services for the web ui
    watson=WatsonEnv.get_AMQ_online_store()

    #socketio.run(app)

    #this is developement
    #socketio.run(app,host='0.0.0.0',port=int(port),debug=True)
    #while deploying to ibm make sure host 0.0.0.0 and port 8080
    socketio.run(app,host='0.0.0.0',port=8081,debug=True)
    #socketio.run(app,host='192.168.0.101',port=80,debug=True)

    #app.run(host='0.0.0.0',port=8080,debug=True)
    #web.run_app(app,host='0.0.0.0',port=8080)
    #socketio.run(app,host='127.0.0.1',port=1111,debug=True)
    # this is prod
    
    #socketio.run(app,debug=True,port=1111)
    