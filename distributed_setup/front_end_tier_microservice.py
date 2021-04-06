#!/usr/bin/env python
# coding: utf-8

# In[25]:


from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, marshal, fields
from flask import  request, jsonify
import json
import requests
import sys
import os
# Initialize Flask

app = Flask(__name__)
api = Api(app)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:



@app.route('/', methods=['GET'])
def lookup():
   """allows the user to specify a topic and returns all entries belonging to that category (a title and an item number are displayed for each match)."""
   if request.data:
       json_data = json.loads(request.data.decode(encoding='UTF-8'))
       payload = { 'key' : 'val' }
       data = '[{"$key": 8},{"$key": 7}]'
       data = '[{"$topic": "testing"}]'
       headers = {"Content-Type": "application/json"}
       if json_data:
           constructed_paylod = {}
           quered_topic = ''
           asked_by = ''
           for key,value in json_data.items():
               if 'topic'==key:
                   if value:
                       quered_topic = "\""+value+"\""
                       asked_by = "\""+"$"+key+"\""
                       
               elif 'id'==key:
                   if value:
                       asked_by = "\""+"$"+str(key)+"\""
                       quered_topic = "\""+str(value)+"\""
           constructed_paylod[asked_by] = quered_topic
           #call catalog server
           constructed_paylod = [constructed_paylod]
           constructed_paylod = str(constructed_paylod)
           constructed_paylod =constructed_paylod.replace("'", '')
           response = requests.get(catalog_server_URL, data=constructed_paylod, headers=headers)
           response = response.content
       else:
           response = jsonify({'response':'Please specifiy another %s'%(asked_by)})
   else:
       response = requests.get(catalog_server_URL, data={}, headers={})
       response = response.content
   return response
   
@app.route('/<int:id>', methods=['GET'])
def query_records(id):
   items_found = []
   response = requests.get(catalog_server_URL+str(id), data={}, headers={})
   record = json.loads(response.content.decode('utf-8'))
   record = record[0]
   try:
       if record["response"]=="0":
           response ="Unfortunately we do not have enough of this item!"
   except:
       response=record
   return jsonify({'response':response})

@app.route('/<string:topic>', methods=['GET'])
def search(topic):
   """allows the user to specify a topic and returns all entries belonging to that category (a title and an item number are displayed for each match)."""
   name = request.args.get('name')

   payload = { 'key' : 'val' }
   headers = {}
   #call catalog server
   res = requests.get(catalog_server_URL, data=payload, headers=headers)
   return res.content
   return jsonify({'results from other microserver': res})

@app.route('/', methods=['PUT'])
def create_record():
   
   try:

       my_json = request.data.decode('utf8').replace("'", '"')

       json_data = my_json
       
       json_data = json_data[0]

       json_data = json.loads(json_data)

       payload = { 'key' : 'val' }
       data = '[{"$key": 8},{"$key": 7}]'
       headers = {"Content-Type": "application/json"}
       result = []
       if json_data:
           constructed_paylod = {}
           quered_topic = ''
           asked_by = ''
           print(json_data,type(json_data))
           for key,value in json_data.items():
                   if value:
                       quered_topic = "\""+str(value)+"\""
                       asked_by = "\""+str(key)+"\""
                       constructed_paylod[asked_by] = quered_topic
           #call catalog server
           result = set(['topic','title','number','cost']) - set(constructed_paylod)
           if result:
               constructed_paylod = [constructed_paylod]
               constructed_paylod = str(constructed_paylod)
               constructed_paylod =constructed_paylod.replace("'", '')
               response = requests.put(catalog_server_URL, data=constructed_paylod, headers=headers)
               response = response.content
       else:
           response = jsonify({'response':'Please set these values %s in your request %s'%(result)})
   except ValueError:
       response = jsonify({'response':'This is not a valid request'})

   return response

   
@app.route('/<int:id>', methods=['DELETE'])
def buy(id):
   """specifies an item number for purchase."""
   try:
       if id:
           headers = {}
           #print("going to buy this in order about ",str(id))
           response = requests.delete(order_server_URL+"/"+str(id), data={}, headers=headers)
           response = json.loads(response.content.decode('utf-8'))
           
       else:
           response = jsonify({'response':'Please set a valid item number %s in your request %s'%(str(id))})
   except ValueError:
       print("ValueError",ValueError)
       response = jsonify({'response':'This is not a valid request '})

   return response

@app.route('/', methods=['POST'])
def update_record():
   try:
       json_data = json.loads(request.data)
       #print(json_data)
       headers = {"Content-Type": "application/json"}
       result = []
       if json_data:
           constructed_paylod = {}
           quered_topic = ''
           asked_by = ''
           for key,value in json_data.items():
                   if value:
                       quered_topic = "\""+str(value)+"\""
                       asked_by = "\""+"$"+str(key)+"\""
                       constructed_paylod[asked_by] = quered_topic
           #call catalog server
           result = set(['topic','title','number','cost']) - set(constructed_paylod)
           if result:
               constructed_paylod = [constructed_paylod]
               constructed_paylod = str(constructed_paylod)
               constructed_paylod =constructed_paylod.replace("'", '')
               #print("going to put this in catalog about ",constructed_paylod)
               response = requests.put(catalog_server_URL, data=constructed_paylod, headers=headers)
               response = response.content
       else:
           response = jsonify({'response':'Please set these values %s in your request %s'%(result)})
   except ValueError:
       print("ValueError",ValueError)
       response = jsonify({'response':'This is not a valid request'})

   return response


# In[ ]:



if __name__ == "__main__":
    server_IP = sys.argv[1]
    catalog_server_URL = "http://"+sys.argv[2]+":5000/"
    order_server_URL = "http://"+sys.argv[3]+":5000/"
    print("running front end microservice..........")
    app.run(host=server_IP, port=5000)

