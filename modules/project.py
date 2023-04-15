#coding=utf-8
#project.py

# Logging

from loguru import logger
from modules.utils import timestamp
from database import Recouch
from modules.employee import Employee
from schemas.schema_api import project_schema as schema, validate
from settings import SYSTEM_LOG, APP_LOG 

logger.add(
    APP_LOG, 
    rotation="50 MB",
    colorize=True, 
    enqueue=True,
    serialize=True
    
    #format="<green>{time}</green> <level>{message}</level>"
)

class Project: 
    error_log:dict = {}   
    projects:list=[]    
    meta_data:dict = {
        "created": 0, 
        "database": {"name":"rb-project", "partitioned": False},              
    }

    def __init__(self, data:dict=None): 
               
        self.conn = Recouch(local_db=self.meta_data.get('database').get('name'))
        self._id:str = None        
        self.index:set = set()
        self.project:dict = {}
        if data and self.validate_data(data, schema):
            self.meta_data["created"] = timestamp()  
            self.meta_data['properties'] = list(data.keys())          
            self.data = data
            self.data["meta_data"] = self.meta_data
                      
            if self.data.get("_id"):
                pass
            else:
                self.generate_id(local=True)
        else:                     
            self.data = {"meta_data":self.meta_data}

    @property    
    def report_error(self):
        return self.error_log

    @property
    def data_validation_error(self):
        self.meta_data["created"] = timestamp()
        self.meta_data['flagged'] = {
            "message": "There was an error in your data, please rectify and try Mounting it again.",
            "flag": self.report_error
        }

    def validate_data(self, data, schema):
        try:
            validate(instance=data, schema=schema)
            return True
        except Exception as e:
            self.error_log['data_validation'] = str(e)
            self.data_validation_error   
            return False

    def setup(self):
        """is called after data has been mounted """
        check_list = self.meta_data.get("properties")
        self.process_address()
        if "owner" in check_list: pass
        else: self.data['owner'] = {
            "name": None,
            "contact": None,
            "address": {"lot": None, "street": None, "town": None,"city_parish": None,"country": None, }
        }
        if "account" in check_list: pass
        else: self.data['account'] = {
            "ballance": 0,
            "started": timestamp(),
            "transactions": {
                "deposits": [], 
                "withdraw": []
            },
            "records": {
                "invoices": [],
                "purchase_orders": []
            }
        }
        if "tasks" in check_list: pass
        else:self.data['tasks'] = [] 
        if "workers" in check_list: pass
        else:self.data['workers'] = [] 
        if "inventory" in check_list: pass
        else:self.data['inventory'] = [] 
        if "activity_log" in check_list: pass
        else:self.data['activity_log'] = [] 
        self.process_event()
        self.process_state()
        self.meta_data['properties'] = list(self.data.keys())
        self.meta_data['properties'].remove('meta_data')

    def runsetup(self):
        """is called after data has been mounted """
        
        PROJECT_TEMPLATE = dict( 
            address = {"lot": None, "street": None, "town": None,"city_parish": None,"country": "Jamaica", },
            owner = {
            "name": None,
            "contact": None,
            "address": {"lot": None, "street": None, "town": None,"city_parish": None,"country": None, }
        },
        account = {
            "ballance": 0,
            "started": timestamp(),
            "transactions": {
                "deposits": [], 
                "withdraw": []
            },
            "records": {
                "invoices": [],
                "purchase_orders": []
            }
        },
        tasks = [],
        workers = [],
        inventory = [],
        activity_log = [],
        event = {
            "started": 0,
            "completed": 0,
            "paused": [],
            "restart": [],
            "terminated": 0
        },
        state =  {
            "active": False,
            "completed": False,
            "paused": False,
            "terminated": False
        }
        )
        #self.data.update(PROJECT_TEMPLATE | self.data)
        self.data = self.data | PROJECT_TEMPLATE
        self.meta_data['properties'] = list(self.data.keys())
        self.meta_data['properties'].remove('meta_data')


    def mount(self, data:dict=None): 
        #remove fragments from previous validation
        if self.meta_data.get('flagged'): del self.meta_data['flagged']       
        if data and self.validate_data(data, schema):
            self.meta_data["created"] = timestamp()
            self.meta_data['properties'] = list(data.keys())
            self.data = data            
            self.data['meta_data'] = self.meta_data
            if self.data.get("_id"):
                pass
            else:
                self.generate_id(local=True)

    ## CRUD OPERATIONS
    async def all(self):
        try:
            r = await self.conn.get(_directive="_design/project-index/_view/name-view") 
            return r           
        except Exception as e:
            return str(e)
        finally: del(r)

    async def nameIndex(self):
        def processIndex(p):
            return  p.get('value')
        try:
            r = await self.conn.get(_directive="_design/project-index/_view/name-view") 
            return list(map( processIndex,  r.json().get('rows')))            
        except Exception as e:
            return str(e)
        finally: del(r)


    async def get(self, id:str=None):
        r = None
        try:
            r = await self.conn.get(_directive=id)

            logger.info(f'Request for Project {r.get("_id")} Completed sucessfully.')
            return r
        except Exception as e:
            logger.error(str(e))
            return str(e)
        finally: del(r)  


    async def save(self, data:dict=None):        
        self.mount(data=data)
        self.setup()
        #return self.data
        logger.info('New project created ')
        return await self.conn.post( json=self.data )       
        

    async def update(self, data:dict=None):
        try:
            logger.info(f'Project {data.get("_id")} updated.')
            return await self.conn.put( json=data)            
        except Exception as e:
            logger.error(str(e))
            return str(e)
        

    async def delete(self, id:str=None):
        status = None
        try:
            status = await self.conn.delete(_id=id)
            return {"status": status}
        except Exception as e:
            return str(e)
        finally:
            del(status)


    async def get_elist(self):
        await self.all_projects()
        return self.projects 

    def generate_id(self, line_1:str=None, line_2:str=None, local:bool=None ):
        ''' Generates unique id's also may update the project data
            may also return a generator function 
            ---
            requires: 
                line_1: a char or string of chars.
                line_2: ditto above,
                local: True or False
            returns a generator function if no argument is provided
        ''' 
        from modules.utils import GenerateId       
        gen = GenerateId() 
        # Case_1: generate id for other
        if line_1 and line_2: 
            try:            
                return  gen.name_id(ln=line_1, fn=line_2) 
            except Exception as ex:
                return str(ex)
            finally:
                del(gen)
                del(GenerateId) 
        # Case_2: generate id locally               
        elif local: 
            try:            
                self._id = gen.name_id(
                    ln=self.data.get('name').split(' ')[1], 
                    fn=self.data.get('name')
                    ) 
                self.data['_id'] = self._id
            except Exception as ex:
                return str(ex)
            finally:                
                del(gen)
                del(GenerateId) 
        # Case_3: return the generator               
        else:
            try:
                return gen
            finally: 
                del(gen)
                del(GenerateId)


    def update_index(self, data:str) -> None:
        '''  Expects a unique id string ex. JD33766'''        
        self.index.add(data) 


    @property 
    def list_index(self) -> list:
        ''' Converts set index to readable list'''
        return [item for item in self.index]
   
    
    ## PROJECT ACCOUNTING
    async def handleTransaction(self, id:str=None, data:dict=None):
        if data:
            gen = self.generate_id()
            project = await self.get(id=id)
            data['id']= gen.gen_id(doc_tag='item')
            # process deposits
            if data.get('type') == 'deposit':                
                project['account']['transactions']['deposit'].append(data)
                #processProjectAccountBallance()
                project['account']['updated'] = timestamp()
            # process withdrawals
            if data.get('type') == 'withdraw':               
                project['account']['transactions']['withdraw'].append(data)
                #processProjectAccountBallance()
                project['account']['updated'] = timestamp()
            try:
                await self.update(data=project)
                return project
            except Exception as e:
                return {'error': str(e)}
            finally:
                del(gen)
                del(project) # clean up
        else:
            return {"error": 501, "message": "You did not provide any data for processing."}

    async def addInvoice(self, id:str=None, data:dict=None):        
        project = await self.get(id=id)
        project['account']['records']['invoices'].append(data)
        try:
            return await self.update(data=project)            
        except Exception as e:
            return {'error': str(e)}
        finally:
            del(project)

    
    async def deleteInvoice(self, id:str=None, data:dict=None):        
        project = await self.get(id=id)
        project['account']['records']['invoices'].remove(data)
        try:
            return await self.update(data=project)            
        except Exception as e:
            return {'error': str(e)}
        finally:
            del(project)

    async def getInvoices(self, id:str=None):        
        project = await self.get(id=id)
        try:
            return project.get('account').get('records').get('invoices')
        except Exception as e:
            return str(e) 
        finally:
            del(project)


    # Project Expences
    async def addExpence(self, id:str=None, data:dict=None):        
        project = await self.get(id=id)
        project['account']['expences'].append(data)
        try:
            await self.update(data=project) 
            return project.get('account').get('expences')         
        except Exception as e:
            return {'error': str(e)}
        finally:
            del(project)

    
    async def deleteExpence(self, id:str=None, data:dict=None):        
        project = await self.get(id=id)
        project['account']['expences'].remove(data)
        try:
            await self.update(data=project) 
            return project.get('account').get('expences')         
        except Exception as e:
            return {'error': str(e)}
        finally:
            del(project)


    # Worker Salary Record
    async def addWorkerSalary(self, id:str=None, data:dict=None):        
        project = await self.get(id=id) 
        withdraw =  {
                "id": data.get("ref"),
                "date": data.get("date"), 
                "type":"withdraw",            
                "amount": data.get("total"), 
                "ref": data.get("ref"),
                "recipient": {
                    "name": data.get("name")
                }
            } 
        project['account']['transactions']['withdraw'].append(withdraw)      
        project['account']['records']['salary_statements'].append(data)
        
        try:
            e = Employee()
            pb = await e.addPay(id=data.get('employeeid'), data=data )       
            print(project['account']['records']['salary_statements'])
            print(pb)
            await self.update(data=project) 
            return project.get('account').get('records').get('salary_statements')         
        except Exception as e:
            return {'error': str(e)}
        finally:
            del(project)

    async def deleteWorkerSalary(self, id:str=None, data:dict=None):
        ## get the project

        # get the account transactions and records 
        # find and remove the salary_statement in question
        # find and remove the withdrawal record from account transactions withdral
        # update the project 
        pass



    async def getExpences(self, id:str=None):        
        project = await self.get(id=id)
        try:
            return project.get('account').get('expences')
        except Exception as e:
            return str(e) 
        finally:
            del(project)


    ## PROJECT WORKERS
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
            def enlist(item): # utility sort function
                return item['id']               
            project = await self.get(id=id)
            workers = list(map(enlist, project['workers'])) 
            updated = None
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
                del(updated)
                del(item)
                del(workers)
                del(project)
        else:
            return {"error": 501, "message": "You did not provide any data for processing."}

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
            del(employees)
            del(e)

    ## PROJECT INVENTORY 
    def sortInventory(self, keywords, datalist):
        def sort(item):
            keyword = item.get('item')
            for word in keywords:
                if word in keyword:
                    return None
                else: return item


    async def addInventory(self, id:str=None, data:list=None):
        if data:                          
            project = await self.get(id=id)  
            # check if this material inventory exists 
            # if not add it 
            project['inventory'].append(data)
        else:
            pass
        return project.get('inventory')
    
    async def addInventoryItem(self, id:str=None, data:list=None):
        if data:                          
            project = await self.get(id=id)  
            # check if this material inventory exists 
            # if not add it 
            project['inventory'].append(data)
        else:
            pass
        return project.get('inventory')

    ## PROJECT RATES
    async def addRate(self, id:str=None, data:list=None):
        if data:                          
            project = await self.get(id=id)         
            for item in data:
                item['_id'] = f"{id}-{item['_id']}"                
                project['rates'].append( item )
            try:
                await self.update(data=project)
                return project
            except Exception as e:
                return {'error': str(e)}
            finally:
                del(item)
                del(project)
        else:
            return {"error": 501, "message": "You did not provide any data for processing."}


    async def updateRate(self, id:str=None, data:list=None):
        if data:                          
            project = await self.get(id=id)         
            for item in data:
                item['_id'] = f"{id}-{item['_id']}"                
                project['rates'].append( item )
            try:
                await self.update(data=project)
                return project
            except Exception as e:
                return {'error': str(e)}
            finally:
                del(item)
                del(project)
        else:
            return {"error": 501, "message": "You did not provide any data for processing."}


    async def getRateById(self, id:str=None):
        idds = id.split('-') 
        def findData(rate): # utility search function
            return rate['_id'] == id
        project = await self.get(id=idds[0])
        try:
            return { "subject": project.get('name'), "id": idds[0], "rate": list(filter(findData, project.get('rates')))[0]}
        except Exception as e:
                return {'error': str(e)}
        finally:
                del(idds)
                del(project)

    async def getRate(self, rate_id:str=None):
        ''''Retreives a rate from the project. 
        Requires the assigned rate id '''
        try:            
            ends = rate_id.split('-')
            def findRate(rate): # utility search function 
                return rate['_id'] == rate_id        
            project = await self.get(id=ends[0])                 
            rate = list(filter( findRate, project.get('rates') ))
            return rate[0]
        except Exception as e:
            return {'error': str(e)}


    async def getEmployeeRates(self, pe_id:str=None):
        ''''Retreives a batch of rates assigned to the employee  from the project. 
        Requires the project id and the employee id'''
        try:            
            ends = pe_id.split('-')                
            def findRates(rate): # utility search function
                return rate['assignedto'] == ends[1]
            project =  await self.get(id=ends[0]) 
            rates = list(filter( findRates, project.get('rates') ))
            return rates
        except Exception as e:            
            return {'error': str(e)}
        finally:
            del(ends)
            del(rates)
            del(project) 


    ## PROJECT JOBS
    async def getJob(self, id:str=None, jobs:list=None):        
        def find_item(item):
                return item['_id'] == id
        try:
            return list(filter(find_item, jobs))[0]
        except Exception as e: return str(e) 
        

    async def addJobToQueue(self, id:str=None, data:dict=None):
        ''' Add a new job to the project jobs queue. returns the updated jobs queue'''
        if data:                          
            project = await self.get(id=id) 
            flg = data.get('title', 'p j')
            flg = flg.split(' ')
            jid = self.generate_id( line_1=flg[0], line_2=flg[1]) 
            data['_id'] = f"{id}-{jid}"                
            project['tasks'].append( data )
            try:
                await self.update(data=project)
                return project.get('tasks')
            except Exception as e:
                return {'error': str(e)}
            finally:
                del(flg)
                del(project)
        else:
            return {"error": 501, "message": "You did not provide any data for processing."}


    async def addTaskToJob(self, id:str=None, data:list=None):
        '''adds a task to a job '''
        idd = id.split('-')        
        project = await self.get(id=idd[0])
        def find_item(item):
                return item['_id'] == id
        job = list(filter(find_item, project.get('tasks')))[0]         
        for task in data:
            job['tasks'].append(task)
            logger.info(f"Task { task.get('_id')} Addedd to Job {idd[1]} on Queue {idd[0]}")        
        await self.update(project)
        return job

    async def processJobCost(self, id:str=None):
        idid = id.split('-')
        IS_METRIC = False
        project = await self.get(id=idid[0])
        if project.get('standard') == 'metric':
            IS_METRIC = True         
        def find_item(item):
            if item.get('_id') == id:
                return item
        job = list(filter(find_item, project.get('tasks')))[0]
        job['progress'] = 0        
        def process_task(task):
            ''''''
            # Process metric rates
            if IS_METRIC:
                metric = task.get('metric')
                cost = metric.get('cost')
                price = metric.get('price')
                quantity = metric.get('quantity')
                # Check and Validate type
                if cost: ## type is string convert to float 
                    if type(cost) == str: task['metric']['cost'] = float(cost)
                else: task['metric']['cost'] = 0.001  ## value is None give a small value   
                if price:  
                    if type(price) == str: task['metric']['price'] = float(price)
                else: task['metric']['price'] = 0.001 
                if quantity:  
                    if type(quantity) == str: task['metric']['quantity'] = float(quantity)
                else: task['metric']['quantity'] = 0.001  
                   
                task['metric']['cost'] = task.get('metric').get('price') * task.get('metric').get('quantity')
                job['cost']['task'] += float(task.get('metric').get('cost')) 
                job['progress'] += float(task.get('progress'))
                output = task.get('output').get('metric', 1)
                # Chech and Validate type
                if type(output) == None: output = 0.00001
                elif type(output) == str: output = float(output)
                # check for zero value
                if output < 1: output = 0.00001               
                task['duration'] = round(task.get('metric').get('quantity', 1) / float(output),2)
                if 'total' in list(task.get('metric').keys()): del(task['metric']['total'])
                else: pass
            # Handle task reassignment
            if task.get('assignedto') == job.get('crew').get('name'):
                task['assignedto'] = None
                task['assigned'] = False 
            else: task['duration'] = task['duration'] / len( task['assignedto'])    
        # Generator       
        tasks = list(map( process_task,  job.get('tasks') ))
        # Process job costs
        job['cost']['contractor'] =  (float(job.get('fees').get('contractor', 0.0001)) / 100) * job.get('cost').get('task', 0)  
        job['cost']['misc'] =  (float(job.get('fees').get('misc', 0.0001)) / 100) * job.get('cost').get('task', 0)  
        job['cost']['insurance'] =  (float(job.get('fees').get('insurance', 0.0001)) / 100) * job.get('cost').get('task', 0) 
        job['cost']['overhead'] =  (float(job.get('fees').get('overhead', 0.0001)) / 100) * job.get('cost').get('task', 0) 
        total_costs = [
            job.get('cost').get('contractor'),
            job.get('cost').get('misc'),
            job.get('cost').get('insurance'),
            job.get('cost').get('overhead'),
            job.get('cost').get('task', 0)
        ]
        job['cost']['total'] = sum(total_costs)
       
        fee_percents = [
            float(job.get('fees').get('contractor', 0)),
            float(job.get('fees').get('misc', 0)),
            float(job.get('fees').get('insurance', 0)),
            float(job.get('fees').get('overhead', 0))

        ]
        job['fees']['job'] = 100 - sum(fee_percents)
        fee_percents.append(
            job.get('fees').get('job')
        )
        # Analytical Data 
        job['analytics'] = {
            "feePercents": fee_percents,
            "costTotals": total_costs,
            'jobCosts': {
                "title": f"Job Costs Disbursement",
                "legend": [
                    "Contractor",
                    "Miscellaneous",
                    "Insurance",
                    "Overheads",
                    "Job"
                    ],
                "series": [
                    {
                        "name": f"{job.get('_id')} Renumeration",
                        "type": "pie",
                        "radius": "55%",
                        "center": ["50%", "60%"],
                        "data": [
                            {"value": job.get('cost').get('contractor'), "name": "Contractor"},
                            {"value": job.get('cost').get('misc'), "name": "Miscellaneous"},
                            {"value": job.get('cost').get('insurance'), "name": "Insurance"},
                            {"value": job.get('cost').get('overhead'), "name": "Overheads"},
                            {"value": job.get('cost').get('task'), "name": "Job"}
                        ]
                    }
                ],
                "emphasis": {
                    "itemStyle": {
                    "shadowBlur": 10,
                    "shadowOffsetX": 0,
                    "shadowColor": "rgba(0, 0, 0, 0.5)"
                    }
                }

            }
        }
        tasks = len(job.get('tasks'))
        if tasks > 0:
            job['progress'] = job['progress'] / tasks
        else: pass
        return job
    

    async def updateJobTasks(self, id:str=None, tasks:list=None)-> list:
        '''Rplaces the projects job tasks list '''
        idd = id.split('-')
        p = await self.get(id=idd[0]) # locate the project
        job = await self.getJob(id=id, jobs=p.get('tasks'))  # locate the job
        job['tasks'] = tasks
        await self.update(data=p)
        return job.get('tasks')
        

        
    ## PROJECT JOB CREW    
    async def getProjectCrews(self, id:str=None):
        ''' return a list of job crews employed to a project'''          
        project = await self.get(id=id)
        crews, names = [], [] 
        def find_item(item):
            if item.get('crew').get('name') not in names:
                names.append(item.get('crew').get('name'))
                crews.append(item.get('crew'))
            return item['crew']
        crews_ = list(map(find_item, project.get('tasks')))
        # remove duplicates
        return crews

    async def addCrewMembers(self, id:str=None, data:list=None):
        '''Assigns members from a list to the job's crew members list'''
        idd = id.split('-')
        p = await self.get(id=idd[0]) # locate the project

        job = await self.getJob(id=id, jobs=p.get('tasks'))  # locate the job
        
        try:
            for member in data:
                job['crew']['members'].append(member)
            
            await self.update(p)
            return job
        except Exception as e: return str(e)


    async def assignTaskToCrewMember(self, id:str=None, wid:str=None):
        '''Assigns a tasks of a number tasks to a crew member'''
        idd = id.split('-')
        p = await self.get(id=idd[0]) # locate the project
        job = await self.getJob(id=f"{idd[0]}-{idd[1]}", jobs=p.get('tasks'))  # locate the job
        
        # process Job task 
        def find_task(task):
            if task.get('_id') == id:
                return task
        task = list(filter(find_task, job.get('tasks')))[0]
        task['assigned'] = True
        if type(task['assignedto']) == str:
            task['assignedto'] = [wid]
        else: 
            task['assignedto'].append(wid)

        # process employee tasks
        def find_worker(worker):
            if worker.get('id') == wid:
                return worker
        worker = list(filter(find_worker, job.get('crew').get('members')))[0]
        
        e = Employee()
        employee_assigned_jobtasks = await e.addJobTask(id=f"{worker.get('occupation')}s:{wid}", data=id)

        worker['tasks'] = employee_assigned_jobtasks.get('tasks')
        try:
            
            await self.update(data=p)
            return job.get('tasks')
        except Exception as e: return str(e)

    async def administerTaskProgress(self, id:str=None, data:int=None):
        ''' Advances the task progress'''
        idd = id.split('-')
        p = await self.get(id=idd[0]) # locate the project
        job = await self.getJob(id=f"{idd[0]}-{idd[1]}", jobs=p.get('tasks'))  # locate the job
        def find_task(task):
            if task.get('_id') == id:
                return task
        task = list(filter(find_task, job.get('tasks')))[0]
        task['progress'] = data
        try:            
            await self.update(data=p)
            return {
                "tasks":job.get('tasks'),
                "analytics": await self.JobProgressAnalytics(job=job)
            }
        except Exception as e: return str(e)

    async def JobProgressAnalytics(self, job:dict=None):
        def get_ids(item):
            idd = item.get('_id').split('-')
            return f"{idd[1]}-{idd[2]}"
        task_ids = list(map(get_ids, job.get('tasks')))
        task_progress = [task.get('progress') for task in job.get('tasks')]

        return {
            "tasks_ids": task_ids,
            "progress": task_progress
        }

    ## PROJECT LOCATION AND ADDRESS MANAGEMENT
    def process_address(self):
        template = {"lot": None, "street": None, "town": None,"city_parish": None,"country": "Jamaica", }
        if 'address' in self.meta_data.get('properties'):
            check_list = list(self.data.get('address').keys())            
            for item in check_list:
                template[item] =  self.data['address'][item]
            self.data['address'] = template
        else: self.data['address'] = template

    ## PROJECT EVENTS 
    def process_event(self):
        template = {
            "started": 0,
            "completed": 0,
            "paused": [],
            "restart": [],
            "terminated": 0
        }
        if 'event' in self.meta_data.get('properties'):
            check_list = list(self.data.get('event').keys())            
            for item in check_list:
                template[item] =  self.data['event'][item]
            self.data['event'] = template
        else: self.data['event'] = template

    ## PROJECT STATE MANAGEMENT       
    def process_state(self):
        template =  {
            "active": False,
            "completed": False,
            "paused": False,
            "terminated": False
        }
        if 'state' in self.meta_data.get('properties'):
            check_list = list(self.data.get('state').keys())            
            for item in check_list:
                template[item] = self.data['state'][item]
            self.data['state'] = template
        else: self.data['state'] = template
            
    ## PROJECT REPORTING
    async def addJobReport(self, id:str=None, data:dict=None):
        project = await self.get(id=id)
        project['reports'].append(data)
        try:
            await self.update(data=project) 
            return data          
        except Exception as e:
            return {'error': str(e)}
        finally:
            del(project)

    async def getJobReports(self, id:str=None):
        idds = id.split('-')
        project = await self.get(id=idds[0])
        reports = project.get('reports')
        if len(reports) > 0:
            def process_report(item):
                if item.get('meta_data').get('job_id') == id:
                    return item

            try:
                return list(filter(process_report, reports))                          
            except Exception as e:
                return {'error': str(e)}
            finally:
                del(project)
        else: return []


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