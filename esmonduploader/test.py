from esmond.api.client.perfsonar.query import ApiConnect, ApiFilters
import time


filters = ApiFilters()
filters.verbose = True
filters.time_start = time.time() - 3600
filters.time_end = time.time()
filters.source = '198.129.254.30'
filters.tool_name = 'bwctl/iperf3'
conn = ApiConnect('http://hcc-pki-ps02.unl.edu:8000/', filters)
for md in conn.get_metadata():
	print md
