import requests

from starlette.responses import PlainTextResponse, FileResponse,JSONResponse

from utils.utilities import GenerateId, timestamp
from boq.modules.database import Connection


class Boq(
    Connection,
    
    ):    
        
    def __init__(self, data:dict=None) -> None:
        self._id:str = None    
        self.meta_data:dict = {"created":timestamp(), "database": "boqs"}
        self.index:set = set()       
        if data:
            self.data = data
            if self.data.get("_id"):
                pass
            else:
                self.data["_id"] = timestamp()
          

    async def mount(self, data:dict=None) -> None:        
        if data:
            self.data = data
            if self.data.get("_id"):
                pass
            else:
                self.data["_id"] = timestamp()
            await self.setup


    async def all(self):
        try:
            r = requests.get(f"{self.db_con}_all_docs") 
            return r.json()            
        except Exception as e:
            return {'error': str(e)}
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
        r = requests.get(f"{self.db_con}{data.get('_id')}").json()
        payload = r | data
        try:
            requests.put(f"{self.db_con}{data.get('_id')}", json=payload)
            return payload
        except Exception as e:
            return {'error': str(e)}
        finally:
            del(data) ; del(r); del(payload)


    async def delete(self, id:str=None):
        r = await self.get(id=id)
        try:
            requests.delete(f"{self.db_con}{id}?rev={r['_rev']}")
            return {"status": f"Estimate with id {id} DELETED"}
        except Exception as e:
            return {'error': str(e)}
        finally:
            del(r)


    async def get_elist(self):
        try:
            s = await self.all()
            return s
        except Exception as e:
            return {'error': str(e)}
        finally: del(s)

    async def nameIndex(self):
        try:
            r = requests.get(f"{self.db_con}_design/bills/_view/name-index") 
            return r.json()            
        except Exception as e:
            return {'error': str(e)}
        finally: del(r)

    
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


    @property
    async def setup(self):    
        if 'meta_data' in self.data.keys():
            self.data['meta_data'] = self.data['meta_data'] | self.meta_data
        else:
            self.data['meta_data'] = self.meta_data
            

# Create     
async def createBoq(request):
    data = await request.json() 
    e = Boq(data=data) 
    try:        
        return JSONResponse({"status": await e.save() })      
    except Exception as er:
        return JSONResponse({'error': str(er)})
    finally: del(data); del(e)

   

# Retreive
async def getBoq(request):
    e = Boq()
    try:
        return JSONResponse( await e.get(id=request.path_params.get('id')) )
    except Exception as er:
        return JSONResponse({'error': str(er)})
    finally: del(e)

async def getBoqIndex(request):
    e = Boq()
    try:       
        return JSONResponse(await e.nameIndex())
    except Exception as er:
        return JSONResponse({'error': str(er)})
    finally: del(e);

# Update
async def updateBoq(request):
    e = Boq()
    try:
        return JSONResponse( await e.update(data=await request.json()) )
    except Exception as er:
        return JSONResponse({'error': str(er)})
    finally: del(e)

async def deleteBoq(request):   
    e = Boq()
    try:
        return JSONResponse( await e.delete(id=request.path_params.get('id')) )
    except Exception as er:
        return JSONResponse({'error': str(er)})
    finally: del(e)

 