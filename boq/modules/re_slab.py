#Tekla BQ Wall Module / Router

from starlette.responses import JSONResponse
from sledge.models.tasks import Task


class BarWeights:
    def __init__(self):
        self.__bar_weights = None

    @property
    def barweights_lib(self):
        self.__bar_weights = {
        "m6": {"value": 0.395, "unit": "kg/m"},
        "m10": {"value": 0.617, "unit": "kg/m"},
        "m12": {"value": 0.888, "unit": "kg/m"},
        "m16": {"value": 1.580, "unit": "kg/m"},
        "m20": {"value": 2.469, "unit": "kg/m"},
        "m25": {"value": 3.858, "unit": "kg/m"},
        }
        return self.__bar_weights




class Slab( BarWeights ):
    ''' A Concrete Masonry Unit . Accepts only Feet and Meters '''
    tracker:list = []
    data_flag:bool = False 

    def __init__(self, data:dict=None):
        if data:
            self.data_flag = True  
            self.tag = data.get('tag')   
            self.type = data.get('type')                   
            self.width = data.get('width')
            self.length = data.get('length')
            self.height = data.get('height')
            self.rebars = data.get('rebars')
            self.openings = data.get('openings', [])
            self.unit = self.set_units(unit=data.get('unit'))  
            self.report = {
            "wall": None,
            "reinforcement": None,
            "finishes": None
            }   
            self.materials = {
            
            }               
            self.process_data  
            self.track_wall    
            self.process_rebar
            self.process_finishes
            

    @property
    def area(self):
        if self.data_flag:
            return {
                "unit": self.unit.get('area'), 
                "value": round((self.length['value'] * self.height['value']) - sum(self.openings.get('areas')),2)
                }
        return None

    @property
    def blocks(self):
        if self.unit['len'] == 'ft':
            block_area = .667 *1.333
        else:
            block_area = 0.2 * 0.4
        return {'unit': 'Each', 'value': round(self.area['value'] / block_area) + 1}

    #------------- Data Processors ---------------- 

    def set_units(self, unit:str=None):
        '''Process wall units'''
        data = { "len": "", "area": "", "vol": ""}
        factor = 1
        if unit == 'm': # Case m needs no conversion             
            data['len'] = 'm'; data['area'] = 'm2'; data['vol'] = 'm3'
            self.process_measurements(factor)
            self.openings = self.process_openings(data = self.openings, factor=factor)
           
        if unit == 'mm': # Case mm convert to m 
            factor = 1000
            data['len'] = 'm'; data['area'] = 'm2'; data['vol'] = 'm3'
            self.process_measurements(factor)
            self.openings = self.process_openings(data = self.openings, factor=factor)
        if unit == 'ft': # Case ft needs no conversion            
            data['len'] = 'ft'; data['area'] = 'ft2'; data['vol'] = 'ft3'                       
        return data

    def process_measurements(self, factor):
        # Convert Measurements
        self.width = self.width/factor
        self.length = self.length/factor
        self.height = self.height/factor

    @property
    def process_data(self):
        self.width = {"unit": self.unit.get('len'),  "value": self.width}
        self.length = {"unit": self.unit.get('len'),  "value": self.length}
        self.height = {"unit": self.unit.get('len'),  "value": self.height}
    
    def process_openings(self, data:list=None, factor:int=None):
        def convert(item ):
            item['height'] = item['height'] / factor
            item['width'] = item['width'] / factor            
            return item
        def areas(item):
            return round((item['width'] * item['height']) * item['amt'], 2)
        def jamb(item):
            if 'D' in item.get('tag'):
                return round((item['width'] + (2 * item['height'])) * item['amt'],2) # Doors
            else:
                return round(((item['width'] * 2) + (2 * item['height'])) * item['amt'], 2)# Windows
        return {
            'openings': list(map(convert, data)),
            'areas': list(map(areas, data)),
            'jamb': list(map(jamb, data)),
        }

    @property
    def process_rebar(self):
        self.rebars['h']['amt'] = round((self.height['value'] / self.rebars['h']['spacing'])) +1            
        self.rebars['v']['amt'] = round((self.length['value'] / self.rebars['v']['spacing'])) + 1
        
        self.rebars['h']['bars'] = round(((self.rebars['h']['amt'] * self.length['value'])) / 9)
        self.rebars['v']['bars'] = round(((self.rebars['v']['amt'] * self.height['value'])) / 9)

        self.rebars['h']['weight'] = {"value": None, "unit": "Kg"}
        self.rebars['v']['weight'] = {"value": None, "unit": "Kg"}
        

    @property
    def process_finishes(self):
        self.finishes = {
            'rough_cast': {"unit": self.unit.get('area'), "value": self.area.get('value', 1) * 2 },            
        }
        self.finishes['render'] = {"unit": self.unit.get('area'), "value": self.finishes['rough_cast'].get('value', 1) }
        self.finishes['flat_jamb'] = {"unit": self.unit.get('len'), "value": sum(self.openings.get('jamb'))}
        
    @property
    async def process_report(self):
        rates = await self.building_rates 
        def findRate(id):
            def search(rate):
                return rate['_id'] == id
            return list(filter(search, rates))[0]   
        blockrateid = self.wall_rate_index.get('masonry').get('blockwork').get('150_gf')  
        roughdressid = self.wall_rate_index.get('masonry').get('finishes').get('rough_dress')  
        roughjambid = self.wall_rate_index.get('masonry').get('finishes').get("rough_jamb") 
        dressjambid = self.wall_rate_index.get('masonry').get('finishes').get('dress_jamb') 
        vbarid = self.wall_rate_index.get('steelwork').get(self.rebars.get('v').get('type')) 
        hbarid = self.wall_rate_index.get('steelwork').get(self.rebars.get('h').get('type'))
        pid = self.wall_rate_index.get('masonry').get('finishes').get("paint_2")                      

        self.report['wall'] = {
        "blockwork": findRate(blockrateid),
        "rough&dress": findRate(roughdressid),
        "roughjamb": findRate(roughjambid),
        "dressjamb": findRate(dressjambid),
        }
        self.report['reinforcement'] = {
        "vertical": findRate(vbarid),
        "horizontal": findRate(hbarid)
        }
        self.report['finishes'] = {
            "painting": findRate(pid)
        }    
        self.report['wall']['blockwork']['_id'] = f"{self.report['wall']['blockwork']['_id']}-{self.tag}"


        self.report['reinforcement']['vertical']['_id'] = f"{self.report['reinforcement']['vertical']['_id']}-{self.tag}"
        self.report['reinforcement']['horizontal']['_id'] = f"{self.report['reinforcement']['horizontal']['_id']}-{self.tag}"


        self.report['wall']['blockwork']['metric']['quantity'] = self.area.get('value')
        self.report['wall']['blockwork']['metric']['total'] = self.report['wall']['blockwork']['metric']['quantity'] * self.report['wall']['blockwork']['metric']['price']
        self.report['wall']['blockwork']['duration'] = { 
        "value": round( self.report['wall']['blockwork']['metric']['quantity'] / self.report['wall']['blockwork']['output']['metric'],2),
        "unit": "days"
        }

        self.report['wall']['rough&dress']['_id'] = f"{self.report['wall']['rough&dress']['_id']}-{self.tag}"
        self.report['wall']['rough&dress']['metric']['quantity'] = self.finishes.get('rough_cast').get('value')
        self.report['wall']['rough&dress']['metric']['total'] =  self.report['wall']['rough&dress']['metric']['quantity'] *  self.report['wall']['rough&dress']['metric']['price']
        self.report['wall']['rough&dress']['duration'] = {
            "value": round( self.report['wall']['rough&dress']['metric']['quantity'] / self.report['wall']['rough&dress']['output']['metric'], 2),
            "unit": "days"
            }

        self.report['wall']['roughjamb']['_id'] = f"{self.report['wall']['roughjamb']['_id']}-{self.tag}"
        self.report['wall']['roughjamb']['metric']['quantity'] = round(self.finishes.get('flat_jamb').get('value'), 2)
        self.report['wall']['roughjamb']['metric']['total'] = self.report['wall']['roughjamb']['metric']['quantity'] * self.report['wall']['roughjamb']['metric']['price']
        self.report['wall']['roughjamb']['duration'] =  { "value": self.report['wall']['roughjamb']['metric']['quantity'] /  self.report['wall']['roughjamb']['output']['metric'], "unit": "days"}

        self.report['wall']['dressjamb']['_id'] = f"{self.report['wall']['dressjamb']['_id']}-{self.tag}"
        self.report['wall']['dressjamb']['metric']['quantity'] = self.report['wall']['roughjamb']['metric']['quantity']
        self.report['wall']['dressjamb']['metric']['total'] = self.report['wall']['dressjamb']['metric']['quantity'] * self.report['wall']['dressjamb']['metric']['price']
        self.report['wall']['dressjamb']['duration'] =  { "value": self.report['wall']['dressjamb']['metric']['quantity'] /  self.report['wall']['dressjamb']['output']['metric'], "unit": "days"}

        self.report['finishes']['painting']['_id'] = f"{self.report['finishes']['painting']['_id']}-{self.tag}"
        self.report['finishes']['painting']['metric']['quantity'] = self.report['wall']['rough&dress']['metric']['quantity']
        self.report['finishes']['painting']['metric']['total'] = self.report['finishes']['painting']['metric']['quantity'] * self.report['finishes']['painting']['metric']['price']
        self.report['finishes']['painting']['duration'] = { "value": round(self.report['finishes']['painting']['metric']['quantity'] / self.report['finishes']['painting']['output']['metric'], 2), "unit": "days"}


    @property
    async def process_materials(self):
        self.materials['wall'] = {
            "id": self.tag,
            "material_list": [
                {"item":1, "description": "Portland Cement","unit": "Bags", "amt":0 },
                {"item":2, "description": "Washed Sand (Fine Agg.)","unit": "Ton", "amt":0 },
                {"item":3, "description": "Crushed Stone (Course Agg.)","unit": "Ton", "amt":0 },
                {"item":4, "description": "Blocks","unit": "bags", "amt":0 },
                {"item":5, "description": "Water", "unit": "liter", "amt":0 },

            ]
        }


    # Trackers
    @property
    def track_wall(self):
        if self.data_flag:
            self.tracker.append({
                'tag': self.tag,
                'length': self.length,
                'width':self.width,
                'area': self.area
            })
    
    @property
    def wall_segments(self): return len(self.tracker)

    @property
    def wall_ids(self): 
        def id_tag(item):
            return item['tag']
        return list(map(id_tag, self.tracker))

    @property
    async def building_rates(self):
        t = Task()
        return await t.all_tasks()

    @property
    def wall_rate_index(self):  
           
        return {
            "masonry":{
                "blockwork": {
                    "150_gf": 'L641216',
                    "150_ff":'L66092',
                    "150_drain": 'L624899',
                    "200_gf":'L86121',
                    "200_ff":'L87793',
                    "200_drain": 'L838580',                    

                },
                "finishes": {
                    "rough_dress": 'RA9114',
                    "rough_wall": 'RC7476',
                    "dress_jamb": "GJ9215",
                    "rough_jamb": "RC6844",
                    "paint_1": "EP27254",
                    "paint_2": "EP43818"
                }
            },
            "steelwork": {
            "m10": "MS0001",
            "m12": "MS0002",
            "m16": "MS0003",
            "m19": "MS0004",
            "m25": "MS0005",
            
            }
        }
        
# Routers

async def  processSlab(request):
    slab =  await request.json()
    #await wall.process_report
    #await wall.process_materials
    payload = {
        "data": {
            "slab": {
                "data": 
                slab
            }
        },        
        "report": {},
        "materials": []
    }
    try:
        return JSONResponse(payload)
    except Exception as e:
        return JSONResponse({"error": str(e)})
    finally: del(slab); del(payload)


