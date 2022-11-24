#tasks.py

import requests
import orjson as json
from starlette.responses import PlainTextResponse, JSONResponse
'''try:
    from utils.utilities import GenerateId, timestamp
except ImportError:
    from sledge.utils.utilities import GenerateId, timestamp
'''
import datetime
from strgen import StringGenerator


# Timestamp 
def timestamp():
        return  int((datetime.datetime.now().timestamp() * 1000))


#----------------------------- ID Generation Service ----------------------------------

class GenerateId:
    tags = dict(
            doc='[h-z5-9]{8:16}',
            app='[a-z0-9]{16:32}',
            key='[a-z0-9]{32:32}',
            job='[a-j0-7]{8:8}',
            user='[0-9]{4:6}',
            item='[a-n1-9]{8:8}',
            code='[a-x2-8]{24:32}'
        )
        
    async def genid(self, doc_tag:str=None):
        """ 
            Doc Tags: String( doc, app, key, job, user, item, code,task,name)
            UseCase: 
                        >>> import genny
                        >>> from genny import genid
                        >>> from genny import genid as gi
                        
                        >>> id = genny.genid('user')
                        >>> id = genid('user')
                        >>> id = gi('user')
                Yeilds ... U474390
                        ... U77301642
                        ... U1593055
        
        """
        
        if doc_tag == 'user':
            #u_id = StringGenerator(str(self.tags[doc_tag])).render(unique=True)
            return f"U{StringGenerator(str(self.tags[doc_tag])).render(unique=True)}"
        return StringGenerator(str(self.tags[doc_tag])).render(unique=True)
            

    async def nameid(self, fn:str='Jane',ln:str='Dear',sec:int=5):
        """ 
            Name Identification by initials fn='Jane', ln='Dear' and given number sequence sec=5.
            
            UseCase: 
                        >>> import genny
                        >>> from genny import nameid
                        >>> from genny import nameid as nid
                        
                        >>> id = genny.nameid('Peter','Built',6)
                        >>> id = nameid('Peter','Built',5)
                        >>> id = nid('Peter','Built',4)
                        >>> id = nid() # default false id 
                        
                Yeilds ... PB474390
                        ... PB77301
                        ... PB1593
                        ... JD1951
        
        """
        code = '[0-9]{4:%s}'% int(sec)
        return f"{fn[0].capitalize()}{ln[0].capitalize()}{StringGenerator(str(code)).render(unique=True)}"
               

    async def short_nameid(self, fn:str='Jane',ln:str='Dear',sec:int=2):
        """ 
            Name Identification by initials fn='Jane', ln='Dear' and given number sequence sec=5.
            
            UseCase: 
                        >>> import genny
                        >>> from genny import short_nameid
                        >>> from genny import short_nameid as id
                        
                        >>> id = genny.short_nameid('Peter','Built',2)
                        >>> id = short_nameid('Peter','Built')
                        >>> id = id(p','b',3)
                        >>> id = id() # default false id 
                        
                Yeilds ... PB47
                        ... PB54
                        ... PB69
                        ... JD19
        
        """
        code = '[0-9]{2:%s}'% int(sec)
        return f"{fn[0].capitalize()}{ln[0].capitalize()}{StringGenerator(str(code)).render(unique=True)}"
        

    async def eventid(self, event,event_code,sec=8):
        """EventId 
            Event Identification by initials fn='Jane', ln='Dear' and given number sequence sec=5.
            
            UseCase: 
                        >>> import genny
                        >>> from genny import eventid
                        >>> from genny import eventid as id
                        
                        >>> id = genny.eventid('Product','LAUNCH',6)
                        >>> id = eventid('Product','LAUNCH',5)
                        >>> id = id('Product', 'LAUNCH',4)                       
                Yeilds ... PROLAUNCH-884730
                        ... PROLAUNCH-18973
                        ... PROLAUNCH-4631                       
        
        """
        code = '[0-9]{4:%s}'% int(sec)
        return f"{event[:3].upper()}{event_code}-{StringGenerator(str(code)).render(unique=True)}"
        

    async def short_eventid(self, event,event_code,sec=2):
        """ShortEventId 
            Event Identification by initials fn='Jane', ln='Dear' and given number sequence sec=2.
            
            UseCase: 
                        >>> import genny
                        >>> from genny import shorteventid
                        >>> from genny import shorteventid as id
                        
                        >>> id = genny.shorteventid('Product','LAUNCH',2)
                        >>> id = shorteventid('Product','LAUNCH')
                        >>> id = id('Product', 'LAUNCH',3)
                Yeilds ... PROLAUNCH-88
                        ... PROLAUNCH-90
                        ... PROLAUNCH-461                       
        
        """
        code = '[0-9]{2:%s}'% int(sec)
        return f"{event[:3].upper()}{event_code}-{StringGenerator(str(code)).render(unique=True)}"
        
        
    def gen_id(self, doc_tag:str=None):
        """ 
            Doc Tags: String( doc, app, key, job, user, item, code,task,name)
            UseCase: 
                        >>> import genny
                        >>> from genny import genid
                        >>> from genny import genid as gi
                        
                        >>> id = genny.genid('user')
                        >>> id = genid('user')
                        >>> id = gi('user')
                Yeilds ... U474390
                        ... U77301642
                        ... U1593055
        
        """
        
        if doc_tag == 'user':
            #u_id = StringGenerator(str(self.tags[doc_tag])).render(unique=True)
            return f"U{StringGenerator(str(self.tags[doc_tag])).render(unique=True)}"
        return StringGenerator(str(self.tags[doc_tag])).render(unique=True)
            

    def name_id(self, fn:str='Jane',ln:str='Dear',sec:int=5):
        """ 
            Name Identification by initials fn='Jane', ln='Dear' and given number sequence sec=5.
            
            UseCase: 
                        >>> import genny
                        >>> from genny import nameid
                        >>> from genny import nameid as nid
                        
                        >>> id = genny.nameid('Peter','Built',6)
                        >>> id = nameid('Peter','Built',5)
                        >>> id = nid('Peter','Built',4)
                        >>> id = nid() # default false id 
                        
                Yeilds ... PB474390
                        ... PB77301
                        ... PB1593
                        ... JD1951
        
        """
        code = '[0-9]{4:%s}'% int(sec)
        return f"{fn[0].capitalize()}{ln[0].capitalize()}{StringGenerator(str(code)).render(unique=True)}"
               

    def short_name_id(self, fn:str='Jane',ln:str='Dear',sec:int=2):
        """ 
            Name Identification by initials fn='Jane', ln='Dear' and given number sequence sec=5.
            
            UseCase: 
                        >>> import genny
                        >>> from genny import short_nameid
                        >>> from genny import short_nameid as id
                        
                        >>> id = genny.short_nameid('Peter','Built',2)
                        >>> id = short_nameid('Peter','Built')
                        >>> id = id(p','b',3)
                        >>> id = id() # default false id 
                        
                Yeilds ... PB47
                        ... PB54
                        ... PB69
                        ... JD19
        
        """
        code = '[0-9]{2:%s}'% int(sec)
        return f"{fn[0].capitalize()}{ln[0].capitalize()}{StringGenerator(str(code)).render(unique=True)}"
        

    def event_id(self, event,event_code,sec=8):
        """EventId 
            Event Identification by initials fn='Jane', ln='Dear' and given number sequence sec=5.
            
            UseCase: 
                        >>> import genny
                        >>> from genny import eventid
                        >>> from genny import eventid as id
                        
                        >>> id = genny.eventid('Product','LAUNCH',6)
                        >>> id = eventid('Product','LAUNCH',5)
                        >>> id = id('Product', 'LAUNCH',4)                       
                Yeilds ... PROLAUNCH-884730
                        ... PROLAUNCH-18973
                        ... PROLAUNCH-4631                       
        
        """
        code = '[0-9]{4:%s}'% int(sec)
        return f"{event[:3].upper()}{event_code}-{StringGenerator(str(code)).render(unique=True)}"
        

    def short_event_id(self, event,event_code,sec=2):
        """ShortEventId 
            Event Identification by initials fn='Jane', ln='Dear' and given number sequence sec=2.
            
            UseCase: 
                        >>> import genny
                        >>> from genny import shorteventid
                        >>> from genny import shorteventid as id
                        
                        >>> id = genny.shorteventid('Product','LAUNCH',2)
                        >>> id = shorteventid('Product','LAUNCH')
                        >>> id = id('Product', 'LAUNCH',3)
                Yeilds ... PROLAUNCH-88
                        ... PROLAUNCH-90
                        ... PROLAUNCH-461                       
        
        """
        code = '[0-9]{2:%s}'% int(sec)
        return f"{event[:3].upper()}{event_code}-{StringGenerator(str(code)).render(unique=True)}"
        
        
try:
    from models.database import Connection
except ImportError:
    from .database import Connection

class Task(
    Connection,
    
):
    _id:str = None    
    meta_data:dict = {"created":"today", "database": "cp-tasks"}
    index:set = set()
    task:dict = {}
    tasks:list = []
    
    def __init__(self, data:dict=None) -> None:
        if data:
            self.data = data
            if self.data.get("_id"):
                pass
            else:
                self.generate_id()


    def mount(self, data:dict=None) -> None:        
        if data:
            self.data = data
            if self.data.get("_id"):
                pass
            else:
                self.generate_id()


    async def all(self):
        r = requests.get(f"{self.db_con}_all_docs") 
        return r.json() 

    async def all_tasks(self):        
        def processTasks(task):
            return task['value']
            
        try:
            r = requests.get(f"{self.db_con}_design/index/_view/document").json()
            return list(map(processTasks,  r.get('rows') ))
        except Exception as e:
            return str(e)
        finally: del(r)
             



    async def get(self, id:str=None):
        r = requests.get(f"{self.db_con}{id}") 
        return r.json()  


    async def save(self):        
        response = requests.post(f"{self.db_con}", json=self.data).json()
        print(response)
        return self.data

    async def update(self, data:dict=None):
        task = requests.get(f"{self.db_con}{data.get('_id')}").json()
        payload = task | data
        try:
            return requests.put(f"{self.db_con}{data.get('_id')}", json=payload)
        except Exception as e:
            print(e)
        finally:
            del(data) ; del(task); del(payload)


    async def delete(self, data:dict=None):
        task = requests.get(f"{self.db_con}{data.get('_id')}").json()
        try:
            return requests.delete(f"{self.db_con}{data.get('_id')}?rev={task['_rev']}")
        except Exception as e:
            print(e)
        finally:
            del(task); del(data)

    async def get_elist(self):
        await self.all()
        return self.tasks

    def generate_id(self):
        ''' Generates a unique task id, also updates the task data''' 
        gen = GenerateId()
        try:
            ln = self.data.get('title').split(' ')
            self._id =  gen.name_id(ln=ln[1], fn=self.data.get('title'))
            
        except:
            self._id = gen.name_id('P', 'T')
        finally:
            self.data['_id']=self._id
            return self._id

    @property
    def db_con(self):
        return self.conn(db=self.meta_data.get('database'))


    def update_index(self, data:str) -> None:
        '''  Expects a unique id string ex. JD33766'''        
        self.index.add(data) 


    @property 
    def list_index(self) -> list:
        ''' Converts set index to readable list'''
        return [item for item in self.index]



async def getTasks( request ):
    try:
        t = Task()
        tasks = await t.all_tasks()
        return JSONResponse(tasks)
    except Exception as e:
        return JSONResponse({"error": str(e)})
    finally: del(t); del(tasks)


async def saveTask( request ):
    try:
        payload = await request.json()
        t = Task(data=payload)        
        response = await t.save()       
        return JSONResponse(response )
    except Exception as e:
        return JSONResponse({"error": str(e)})
    finally: del(t); 





