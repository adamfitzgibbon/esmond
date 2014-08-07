import time
from optparse import OptionParser

from esmond.api.client.perfsonar.query import ApiConnect, ApiFilters
from esmond.api.client.perfsonar.post import MetadataPost, EventTypePost, EventTypeBulkPost

# Set filter object
filters = ApiFilters()
gfilters = ApiFilters()

# Set command line options
parser = OptionParser()
parser.add_option('-d', '--disp', help='display metadata from specified url', dest='disp', default=False, action='store_true')
parser.add_option('-e', '--end', help='set end time for gathering data (default is now)', dest='end', default=0)
parser.add_option('-p', '--post',  help='begin get/post loop from specified url', dest='post', default=False, action='store_true')
parser.add_option('-s', '--start', help='set start time for gathering data (default is -12 hours)', dest='start', default=-43200)
parser.add_option('-u', '--url', help='set url to gather data from (default is http://hcc-pki-ps02.unl.edu)', dest='url', default='http://hcc-pki-ps02.unl.edu')
parser.add_option('-y', '--delay', help='set delay for gathering data (default is 12 hours)', dest='delay', default=43200)
(opts, args) = parser.parse_args()


class EsmondUploader(object):
    
    def __init__(self,verbose,start,end,delay,connect,username='afitz',key='fc077a6a133b22618172bbb50a1d3104a23b2050'):

        # Filter variables
        filters.verbose = verbose
        filters.time_start = time.time() + start
        filters.time_end = time.time() + end
        gfilters.verbose = False        
        gfilters.time_start = time.time() - 86400
        gfilters.time_end = time.time()

        # Username/Key/Location/Delay
        self.connect = connect
        self.username = username
        self.key = key
        self.goc = 'http://osgnetds.grid.iu.edu'
        self.conn = ApiConnect(self.connect,filters)
        self.gconn = ApiConnect(self.goc,gfilters)
        self.delay = delay
                
        # Metadata variables
        self.destination = []
        self.input_destination = []
        self.input_source = []
        self.measurement_agent = []
        self.source = []
        self.subject_type = []
        self.time_duration = []
        self.tool_name = []
        self.event_types = []
        self.summaries = []
        self.datapoint = []
        self.metadata_key = []
        self.old_list = []
        self.old_timestamp = []
   
    # Get Existing GOC Data
    def getGoc(self):
        for gmd in self.gconn.get_metadata():
            self.old_list.append(gmd.metadata_key)
            for get in gmd.get_all_event_types():
                gdpay = get.get_data()
                for gdp in gdpay.data:
                    self.old_timestamp.append(gdp.ts_epoch)           
                    print self.old_timestamp
    # Get Data
    def getData(self,disp=False):
        self.getGoc()
        old_time_max = max(self.old_timestamp)
        i = 0
        for md in self.conn.get_metadata():
            # Check for repeat data
            if md.metadata_key in self.old_list:
                continue
            else:
                # Assigning each metadata object property to class variables
                self.destination.append(md.destination)
                self.input_destination.append(md.input_destination)
                self.input_source.append(md.input_source)
                self.measurement_agent.append(md.measurement_agent)
                self.source.append(md.source)
                self.subject_type.append(md.subject_type)
                self.time_duration.append(md.time_duration)
                self.tool_name.append(md.tool_name)
                self.event_types.append(md.event_types)
                self.metadata_key.append(md.metadata_key)
                # Display all metadata when -d or --disp option is used
                if disp:
                    print "NEW METADATA/DATA #" + str(i+1) + "\n\n"
                    print "Destination: " + self.destination[i]
                    print "Input Destination: " + self.input_destination[i]
                    print "Input Source: " + self.input_source[i]
                    print "Measurement Agent: " + self.measurement_agent[i]
                    print "Source: " + self.source[i]
                    print "Subject_type: " + self.subject_type[i]
                    print "Time Duration: " + self.time_duration[i]
                    print "Tool Name: " + self.tool_name[i]
                    print "Event Types: " + str(self.event_types[i])
                    print "Metadata Key: " + self.metadata_key[i]
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
                # Print out summaries and datapoints if -d or --disp option is used
                if disp:
                    print "Summaries: " + str(self.summaries[i])
                    print "Datapoints: " + str(self.datapoint[i]) + "\n\n"
            i += 1
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
            }
        
            mp = MetadataPost(self.goc,username=self.username, api_key=self.key, **args)
            # Posting Event Types and Summaries
            for event_type, summary in zip(self.event_types[i], self.summaries[i]):
                mp.add_event_type(event_type)
                if summary:
                    mp.add_summary_type(event_type, summary[0][0], summary[0][1])
            new_meta = mp.post_metadata()
            # Posting Data Points
            for event_num in range(len(self.event_types[i])):
                ### Histograms were being rejected (wants dict, not list of dicts) disregarding them for now ###
                if isinstance(self.datapoint[i][event_num][1], list):
                    if isinstance(self.datapoint[i][event_num][1][0], dict):
                        continue
                if isinstance(self.datapoint[i][event_num][1], dict):
                    continue
                et = EventTypePost(self.goc, username=self.username, api_key=self.key, metadata_key=new_meta.metadata_key, event_type=self.event_types[i][event_num])
                et.add_data_point(self.datapoint[i][event_num][0],self.datapoint[i][event_num][1])
                et.post_data()
       
        # Wipe lists (emptied for looping get/post)
        del self.destination[:]
        del self.input_destination[:]
        del self.source[:]
        del self.measurement_agent[:]
        del self.input_source[:]
        del self.time_duration[:]
        del self.tool_name[:]
        del self.subject_type[:]
        del self.event_types[:]
        del self.summaries[:]
        del self.datapoint[:]
        del self.metadata_key[:]
