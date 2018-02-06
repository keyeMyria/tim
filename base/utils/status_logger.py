from pymongo import MongoClient
from pymongo import ASCENDING
import datetime
import os

class MongodbLogger:
    def __init__(self,hostname='localhost', port=27017, database='oneiros', collection='status_log'):
	
	client = MongoClient(hostname, port)
	db = client[database]
	self.log_collection = db[collection]
	self.log_collection.ensure_index([("timestamp", ASCENDING)]) 
	self.pid = os.getpid()

    def _entry(self):
	entry = {}
	entry['timestamp'] = datetime.datetime.utcnow()
	entry['pid'] = self.pid
	return dict(entry)

    def info(self,msg):
        """Log `msg` to MongoDB log"""
	entry = self._entry()
        entry['msg'] = msg
        self.log_collection.insert(entry)

    def error(self,msg):
        """Log `msg` to MongoDB log"""
	entry = self._entry()
        entry['error'] = msg
        self.log_collection.insert(entry)

    def status(self,msg):
        """Log `msg` to MongoDB log"""
	entry = self._entry()
	if isinstance(msg, dict):
	   for key, value in msg.iteritems():
		entry[key] = value
	else: entry['status'] = msg
        self.log_collection.insert(entry)

    def _find_line(self, msg):
	pass	
