#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, marshal, fields
from flask import  request, jsonify
import json
import csv
import logging
import sys
import os
import time
# Initialize Flask
app = Flask(__name__)
api = Api(app)

warehouse_file = 'items_warehouse_file.csv'
global_id_counter = 1


# In[ ]:





# In[ ]:


@app.route('/', methods=['GET'])
def default_query():
    """an item is specified and all relevant details are returned"""
    # we add this 20 milliseconds to evaluate the benefit of caching
    time.sleep(0.02)
    items_found = []
    if request.data:
        json_data = json.loads(request.data.decode(encoding='UTF-8'))
        logging.info("request for GET received: "+str(json_data))
        json_data = json_data[0]
        try:
            if json_data["$topic"]:
                for record,values in each_book_info.items():
                    if values['topic'] in json_data["$topic"] or json_data["$topic"] in values['topic']:
                        items_found.append(values)
        except:
            try:
                if json_data["$id"]:
                    for record,values in each_book_info.items():
                        if int(record) == int(json_data["$id"]):
                            values["$item_number"] = record
                            items_found.append(values)
#                         else:
#                             print('what',record , int(json_data["$id"]),each_book_info)
            except ValueError:
                print('oops! ValueError',ValueError)
                pass
        #print("these are all found items ",items_found)
        if items_found:
            logging.info("request for GET processed: "+str(items_found))

            return items_found
        else:
            logging.info('request for GET processed')
            return jsonify({'oops! there is no item for your request!':''})
    else:
        logging.info("request for GET received: asking all records")
        for record,values in each_book_info.items():
            values["item_number"] = record
            items_found.append(values)
        logging.info("request for GET proessed")
        return jsonify(items_found)
    
@app.route('/<string:topic>', methods=['GET'])
def query_records_topic(topic):
    # we add this 20 milliseconds to evaluate the benefit of caching
    time.sleep(0.02)
    """a topic is specified and the server returns all matching entries"""
    logging.info("request for GET:topic received: "+str(topic))
    items_found = []
    if topic:
        for record in each_book_info:
            if record['topic'] in topic or topic in record['topic']:
                items_found.append(record)
                
    if items_found:
        logging.info("request for GET topic processed: "+str(topic))
        return jsonify(items_found)
    else:
        logging.info("request for GET topic processed: "+str(topic))
        return jsonify({'response':'there is no item with topic '+topic})
    
    
@app.route('/<int:id>', methods=['GET'])
def query_records(id):
    # we add this 20 milliseconds to evaluate the benefit of caching
    if int(id)==4444:
        return jsonify([{"response":"heart_beat"}])
    else:
        time.sleep(0.02)    
        if int(id)>2021 and int(id)<4021:
            ID = int(id)%2021
            try:
                for ID,values in each_book_info.items():
                    if int(json_data["$id"]) == int(ID):
                        if int(values["number"])>0:
                            each_book_info[ID] = {"title":values['title'],"number":(int(values['number'])-1),"cost":values['cost'],"topic":values['topic']}
                            response = "1"
                        else:
                            response = "0"
                        exist = True
                        break

            except:
                response = "-2"

        else:

            logging.info("request for GET id received: "+str(id))
            items_found = []

            for record,values in each_book_info.items():
                #print('each_book_info',each_book_info)
                if int(record) == int(id):
                    values["$item_number"] = record
                    items_found.append(values)
                    logging.info("request for GET id processed: "+str(items_found))
                    return jsonify(items_found)
            logging.info("request for GET id processed: "+str(id))
            return jsonify([{"response":"0"}])
    

@app.route('/', methods=['PUT'])
def create_record():
    # we add this 20 milliseconds to evaluate the benefit of caching
    time.sleep(0.02)  
    json_data = json.loads(request.data.decode(encoding='UTF-8'))
    json_data = json_data[0]
    logging.info("request for PUT received: "+str(json_data))
    if json_data:
        global global_id_counter
        exist = False
        for ID,values in each_book_info.items():
            if json_data["$title"] == values['title']:
                exist = True
                break
        if exist:
            #print(values)
            each_book_info[ID] = {"title":values['title'],"number":(int(values['number'])+1),"cost":values['cost'],"topic":values['topic']}
            response = "We increased the number of this book by one sucessfully!"
        else:
            each_book_info[global_id_counter] = {"title":json_data["$title"] ,"number":json_data["$number"] ,"cost":json_data["$cost"] ,"topic":json_data["$topic"] }    
            global_id_counter+=1
            response = "Item was added successfully!"
        available_catalog_servers  = fault_tolerent_object.ongoing_replica_checker("catalog")
        
        headers = {"Content-Type": "application/json"}
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
        
        for replicated_catalog_server_URL in available_catalog_servers:
            if replicated_catalog_server_URL not in catalog_server_URL:
                response = requests.put(replicated_catalog_server_URL, data=constructed_paylod, headers=headers)
    else:
        response = 'Please add valid records!'
    logging.info("request for PUT processed: "+response)
    return jsonify({"Reponse from server":response})

@app.route('/', methods=['POST'])
def update_record():
    """allows the cost of an item to be updated"""
    
    # we add this 20 milliseconds to evaluate the benefit of caching
    time.sleep(0.02)
    json_data = json.loads(request.data.decode(encoding='UTF-8'))
    logging.info("request for POST received: "+str(json_data))
    items_found = []
    
    json_data = json_data[0]

    exist = False
    
    try:
        for ID,values in each_book_info.items():
            if int(json_data["$id"]) == int(ID):
                if int(values["number"])>0:
                    each_book_info[ID] = {"title":values['title'],"number":(int(values['number'])-1),"cost":values['cost'],"topic":values['topic']}
                    response = "1"
                else:
                    response = "0"
                exist = True
                break
        if not exist:
            response = "-1"
    except:
        response = "-2"
    logging.info("request for POST processed: "+response)
    return jsonify([{"response":response}])
    
@app.route('/', methods=['DELETE'])
def delete_record():
    record = json.loads(str(request.data))
    json_data = json.loads(request.data.decode(encoding='UTF-8'))
    logging.info("request received: "+json_data)
    new_records = []
    logging.info("request processed: "+str(json_data))
    return jsonify(record)


# In[ ]:





# In[7]:


books = [{
            "id": 1,
            "title": "How to get a good grade in 677 in 20 minutes a day.",
            "number": 10,
            "cost": 195,
            "topic": "distributed systems"
        },
            {
            "id": 2,
            "title": "RPCs for Dummies.",
            "number": 100,
            "cost": 319,
            "topic": "distributed systems"
        },
            {
            "id": 3,
            "title": "Xen and the Art of Surviving Graduate School.",
            "number": 54,
            "cost": 195,
            "topic": "graduate school"
        },
            {
            "id": 4,
            "title": "Cooking for the Impatient Graduate Student.",
            "number": 46,
            "cost": 319,
            "topic": "graduate school"
        }
]

each_book_info = {}
with open(warehouse_file, "r") as f:
        reader = csv.reader(f, delimiter=",")
        for line in (reader):
            item_record_ID = int(line[0])
            title = line[1]
            number = int(line[2])
            cost = float(line[3])
            topic = line[4]
            each_book_info[global_id_counter] = {"title":title,"number":number,"cost":cost,"topic":topic}
            global_id_counter+=1


# In[ ]:


catalog_log_file = 'catalog_log_file.log'
logging.basicConfig(filename=catalog_log_file, filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)

if __name__ == "__main__":
    server_IP = sys.argv[1]
    server_port = sys.argv[2]
    print("running catalog microservice..........",server_IP)
    logging.info("running catalog microservice..........")
    app.run(host=server_IP, port=int(server_port))

