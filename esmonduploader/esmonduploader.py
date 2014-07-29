from esmond.api.client.perfsonar.query import ApiConnect, ApiFilters
from esmond.api.client.perfsonar.post import MetadataPost, EventTypePost, EventTypeBulkPost
import time
from optparse import OptionParser

filters = ApiFilters()

parser = OptionParser()
parser.add_option('-b', help='boolean option', dest='bool', default=False, action='store_true')
(opts, args) = parser.parse_args()

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
		self.destination = []
		self.input_destination = []
		self.input_source = []
		self.measurement_agent = []
		self.sample_bucket_width = []
		self.source = []
		self.subject_type = []
		self.time_duration = []
		self.tool_name = []
		self.event_types = []
		self.summaries = []
		self.datapoint = []

	# Get Data
	def getData(self):
		for md in self.conn.get_metadata():
			# Assigning each metadata object property to class variables
			self.destination.append(md.destination)
			self.input_destination.append(md.input_destination)
			self.input_source.append(md.input_source)
			self.measurement_agent.append(md.measurement_agent)
			self.sample_bucket_width.append(md.sample_bucket_width)
			self.source.append(md.source)
			self.subject_type.append(md.subject_type)
			self.time_duration.append(md.time_duration)
			self.tool_name.append(md.tool_name)
			self.event_types.append(md.event_types)
			
			# Get Events and Data Payload
			temp_list = [] 
			temp_list2 = []
			for et in md.get_all_event_types():
				temp_list.append(et.summaries)
				dpay = et.get_data()
				for dp in dpay.data:
					tup = (dp.ts_epoch,dp.val)
				temp_list2.append(tup)
			self.datapoint.append(temp_list2)
			self.summaries.append(temp_list)

	# Post Data
	def postData(self):
		for i in range(len(self.destination)):
			# Looping through metadata
			args = {
				"subject_type": self.subject_type[i],
				"source": self.source[i],
				"destination": self.destination[i],
				"tool_name": self.tool_name[i],
				"measurement_agent": self.measurement_agent[i],
				"input_source": self.connect[i],
				"input_destination": self.goc[i],
				"time_duration": self.time_duration[i],
				# "ip_transport_protocol": "tcp"
			}
		
			mp = MetadataPost(self.goc,username=self.username, api_key=self.key, **args)			
			# Posting Event Types and Summaries
			for event_type, summary in zip(self.event_types[i], self.summaries[i]):
				mp.add_event_type(event_type)
				if summary:
					mp.add_summary_type(event_type, summary[0][0], summary[0][1])
			new_meta = mp.post_metadata()
			# Posting Data Points	
			for event_type in range(len(self.event_types[i])):
				et = EventTypePost(self.goc, username=self.username, api_key=self.key, metadata_key=new_meta.metadata_key, event_type=self.event_types[event_type])
				et.add_data_point(self.datapoint[i][event_type][0],self.datapoint[i][event_type][1])
				et.post_data()
