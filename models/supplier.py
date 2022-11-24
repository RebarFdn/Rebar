#modeler.py
#import aiohttp
from asyncio import tasks
import requests
import orjson as json

from starlette.responses import PlainTextResponse, JSONResponse

from utils.utilities import GenerateId, timestamp
from models.database import Connection


class Supplier(
    Connection,
    
):
    
    suppliers:list=[]
    
    def __init__(self, data:dict=None) -> None:
        self._id:str = None 
        self.data:dict = None   
        self.meta_data:dict = {"created":timestamp(), "database": "cp-suppliers", "databaseII": "cp-projects"}
        self.index:set = set()        
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
        try:
            r = requests.get(f"{self.db_con}_all_docs").json()                       
        except Exception as e:
            r = {'error': str(e)}
        finally: return r


    async def nameIndex(self):
        def processIndex(p):
            return  p.get('key')
        try:
            r = requests.get(f"{self.db_con}_design/suppliers/_view/name-index").json() 
            r = list(map( processIndex,  r.get('rows')))            
        except Exception as e:
            r = {'error': str(e)}
        finally: return r


    async def invoiceIdIndex(self):
        def processIndex(p):
            return  p.get('key')
        try:
            r = requests.get(f"{self.db_con2}_design/project-index/_view/invoice-id").json() 
            r = list(map( processIndex,  r.get('rows')))            
        except Exception as e:
            r = {'error': str(e)}
        finally: 
            return r


    async def get(self, id:str=None):
        try:
            r = requests.get(f"{self.db_con}{id}") 
            r = r.json()  
        except Exception as e:
            r = {'error': str(e)}
        finally: return r


    async def save(self):
        self.data['meta_data'] = self.meta_data
        try:
            res = requests.post(f"{self.db_con}", json=self.data).json()            
        except Exception as e:
            res = {'error': str(e)}
        finally: return res

    async def update(self, data:dict=None):
        supplier = requests.get(f"{self.db_con}{data.get('_id')}").json()        
        try:
            payload = supplier | data
            requests.put(f"{self.db_con}{data.get('_id')}", json=payload)            
        except Exception as e:
            payload = {'error': str(e)}
        finally: del(supplier); return payload


    async def delete(self, data:dict=None):
        supplier = requests.get(f"{self.db_con}{data.get('_id')}").json()
        try:
            response = requests.delete(f"{self.db_con}{data.get('_id')}?rev={supplier['_rev']}")
            response = response.json()
        except Exception as e:
            response = {'error': str(e)}
        finally:
            del(supplier); return response


    async def get_elist(self):
        try:
            s = await self.all()            
        except Exception as e:
            s = {'error': str(e)}
        finally: return s


    def generate_id(self):
        ''' Generates a unique supplier id, also updates the supplier data''' 
        gen = GenerateId()
        try:
            ln = self.data.get('name').split(' ')
            self._id =  gen.name_id(ln=ln[1], fn=self.data.get('name'))            
        except:
            self._id = gen.name_id('C', 'P')
        finally:
            self.data['_id']=self._id
            return self._id

    @property
    def db_con(self):
        return self.conn(db=self.meta_data.get('database'))

    @property
    def db_con2(self):
        return self.conn(db=self.meta_data.get('databaseII'))


    def update_index(self, data:str) -> None:
        '''  Expects a unique id string ex. JD33766'''        
        self.index.add(data) 


    @property 
    def list_index(self) -> list:
        ''' Converts set index to readable list'''
        return [item for item in self.index]


## ROUTERS
async def createSupplier(request ):    
    '''Create a new Supplier .POST '''
    
    data = await request.json() 
    sp = Supplier(data=data)
    try:
        res = await sp.save()
        if res.get('ok') == True:
            res = sp.data
    except Exception as e:
        res = {'error', str(e)}
    finally: 
        del(data); del(sp)
        return JSONResponse(res)

async def getSuppliers(request ):    
    '''Returns a list of Suppliers  .GET '''   
    
    sp = Supplier()
    try:
        res = await sp.all()
    except Exception as e:
        res = {'error', str(e)}
    finally: 
        del(sp)
        return JSONResponse(res)

async def getSupplier(request ):    
    '''Returns a Single Supplier  .GET '''   
    id = request.path_params.get('id')    
    sp = Supplier()
    try:
        res = await sp.get(id=id)
    except Exception as e:
        res = {'error', str(e)}
    finally: 
        del(sp)
        return JSONResponse(res)

async def suppliersNameIndex(request):
    '''Returns a list of Suppliers  name and tax_id '''   
    
    sp = Supplier()
    try:
        res = await sp.nameIndex()
    except Exception as e:
        res = {'error', str(e)}
    finally: 
        del(sp)
        return JSONResponse(res)

async def invoiceIdIndex(request):
    '''Returns a list of invoice numbers and Suppliers  name'''    
    sp = Supplier()
    try:
        res = await sp.invoiceIdIndex()
        res = res[0]
    except Exception as e:
        res = {'error', str(e)}
    finally: 
        del(sp)
        return JSONResponse(res)     


async def checkInvoice(request):
    '''Validate and invoice'''
    tocheck = await request.json()
    sp = Supplier()
    invoice_index = await sp.invoiceIdIndex()
    try:
        result = { 'result': tocheck in invoice_index[0] }
    except Exception as e:
        result = { 'result': str(e) }
    finally: del(tocheck); del(sp); del(invoice_index); 
    return JSONResponse( result ) 


       
