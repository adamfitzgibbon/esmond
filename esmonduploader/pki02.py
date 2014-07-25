from esmonduploader import *

caller = FilterArgs(verbose=False,start=-3600,end=0,source='198.129.254.30',tool_name='bwctl/iperf3',connect='http://hcc-pki-ps02.unl.edu:8000/')

conn = caller.apiConn()

caller.getData(conn)

