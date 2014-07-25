from esmonduploader import *

caller = FilterArgs(verbose=True,start=-3600,end=0,source='198.129.254.30',tool_name='bwcrtl/iperf3',connect='http://hcc-pki-ps02.unl.edu:8000/')

conn = caller.apiConn()

caller.getData(conn)
