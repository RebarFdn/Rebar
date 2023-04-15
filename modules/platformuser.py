#modeler.py
#import aiohttp
try:
    from modules.utils import timestamp
except ImportError:
    from utils import timestamp

from database import Recouch

from memory_profiler import profile

fp=open('mem_pflr.log', 'w+')


class User:    
    uernames:list=[]
    meta_data:dict = {
        "created": 0, 
        "database": {"name":"rb-user", "partitioned": False},
        "img_url": None       
    }
    
    def __init__(self, data:dict=None) -> None:
        self.conn = Recouch(local_db=self.meta_data.get('database').get('name'))
        self._id:str = None    
        self.meta_data["created"] = timestamp()
        self.index:set = set()
        self.user:dict = {}
        if data:
            self.data = data
            if self.data.get("_id"):
                pass
            else:
                self.generate_id()
          
    #@profile
    async def mount(self, data:dict=None) -> None:        
        if data:
            self.data = data
            if self.data.get("_id"):
                pass
            else:
                self.generate_id()
            await self.setup

    #@profile
    async def all(self):
        try:
            r = await self.conn.get(_directive ="_all_docs") 
            return r            
        except Exception as e:
            return {'error': str(e)}
        finally: del(r)

    
    #@profile(precision=4, stream=fp)
    async def nameIndex(self):
        def processIndex(p):
            return  p.get('value')
        r = None
        try:
            r = await self.conn.get(_directive="_design/users-index/_view/name-view") 
            return list(map( processIndex,  r.get('rows')))            
        except Exception as e:
            {'error': str(e)}
        finally: del(r)


    #@profile
    async def get(self, id:str=None):
        r = None
        try:
            r = await self.conn.get( _directive=id) 
            return r  
        except Exception as e:
            {'error': str(e)}
        finally: del(r)

    #@profile
    async def save(self):  
        await self.setup                    
        res = await self.conn.post( json=self.data)
        return res        

    #@profile
    async def update(self, data:dict=None):
        if '_rev' in list(data.keys()): del(data['_rev'])
        try: return await self.conn.put(json=data)            
        except Exception as e: return {'error': str(e)}        

    #@profile
    async def delete(self, id:str=None):        
        try: return await self.conn.delete(_id=id)
        except Exception as e: return {'error': str(e)}     

    #@profile
    async def get_elist(self):
        try: return await self.all()            
        except Exception: return {'error': str(Exception)}

    @profile
    def generate_id(self):
        ''' Generates a unique user id, also updates the User data''' 
        from modules.utils import GenerateId 
        ln = None      
        gen = GenerateId()
        try:
            ln = self.data.get('name').split(' ')
            self._id =  gen.name_id(ln=ln[1], fn=self.data.get('name'))
        except: self._id = gen.name_id('C', 'P')
        finally:
            self.data['_id']=self._id
            del(ln)
            del(gen)
            del(GenerateId)
            return self._id

    #@profile    
    async def make_password(self, raw_text:str=None):
        from werkzeug.security import generate_password_hash
        try: return  generate_password_hash(raw_text, method='pbkdf2:sha256', salt_length=8)
        except: return None
        finally: del generate_password_hash
    
    #@profile
    async def check_password(self, password_hash, raw_text):
        from werkzeug.security import check_password_hash
        try: return check_password_hash( password_hash, raw_text)
        except Exception: return False
        finally: del(check_password_hash)

    #@profile
    def update_index(self, data:str) -> None:
        '''  Expects a unique id string ex. JD33766'''        
        self.index.add(data) 


    #@property 
    def list_index(self) -> list:
        ''' Converts set index to readable list'''
        return [item for item in self.index]

    #@profile
    @property
    async def setup(self):       
        self.data['meta_data'] = self.meta_data



""" TEST
data = {
    "name":"90lb Jackhammer",   
    "serial":"",
    "model":"",
    "brand":"Dewalt",
    "power": "electric",


}      

p = User(data=data)


print()
print(p.data)

"""