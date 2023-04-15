#coding=utf-8
#supplier.py
from modules.utils import timestamp
from database import Recouch
from starlette.responses import JSONResponse

class Supplier:    
    suppliers:list=[]
    meta_data:dict = {
        "created": 0, 
        "database": {"name":"supplier", "partitioned": False},
        }    
    def __init__(self, data:dict=None) -> None:
        self.conn = Recouch(local_db=self.meta_data.get('database').get('name'))
        self._id:str = None 
        self.data:dict = None   
        self.index:set = set()        
        if data:
            self.data = data
            if self.data.get("_id"): pass
            else: self.generate_id()

    def mount(self, data:dict=None) -> None:        
        if data:
            self.data = data
            if self.data.get("_id"): pass
            else: self.generate_id()

    async def all(self):
        try:
            r = await self.conn.get(_directive="_all_docs") 
            return r            
        except Exception as e: return str(e)
        finally: del(r)

    async def nameIndex(self):
        def processIndex(p): return p.get('key')
        try:
            r = await self.conn.get(_directive="_design/suppliers/_view/name-index") 
            return list(map( processIndex,  r.get('rows')))            
        except Exception as e: return str(e)
        finally: del(r)

    async def invoiceIdIndex(self):
        def processIndex(p): return  p.get('key')
        try:
            r = await self.conn.get(_directive="_design/project-index/_view/invoice-id") 
            return list(map( processIndex,  r.get('rows')))            
        except Exception as e: r = {'error': str(e)}
        finally: del(r)

    async def get(self, id:str=None):
        try:
            r = await self.conn.get(_directive=id) 
            return r  
        except Exception as e: return {'error': str(e)}
        finally: del(r)

    async def save(self):
        self.meta_data["created"] = timestamp()
        self.data['meta_data'] = self.meta_data
        try: return await self.conn.post( json=self.data)                        
        except Exception as e: return {'error': str(e)}
        

    async def update(self, data:dict=None):
        payload = None
        supplier = await self.get(id=data.get('_id'))        
        try:
            payload = supplier | data
            await self.conn.put(json=payload) 
            return payload           
        except Exception as e: return {'error': str(e)}
        finally: 
            del(payload)
            del(supplier)

    async def delete(self, id:str=None):
        try: return await self.conn.delete(_id=id)           
        except Exception as e: response = {'error': str(e)}
        finally:
            del(supplier)
            return response

    async def get_elist(self):
        try: s = await self.all()            
        except Exception as e: s = {'error': str(e)}
        finally: return s

    def generate_id(self):
        ''' Generates a unique supplier id, also updates the supplier data''' 
        from modules.utils import GenerateId       
        gen = GenerateId()
        ln = None 
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


    def update_index(self, data:str) -> None:
        '''  Expects a unique id string ex. JD33766'''        
        self.index.add(data) 


    @property 
    def list_index(self) -> list:
        ''' Converts set index to readable list'''
        return [item for item in self.index]


## ROUTERS
from decoRouter import Router

supplier_router = Router()


@supplier_router.post('/supplier')
async def createSupplier(request ):    
    '''Create a new Supplier .POST '''    
    data = await request.json() 
    sp = Supplier(data=data)
    try:
        res = await sp.save()
        print(res)
        if res.get('ok') == True: 
            return JSONResponse(sp.data)
    except Exception as e: 
        return JSONResponse({'error', str(e)})
    finally: 
        del(data)
        del(sp)
        

@supplier_router.get('/suppliers')
async def getSuppliers(request ):    
    '''Returns a list of Suppliers  .GET '''     
    sp = Supplier()
    try: res = await sp.all()
    except Exception as e: res = {'error', str(e)}
    finally: 
        del(sp)
        return JSONResponse(res)

@supplier_router.get('/supplier/{id}')
async def getSupplier(request ):    
    '''Returns a Single Supplier  .GET '''   
    id = request.path_params.get('id')    
    sp = Supplier()
    try: res = await sp.get(id=id)
    except Exception as e: res = {'error', str(e)}
    finally: 
        del(sp)
        return JSONResponse(res)


@supplier_router.get('/suppliersIndex')
async def suppliersNameIndex(request):
    '''Returns a list of Suppliers  name and tax_id ''' 
    sp = Supplier()
    try: res = await sp.nameIndex()
    except Exception as e: res = {'error', str(e)}
    finally: 
        del(sp)
        return JSONResponse(res)


@supplier_router.get('/invoices')
async def invoiceIdIndex(request):
    '''Returns a list of invoice numbers and Suppliers  name'''    
    sp = Supplier()
    try:
        res = await sp.invoiceIdIndex()
        res = res[0]
    except Exception as e:  res = {'error', str(e)}
    finally: 
        del(sp)
        return JSONResponse(res) 


@supplier_router.post('/checkinvoice')
async def checkInvoice(request):
    '''Validate and invoice'''
    tocheck = await request.json()
    sp = Supplier()
    invoice_index = await sp.invoiceIdIndex()
    try: result = { 'result': tocheck in invoice_index[0] }
    except Exception as e: result = { 'result': str(e) }
    finally: 
        del(tocheck)
        del(sp)
        del(invoice_index)
        return JSONResponse( result ) 


       
