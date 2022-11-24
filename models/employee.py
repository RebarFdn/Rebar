#modeler.py
#import aiohttp
from asyncio import tasks
import requests
import orjson as json

from utils.utilities import GenerateId
from models.database import Connection

gen = GenerateId()


class Employee(
    Connection
):
    _id:str = None   
    data:dict = {}  
    meta_data:dict = {
        "created":"today",
        "database": "cp-workers"
    }
    index:set = set()
    worker:dict = {}
    workers:list = []

    def __init__(self, data:dict=None) -> None:
        try:
            if not data:
                self.generate_id()
            else:
                self.data = data
                if self.data.get("_id"):
                    pass
                else: self.generate_id()
        except Exception as e:
            print(e)

    
    def mount(self, data:dict=None) -> None:        
        if data:
            self.data = data
            if self.data.get("_id"):
                pass
            else:
                self.generate_id()


    async def all_workers(self):
        try:
            return requests.get(f"{self.url}_design/workers/_view/name-index").json() 
        except Exception as e:
            return {"error": str(e)}


    async def get_worker(self, id:str=None):
        r = requests.get(f"{self.url}{id}") 
        self.worker = r.json()  
        self.processAccountTotals 
        return self.worker


    async def save(self, data:dict=None):
        self.mount(data=data)
        requests.post(f"{self.url}", json=self.data)
        return self.data

    
    async def update(self, data:dict=None):
        worker = requests.get(f"{self.url}{data.get('_id')}").json()
        payload = worker | data
        try:
            requests.put(f"{self.url}{data.get('_id')}", json=payload)
            return payload
        except Exception as e:
            return {"error": str(e)}
        finally: del(worker); del(payload); del(data)
        

    async def delete(self, data:dict=None):
        worker = requests.get(f"{self.url}{data.get('_id')}").json()
        try:
            res = requests.delete(f"{self.url}{data.get('_id')}?rev={worker['_rev']}")
        except Exception as e:
            print(e)
        finally:
            print(worker)                   


    async def get_elist(self):
        await self.all_workers()
        return self.workers 
        

    def generate_id(self):
        ''' Generates a unique Worker id, also updates the worker data'''        
        try:
            ln = self.data.get('name').split(' ')
            self._id =  gen.name_id(ln=ln[1], fn=self.data.get('name'))            
        except:
            self._id = gen.name_id('C', 'W')
        finally:            
            self.data['_id']=self._id
            return self._id


    @property
    def db_con(self):
        return self.conn(db=self.meta_data.get('database'))

    @property
    def processAccountTotals(self):
        #function to process pay 
        def processPay(p):
            return p['amount']

        self.worker['account']['totals_payments'] = list(map(processPay, self.worker['account']['payments']))   
        self.worker['account']['total'] = sum(self.worker['account']['totals_payments'])   
        


    async def addPay(self, id=None, data=None): 
        
        #get the worker's data
        await self.get_worker(id=id)        
        self.worker['account']['payments'].append(data) 
        self.processAccountTotals        
        requests.put(f"{self.url}{id}", json=self.worker)      

        return self.worker



