from esmond.api.client.perfsonar.query import ApiConnect, ApiFilters
from esmond.api.client.perfsonar.post import MetadataPost, EventTypePost, EventTypeBulkPost
import time
from optparse import OptionParser

filters = ApiFilters()
parser = OptionParser()

class EsmondUploader(object):
	
	def __init__(self,verbose=True,start=-3600,end=0,connect='http://hcc-pki-ps02.unl.edu',username='afitz',key='fc077a6a133b22618172bbb50a1d3104a23b2050'):
		
		# Filter variables
		filters.verbose = verbose
		filters.time_start = time.time() + start
		filters.time_end = time.time() + end
		
		
		# Username/Key/Location
		self.connect = connect
		self.username = username
		self.key = key
		self.goc = 'http://osgnetds.grid.iu.edu'
		self.conn = ApiConnect(self.connect,filters)

		
		# Metadata variables
		self.destination = ''
		self.input_destination = ''
		self.input_source = ''
		self.measurement_agent = ''
		self.sample_bucket_width = ''
		self.source = ''
		self.subject_type = ''
		self.time_duration = ''
		self.tool_name = ''

	# Get Data
	def getData(self):
		for md in self.conn.get_metadata():
			# Assigning each meta data object property to class variables
			self.destination = md.destination
			self.input_destination = md.destination
			self.input_source = md.input_source
			self.measurement_agent = md.measurement_agent
			self.sample_bucket_width = md.sample_bucket_width
			self.source = md.source
			self.subject_type = md.subject_type
			self.time_duration = md.time_duration
			self.tool_name = md.tool_name
			
	# Post Data
	def postData(self):
		args = {
			"subject_type": self.subject_type,
			"source": self.source,
			"destination": self.destination,
			"tool_name": self.tool_name,
			"measurement_agent": self.measurement_agent,
			"input_source": self.connect,
			"input_destination": self.goc,
			"time_duration": self.time_duration,
			# "ip_transport_protocol": "tcp"
		}
	
		mp = MetadataPost(self.goc,username=self.username, api_key=self.key, **args)			
		

		new_meta = mp.post_metadata()	
