from esmonduploader import *

caller = EsmondUploader(verbose=False,start=-3600,end=0,connect='http://hcc-pki-ps02.unl.edu')

caller.getData()

caller.postData()
