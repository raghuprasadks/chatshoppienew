import json
import os
import AMQonlinestore
from cloudant.client import Cloudant
from dotenv import load_dotenv

#from slackclient import SlackClient
import slack
from watson_developer_cloud import AssistantV1
from watson_developer_cloud import DiscoveryV1

# we need to fix this issue
# the import is done in cmd

#from AMQonlinestore.AMQ_Dba.cloudant_online_store import CloudantOnlineStore

import db


from AMQonlinestore.AMQ_onlinestore import AMQOnlineStore
#import user

#import app
#from user import User

#from db import get_user, save_user

#from flask_login import current_user


class WatsonEnv:

    def __init__(self):
            pass

    @staticmethod

    def get_vcap_credentials(vcap_env,service):

        if service in vcap_env:

            vcap_instance_list=vcap_env[service]
            if isinstance(vcap_instance_list,list):

                first=vcap_instance_list[0]

                if 'credentials' in first:
                    return first['credentials']


    #@staticmethod
    #def get_slack_user_id(slack_client):

     #   ''' Get slack bot user id from SLACK_BOT_USER or BOT_ID env vars
      #  use the original BOT_ID if found, but now we can instead SLACK_BOT_USER and look up the ID

       # This should be called after env is loaded when using dotenv
        #'''
        #slack_bot_user=os.environ.get('SLACK_BOT_USER')

        #print("Looking up BOT_ID for '%s'" % slack_bot_user )


        #api_call=slack_client.api_call("users.list")

        #if api_call.get('ok'):

         #retrieve all users so that we can find our bot

         # users=api_call.get('members')

          #for user in users:

           #  if 'name' in user and user.get('name')==slack_bot_user:

            #     bot_id=user.get('id')
             #    print ("Found BOT_ID=" +bot_id)
              #   return bot_id

             #else:

              #  print("could not find user with the name"+slack_bot_user)

        #else:

         #   print("could not find the user because api_call did not return 'ok'")


        #return None


    @staticmethod
    
    def get_AMQ_online_store():

        load_dotenv(os.path.join(os.path.dirname(__file__),".env"))

        #use these env vars first if set

        #bot_id=os.environ.get("BOT_ID")
        #slack_bot_token=os.environ.get("SLACK_BOT_TOKEN")
        assistant_username=os.environ.get("ASSISTANT_USERNAME")
        assistant_password=os.environ.get("ASSISTANT_PASSWORD")
        assistant_iam_apikey=os.environ.get("ASSISTANT_IAM_APIKEY")
        assistant_url=os.environ.get("ASSISTANT_URL")
        #workspace_id=os.environ.get("WORKSPACE_ID")
        if not assistant_url:

            #Direct access to VCAP to work around SDK problems

            vcap_services=os.environ.get("VCAP_SERVICES")
            vcap_env=json.loads(vcap_services) if vcap_services else None
            if vcap_env:

                assistant_creds=WatsonEnv.get_vcap_credentials(vcap_env,'conversation')

                if assistant_creds:

                    assistant_url=assistant_creds['url'] #overrides default
                    assistant_iam_apikey=(assistant_iam_apikey or assistant_creds.get('apikey'))

        cloudant_username=os.environ.get("CLOUDANT_USERNAME")
        cloudant_password=os.environ.get("CLOUDANT_PASSWORD")
        cloudant_url=os.environ.get("CLOUDANT_URL")
        cloudant_db_name=os.environ.get("CLOUDANT_DB_NAME")

        discovery_username=os.environ.get('DISCOVERY_USERNAME')
        discovery_password=os.environ.get('DISCOVERY_PASSWORD')
        discovery_url=os.environ.get('DISCOVERY_URL')
        discovery_iam_apikey=os.environ.get("DISCOVERY_IAM_APIKEY")
        

        # if the CLOUDANT_USERNAME env var was not set then use
        # VCAP_SERVICES like a WatsonService would

        if not cloudant_username:

            vcap_services=os.environ.get("VCAP_SERVICES")
            vcap_env=json.loads(vcap_services) if vcap_services else None

            if vcap_env:

                cloudant_creds=WatsonEnv.get_vcap_credentials(vcap_env,'cloudantNoSQLDB')

                if cloudant_creds:

                    cloudant_url=cloudant_creds['url']
                    if 'username' in cloudant_creds:

                           cloudant_username=cloudant_creds['username']

                    if 'password' in cloudant_creds:

                            cloudant_password=cloudant_creds['password']


        #Instantiate Watson Assistant Client
        #-only give url if we have one (dont over ride the default)

        assistant_kwargs={
            
            'version':'2018-07-10',
            'username':assistant_username,
            'password':assistant_password,
            'iam_apikey':assistant_iam_apikey
            
        }

        if assistant_url:

            assistant_kwargs['url'] = assistant_url

        assistant_client=AssistantV1(**assistant_kwargs)

        # Instantiate Cloudant DB

       # cloudant_online_store = CloudantOnlineStore(

        #    Cloudant(
         #       cloudant_username,
                #cloudant_password,
                #url = CloudantOnlineStore.optimize_cloudant_url(cloudant_url),
                #connect=True
            #),
            #cloudant_db_name
        #)

        #Instantiate Watson Discovery Client
        #-only give a url if we have one(don't override the default)

        discovery_kwargs={

            'version':'2018-08-01',
            'username':discovery_username,
            'password':discovery_password,
            'iam_apikey':discovery_iam_apikey,
                       
        }
        if discovery_url:

            discovery_kwargs['url']=discovery_url

        discovery_client=DiscoveryV1(**discovery_kwargs)

        #Instantiate Slack chatbot

        #if not slack_bot_token or 'placeholder' in slack_bot_token:
         #   print("SLACK_BOT_TOKEN should be correctly set."
          #        "It is currently set to '%s'." % slack_bot_token)
           # print("only the WEB UI will be available")

            #slack_client=None
        #else:

         #   slack_client=SlackClient(slack_bot_token)
            # if BOT_ID wasn't set, we can get it using SLACK_BOT_USER
          #  if not bot_id:
           #     bot_id=WatsonEnv.get_slack_user_id(slack_client)
            #    if not bot_id:

             #       print("Error: Missing BOT_ID or invalid SLACK_BOT_USER")

              #      return None
        
        #user=current_user.username
        #print (user)
        #print ("user2")
        #start AMQ Online Store app

        #AMQonlinestore= AMQOnlineStore (assistant_client,discovery_client,cloudant_online_store,user)
        AMQonlinestore= AMQOnlineStore (assistant_client,discovery_client)
        return AMQonlinestore
        


if __name__=="__main__":

   AMQonlinestore=WatsonEnv.get_AMQ_online_store()

   #if AMQonlinestore:

   #AMQonlinestore.run()