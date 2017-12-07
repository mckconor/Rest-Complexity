#Node for computing cyclomatic complexity
from threading import Thread
from git import Repo
import os
from flask import jsonify
from flask import request
import json
from pprint import pprint
import requests
from flask import Flask
import pymongo

application = Flask(__name__)

#DB and server details
serv_addr = "localhost"
port = "27017"
full_serv_addr = "http://127.0.0.1:5000"
mongo_db_addr = "mongodb://" + serv_addr + ":" + port
mongo_client = pymongo.MongoClient(mongo_db_addr)
mongo_db = mongo_client.authServ	#connect in to auth db
headers = {"Content-type": "application/json"}

def registerWorkerNode():
	requests.post(full_serv_addr + "/register", data=json.dumps({}), headers=headers)

def requestWork():
	requests.get(full_serv_addr + "/getWork", headers=headers)

if __name__ == '__main__':
	registerWorkerNode()
	application.run()