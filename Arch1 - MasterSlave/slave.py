#Node for computing cyclomatic complexity
from threading import Thread
from git import Repo
import os
from flask import jsonify
from flask import request
import json
from pprint import pprint
import requests

master_url = "http://127.0.0.1:5000"
git_repo_url = "https://github.com/mckconor/Scalable-Computing-TCPServer"
home_directory = os.path.dirname(os.path.realpath('__file__'))
headers = {"Content-type": "application/json"}

def getWork():
	in_data = requests.get(master_url + "/getWork", headers=headers)
	json_data = json.loads(in_data.text)

	commit_number = json_data.get("commit_number")

	doWork(commit_number)

def doWork(commit_number):
	for commit in list(repo.iter_commits()):
		commit.stats.files

def submitWork(commit_number, commit_complexity):
	print("bye")

if __name__ == '__main__':
	getWork()