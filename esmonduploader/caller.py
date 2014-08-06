from esmonduploader import *
from time import sleep

### File that would call EsmondUploader() with specified parameters to get and post the data ###
caller = EsmondUploader(verbose=False,start=int(opts.start),end=int(opts.end),delay=int(opts.delay),connect=opts.url)

# Option: Display Metadata
if opts.disp:
	caller.getData(opts.disp)

# Option: Get and Post Metadata
if opts.post:
	while True:
		
		print "Getting data..."
		caller.getData()

		print "Posting data..."
		caller.postData()
		
		print "Waiting %s seconds..." % caller.delay
		sleep(float(caller.delay))
