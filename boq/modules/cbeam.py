#Tekla BQ Concrete Beam Module / Router

import math
from time import ctime
from dataclasses import dataclass
from starlette.responses import JSONResponse

from sledge.models.tasks import Task
from boq.modules.lib import RebarLib, ConcreteLib


@dataclass
class Beam(RebarLib):
    tag: str = None
    type: str = None
    cgrade:str = None
    length: dict = None
    bredth: dict = None
    depth: dict = None      
    unit:str = None  
    span_factor: int = 3     
    rebars: dict = None    
    formwork:dict = None
    ftm:float = 3.28084 # feet per meter    


    @property
    def girth(self):        
        return { 
            "value": round((self.depth.get('value') *2) +  (self.bredth.get('value') ),2),
            "unit": "m"
        }
    @property
    def area(self):        
        return { 
            "value": round((self.depth.get('value') * self.bredth.get('value') ),2),
            "unit": "m2"
        }   
    
    @property
    def volume(self):
        return { 
            "value": round(self.area.get('value') * self.length.get('value'),3),
            "unit": "m3"
        }

    def set_beam_span(self):        
        self.main_quarter = {"unit": "m", "value": round(self.length.get('value') / self.span_factor,2)}

    def process_rebars(self):
        if self.rebars:
            if self.rebars.get('cover'):
                pass
            else: self.rebars['cover'] = {"unit":"m", "value": 0.025}
            self.set_beam_span() # beam oversupported span
            #include toe bend
            self.rebars['bend'] = {"unit": "m", "value": 0.20} # toe bend
            # process main bars
            self.rebars['bottom']['cut_length'] = {"unit":"m", "value": round(self.length.get('value') + (self.rebars.get('bend').get('value') + 2), 2)}
            # single bar weight
            self.rebars['bottom']['weight'] = {"unit": "kg", "value":  round(self.rebars.get('bottom').get('cut_length').get('value') * self.rebarnotes.get(self.rebars['bottom']['type']).get('weight')[self.unit].get('value'),3)}
            # total weight
            self.rebars['bottom']['total_weight'] = \
                {"unit": "kg", "value": round(self.rebars['bottom']['weight']['value'] * self.rebars['bottom']['amt']['value'],3)}
            
            # process mid bars
            self.rebars['mid']['cut_length'] = {"unit":"m", "value": round(self.length.get('value') , 2)}
            
            self.rebars['mid']['weight'] = {"unit": "kg", "value":  round(self.rebars.get('mid').get('cut_length').get('value') * self.rebarnotes.get(self.rebars['mid']['type']).get('weight')[self.unit].get('value'),3)}

            self.rebars['mid']['total_weight'] = \
                {"unit": "kg", "value": round(self.rebars['mid']['weight']['value'] * self.rebars['mid']['amt']['value'],3)}

            # process top bars
            self.rebars['top']['cut_length'] = {"unit":"m", "value": round(self.length.get('value') + (self.rebars.get('bend').get('value') + 2), 2)}
            # single bar weight
            self.rebars['top']['weight'] = {"unit": "kg", "value":  round(self.rebars.get('top').get('cut_length').get('value') * self.rebarnotes.get(self.rebars['top']['type']).get('weight')[self.unit].get('value'),3)}
            # total weight
            self.rebars['top']['total_weight'] = \
                {"unit": "kg", "value": round(self.rebars['top']['weight']['value'] * self.rebars['top']['amt']['value'],3)}

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
            process_mid_bar()
            process_top_bar()
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

    def process_formwork(self):
        if self.formwork:
            self.formwork['ply'] = {
                    "sheet_area": {"unit": "m2", "value": round((4/3.24) * (8/3.24),2)}, # m2 area of standard 4ft x 8ft sheet of ply
                    "amt": {"unit": "sheet", "value": round( self.area.get('value')/ ((4/3.24) * (8/3.24)),2)} # sheets required
            }
        else:
            self.formwork = { 
            "ply": {
                    "sheet_area": {"unit": "m2", "value": round((4/3.24) * (8/3.24),2)}, # m2 area of standard 4ft x 8ft sheet of ply
                    "amt": {"unit": "sheet", "value": round( self.area.get('value')/ ((4/3.24) * (8/3.24)),2)} # sheets required
                }
            }
        def cut_in(w):
            return round(( 4 / 3.24084 ) / w, 3) # width of sheet of ply

        cuts = [cut_in(2), cut_in(3), cut_in(4), cut_in(1)]

        side={
            "amt": {"unit": "each", "value": 2},
            "width": self.depth,
            "area": {
                "unit": "m2", 
                "value": round((self.depth.get('value') + 0.15  ) * self.length.get('value'),2),
                "total": {"unit": "m2", "value": 2}
            },
            "frame":self.formwork.get("frame")       
        }
        side['area']['total']['value'] = side.get('amt').get('value') * side.get('area').get('value') 
        
        bulk_edge={
            "amt": {"unit": "each", "value": 2},
            "width": self.bredth,
            "area": {
                "unit": "m2", 
                "value": round(self.bredth.get('value') * self.length.get('value'),2),
                "total": {"unit": "m2", "value": 2}
            },
            "frame":self.formwork.get("frame"),   
            "nail": {}  

        }
        bulk_edge['area']['total']['value'] = bulk_edge.get('amt').get('value') * bulk_edge.get('area').get('value') 

        self.formwork['area'] = {"unit": "m2", "value": bulk_edge['area']['total']['value'] + side['area']['total']['value'], 
        }
        self.formwork['area']['material'] = {"unit": "m2", "value":
            self.formwork.get('area').get('value') * 1.
        }
       
        
        self.formwork['ply']['cut_widths']= cuts
        self.formwork['side'] = side
        self.formwork['bulk'] = bulk_edge
         


        '''materials_list = [
        {"itemno":1, "description": "5/8 ( 16mm ) Form Ply","unit": "Sheets", "amt": self.formwork.get('ply').get('amt').get('value') },
        {"itemno":2, "description": f'{self.formwork["joist"]["type"]} WPP Lumber as joists',"unit": "Length", "amt":self.formwork['joist']['amt']['value'] },
         {"itemno":5, "description": f'{self.formwork["nails"]["type"]}',"unit": f'{self.formwork["nails"]["amt"]["unit"]}', "amt": self.formwork["nails"]["amt"]["value"] },
        
        ]'''
        
        
    def setup(self):
        self.materials_list:list = []
        self.process_rebars()
        self.process_concrete()
        self.process_formwork()

    @property
    async def generate_report(self):   
         
        
        self.report = {
            "title": f"Structural Engineering Report for Building column {self.tag}",
            "column_type": self.type,
            "tag": self.tag,
            "data": {
                "id": self.tag,
                "unit": self.unit,
                "depth": self.depth,
                "bredth": self.bredth,
                "length": self.length,                
                "girth": self.girth,
                "area": self.area,
                "volume": self.volume,
                "concrete": self.concrete,
                "formwork": self.formwork,
                "rebars": self.rebars                
            },
            "materials_list": self.materials_list,
            "boq": {},
            "request_time": str(ctime())
        }   


async def ProcessBeam(data:dict=None):
    if data:
        b = Beam(
        tag = data.get('tag'),
        type = data.get('type'),
        unit = data.get('unit'),
        cgrade = data.get('cgrade'),
        span_factor= data.get('span'),
        bredth=data.get('bredth'), 
        depth=data.get('depth'), 
        length=data.get('length'),
        rebars=data.get('rebars'),       
        formwork=data.get('formwork')

        )  
        b.setup()
        await b.generate_report
        return b.report   
           
     
  