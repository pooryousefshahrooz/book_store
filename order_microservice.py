#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, marshal, fields
from flask import  request, jsonify
import json
import logging
import requests
# Initialize Flask
app = Flask(__name__)
api = Api(app)
catalog_server_URL     = 'http://127.0.0.2:5000/'


# In[ ]:




@app.route('/<int:id>', methods=['DELETE'])
def buy(id):
            
    """first verify that the item is in stock by querying the catalog server and then 
    decrement the number of items in stock by one. 
    The buy request can fail if the item is out of stock."""
    constructed_paylod = {}
    quered_topic = ''
    asked_by = ''
    print("we are in buy that is for buy")
    if id:
        headers = {"Content-Type": "application/json"}
        constructed_paylod ={}
        asked_by = "\""+"$id\""
        quered_topic = "\""+str(id)+"\""
        constructed_paylod[asked_by] = quered_topic
        #call catalog server
        constructed_paylod = [constructed_paylod]
        constructed_paylod = str(constructed_paylod)
        constructed_paylod =constructed_paylod.replace("'", '')
        print("going to buy this item to ask catalog ",constructed_paylod)
        response = requests.get(catalog_server_URL, data=constructed_paylod, headers=headers)
        response = response.content
        record = json.loads(response)
        record = record[0]
        print(type(record),record)
        if record:
            constructed_paylod ={}
            asked_by = "\""+"$id\""
            quered_topic = "\""+str(id)+"\""
            constructed_paylod[asked_by] = quered_topic
            #call catalog server
            constructed_paylod = [constructed_paylod]
            constructed_paylod = str(constructed_paylod)
            constructed_paylod =constructed_paylod.replace("'", '')
            print("going to buy this item to ask catalog ",constructed_paylod)
            response = requests.post(catalog_server_URL, data=constructed_paylod, headers=headers)
            response = response.content
            record = json.loads(response)
            print("after updating from catalog",type(record),record)
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
    return jsonify({"reponse":response})
#     json_data = json.loads(request.data.decode(encoding='UTF-8'))
#     logging.info(json_data)
#     new_records = []
    print("we are order server buy record ",record)
#     with open('/tmp/data.txt', 'r') as f:
#         data = f.read()
#         records = json.loads(data)
#         for r in records:
#             if r['name'] == record['name']:
#                 continue
#             new_records.append(r)
#     with open('/tmp/data.txt', 'w') as f:
#         f.write(json.dumps(new_records, indent=2))
#     logging.info(json_data)
    return jsonify(record)


# In[ ]:


# order_log_file = 'orderserver_log_file.log'
# logging.basicConfig(filename=order_log_file, filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)
if __name__ == "__main__":
    app.run(host="127.0.0.3", port=5000)

