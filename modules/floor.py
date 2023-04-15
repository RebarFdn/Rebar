
from time import ctime
from dataclasses import dataclass

from modules.rate import Rate
from modules.lib import RebarLib, ConcreteLib


@dataclass
class Floor(RebarLib):
    tag:str = None,
    type: str = None
    unit:str = None 
    span_factor: int = 3 
    width:dict = None,
    length:dict = None,      
    thickness:dict = None
    rebars: dict = None
    openings: list = None    
    ftm:float = 3.28084 # feet per meter

    def opening_area(self):
        def calculate_area(item):
            return  round(
            (item.get('width').get('value') * item.get('length').get('value')) \
                * item.get('amt').get('value'),2)

        return {"unit": "m2", "value": sum(list(map(calculate_area, self.openings)))}

    @property
    def area(self):
        return { 
            "unit": "m2",
            "value": round(((self.width.get('value') * self.length.get('value')) - self.opening_area().get('value')) ,2),
            
        }
    
    @property
    def volume(self):
        return { 
            "value": round(self.thickness.get('value') * self.area.get('value'),3),
            "unit": "m3"
        }

    @property
    def perimeter(self):
        return {"value": sum([self.width.get('value') * 2, self.length.get('value') * 2]),"unit": "m"}

    def process_reinforcement(self):
        if self.rebars:
            item =  {"itemno":0, "description": "JRC Fabric Reinforcement","unit": "sheets", "amt":0 }

            self.rebars['sheet'] = {
            "area": {"unit": "m2", "value": round((17/self.ftm)*(8/self.ftm),2)},
             }
            self.rebars['sheet']["amt"] =  {"unit": "each", "value": self.area.get('value') / self.rebars.get('sheet').get('area').get('value')}
            if self.rebars.get('top').get('type'):
                self.rebars['top']['amt'] = self.rebars.get('sheet').get('amt')
                item['amt'] += self.rebars.get('top',{}).get('amt',{}).get('value', 0)
            if self.rebars.get('bottom').get('type'):
                self.rebars['bottom']['amt'] = self.rebars.get('sheet').get('amt')
                item['amt'] += self.rebars.get('bottom',{}).get('amt',{}).get('value', 0)
            materials_list = [item ]
            try:
                def sort_list(item):
                    item['itemno'] = len(self.materials_list) + 1
                    self.materials_list.append(item)
                    return item
                list(map(sort_list, materials_list)) 
            
                return self.rebars
            except Exception as e:
                return {"status": str(e)}
            finally: del(item); del(materials_list)

        else: pass
       
       

    def process_concrete(self):
        v = self.volume
        data = {
            "cement_bag": ConcreteLib.bag_weight,
            "cement_density":  ConcreteLib.cement_density,
            "sand_density":  ConcreteLib.aggregate.get('washed_sand').get('weight') ,
            "stone_density":  ConcreteLib.aggregate.get('stone').get('weight'),
            "concrete_type": self.type,
            "wet_volume": self.volume,
            "dry_volume": self.volume,
            "mix_ratio": ConcreteLib.concrete.get(self.type).get('mix_ratio'),
            "water_cement_ratio": ConcreteLib.concrete.get(self.type).get('water_cement_ratio'),

        }
        data['dry_volume']['value'] = round( data['dry_volume']['value'] * ConcreteLib.dry_volume__factor, 3)
       
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



        

    def setup(self):
        self.materials_list:list = []
        #self.set_span()
        self.process_reinforcement()
        self.concrete = self.process_concrete()
        #self.process_formwork()


    @property
    def report(self):
        return {
         "data": { 
                "id": self.tag,
                "concrete_grade": self.type,
                "length": self.length,
                "width": self.width,
                "thickness": self.thickness,
                "perimeter": self.perimeter,
                "area": self.area,
                "volume": self.volume,
                "concrete": self.concrete,
                
                "rebars": self.rebars                
            },
            "materials_list": self.materials_list,
            "boq": {},
            "request_time": str(ctime())
        
        }


async def processFloor(request):
    data = await request.json()
    fl = Floor(
        tag = data.get('tag'),
        type = data.get('type'),
        unit = data.get('unit'),
        span_factor= data.get('span'),
        width=data.get('width'), 
        length=data.get('length'), 
        thickness=data.get('thickness'),
        rebars=data.get('rebars'),
        openings= data.get('openings'),
                    
    )
    try:
        fl.setup()
        return JSONResponse(fl.report)
    except Exception as e:
        return JSONResponse({"status": str(e)})
    finally: del(data); del(fl)
    

    

    
    
    