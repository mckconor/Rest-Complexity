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
import lizard

application = Flask(__name__)

#DB and server details
serv_addr = "localhost"
port = "27017"
full_serv_addr = "http://127.0.0.1:5000"
mongo_db_addr = "mongodb://" + serv_addr + ":" + port
mongo_client = pymongo.MongoClient(mongo_db_addr)
mongo_db = mongo_client.authServ	#connect in to auth db
home_directory = os.path.dirname(os.path.realpath('__file__'))
headers = {"Content-type": "application/json"}

git_repo_url = ""
workerId = -1

def registerWorkerNode():
	response = requests.post(full_serv_addr + "/register", data=json.dumps({}), headers=headers)
	
	global workerId
	workerId = response.json().get('worker_id')
	
	global git_repo_url
	git_repo_url = response.json().get('repo_url')

def submitWork(file, commit, score):
	results = {'file': file, 'commit': commit, 'score': score}
	requests.post(full_serv_addr + "/submitWork", data=json.dumps(results), headers=headers)

def doWork(file, commit):
	if(os.path.exists(home_directory + "/.worker" + str(workerId)) != True):
		print(git_repo_url)
		repo = Repo.clone_from(git_repo_url, home_directory + "/.worker" + str(workerId))
	else:
		repo = Repo(home_directory + "/.worker" + str(workerId))

	#checkout commit
	repo_checkout = repo.git.checkout(commit)

	score = lizard.analyze_file(file).average_cyclomatic_complexity

	print("File: ", file, "\nCommit: ", commit, "\nCC: ", score)

	submitWork(file, commit, score)

def requestWork():
	response = requests.get(full_serv_addr + "/getWork", headers=headers)
	response_json = response.json()

	if response_json.get('Finished') is True:
		return True

	doWork(response_json.get('file'), response_json.get('commit_number'))

def operations():
	while(requestWork() is not True):
		print("...\n")

if __name__ == '__main__':
	registerWorkerNode()
	operations()
	print("Done!")