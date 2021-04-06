#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, marshal, fields
from flask import  request, jsonify
import json
import logging
import requests
import sys
import os
# Initialize Flask
app = Flask(__name__)
api = Api(app)


# In[ ]:




@app.route('/<int:id>', methods=['DELETE'])
def buy(id):
            
    """first verify that the item is in stock by querying the catalog server and then 
    decrement the number of items in stock by one. 
    The buy request can fail if the item is out of stock."""
    constructed_paylod = {}
    quered_topic = ''
    asked_by = ''
    if id:
        logging.info("request received: received request for buying item %s"%(str(id)))
        headers = {"Content-Type": "application/json"}
        constructed_paylod ={}
        asked_by = "\""+"$id\""
        quered_topic = "\""+str(id)+"\""
        constructed_paylod[asked_by] = quered_topic
        constructed_paylod = [constructed_paylod]
        constructed_paylod = str(constructed_paylod)
        constructed_paylod =constructed_paylod.replace("'", '')
        response = requests.get(catalog_server_URL+str(id), data={}, headers={})
        record = json.loads(response.content.decode('utf-8'))

        record = record[0]
        #print(type(record),record)
        try:
            if record["response"]=="0":
                response ="We do not have enough of this item"
        except:
            constructed_paylod ={}
            asked_by = "\""+"$id\""
            quered_topic = "\""+str(id)+"\""
            constructed_paylod[asked_by] = quered_topic
            #call catalog server
            constructed_paylod = [constructed_paylod]
            constructed_paylod = str(constructed_paylod)
            constructed_paylod =constructed_paylod.replace("'", '')
            #print("we have this item in catalog let decrease it by askin the catalog to do that for us ",constructed_paylod)
            response = requests.post(catalog_server_URL, data=constructed_paylod, headers=headers)
            record = json.loads(response.content.decode('utf-8'))
            record = record[0]
            if record["response"]=="1":
                response ="Item numbers was decreased on the database sucessfully"
            elif record["response"]=="0":
                response ="We do not have enough of this item"
            elif record["response"]=="-1":
                response ="Unfortunately we do not have this item"
            elif record["response"]=="-2":
                response ="This is not a valid request"
    else:
        response ="This is not a valid request"
        logging.info("request received: This is not a valid request ")
    logging.info("request processed: received request for buying item %s processed"%(str(id)))
    return jsonify({"reponse":response})

    return jsonify(record)


# In[ ]:


order_log_file = 'orderserver_log_file.log'
logging.basicConfig(filename=order_log_file, filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)
if __name__ == "__main__":
    server_IP = sys.argv[1]
    catalog_server_URL = "http://"+sys.argv[2]+":5000/"
    print("running order microservice..........")
    logging.info("running order microservice..........")
    app.run(host=server_IP, port=5000)

