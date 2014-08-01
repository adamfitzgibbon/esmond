from esmonduploader import *
from time import sleep

### File that would call EsmondUploader() with specified parameters to get and post the data ###

caller = EsmondUploader(verbose=False,start=-43200,end=0,delay=43200,connect='http://hcc-pki-ps02.unl.edu')
	
while True:
	
	print "Getting data..."
	caller.getData()

	print "Posting data..."
	caller.postData()
	
	print "Waiting %s seconds..." % caller.delay
	sleep(caller.delay)
