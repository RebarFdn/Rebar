#rate.py
try:
    from modules.utils import timestamp
    from database import Recouch
except:
    from utils import timestamp
    from database import Recouch

#from modules.platformuser import fp, profile

class Rate:
    _id:str = None    
    meta_data:dict = {"created":timestamp(), "database": {"name": "rate-sheet", "partioned": False}}
    index:set = set()
    rate:dict = {}
    rates:list = []


    #@profile(precision=1, stream=fp)    
    def __init__(self, data:dict=None) -> None:
        self.conn = Recouch(local_db=self.meta_data.get('database').get('name'))        
        if data:
            self.data = data
            if self.data.get("_id"): self._id = self.data.get("_id")
            else: self.generate_id()
            self.meta_data.update(self.meta_data | {"_id": self._id})
            self.data['metadata'] = self.meta_data

    #@profile(precision=1, stream=fp)
    def mount(self, data:dict=None) -> None:        
        if data:
            self.data = data
            if self.data.get("_id"): self._id = self.data.get("_id")
            else: self.generate_id()
            self.meta_data.update(self.meta_data | {"_id": self._id})
            self.data['metadata'] = self.meta_data

    #@profile(precision=2, stream=fp)
    async def all(self):
        try:            
            return await self.conn.get(_directive="_all_docs")            
        except Exception as e:
            return str(e)
        

    #@profile(precision=2, stream=fp)
    async def all_rates(self): 
        '''Retreives a list of rate data.
        ''' 
        r = None      
        def processrates(rate):
            return rate['value']            
        try:
            r = await self.conn.get(_directive="_design/index/_view/document")
            return list(map(processrates,  r.get('rows') ))
        except Exception as e: return str(e)
        finally: del(r)
             
    #@profile(precision=2, stream=fp)
    async def get(self, id:str=None):
        '''Retreives an indivual rate item by its Id.
        '''
        return await self.conn.get(_directive=id) 
    
    #@profile(precision=2, stream=fp)
    async def save(self):      
        '''Stores a Rate Item Permanently on the Platform.
        '''  
        return await self.conn.post(json=self.data) 
        
    #@profile(precision=2, stream=fp)
    async def update(self, data:dict=None):
        '''Updates a Rate Item with data provided.
        --- Footnote:
                enshure data has property _id
            extra:
                updates the objects meta_data property 
                or create and stamp the meta_data field
                if missing                 
        '''
        if '_rev' in list(data.keys()): del(data['_rev'])      
        try: return await self.conn.put(json=data)            
        except Exception as e: return {'error': str(e)}
        

    #@profile(precision=2, stream=fp)
    async def delete(self, id:str=None):
        '''Permanently Remove a Rate Item from the Platform.
        ---Requires:
            name: _id
            value: string 
            inrequest_args: True
        '''        
        try: return await self.conn.delete(_id=id)
        except Exception: return {"status": str(Exception)}
        

    #@profile(precision=2, stream=fp)
    async def get_elist(self):
        self.rates = await self.all()
        return self.rates

    #@profile(precision=2, stream=fp)
    def generate_id(self):
        ''' Generates a unique rate id, also updates the rate data'''        
        from modules.utils import GenerateId       
        gen = GenerateId() 
        try: self._id =  gen.name_id(ln=self.data.get('title').split(' ')[1], fn=self.data.get('title'))            
        except: self._id = gen.name_id('P', 'T')
        finally:
            self.data['_id']=self._id
            del(gen)
            del(GenerateId) # clean up
            return self._id

    #@profile(precision=2, stream=fp)
    def update_index(self, rate_id:str) -> None:
        '''Expects a unique id string ex. JD33766'''        
        self.index.add(rate_id) 

    #@profile(precision=2, stream=fp)
    @property 
    def list_index(self) -> list:
        ''' Converts set index to readable list'''
        return [item for item in self.index]



