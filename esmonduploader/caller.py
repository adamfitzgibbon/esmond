from time import sleep
import sys
from esmonduploader import *

### File that would call EsmondUploader() with specified parameters to get and post the data ###
caller = EsmondUploader(verbose=False,start=int(opts.start),
        end=int(opts.end),delay=int(opts.delay),connect=opts.url)
# Option: Display Metadata
if opts.disp:
    try:
        caller.getData(opts.disp)
    except Exception as err:
        print "An error occurred! Exception:  \"%s\" of type: \"%s\" was thrown!" % (err, type(err))

# Option: Get and Post Metadata
if opts.post:
    while True:
        
        print "Getting data..."
        try:
            caller.getData()
        except Exception as err:
            print "Error! Get unsuccessful! Exception: \"%s\" of type: \"%s\" was thrown! Quitting out." % (err,type(err))
            break
        else:
            print "Get successful!"
        print "Posting data..."
        try:
            caller.postData()
        except Exception as err:
            print "Error! Post unsuccessful! Exception: \"%s\" of type: \"%s\" was thrown! Quitting out." % (err,type(err))
            break
        else:
            print "Post successful!"
        print "Waiting %s seconds..." % caller.delay
        sleep(float(caller.delay))
