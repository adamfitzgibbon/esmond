from esmonduploader import *
from time import sleep

### File that would call EsmondUploader() with specified parameters to get and post the data ###

caller = EsmondUploader(verbose=False,start=-43200,end=0,connect='http://hcc-pki-ps02.unl.edu')
	
while True:

	caller.getData()

	caller.postData()
	
	sleep(43200)
