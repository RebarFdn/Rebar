
from starlette.responses import JSONResponse
from sledge.models.tasks import Task
from time import ctime


import math
from dataclasses import dataclass
from boq.modules.lib import RebarLib, ConcreteLib

@dataclass
class Measured:
    value: float = None
    unit: str = None

@dataclass
class Slab(RebarLib):
    width: dict
    length: dict   
    tag: str = None
    type: str = None
    unit:str = None  
    span_factor: int = 4  
    thickness: Measured = None
    rebars: dict = None
    openings: list = None
    formwork:dict = None
    ftm:float = 3.28084 # feet per meter
    
    

    @property
    def area(self):
        return { 
            "value": round((self.width.get('value') * self.length.get('value')),2),
            "unit": "m2"
        }
    
    @property
    def volume(self):
        return { 
            "value": round(self.thickness.get('value') * self.area.get('value'),3),
            "unit": "m3"
        }
    
    @property
    def perimeter(self):
        return {"value": math.fsum([self.width.get('value') * 2, self.length.get('value') * 2]),"unit": "m"}

    def opening_area(self):
        def calculate_area(item):
            return  round(
            (item.get('width').get('value') * item.get('length').get('value')) \
                * item.get('amt').get('value'),2)

        return {"unit": "m2", "value": sum(list(map(calculate_area, self.openings)))}

    
    
    

    
    def set_span(self):
        if self.length.get('value') > self.width.get('value'):
            self.main_span = self.width
            self.dist_span = self.length
        else:
            self.main_span = self.length
            self.dist_span = self.width 
        self.main_quarter = {"unit": "m", "value": round(self.main_span.get('value') / self.span_factor,2)}
        self.dist_quarter = {"unit": "m", "value": round(self.dist_span.get('value') / self.span_factor, 2)}   
    
    def process_rebars(self):
        if self.rebars:
            # process main bars
            self.rebars['b1']['cut_length']['value'] = round(self.main_span.get('value') + self.thickness.get('value'), 2)
            self.rebars['b1']['amt']['value']  = self.dist_span.get('value') / self.rebars.get('b1').get('spacing').get('value')
            self.rebars['b1']['weight']['value']  = \
                self.rebars.get('b1').get('cut_length').get('value') * self.rebarnotes.get(self.rebars['b1']['type']).get('weight')[self.unit].get('value')
            self.rebars['b1']['total_weight'] = \
                {"unit": "kg", "value": round(self.rebars['b1']['weight']['value'] * self.rebars['b1']['amt']['value'],3)}
            # process distribution bars
            self.rebars['b2']['cut_length']['value'] = round(self.dist_span.get('value') + self.thickness.get('value'),2)
            self.rebars['b2']['amt']['value']  = self.main_span.get('value') / self.rebars.get('b2').get('spacing').get('value')
            self.rebars['b2']['weight']['value']  = \
                self.rebars.get('b2').get('cut_length').get('value') * self.rebarnotes.get(self.rebars['b2']['type']).get('weight')[self.unit].get('value')
            self.rebars['b2']['total_weight'] = \
                {"unit": "kg", "value": round(self.rebars['b2']['weight']['value'] * self.rebars['b2']['amt']['value'],3)}

            # process top main bars
            self.rebars['t1']['cut_length']['value'] = round(self.main_quarter.get('value') + self.thickness.get('value'),2)
            self.rebars['t1']['amt']['value']  = round(((self.main_span.get('value') + self.dist_quarter.get('value')) * 2)/ self.rebars.get('t1').get('spacing').get('value'))
            self.rebars['t1']['weight']['value']  = \
                self.rebars.get('t1').get('cut_length').get('value') * self.rebarnotes.get(self.rebars['t1']['type']).get('weight')[self.unit].get('value')
            self.rebars['t1']['total_weight'] = \
                {"unit": "kg", "value": round(self.rebars['t1']['weight']['value'] * self.rebars['t1']['amt']['value'],3)}

            # process dist main bars
            self.rebars['t2']['cut_length']['value'] = round(self.dist_quarter.get('value'),2)

            self.rebars['t2']['amt']['value']  = round( (self.main_quarter.get('value')  * 4)/ self.rebars.get('t2').get('spacing').get('value'))
            
            self.rebars['t2']['weight']['value']  = \
                self.rebars.get('t2').get('cut_length').get('value') * self.rebarnotes.get(self.rebars['t2']['type']).get('weight')[self.unit].get('value')
            self.rebars['t2']['total_weight'] = \
                {"unit": "kg", "value": round(self.rebars['t2']['weight']['value'] * self.rebars['t2']['amt']['value'],3)}
            
            rebar_weights = [
            (self.rebars['b1']['type'],self.rebars['b1']['total_weight']['value'],),
            (self.rebars['b2']['type'],self.rebars['b2']['total_weight']['value']),
            (self.rebars['t1']['type'],self.rebars['t1']['total_weight']['value']),
            (self.rebars['t2']['type'],self.rebars['t2']['total_weight']['value'])
            ]            
            materials_list = [
                {
                "itemno":1, 
                "description": "Binding wire",
                "unit": "kg", 
                "amt":0 
                }
            
            ]
            def processbar_1():
                item = {
                "itemno":1, 
                "description": f"{ self.rebars['b1']['type'] } Mild Steel Bar",
                "unit": "kg", 
                "amt":0
                }
                for i in rebar_weights:
                    if i[0] == self.rebars['b1']['type']:
                        item["amt"] += i[1]
                        pass
                item["amt"] = round(item["amt"], 2)
                materials_list.append(item)
                
            def processbar_2():
                item = {
                "itemno":1, 
                "description": f"{ self.rebars['b1']['type'] } Mild Steel Bar",
                "unit": "kg", 
                "amt":0 
                }
                for i in rebar_weights:
                    if i[0] is not self.rebars['b1']['type']:
                        item["amt"] = 0 # flush
                        item["description"] = f"{i[0] } Mild Steel Bar"
                        item["amt"] += i[1]
                        pass
                item["amt"] = round(item["amt"], 2)
                materials_list.append(item)

            processbar_1()
            processbar_2()              
           
            
            try:
                def sort_list(item):
                    item['itemno'] = len(self.materials_list) + 1
                    self.materials_list.append(item)
                    return item

                list(map(sort_list, materials_list))            
                
            except Exception as e:
                return {"status": str(e)}
            finally: del(materials_list)

        else: 
            pass
    

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


    def process_formwork(self):
        if self.formwork:
            self.formwork['joist']["joist_span"] =  self.main_span # overall length of one joist
            self.formwork['wailer']["wail_span"] = self.dist_span # overall length of one wailer
            self.formwork["decking_area"] = self.area # total area of formwork coverage
            self.formwork["ply"] = { 
                    "sheet_area": {"unit": "m2", "value": round((4/3.24) * (8/3.24),2)}, # m2 area of standard 4ft x 8ft sheet of ply
                    "amt": {"unit": "sheet", "value": round( self.area.get('value')/ ((4/3.24) * (8/3.24)),2)} # sheets required
                }        
        else:
            self.formwork = {
                "joist": {
                    "type":"2x4", 
                    "spacing": {"value":0.6, "unit": "m"},
                    "joist_span": self.main_span,
                    "cut_length": {"value":0.0, "unit": "m"}, 
                    "weight": {"value":0.0, "unit": "kg"}, 
                    "amt": {"value":0.0, "unit": "each"}           
                },
                "wailer": {
                    "type":"2x4", 
                    "spacing": {"value":0.9, "unit": "m"},
                    "wail_span": self.dist_span,
                    "cut_length": {"value":0.0, "unit": "m"}, 
                    "weight": {"value":0.0, "unit": "kg"}, 
                    "amt": {"value":0.0, "unit": "each"}           
                }, 
                "decking_area": self.area,
                "ply": { 
                    "sheet_area": {"unit": "m2", "value": round((4/self.ftm) * (8/self.ftm),2)},
                    "amt": {"unit": "sheet", "value": round( self.area.get('value')/ ((4/self.ftm) * (8/self.ftm)),2)}
                }
            }

        self.formwork['joist']['amt']['value'] = round(self.formwork.get('wailer').get('wail_span').get('value') / self.formwork['joist'].get('spacing').get('value')) 
        self.formwork['wailer']['amt']['value'] = round(self.formwork.get('joist').get('joist_span').get('value') / self.formwork.get('wailer').get('spacing').get('value')) 
        
        
        def best_fit(l=None, spl=None, ftm=self.ftm): 
            metric_lumber = round(l/ftm,2)
            amount = round(spl / metric_lumber,2)
            required = round(spl // metric_lumber,2)

            if amount > required:
                required +=1

            waste =  round((required - amount) * metric_lumber,2)
            return {            
                "lumber_choice": f"{l}",
                "metric_length": metric_lumber,
                "amt_per_span": amount,
                "amt_required": required,            
                "span-distance": spl,
                "waste": waste,
            }
        
        def process_joists(span_length=0):
            def test_fit(splen):  

                fits = [10, 12, 14, 16, 18]
                test_samples = []

                for i in fits:
                    test_samples.append(best_fit(l=i, spl=splen))
                return test_samples

            def sample(x):
                return x['waste']

            samples = test_fit(span_length)
            waste_matter = list(map(sample , samples))
            choice = min(waste_matter)

            def choose(sample):
                if sample['waste'] == choice:
                    return sample
                return None

            chosen = list(filter(choose, samples))[0]
            self.formwork["joist"]["type"] = f'{self.formwork["joist"]["type"]} {chosen.get("lumber_choice")}'                    
            self.formwork['joist']['cut_length']['value'] = chosen.get('metric_length')
            self.formwork['joist']['lumber_amt'] = {
                "unit": "each", 
                "per_span": chosen.get('amt_required'),
                "total": self.formwork['joist']['amt']['value'] * chosen.get('amt_required') 
            }

        def process_wailers(span_length=0):
            ''' '''
            def test_fit(splen): 

                fits = [10, 12, 14, 16, 18]
                test_samples = []

                for i in fits:
                    test_samples.append(best_fit(l=i, spl=splen)) 

                return test_samples

            def sample(x):
                return x['waste']

            samples = test_fit(span_length)
            waste_matter = list(map(sample , samples))
            choice = min(waste_matter)

            def choose(sample):
                if sample['waste'] == choice:
                    return sample
                return None

            chosen = list(filter(choose, samples))[0]
            self.formwork["wailer"]["type"] = f'{self.formwork["wailer"]["type"]} {chosen.get("lumber_choice")}'                    
            self.formwork['wailer']['cut_length']['value'] = chosen.get('metric_length')
            self.formwork['wailer']['lumber_amt'] = {
                "unit": "each", 
                "per_span": chosen.get('amt_required'),
                "total": self.formwork['wailer']['amt']['value'] * chosen.get('amt_required') 
                }

        def process_backup(span_length=0):
            def test_fit(splen):  
                fits = [10, 12, 14, 16, 18]
                test_samples = []
                for i in fits:
                    test_samples.append(best_fit(l=i, spl=splen))
                return test_samples

            def sample(x):
                return x['waste']

            samples = test_fit(span_length)
            waste_matter = list(map(sample , samples))
            choice = min(waste_matter)

            def choose(sample):
                if sample['waste'] == choice:
                    return sample
                return None

            chosen = list(filter(choose, samples))[0]
            self.formwork["backup"] = {            
                "length": self.perimeter,
                "lumber": {
                    "type": f'2x6 {chosen.get("lumber_choice")}',
                    "metric_lenght": chosen.get('metric_length'),
                    "amt_required": chosen.get('amt_per_span'),
                    "amt": chosen.get('amt_required')            
                }
            }

        def processShores():
            wailers = self.formwork.get('wailer')
            props = round((wailers['wail_span']['value']/ wailers['spacing']['value']) * wailers['amt']['value'])
            try:
                self.formwork['shores'] = {
                "spacing": wailers['spacing'],
                "row_length": wailers['wail_span'],
                "rows": wailers['amt'],
                "amt": {"unit": "each", "value": props}
                }
            except Exception as e:
                return str(e)
            finally:
                del(wailers); del(props)
            
        def process_nails():
            self.formwork['nails'] = {
            "type": '2 inch (50mm) wire Nail',
            "per_ply": {
                "unit": "lb",
                "value": 0.13
            },
            }
            self.formwork['nails']['amt'] = {
                "unit": "lb",
                "value": round((self.formwork['nails']['per_ply']['value'] * self.formwork.get('ply').get('amt').get('value')),1)
                }
            
            pass


        jspan = self.formwork.get('joist').get('joist_span').get('value')
        wspan = self.formwork.get('wailer').get('wail_span').get('value')

        process_joists(jspan)
        process_wailers(wspan)
        processShores()
        process_backup(self.perimeter.get('value'))
        process_nails()
        #print(self.formwork['backup'])
        
        materials_list = [
        {"itemno":1, "description": "5/8 ( 16mm ) Form Ply","unit": "Sheets", "amt": self.formwork.get('ply').get('amt').get('value') },
        {"itemno":2, "description": f'{self.formwork["joist"]["type"]} WPP Lumber as joists',"unit": "Length", "amt":self.formwork['joist']['amt']['value'] },
        {"itemno":3, "description": f'{self.formwork["wailer"]["type"]} WPP Lumber as wailers',"unit": "Length", "amt":self.formwork['wailer']['lumber_amt']['total'] },
         {"itemno":4, "description": f'{self.formwork.get("backup").get("lumber").get("type")} WPP Lumber as backup board',"unit": "Length", "amt": self.formwork.get("backup").get("lumber").get("amt") },
        {"itemno":5, "description": f'{self.formwork["nails"]["type"]}',"unit": f'{self.formwork["nails"]["amt"]["unit"]}', "amt": self.formwork["nails"]["amt"]["value"] },
        {"itemno":6, "description": 'Adjustable Iron Shores',"unit": "each", "amt": self.formwork.get('shores').get('amt').get('value') }      
       
        ]

        try:
            def sort_list(item):
                item['itemno'] = len(self.materials_list) + 1
                self.materials_list.append(item)
                return item

            list(map(sort_list, materials_list))
            return None           
        except Exception as e:
            return {"status": str(e)}
        finally: del(materials_list)

    @property
    def todos(self):
        return [
            'process rebar splice',             
            'produce bill of quantities ',
        ]      
    

    def setup(self):
        self.materials_list:list = []
        self.set_span()
        self.process_rebars()
        self.concrete = self.process_concrete()
        self.process_formwork()
    
    @property 
    def slab(self):
        return {
            "data": { 
                "id": self.tag,
                "length": self.length,
                "width": self.width,
                "thickness": self.thickness,
                "perimeter": self.perimeter,
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


### ---------------------------------------------###

request_data = { 
    "tag": "GF01",
	"type": "M15",
	"unit": "metric",
    "span": 3,
    "width": {"value": 0, "unit":"m"},
    "length": {"value":0, "unit":"m"},
    "thickness": {"value":0, "unit":"m"},
    "rebars": {
        "b1": {
            "type":"m12", 
            "spacing": {"value":0.2, "unit": "m"},
            "cut_length": {"value":0.0, "unit": "m"}, 
            "weight": {"value":0.0, "unit": "kg"}, 
            "amt": {"value":0.0, "unit": "ea"}  

        },
        "b2": {
            "type":"m12", 
            "spacing": {"value":0.2, "unit": "m"},
            "cut_length": {"value":0.0, "unit": "m"}, 
            "weight": {"value":0.0, "unit": "kg"}, 
            "amt": {"value":0.0, "unit": "m"}           
        },
        "t1": {
            "type":"m12", 
            "spacing": {"value":0.15, "unit": "m"},
            "cut_length": {"value":0.0, "unit": "m"}, 
            "weight": {"value":0.0, "unit": "kg"}, 
            "amt": {"value":0.0, "unit": "m"}           
        },
        "t2": {
            "type":"m10", 
            "spacing": {"value":0.25, "unit": "m"},
            "cut_length": {"value":0.0, "unit": "m"}, 
            "weight": {"value":0.0, "unit": "kg"}, 
            "amt": {"value":0.0, "unit": "m"}           
        }
    },
    "openings": [{
                "tag": "Stairwell", 
                "width": {"value":0, "unit":"m"}, 
                "length": {"value":0, "unit":"m"}, 
                "amt": {"value":0, "unit":"each"}
            },],
    "formwork": {
        "joist": {
            "type":"2x4", 
            "spacing": {"value":0.6, "unit": "m"},
            "cut_length": {"value":0.0, "unit": "m"}, 
            "weight": {"value":0.0, "unit": "kg"}, 
            "amt": {"value":0.0, "unit": "each"}           
        },
        "wailer": {
            "type":"2x6", 
            "spacing": {"value":0.9, "unit": "m"},
            "cut_length": {"value":0.0, "unit": "m"}, 
            "weight": {"value":0.0, "unit": "kg"}, 
            "amt": {"value":0.0, "unit": "each"}           
        }

    }
}

async def processSlab(request):
    data = await request.json()
    s = Slab(
        tag = data.get('tag'),
        type = data.get('type'),
        unit = data.get('unit'),
        span_factor= data.get('span'),
        width=data.get('width'), 
        length=data.get('length'), 
        thickness=data.get('thickness'),
        rebars=data.get('rebars'),
        openings= data.get('openings'),
        formwork=data.get('formwork')            
    )
    try:
        s.setup()
        return JSONResponse(s.slab)
    except Exception as e:
        return JSONResponse({"status": str(e)})
    finally: del(data); del(s)
    


