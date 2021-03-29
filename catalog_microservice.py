#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, marshal, fields
from flask import  request, jsonify
import json
import csv
import logging
# Initialize Flask
app = Flask(__name__)
api = Api(app)

warehouse_file = 'items_warehouse_file.csv'
global_id_counter = 1


# In[ ]:


class Catalog:
    def __init__(self):
        
        self.catalog_log_file = 'catalog_log_file.log'
        logging.basicConfig(filename=self.catalog_log_file, filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)

        # the list of all of the books
        books = {{
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
            }
        
        
        # Schema For the Book Request JSON
        bookFields = {
            "id": fields.Integer,
            "title": fields.String,
            "number": fields.Integer,
            "cost": fields.Integer,
            "topic": fields.String
        }
        
        
        for record in books:
            
            logging.info(record)
        
    def query_by_subject(self,subject):
        """a topic is specified and the server returns all matching entries"""
        logging.info(record)
        logging.info(record)
    def query_by_item(self,item):
        """an item is specified and all relevant details are returned"""
        logging.info(record)
        logging.info(record)
    def update_cost(self,item,new_cost):
        """allows the cost of an item to be updated"""
        logging.info(record)
        logging.info(record)
    def update(self,):
        """the number of items in stock to be increased or decreased."""
        logging.info(record)
        logging.info(record)
        


# In[ ]:


@app.route('/', methods=['GET'])
def default_query():
    items_found = []
    if request.data:
        json_data = json.loads(request.data.decode(encoding='UTF-8'))
        logging.info(json_data)
        
        print("at catalog and items ",json_data)
        json_data = json_data[0]
        #for key,value in json_data.items():
        #print("catalog servr ",key,value)
        try:
            if json_data["$topic"]:
                logging.info(topic)
                for record,values in each_book_info.items():
                    if values['topic'] in json_data["$topic"] or json_data["$topic"] in values['topic']:
                        items_found.append(values)
        except:
            try:
                if json_data["$id"]:
                    logging.info(topic)
                    for record,values in each_book_info.items():
                        if record == int(json_data["$id"]):
                            values["item_number"] = record
                            items_found.append(values)
                        else:
                            print('what',record , int(json_data["$id"]),each_book_info)
            except ValueError:
                print('ooppss ValueError',ValueError)
                pass
        if items_found:
            return jsonify(items_found)
        else:
            return jsonify({'oops! there is no item for your request!':''})
    else:
        for record,values in each_book_info.items():
            values["item_number"] = record
            items_found.append(values)
        #print('items_found ',items_found)
        return jsonify(items_found)
    
@app.route('/<string:topic>', methods=['GET'])
def query_records_topic(topic):
    logging.info(topic)
    items_found = []
    if topic:
        logging.info(topic)
        print('from the catalog server',name)
        
        for record in each_book_info:
            if record['topic'] in topic or topic in record['topic']:
                items_found.append(record)
                
    if items_found:
        return jsonify(items_found)
    else:
        return jsonify({'response':'there is no item with topic '+topic})
    
    
@app.route('/<int:id>', methods=['GET'])
def query_records(id):
    logging.info(id)
    name = request.args.get('name')
    print('from the catalog server',name)
#     url     = 'http://example.tld'
#     payload = { 'key' : 'val' }
#     headers = {}
#     res = requests.post(url, data=payload, headers=headers)
    
#     with open('/tmp/data.txt', 'r') as f:
#         data = f.read()
#         records = json.loads(data)
#         for record in records:
#             if record['name'] == name:
#                 return jsonify(record)
    logging.info(id)
    return jsonify({'hi':'you got it!'})

@app.route('/', methods=['PUT'])
def create_record():
    
    print("we are catalog server create record ",request.data)
    json_data = json.loads(request.data.decode(encoding='UTF-8'))
    json_data = json_data[0]
    logging.info(json_data)
    if json_data:
#         json_data = json.loads(str(request.data))
        print("******* it is not none",json_data,type(json_data))
        global global_id_counter
        exist = False
        for ID,values in each_book_info.items():
            if json_data["$title"] == values['title']:
                exist = True
                break
        if exist:
            print(values)
            each_book_info[ID] = {"title":values['title'],"number":(int(values['number'])+1),"cost":values['cost'],"topic":values['topic']}
            response = "We increased the number of this book by one sucessfully!"
        else:
            each_book_info[global_id_counter] = {"title":json_data["$title"] ,"number":json_data["$number"] ,"cost":json_data["$cost"] ,"topic":json_data["$topic"] }    
            global_id_counter+=1
            response = "Item was added successfully!"
        logging.info(response)
    else:
        response = 'Please add valid records!'
    return jsonify({"Reponse from server":response})

@app.route('/', methods=['POST'])
def update_record():

    
    json_data = json.loads(request.data.decode(encoding='UTF-8'))
    logging.info(json_data)
    items_found = []
    
    json_data = json_data[0]
    print("at catalog and items ",json_data,each_book_info,json_data["$id"])
    logging.info(json_data)

    print(json_data)
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
    logging.info(response)
    return jsonify({"response":response})
    
@app.route('/', methods=['DELETE'])
def delete_record():
    record = json.loads(request.data)
    json_data = json.loads(request.data.decode(encoding='UTF-8'))
    logging.info(json_data)
    new_records = []
    print("we are catalog server delete record ",record)
#     with open('/tmp/data.txt', 'r') as f:
#         data = f.read()
#         records = json.loads(data)
#         for r in records:
#             if r['name'] == record['name']:
#                 continue
#             new_records.append(r)
#     with open('/tmp/data.txt', 'w') as f:
#         f.write(json.dumps(new_records, indent=2))
    logging.info(json_data)
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
# for item in books:
# #     for k,value in item.items():
# #         print(k,value)
#     with open(items_warehouse_file, 'a') as newFile:
#         newFileWriter = csv.writer(newFile)
#         newFileWriter.writerow([item['id'],item['title'],item['number'],item['cost'],item['topic']]) 


# In[ ]:


# catalog_log_file = 'catalog_log_file.log'
# logging.basicConfig(filename=catalog_log_file, filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)

if __name__ == "__main__":
    app.run(host="127.0.0.2", port=5000)

