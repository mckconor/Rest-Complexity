from flask import Flask
from git import Repo
import collections
from flask import jsonify
from flask import request
import os
import datetime
import glob
import pymongo

application = Flask(__name__)

# git_repo_url = "https://github.com/mckconor/Scalable-Computing-TCPServer"
git_repo_url = "https://github.com/mckconor/Python-DFS"
home_directory = os.path.dirname(os.path.realpath('__file__'))

serv_addr = "localhost"
port = "27017"
mongo_db_addr = "mongodb://" + serv_addr + ":" + port
mongo_client = pymongo.MongoClient(mongo_db_addr)
mongo_db = mongo_client.work_steal

mongo_db.workers.drop()
mongo_db.work.drop()

@application.route('/register', methods=['POST'])
def register():
	#register worker
	worker_data = request.get_json(force=True)

	worker_id = mongo_db.workers.count() + 1;
	worker_address = request.remote_addr

	worker = {"id": worker_id, "address": worker_address}

	mongo_db.workers.insert(worker)

	jsonString = {"response_code": 200}
	return jsonify(jsonString)

def getUnassignedWork():
	work = mongo_db.work.find_one({'completed' : False})
	return work

@application.route('/getWork', methods=['GET'])
def giveWork():
	#get work from db, give to requester
	workToDo = getUnassignedWork()

	file = workToDo.get("file_path")
	jsonString = {"file": file}

	mongo_db.work.update_one({'file_path': file}, {"$set":{"worker": mongo_db.workers.find_one({"address": request.remote_addr})}})

	return jsonify(jsonString)

@application.route('/submitWork', methods=['GET'])
def receiveWork():
	print("")


def getAllFiles ():
	files = glob.glob(home_directory + "/managerRepo" + '/**/*' + ext, recursive = True)
	return files


def compileWorkList():
	#Download copy of repo
	if(os.path.exists(home_directory + "/.managerRepo") != True):
		repo = Repo.clone_from(git_repo_url, home_directory + "/.managerRepo")
	else:
		repo = Repo(home_directory + "/.managerRepo")

	#all commits
	list_of_commits = list(repo.iter_commits())
	for commit in list_of_commits:
		repo.git.checkout(commit)
		files = glob.glob(home_directory + "/.managerRepo" + '/**/*' + ".py", recursive = True)

		for f in files:
			file = {"commit": str(commit), "file_path": f, "start_time": -1, "completed": False, "worker": "", "worker_addr": "", "cyclo_comp": -1}
			mongo_db.work.insert(file)


if __name__ == '__main__':
	compileWorkList()
	application.run()