#modeler.py
#import aiohttp

import bcrypt
import requests
import orjson as json
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.routing import Route
from config import config


from utils.utilities import GenerateId, timestamp
from models.database import Connection


class User(
    Connection,
    
):
    
    uernames:list=[]
    
    def __init__(self, data:dict=None) -> None:
        self._id:str = None    
        self.meta_data:dict = {"created":timestamp(), "database": "cp-users", "img_url": ""}
        self.index:set = set()
        self.user:dict = {}
        if data:
            self.data = data
            if self.data.get("_id"):
                pass
            else:
                self.generate_id()
          

    async def mount(self, data:dict=None) -> None:        
        if data:
            self.data = data
            if self.data.get("_id"):
                pass
            else:
                self.generate_id()
            await self.setup


    async def all(self):
        try:
            r = requests.get(f"{self.db_con}_all_docs") 
            return r.json()            
        except Exception as e:
            return {'error': str(e)}
        finally: del(r)

    async def nameIndex(self):
        def processIndex(p):
            return  p.get('value')
        try:
            r = requests.get(f"{self.db_con}_design/users-index/_view/name-view") 
            return list(map( processIndex,  r.json().get('rows')))            
        except Exception as e:
            {'error': str(e)}
        finally: del(r)


    async def get(self, id:str=None):
        try:
            r = requests.get(f"{self.db_con}{id}") 
            return r.json()  
        except Exception as e:
            {'error': str(e)}
        finally: del(r)


    async def save(self):  
        await self.setup                    
        res = requests.post(f"{self.db_con}", json=self.data)
        return res.json()
        

    async def update(self, data:dict=None):
        if '_rev' in list(data.keys()):
            del(data['_rev'])
            

        user = requests.get(f"{self.db_con}{data.get('_id')}").json()
        payload = user | data
        try:
            requests.put(f"{self.db_con}{data.get('_id')}", json=payload)
            return payload
        except Exception as e:
            return {'error': str(e)}
        finally:
            del(data) ; del(user); del(payload)


    async def delete(self, id:str=None):
        user = await self.get(id=id)
        try:
            requests.delete(f"{self.db_con}{id}?rev={user['_rev']}")
            return {"status": f"User with id {id} DELETED"}
        except Exception as e:
            return {'error': str(e)}
        finally:
            del(user)


    async def get_elist(self):
        try:
            s = await self.all()
            return s
        except Exception as e:
            return {'error': str(e)}
        finally: del(s)


    def generate_id(self):
        ''' Generates a unique user id, also updates the User data''' 
        gen = GenerateId()
        try:
            ln = self.data.get('name').split(' ')
            self._id =  gen.name_id(ln=ln[1], fn=self.data.get('name'))
            
        except:
            self._id = gen.name_id('C', 'P')
        finally:
            self.data['_id']=self._id
            return self._id

    
    async def make_password(self, raw_text:str=None):
        try:
            return bcrypt.hashpw(raw_text.encode('utf-8'), bcrypt.gensalt())
        except Exception as e:
            return None
    
    async def check_password(self, password_hash, raw_text):
        try:
            return bcrypt.checkpw(raw_text.encode('utf-8'), password_hash.encode('utf-8'))
        except Exception:
            return False

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


    #

    @property
    async def setup(self):     
       
        self.data['meta_data'] = self.meta_data

# Create     
async def createUser(request):
    try:
        data = await request.json() 
        e = User(data=data) 
        if e.data.get("password"):
            pass_word = await e.make_password(raw_text=e.data['password'])
            if pass_word:                
                e.data['password_hash'] = pass_word.decode('utf-8')
                del(e.data['password'])
                res = await e.save()    
                return JSONResponse({"status": res})
            else:  return JSONResponse({"status":'Password Generation Failed! '})
        else: 
            return JSONResponse({"status":'You did not provide a password'}) 
        
    except Exception as er:
        return JSONResponse({'error': str(er)})
   

# Retreive
async def getUser(request):
    try:    
        e = User()
        user = await e.get(id=request.path_params.get('id'))
        return JSONResponse(user)
    except Exception as er:
        return JSONResponse({'error': str(er)})
    finally: del(e); del(user)

async def getUsersIndex(request):
    try:      
        e = User()
        data = await e.nameIndex()
        return JSONResponse(data)
    except Exception as er:
        return JSONResponse({'error': str(er)})
    finally: del(e); del(data)

# Update
async def updateUser(request):
    data = await request.json()
    e = User()
    try:
        res = await e.update(data=data)
        return JSONResponse(res)
    except Exception as er:
        return JSONResponse({'error': str(er)})
    finally: del(res); del(e); del(data)

# Delete
async def deleteUser(request):
    id = request.path_params.get('id')
    e = User()
    try:
        res = await e.delete(id=id)
        return JSONResponse(res)
    except Exception as er:
        return JSONResponse({'error': str(er)})
    finally: del(res); del(e); del(id)
    
async def AuthenticateUser(request):    
    request_data = await  request.json()
    e = User()
    user = await e.get(id=request_data.get('_id'))
    if await e.check_password(user.get('password_hash'), request_data.get('password') ):
        del(user['password_hash'])
        return JSONResponse(user)
    else:
        return JSONResponse({"status": "Invalid Credentials"})
    


    



            

    



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