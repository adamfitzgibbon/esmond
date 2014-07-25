from esmond.api.client.perfsonar.query import ApiConnect, ApiFilters
from esmond.api.client.perfsonar.post import MetadataPost, EventTypePost, EventTypeBulkPost
import time

filters = ApiFilters()

class FilterArgs(object):
	
	def __init__(self,verbose=True,start=-3600,end=0,source='198.129.254.30',tool_name='bwcrtl/iperf3',connect='http://hcc-pki-ps02.unl.edu:8000',username='afitz',key='fc077a6a133b22618172bbb50a1d3104a23b2050'):
	
		filters.verbose = verbose
		filters.time_start = time.time() + start
		filters.time_end = time.time() + end
		filters.source = source
		filters.tool_name = tool_name
		self.connect = connect
		self.username = username
		self.key = key

	def apiConn(self):
		conn = ApiConnect(self.connect,filters)
		
		if not conn:
			print "Something went wrong!"
		
		else:
			return conn
	
	def getData(self,conn):
		for md in conn.get_metadata():
			print md

	def postData(self):
		args = {
			"subject_type": "point-to-point",
			"source": "10.10.0.1",
			"destination": "10.10.0.2",
			"tool_name": "bwctl/iperf3",
			"measurement_agent": "10.10.0.2",
			"input_source": "host1",
			"input_destination": "host2",
			# "time_duration": 30,
			# "ip_transport_protocol": "tcp"
		}
	
		mp = MetadataPost('http://localhost:8000/',username=self.username, api_key=self.key, **args)			
			
