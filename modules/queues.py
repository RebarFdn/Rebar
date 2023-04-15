
from modules.utils import timestamp
##from modules.zen import zen_now
#from database import Recouch
import threading
#from queue import Queue

'''
class TaskQueue:
    _id:str = None   
    queue = Queue()  
    meta_data:dict = {
        "added": timestamp(),
        "database": {
            "name":"queues-pt", "partitioned": True           
            },
        "queue": "tasks"
    }
    
    def __init__(self, data:dict=None) -> None:
        if data:
            self._id = f"{self.meta_data.get('queue')}:{self._id}"
            self.queue.put(data)

    def add_task(self, data:dict=None) -> None:
        if data:
            self.queue.put(data)
            
'''