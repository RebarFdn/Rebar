#Tekla BQ Concrete Foundation Footing Module / Router
from time import ctime
from dataclasses import dataclass
from starlette.responses import JSONResponse

from sledge.models.tasks import Task
from boq.modules.lib import RebarLib, ConcreteLib



@dataclass
class StripFoundation(RebarLib):
    tag: str = None
    type: str = None
    cgrade:str = None
    length: dict = None
    width: dict = None
    thickness: dict = None   
    depth: dict = None      
    unit:str = None        
    rebars: dict = None   
    ftm:float = 3.28084 # feet per meter 

    @property
    def area(self):        
        return { 
            "value": round((self.width.get('value') * self.thickness.get('value') ),2),
            "unit": "m2"
        }   
    
    @property
    def volume(self):
        return { 
            "value": round(self.area.get('value') * self.length.get('value'),3),
            "unit": "m3"
        }

    def process_rebars(self):
        if self.rebars:
            if self.rebars.get('cover'):
                pass
            else: self.rebars['cover'] = {"unit":"m", "value": 0.025}
            
            #include toe bend
            self.rebars['bend'] = {"unit": "m", "value": 0.20} # toe bend
            # process main bars
            self.rebars['bottom']['cut_length'] = {"unit":"m", "value": round(self.length.get('value') + (self.rebars.get('bend').get('value') ), 2)}
            # single bar weight
            self.rebars['bottom']['weight'] = {"unit": "kg", "value":  round(self.rebars.get('bottom').get('cut_length').get('value') * self.rebarnotes.get(self.rebars['bottom']['type']).get('weight')[self.unit].get('value'),3)}
            # total weight
            self.rebars['bottom']['total_weight'] = \
                {"unit": "kg", "value": round(self.rebars['bottom']['weight']['value'] * self.rebars['bottom']['amt']['value'],3)}
            
            # process mid bars
            if self.rebars.get('mid').get('type'):
                self.rebars['mid']['cut_length'] = {"unit":"m", "value": round(self.length.get('value') + self.rebars.get('bend').get('value') , 2)}
                
                self.rebars['mid']['weight'] = {"unit": "kg", "value":  round(self.rebars.get('mid').get('cut_length').get('value') * self.rebarnotes.get(self.rebars['mid']['type']).get('weight')[self.unit].get('value'),3)}

                self.rebars['mid']['total_weight'] = \
                    {"unit": "kg", "value": round(self.rebars['mid']['weight']['value'] * self.rebars['mid']['amt']['value'],3)}
            else: pass

            # process top bars
            if self.rebars.get('top').get('type'):
                self.rebars['top']['cut_length'] = {"unit":"m", "value": round(self.length.get('value') + self.rebars.get('bend').get('value'), 2)}
                # single bar weight
                self.rebars['top']['weight'] = {"unit": "kg", "value":  round(self.rebars.get('top').get('cut_length').get('value') * self.rebarnotes.get(self.rebars['top']['type']).get('weight')[self.unit].get('value'),3)}
                # total weight
                self.rebars['top']['total_weight'] = \
                    {"unit": "kg", "value": round(self.rebars['top']['weight']['value'] * self.rebars['top']['amt']['value'],3)}
            else: pass

            # process stirrups            
            self.rebars['stirrup']['cover_length'] = {"unit": "m", "value": self.rebars.get('cover').get('value') * 4}
            self.rebars['stirrup']['cut_length'] = {"unit": "m", "value":round( self.girth.get('value') - self.rebars.get('stirrup').get('cover_length').get('value'),2)}

            self.rebars['stirrup']['weight'] =  {"unit": "kg", "value": round(self.rebars['stirrup']['cut_length']['value']* self.rebarnotes.get(self.rebars['stirrup']['type']).get('weight')[self.unit].get('value'),3)

            }
           
           
            ends_length =  self.main_quarter.get('value') * 2
            mid_length = self.length.get('value')- ends_length
            mid_amt = mid_length / self.rebars.get('stirrup').get('spacing').get('value')
            ends_amt = ends_length / self.rebars.get('stirrup').get('end_spacing').get('value')
            self.rebars['stirrup']['amt'] = {"unit": "each", "value": sum([round(mid_amt)+1,round(ends_amt)+1])}

            self.rebars['stirrup']['total_weight'] = {"unit": "kg", "value": round(self.rebars['stirrup']['weight']['value'] * self.rebars['stirrup']['amt']['value'],3)}


            rebar_weights = [
            (self.rebars['bottom']['type'],self.rebars['bottom']['total_weight']['value'],),
            (self.rebars['mid']['type'],self.rebars['mid']['total_weight']['value']),
            (self.rebars['top']['type'],self.rebars['top']['total_weight']['value'],),
            (self.rebars['stirrup']['type'],self.rebars['stirrup']['total_weight']['value'])            
            ]    

            self.rebars['rebar_weights'] = rebar_weights        
            materials_list = [
                {
                "itemno":1, 
                "description": "Binding wire",
                "unit": "kg", 
                "amt":0 
                }
            
            ]
            def process_bottom_bar():
                item = {
                "itemno":1, 
                "description": f"{ self.rebars['bottom']['type'] } Mild Steel Bar",
                "unit": "kg", 
                "amt":0
                }
                for i in rebar_weights:
                    if i[0] == self.rebars['bottom']['type']:
                        item["amt"] += i[1]
                        pass
                item["amt"] = round(item["amt"], 2)
                materials_list.append(item)

            def process_mid_bar():
                item = {
                "itemno":1, 
                "description": f"{ self.rebars['mid']['type'] } Mild Steel Bar",
                "unit": "kg", 
                "amt":0 
                }
                for i in rebar_weights:
                    if i[0] == self.rebars['mid']['type']:
                        item["amt"] += i[1]
                        pass
                item["amt"] = round(item["amt"], 2)
                materials_list.append(item)

            
            def process_top_bar():
                item = {
                "itemno":1, 
                "description": f"{ self.rebars['top']['type'] } Mild Steel Bar",
                "unit": "kg", 
                "amt":0 
                }
                for i in rebar_weights:
                    if i[0] == self.rebars['top']['type']:
                        item["amt"] += i[1]
                        pass
                item["amt"] = round(item["amt"], 2)
                materials_list.append(item)

            def process_stirrup_bar():
                item = {
                "itemno":1, 
                "description": f"{ self.rebars['stirrup']['type'] } Mild Steel Bar",
                "unit": "kg", 
                "amt":0 
                }
                for i in rebar_weights:
                    if i[0] == self.rebars['stirrup']['type']:
                        item["amt"] += i[1]
                        pass
                item["amt"] = round(item["amt"], 2)
                materials_list.append(item)
            
            process_bottom_bar()
            if self.rebars.get('mid').get('type'):
                process_mid_bar()
            else: pass
            if self.rebars.get('top').get('type'):
                process_top_bar()
            else: pass
            process_stirrup_bar()

            try:
                def sort_list(item):
                    item['itemno'] = len(self.materials_list) + 1
                    self.materials_list.append(item)
                    return item

                list(map(sort_list, materials_list))            
                
            except Exception as e:
                return {"status": str(e)}
            finally: del(materials_list)


    def process_concrete(self):
        data  = {
            "cement_bag": ConcreteLib.bag_weight,
            "cement_density":  ConcreteLib.cement_density,
            "sand_density":  ConcreteLib.aggregate.get('washed_sand').get('weight') ,
            "stone_density":  ConcreteLib.aggregate.get('stone').get('weight'),
            "concrete_type": self.cgrade,
            "wet_volume": self.volume,
            "dry_volume": {"unit": "m3", "value": round(self.volume.get('value') * ConcreteLib.dry_volume__factor,3)},
            "mix_ratio": ConcreteLib.concrete.get(self.cgrade).get('mix_ratio'),
            "water_cement_ratio": ConcreteLib.concrete.get(self.cgrade).get('water_cement_ratio'),
        
        }

        data['total_proportion'] = sum(data.get('mix_ratio'))
        data['cement_proportion'] = round(data.get('mix_ratio')[0] / data['total_proportion'],3)
        data['sand_proportion'] = round(data.get('mix_ratio')[1] / data['total_proportion'],3)
        data['stone_proportion'] = round(data.get('mix_ratio')[2] / data['total_proportion'],3)
        data['cement_volume'] = {"unit":"m3", "value": round(data.get('cement_proportion') * data.get('dry_volume').get('value'),3) }
        data['sand_volume'] = {"unit":"m3", "value": round(data.get('sand_proportion') * data.get('dry_volume').get('value'),3) }
        data['stone_volume'] = {"unit":"m3", "value": round(data.get('stone_proportion') * data.get('dry_volume').get('value'),3) }
        data['cement_weight'] = {"unit":"kg", "value": round(data.get('cement_volume').get('value') * data.get('cement_density').get('value'),3)
        }

        data['sand_weight'] = {"unit":"kg", "value": round(data.get('sand_volume').get('value') * data.get('sand_density').get('value'),3)
        }
        data['stone_weight'] = {"unit":"kg", "value": round(data.get('stone_volume').get('value') * data.get('stone_density').get('value'),3)
        }
        data['water_volume'] = {"unit":"litre", "value": round(data.get('cement_weight').get('value') * data.get("water_cement_ratio"),3)
        }
        data['bags_cement'] ={"unit": "bags", "value": round(data['cement_weight'].get('value') / data['cement_bag'].get('value'),2)}

        materials_list = [
        {"itemno":0, "description": "Portland Cement","unit": "Bags", "amt":data['bags_cement'].get('value') },
        {"itemno":0, "description": "Washed Sand (Fine Agg.)","unit": "Ton", "amt":data['sand_weight'].get('value')/1000 },
        {"itemno":0, "description": "Crushed Stone (Course Agg.)","unit": "Ton", "amt":data['stone_weight'].get('value')/1000 },       
        {"itemno":0, "description": "Water", "unit": "litre", "amt":data.get('water_volume').get('value') },
        ]
        self.concrete = data
        try:
            def sort_list(item):
                item['itemno'] = len(self.materials_list) + 1
                self.materials_list.append(item)
                return item
            list(map(sort_list, materials_list)) 
           
            return data
        except Exception as e:
            return {"status": str(e)}
        finally: del(data); del(materials_list)

    def process_excavation(self):
        self.excavation = {}
        


    @property
    def rate_index(self):  
           
        return {
            "excavation":{
                "backfill": "BT78225",
                "asphalt": "EA0976",
                "compact_marl": "EA0977",
                "compact_sand": "EA0978",
                "stiff_clay": "EA0979",
                "rock_concrete_man": "ER0980",
                "rock_concrete_comp": "ER0981",
                "by_length": "ES9900",
                
            },
            "concrete": {
            "man_mix": "CC39000",
            },
            "steelwork": {
                "m10": "MS0001",
                "m12": "MS0002",
                "m16": "MS0003",
                "m19": "MS0004",
                "m25": "MS0005",
                "stirrup": {
                    "m6": "MS0007",
                    "m10": "MS0008",
                    "m10_lg": "MS0009",
                    "m12": "MS0010",
                    "m12_lg": "MS0011",
                
                },
                "links": {
                    "m6": "MS0012",
                    "m10": "MS0013",                   
                    "m12": "MS0014",
                
                },
                 "chairs": {                    
                    "m10": "MS0015",                   
                    "m12": "MS0016",
                
                }
            
            }
        }


    def setup(self):
        self.materials_list:list = []
        #self.process_rebars()
        self.process_concrete()
        self.process_excavation()
        

    @property
    async def generate_report(self):         
        
        self.report = {
            "title": f"Structural Engineering Report for Building Foundation {self.tag}",
            "type": self.type,
            "tag": self.tag,
            "data": {
                "id": self.tag,
                "unit": self.unit,
                "depth": self.depth,
                "width": self.width,
                "thickness": self.thickness,
                "length": self.length,                
                "area": self.area,
                "volume": self.volume,
                "concrete": self.concrete,               
                #"rebars": self.rebars                
            },
            "materials_list": self.materials_list,
            "boq": {},
            "request_time": str(ctime())
        }   



@dataclass
class PadFoundation(RebarLib):
    tag: str = None
    type: str = None
    cgrade:str = None
    length: dict = None
    width: dict = None
    thickness: dict = None   
    depth: dict = None      
    unit:str = None        
    rebars: dict = None    
   
    ftm:float = 3.28084 # feet per meter 

    def setup(self):
        self.materials_list:list = []
        #self.process_rebars()
        #self.process_concrete()
        #self.process_formwork()

    @property
    async def generate_report(self):         
        
        self.report = {
            "title": f"Structural Engineering Report for Building Foundation {self.tag}",
            "type": self.type,
            "tag": self.tag,
            "data": {
                "id": self.tag,
                "unit": self.unit,
                "depth": self.depth,
                "width": self.width,
                "thickness": self.thickness,
                "length": self.length,                
                "area": self.area,
                "volume": self.volume,
               # "concrete": self.concrete,               
                #"rebars": self.rebars                
            },
            "materials_list": self.materials_list,
            "boq": {},
            "request_time": str(ctime())
        }   


   

async def processFoundation(request):
    data = await request.json()
    if data:
        if data.get('type') == 'strip':
            fdn = StripFoundation(
                tag = data.get('tag'),
                type = data.get('type'),
                unit = data.get('unit'),
                cgrade = data.get('cgrade'),                
                width=data.get('width'), 
                depth=data.get('depth'), 
                thickness=data.get('thickness'), 
                length=data.get('length'),
                rebars=data.get('rebars')

            ) 
        elif data.get('type') == 'pad':
            fdn = PadFoundation(
                tag = data.get('tag'),
                type = data.get('type'),
                unit = data.get('unit'),
                cgrade = data.get('cgrade'),               
                length=data.get('length'), 
                thickness=data.get('thickness'), 
                depth=data.get('depth'), 
                width=data.get('width'),
                rebars=data.get('rebars'),       
                

            )
        
        try:
            fdn.setup()
            await fdn.generate_report
            return JSONResponse( fdn.report )  
        except Exception as e:
            return JSONResponse({"status": str(e)})
        finally: del(data); del(fdn)
     
           
     
  