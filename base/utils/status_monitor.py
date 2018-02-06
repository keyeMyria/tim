from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
import datetime
import os
from status_logger import MongodbLogger
import psutil
import config_parser

class StatusMonitor:
    def __init__(self, database='oneiros', port='27017'):

        hostname = 'localhost'
        port = 27017
        database='oneiros'
        collection='status_log'


	client = MongoClient(hostname, port)
	db = client[database]
	self.collection = db[collection]
	get_installed = self._get_installed()
        self.installed_bots = get_installed['installed']

    def _find_pid(self, pid):
	if psutil.pid_exists(pid):
	   return True
	else: return False

    def _get_installed(self):
	conf = config_parser.StartupConfig()
	installed_bots = conf.bots()
	return installed_bots


    def _running_bots(self):
	# monitor proc pid, find out if the pid in the db is the one that is running
	# find installed > find has running > find if actually running > return pids
	running_bots = {}
	for bot in self.installed_bots:
	    latest = self.collection.find({
	             "bot_name": bot, 
		     "status": "running"
                     }).sort([('timestamp', DESCENDING)]).limit(1)
	    if latest.count() == 0:
		continue
	    else:
	        proc = latest.next()
		if self._find_pid(proc['pid']):
		   running_bots[bot] = proc['pid']
	return running_bots 

    def status(self):
	running = self._running_bots()
	status = {}
	for bot in self.installed_bots:
	    if bot in running:
	       info = {'pid':running[bot],'status':True}
	       status[bot] = info
	    else: status[bot] = {'pid':0,'status':False}
	return status










