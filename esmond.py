from esmond.api.client.perfsonar.query import ApiConnect, ApiFilters
from optparse import OptionParser
import time


filters = ApiFilters()

filters.verbose = True
filters.time_start = time.time() - 3600
filters.time_end = time.time()
filters.source = '198.129.254.30'
filters.tool_name = 'bwcrtl/iperf3'

conn = ApiConnect('http://hcc-pki-ps02.unl.edu:8000/',filters)


