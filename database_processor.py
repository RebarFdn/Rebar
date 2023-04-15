#Recouch 1.0.2 Rebar Database Adaptor Service database.py 
#Apache CouchDb Handler and Controller
#author: Tan Moncrieffe
#date Nov 23 2022
#couchdb cookie value = 299C5A4368900F0F038E528974770DC4

#Dependencies
# Native Imports
from time import time 
from asyncio import run
import httpx


class Recouch:
    local_database:str = None
    base_url:str = None
    local_url:str = None
    slave_database:str = None
    slave_url:str = None

    def __init__(self, local_db:str = None):
        '''Apache Couchdb async Client 
        ---
            
        '''
        from settings import (DB_ADMIN, ADMIN_ACCESS)   
        self.base_url = f"http://{DB_ADMIN}:{ADMIN_ACCESS}@localhost:5984/"
        self.slave_url = self.base_url               
        if local_db:
            self.local_database = local_db  
            self.local_url = f"{self.base_url}{self.local_database}/"
        else:
            pass 
    
    def resolve_url_path(self, db:str=None, _directive:str=None ):
        '''Resolves the database query url string.
        ---
        defaults to the database server connection handle if called
        without arguments. 
        db shall be the slave database used for a partuclar request
        _directive can be any of the following: 
        [an items _id "", "_all_docs", "_design/xxxx/_view/xx"]
        '''
        def reset_slave_url():
            self.slave_url = self.base_url

        url_path:str = None
        try:
            reset_slave_url()            
            # Case-1 database and directive
            if db and _directive: 
                self.slave_database = db # assign slave 
                self.slave_url = f"{self.slave_url}{self.slave_database}/" # construct url                
                url_path = f"{self.slave_url}{_directive}"                
            # Case-2 direvtive without database but a local database exist         
            elif self.local_database and _directive and not db:
                url_path = f"{self.local_url}{_directive}"
            # Case-3 database without directive
            elif db and not _directive:
                self.slave_database = db # assign slave 
                self.slave_url = f"{self.slave_url}{self.slave_database}/" # construct url
                url_path = f"{self.slave_url}"
            # Case-4 no database no directive
            else: url_path = self.base_url # return the database connector 

            return url_path
        except:            
            return self.base_url
        finally: del url_path


    async def get(self, db:str=None, _directive:str=None, client:any=None):
        '''Retreives a single item or a list of items based on the given directive
        ---
            applied directives: 
                _id:  retreive the item by its id 
                _all_docs: retreives an index list of items 
                _design/xx/_view/aview: retreive a list of documents by design
        '''
        r = None
        res:dict = None
        url_path = self.resolve_url_path(db=db, _directive=_directive)
      
        try:            
            r = await client.get(url_path)
            return r.json()
        except Exception as ex:
            return {"status": str(ex)}
        finally: await r.aclose(); del(res); del(url_path); del(r) #close connection and clean up


    async def post(self, db:str=None, json:dict=None, client:any=None):  
        '''Create a new resource in storage.
        ---
        requires a data ditionary object with key _id
        ''' 
        r = None     
        url_path =self.resolve_url_path(db=db) 
           
        try:
            r = await client.post(url_path, json=json)
            return r.json()
        except Exception as ex:
            return {"status": str(ex)}
        finally: await r.aclose(); del(url_path); del(r)#close connection and clean up

    
    async def put(self, db:str=None, json:dict=None, client:any=None): 
        '''Updates a resource with data provided 
        ---
        requires a data ditionary object with key _id
        '''     
        r = None  
        url_path = self.resolve_url_path(db=db, _directive=json.get('_id'))         
        old_data = await self.get(db=db, _directive=json.get("_id"))         
        old_data.update(old_data | json)       
        try:
            r = await client.put(url_path, json=old_data)
            return r.json()
        except Exception as ex:
            return {"status": str(ex)}
        #close connection and clean up
        finally: await r.aclose(); del(old_data);del(url_path); del(r)        


    async def delete(self, db:str=None, _id:str=None, client:any=None): 
        '''Permanently removes a resource from storage.
        ---
            requires the resource _id 
        '''
        r = None         
        data = await self.get(db=db, _directive=_id)
        directive=f"{_id}?rev={data.get('_rev')}"
        url_path = self.resolve_url_path(db=db, _directive=directive)  
           
        try:
            r = await client.delete(url=url_path)
          
            return r.json()
        except Exception as ex:
            return {"status": str(ex)}
        finally: await r.aclose(); del(url_path); del(data); del(r) #close connection and clean up

recouch = Recouch(local_db=None)


async def process_request(args, **kwargs ):
    async with httpx.AsyncClient() as client:
        if args == 'get' or args == 'GET':
            data = await recouch.get(db=kwargs.get("db"), _directive=kwargs.get("_directive"), client=client)
        if args == 'post' or args == 'POST':
            data = await recouch.post(db=kwargs.get("db"), json=kwargs.get("json"), client=client),
        if args == 'put' or args == '   PUT':
            data = await recouch.put(db=kwargs.get("db"), json=kwargs.get("json"), client=client),
        if args == 'delete' or args == 'DELETE':
            data = await recouch.delete(db=kwargs.get("db"), _id=kwargs.get("_id"), client=client)
        return data
            
            




