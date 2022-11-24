#modeler.py
#import aiohttp
from asyncio import tasks
import requests
import orjson as json

from starlette.responses import JSONResponse

from utils.utilities import GenerateId, timestamp
from models.database import Connection
from models.employee import Employee




class Project(
    Connection,
    
):
    
    projects:list=[]
    
    def __init__(self, data:dict=None) -> None:
        self._id:str = None    
        self.meta_data:dict = {"created":timestamp(), "database": "cp-projects"}
        self.index:set = set()
        self.project:dict = {}
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
            r = requests.get(f"{self.db_con}_all_docs") 
            return r.json()            
        except Exception as e:
            return str(e)
        finally: del(r)

    async def nameIndex(self):
        def processIndex(p):
            return  p.get('value')
        try:
            r = requests.get(f"{self.db_con}_design/project-index/_view/name-view") 
            return list(map( processIndex,  r.json().get('rows')))            
        except Exception as e:
            return str(e)
        finally: del(r)


    async def get(self, id:str=None):
        r = requests.get(f"{self.db_con}{id}") 
        return r.json()  


    async def save(self, data:dict=None):
        self.mount(data=data)
        res = requests.post(f"{self.db_con}", json=self.data)
        return res

    async def update(self, data:dict=None):
        project = requests.get(f"{self.db_con}{data.get('_id')}").json()
        payload = project | data
        try:
            requests.put(f"{self.db_con}{data.get('_id')}", json=payload)
            return project
        except Exception as e:
            return str(e)
        finally:
            del(data) ; del(project); del(payload)


    async def delete(self, data:dict=None):
        project = requests.get(f"{self.db_con}{data.get('_id')}").json()
        try:
            requests.delete(f"{self.db_con}{data.get('_id')}?rev={project['_rev']}")
            return {"status": f"Project with id {project._id} DELETED"}
        except Exception as e:
            return str(e)
        finally:
            del(project); del(data)


    async def get_elist(self):
        await self.all_projects()
        return self.projects 

    def generate_id(self):
        ''' Generates a unique Project id, also updates the project data''' 
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


    def update_index(self, data:str) -> None:
        '''  Expects a unique id string ex. JD33766'''        
        self.index.add(data) 


    @property 
    def list_index(self) -> list:
        ''' Converts set index to readable list'''
        return [item for item in self.index]


    async def process_workers(self, index:list=None) -> dict:
        try:
            employees = []
            e = Employee()
            if len(index) > 0:
                for eid in index: 
                    worker = await e.get_worker(id=eid)
                    employees.append(worker)                
              
                return {"employees": employees} 
            else: return {"employees": []}                     
        except Exception as er:
            return str(er)
        finally: 
            del(employees);del(e)

    
    async def getTask(self, task_id:str=None):
        ''''Retreives a task from the project. 
        Requires the assigned task id '''
        try:            
            ends = task_id.split('-')
                
            def findTask(task):
                return task['_id'] == task_id
        
            project = await self.get(id=ends[0])                 
            task = list(filter( findTask, project.get('tasks') ))
            return task[0]
        except Exception as e:
            return {'error': str(e)}


    async def getEmployeeTasks(self, pe_id:str=None):
        ''''Retreives a batch of tasks assigned to the employee  from the project. 
        Requires the project id and the employee id'''
        try:            
            ends = pe_id.split('-')
                
            def findTasks(task):
                return task['assignedto'] == ends[1]

            project =  await self.get(id=ends[0]) 
            tasks = list(filter( findTasks, project.get('tasks') ))
            return tasks

        except Exception as e:            
            return {'error': str(e)}
        finally:
            del(ends) ; del(project) ; del(tasks)

    ## PROJECT ACCOUNTING 

    async def handleTransaction(self, id:str=None, data:dict=None):
        if data:
            gen = GenerateId()
            project = await self.get(id=id)
            data['id']= gen.gen_id(doc_tag='item')
            # process deposits
            if data.get('type') == 'Deposit':
                data['type'] = 'deposit'
                project['account']['transactions']['deposit'].append(data)
                project['account']['ballance'] += data.get('amount')
                project['account']['updated'] = timestamp()
            # process withdrawals
            if data.get('type') == 'Withdraw':
                data['type'] = 'withdraw'
                project['account']['transactions']['withdraw'].append(data)
                project['account']['ballance'] -= data.get('amount')
                project['account']['updated'] = timestamp() 

            try:
                requests.put(f"{self.db_con}{id}", json=project)
                res = {'sucess': True}
            except Exception as e:
                res = {'error': str(e)}
            finally:
                del(data);
                return project
        else:
            return {"error": 501, "message": "You did not provide any data for processing."}

    
    async def addWorkers(self, id:str=None, data:list=None):
        '''Requires a list of workers. Enshure the following JSON data format
            {
            "id": "LT0000",
            "key": "LT0000",
            "value": {
                "name": "Love True",
                "oc": "truelove",
                "occupation": "labourer",
                "added": 1664197078000
            }
            },
        '''
        if data:
            def enlist(item):
                return item['id']
               
            project = await self.get(id=id)
            workers = list(map(enlist, project['workers'])) 
            for item in data:
                if item.get('id') in workers:
                    pass
                else:
                    project['workers'].append(item )
            try:
                updated = await self.update(data=project)
                return updated
            except Exception as e:
                return {'error': str(e)}
            finally:
                del(data) ; del(project); del(workers)
        else:
            return {"error": 501, "message": "You did not provide any data for processing."}


    async def addTask(self, id:str=None, data:list=None):
        if data:                          
            project = await self.get(id=id)         
            for item in data:
                item['_id'] = f"{id}-{item['_id']}"                
                project['tasks'].append( item )
            try:
                requests.put(f"{self.db_con}{id}", json=project)
                return project
            except Exception as e:
                return {'error': str(e)}
            finally:
                del(data) ; del(project)
        else:
            return {"error": 501, "message": "You did not provide any data for processing."}


    async def updateTask(self, id:str=None, data:list=None):
        if data:
                          
            project = await self.get(id=id)
         
            for item in data:
                item['_id'] = f"{id}-{item['_id']}"
                
                project['tasks'].append( item )
            try:
                requests.put(f"{self.db_con}{id}", json=project)
                return project
            except Exception as e:
                return {'error': str(e)}
            finally:
                del(data) ; del(project)
        else:
            return {"error": 501, "message": "You did not provide any data for processing."}


    async def getTask(self, id:str=None):
        idds = id.split('-') 
        def findData(task):
            return task['_id'] == id
        project = await self.get(id=idds[0])
        try:
            return { "subject": project.get('name'), "id": idds[0], "task": list(filter(findData, project.get('tasks')))[0]}
        except Exception as e:
                return {'error': str(e)}
        finally:
                del(idds) ; del(project)

    async def addInvoice(self, id:str=None, data:dict=None):
        project = await self.get(id=id)
        project['account']['records']['invoices'].append(data)
        try:
            result = await self.update(data=project)            
        except Exception as e:
            result = {'error': str(e)}
        finally:
            del(project)
            return result


async def addProjectInvoice(request):
    id = request.path_params.get('id')
    invoice_data = await request.json()
    p = Project()
    try:
        result = await p.addInvoice(id=id, data=invoice_data)
    except Exception as e:
            result = {'error': str(e)}
    finally:
        del(p)
        return JSONResponse( result )
    




""" TEST
data = {
    "name":"The Donotia Experience",   
    "address":{},

}      

p = Project(data=data)


print()
print(p.data)

import asyncio
#asyncio.run(p.delete(p.data))

asyncio.run(p.all_workers())

print(p.workers)
"""