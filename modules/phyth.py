import sys
import json
import os

def getData():
	json_data = sys.argv[1]
	data = json.loads(json_data)
	return data

def getRawData():
	return sys.argv[1]

def error(error_msg):
	# if causing errors, make sure web server user owns log.txt
	with open("log.txt", "a") as myfile:
		myfile.write(error_msg+"\n")

def respond(data_dict, error):
	reply_data = { 'data': data_dict,'error': error }
	print json.dumps(reply_data, separators=(',',':'))

def start(func):
	try:
		func()
		cleanTmpDir()
	except Exception as e:
		# when a module throws an error and does not handle it
		respond("", {"msg":"ERROR: Module failed; exception not handled by module", "raw":str(e)})

def verifyFile(file_data):
	file_path = str(os.getcwd())+"/tmp/"+file_data['name']
	if (
		file_data['error'] == 0 and # did php mark any errors?
		file_data['size'] > 0 and   # did php actually get a file i.e. does it have any bytes
		os.path.isfile(file_path)   # was the file moved to the phyth tmp dir?
		):
		return True
	else:
		return False

def cleanTmpDir():
	# Deletes all files in tmp dir after script completion
	tmp_dir_path = os.getcwd()+"/tmp/"
	file_names = os.listdir(tmp_dir_path)
	for file in file_names: 
		error("File: "+file+" was deleted from tmp dir")
		os.remove(tmp_dir_path+file)





