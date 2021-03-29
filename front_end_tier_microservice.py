#!/usr/bin/env python
# coding: utf-8

# In[25]:


from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, marshal, fields
from flask import  request, jsonify
import json
import requests
# Initialize Flask
app = Flask(__name__)
api = Api(app)


# In[ ]:





# In[ ]:





# In[ ]:


catalog_server_URL     = 'http://127.0.0.2:5000/'
order_server_URL = 'http://127.0.0.3:5000/'


# In[ ]:


# help="The title of the book must be provided"
# help="The author of the book must be provided"
# help="The length of the book (in pages)"
# help="The rating must be provided"
 # Check if the passed value is not null
    
@app.route('/', methods=['GET'])
def lookup():
    """allows the user to specify a topic and returns all entries belonging to that category (a title and an item number are displayed for each match)."""
    if request.data:
        json_data = json.loads(request.data.decode(encoding='UTF-8'))

        print('we are in default get',json_data)
        payload = { 'key' : 'val' }
        data = '[{"$key": 8},{"$key": 7}]'
        data = '{"$key": 8,},{"$key": 7}'
        data = '[{"$key": 8,"$topic": "coding"},{"$key": 7,"$topic": "testing"}]'
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
                        print(key,value)
                elif 'id'==key:
                    if value:
                        asked_by = "\""+"$"+str(key)+"\""
                        quered_topic = "\""+str(value)+"\""
            constructed_paylod[asked_by] = quered_topic
            #call catalog server
            constructed_paylod = [constructed_paylod]
            constructed_paylod = str(constructed_paylod)
            constructed_paylod =constructed_paylod.replace("'", '')
            print("going to ask catalog about ",constructed_paylod)
            print("default is ",data)
            response = requests.get(catalog_server_URL, data=constructed_paylod, headers=headers)
            response = response.content
            print("this is what we got from catalog server ",response)
        else:
            response = jsonify({'response':'Please specifiy another %s'%(asked_by)})
    else:
        print("this is without data")
        response = requests.get(catalog_server_URL, data={}, headers={})
        response = response.content
    return response
    return jsonify({'results from other microserver': res})
    
@app.route('/<string:topic>', methods=['GET'])
def search(topic):
    """allows the user to specify a topic and returns all entries belonging to that category (a title and an item number are displayed for each match)."""
    name = request.args.get('name')
    print('we are in search by topic',topic,name,request.args)
    
    payload = { 'key' : 'val' }
    headers = {}
    #call catalog server
    res = requests.get(catalog_server_URL, data=payload, headers=headers)
    print("this is what we got from catalog server ",res.content)
    return res.content
    return jsonify({'results from other microserver': res})
# @app.route('/<int:id>', methods=['GET'])
# def lookup(id):
#     """allows the user to specify a topic and returns all entries belonging to that category (a title and an item number are displayed for each match)."""
#     name = request.args.get('name')
#     print('we are in lookup',id,name,request.args)
#     url     = 'http://127.0.0.2:5000/'
#     payload = { 'key' : 'val' }
#     headers = {}
#     #call catalog server
#     res = requests.get(url, data=payload, headers=headers)
    
# #     with open('/tmp/data.txt', 'r') as f:
# #         data = f.read()
# #         records = json.loads(data)
# #         for record in records:
# #             if record['name'] == name:
# #                 return jsonify(record)
#     print("this is what we got from catalog server ",res.content)
#     return res.content
#     return jsonify({'results from other microserver': res})

@app.route('/', methods=['PUT'])
def create_record():
    print("we are in create records ")
    try:
        json_data = json.loads(request.data)
        print(json_data)
        url     = 'http://127.0.0.2:5000/'
        payload = { 'key' : 'val' }
        data = '[{"$key": 8},{"$key": 7}]'
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
                print("going to put this in catalog about ",constructed_paylod)
                response = requests.put(catalog_server_URL, data=constructed_paylod, headers=headers)
                response = response.content
                print("this is what we got from catalog server ",response)
        else:
            response = jsonify({'response':'Please set these values %s in your request %s'%(result)})
    except ValueError:
        print("ValueError",ValueError)
        response = jsonify({'response':'This is not a valid request'%(json_data)})

    return response

    
@app.route('/<int:id>', methods=['DELETE'])
def buy(id):
    """specifies an item number for purchase."""
    try:
        if id:
            print("we are in buy function at front tier")
            headers = {}
            constructed_paylod = {}
            quered_topic = "\""+str(id)+"\""
            asked_by = "\""+"$item_number\""
            constructed_paylod[asked_by] = quered_topic
            constructed_paylod = [constructed_paylod]
            constructed_paylod = str(constructed_paylod)
            constructed_paylod =constructed_paylod.replace("'", '')
            print("going to buy this in order about ",constructed_paylod)
            response = requests.delete(order_server_URL+"/"+str(id), data=constructed_paylod, headers=headers)
            response = response.content
            print("this is what we got from catalog server ",response)
        else:
            response = jsonify({'response':'Please set a valid item number %s in your request %s'%(str(id))})
    except ValueError:
        print("ValueError",ValueError)
        response = jsonify({'response':'This is not a valid request'%(str(id))})

    return response

@app.route('/', methods=['POST'])
def update_record():
    print("we are in update record")
    try:
        json_data = json.loads(request.data)
        print(json_data)
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
                print("going to put this in catalog about ",constructed_paylod)
                response = requests.put(catalog_server_URL, data=constructed_paylod, headers=headers)
                response = response.content
                print("this is what we got from catalog server ",response)
        else:
            response = jsonify({'response':'Please set these values %s in your request %s'%(result)})
    except ValueError:
        print("ValueError",ValueError)
        response = jsonify({'response':'This is not a valid request'%(json_data)})

    return response


# In[ ]:



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)

