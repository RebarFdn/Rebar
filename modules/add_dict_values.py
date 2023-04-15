
source_list= [
{"itemno":1,"description": f"Mild Steel Bar", "unit": "kg", "amt":0},
{"itemno":2, "description": "Portland Cement","unit": "Bags", "amt":20 },
{"itemno":3, "description": "Washed Sand (Fine Agg.)","unit": "Ton", "amt":563.5 },
{"itemno":4, "description": "Crushed Stone (Course Agg.)","unit": "Ton", "amt":1200.23 },       
{"itemno":5, "description": "Water", "unit": "litre", "amt":200 },
]

supply_list= [
{"itemno":1,"description": f"Mild Steel Bar", "unit": "kg", "amt":150},
{"itemno":2, "description": "Portland Cement","unit": "Bags", "amt":117 },
{"itemno":3, "description": "Washed Sand (Fine Agg.)","unit": "Ton", "amt":163.5 },
{"itemno":4, "description": "Crushed Stone (Course Agg.)","unit": "Ton", "amt":2100.23 },       
{"itemno":5, "description": "Water", "unit": "litre", "amt":300 },
]
 

def update_material_list(source_list:list=None, supply_list:list=None):

    def add_items(item:str=None, source:dict=None, supply:dict=None):      
        if supply.get("description") == item:
            for key in source:       
                if key == "amt":
                    source[key] = source.get(key, 0) + supply.get(key,0) 
            return source
        else:
            return source

    for item in source_list:    
        source_list[ source_list.index(item)] = add_items(item=item.get("description", ""), source=item, supply=supply_list[ source_list.index(item)])

update_material_list(source_list= source_list, supply_list=supply_list)


