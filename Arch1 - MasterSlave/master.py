from flask import Flask
import slave
from git import Repo
import collections
from flask import jsonify
from flask import request

application = Flask(__name__)

commit_dictionary = {}

@application.route('/getWork', methods=['GET'])
def getWork():
	####
	commit_dictionary.update({"Commit #" + str(len(commit_dictionary) + 1) : -1})
	jsonString = {"commit_number": len(commit_dictionary)}
	return jsonify(jsonString)


@application.route('/submitWork', methods=['POST'])
def submitWork():
	####
	in_data = request.get_json(force=True)

	commit_number = "Commit #" + in_data.get('commit_number')
	commit_complexity = in_data.get('commit_complexity')

	# commit_dictionary.update({commit_number:commit_complexity})
	#Order dictionary in case one completes early
	# commit_dictionary = collections.OrderedDict(sorted(commit_dictionary.items()))

	commit_dictionary[commit_number] = commit_complexity

if __name__ == '__main__':
	application.run()