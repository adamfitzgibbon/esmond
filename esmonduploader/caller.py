from esmonduploader import *
from time import sleep

### File that would call EsmondUploader() with specified parameters to get and post the data ###

caller = EsmondUploader(verbose=False,start=opts.start,end=opts.end,delay=opts.delay,connect=opts.url)

if opts.disp:
	caller.getData(opts.disp)
if opts.post:
	while True:
		
		print "Getting data..."
		caller.getData()

		print "Posting data..."
		caller.postData()
		
		print "Waiting %s seconds..." % caller.delay
		sleep(caller.delay)
