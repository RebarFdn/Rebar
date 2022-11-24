#tekla utilities library

import math
from dataclasses import dataclass
from typing import Optional

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


class RebarLib:
    rebarnotes:dict = {
      "m10": {
        "size": "#3",
        "insize": "3/8",
        "area": {
          "imperial": {"value": 0.11,"unit": "in2"},
          "metric": {"value": 7.0968e-5,"unit": "m2"}
        },
        "weight": {
          "imperial": {"value": 0.376, "unit": "lb/ft"},
          "metric": {"value": 0.55955, "unit": "kg/m"}
        },
        "diameter": {
          "imperial": {"value": 0.375, "unit": "in" },
          "metric": {"value": 0.009525, "unit": "m"}
        }
      },
      "m12": {
        "size": "#4",
        "insize": "1/2",
        "area": {
          "imperial": {"value": 0.20,"unit": "in2"},
          "metric": {"value": 0.000129032,"unit": "m2"}
        },
        "weight": {
          "imperial": {"value": 0.668, "unit": "lb/ft"},
          "metric": {"value": 0.9940935, "unit": "kg/m"}
        },
        "diameter": {
          "imperial": {"value": 0.500, "unit": "in" },
          "metric": {"value": 0.0127, "unit": "m"}
        },
      },
     
      "m16": {
        "size": "#5",
        "insize": "5/8",
        "area": {
          "imperial": {"value": 0.31,"unit": "in2"},
          "metric": {"value": 0.0002,"unit": "m2"}
        },
        "weight": {
          "imperial": {"value": 1.043, "unit": "lb/ft"},
          "metric": {"value": 1.552155, "unit": "kg/m"}
        },
        "diameter": {
          "imperial": {"value": 0.625, "unit": "in" },
          "metric": {"value": 0.015875, "unit": "m"}
        },
      },
      "m20": {
        "size": "#6",
        "insize": "3/4",
        "area": {
          "imperial": {"value": 0.44,"unit": "in2"},
          "metric": {"value": 0.00028387,"unit": "m2"}
        },
        "weight": {
          "imperial": {"value": 1.502, "unit": "lb/ft"},
          "metric": {"value": 2.2352222, "unit": "kg/m"}
        },
        "diameter": {
          "imperial": {"value": 0.750, "unit": "in" },
          "metric": {"value": 0.01905, "unit": "m"}
        },
      }
    }

    def convert_bar(self, bar:str=None):
          converter = {
              "m6": "1/4",
              "m10": "3/8",
              "m12": "1/2",
              "m16": "5/8",
              "m20": "3/4",
              "3/4": "m20",
              "5/8": "m16",
              "1/2": "m12",
              "3/8": "m10",
              "1/4": "m6"
          }
          return converter.get(bar, '1/2')


class CmuLib:
    cmulib:dict = {
        "100": {
                "type": "cmu-100",
                "cores": 2,
                "dimension":{
                  "thickness": 0.100,
                  "length": 0.400,
                  "height": 0.200,
                  "breadth": 0.100,
                  "unit": "m"

                }, 
                "area": {
                  "value": 0.08,
                  "unit": "m2"
                },               
                "weight": {
                  "imperial": { "value": 26, "unit": "lb" },
                  "metric": { "value": 14.5, "unit": "kg" }
                },
                "core_volume": {
                  "imperial": { "value": 0.0847552001, "unit": "ft3" },
                  "metric": { "value": 0.0024, "unit": "m3" }
                },
                "mortar": {
                  "imperial": { "value": 0, "unit": "ft3" },
                  "metric": { "value": 0, "unit": "m3" }
                }

            },
            "150": {
                "type": "cmu-150",
                "cores": 2,
                "dimension":{
                  "thickness": 0.150,
                  "length": 0.400,
                  "height": 0.200,
                  "breadth": 0.150,
                  "unit": "m"

                }, 
                "area": {
                  "value": 0.08,
                  "unit": "m2"
                },               
                "weight": {
                  "imperial": { "value": 32, "unit": "lb" },
                  "metric": { "value": 0, "unit": "kg" }
                },
                "core_volume": {
                  "imperial": { "value": 0.229545334, "unit": "lb" },
                  "metric": { "value": 0.0065, "unit": "m3" }
                },
                "mortar": {
                  "imperial": { "value": 0, "unit": "ft3" },
                  "metric": { "value": 0, "unit": "m3" }
                }

            },
            "200": {                
                "type": "cmu-200",
                "cores": 2,
                "dimension":{
                  "thickness": 0.200,
                  "length": 0.400,
                  "height": 0.200,
                  "breadth": 0.200,
                  "unit": "m"

                }, 
                "area": {
                  "value": 0.08,
                  "unit": "m2",
                },               
                "weight": {
                  "imperial": { "value": 38, "unit": "lb" },
                  "metric": { "value": 0, "unit": "kg" }
                },
                "core_volume": {
                  "imperial": { "value": 0.2966432, "unit": "ft3" },
                  "metric": { "value": 0.0084, "unit": "m3" }
                },
                "mortar": {
                  "imperial": { "value": 0, "unit": "ft3" },
                  "metric": { "value": 0, "unit": "m3" }
                }
                },
            "250": {
                "type": "cmu-250",
                "cores": 2,
                "dimension":{
                  "thickness": 0.250,
                  "length": 0.400,
                  "height": 0.200,
                  "breadth": 0.250,
                  "unit": "m"

                }, 
                "area": {
                  "value": 0.08,
                  "unit": "m2",
                },               
                "weight": {
                  "imperial": { "value": 49, "unit": "lb" },
                  "metric": { "value": 0, "unit": "kg" }
                },
                "core_volume": {
                  "imperial": { "value": 0.423776, "unit": "ft3" },
                  "metric": { "value": 0.012, "unit": "m3" }
                },
                "mortar": {
                  "imperial": { "value": 0, "unit": "ft3" },
                  "metric": { "value": 0, "unit": "m3" }
                }
                },
                "note": """General Cmu Notes"""
    }
    sheetrocklib:dict = {
            "75": {
                "type": "drywall-75",
                "thickness": 75,
                "sheetrock": {
                "vol": 1,
                "unit": "mm",
                "length": 2400,
                "bredth": 1200,
                "thickness": 15,
                "kg": 0,
                 "lb": 0,
                "layers": 1,
                "compound": 1.2,
                "screws": 36,
                "tape": 7200
                },
                "estimate":{}

            },
            "100": {
                "type": "drywall-100",
                "thickness": 100,
                "sheetrock": {
                "vol": 1,
                "unit": "mm",
                "length": 2400,
                "bredth": 1200,
                "thickness": 15,
                "kg": 0,
                 "lb": 0,
                "layers": 1,
                "compound": 1.2,
                "screws": 36,
                "tape": 7200
                },
                "estimate":{}

            },
            "150": {
                "type": "drywall-150",
                "thickness": 150,
                "sheetrock": {
                "vol": 1,
                "unit": "mm",
                "length": 2400,
                "bredth": 1200,
                "thickness": 15,
                "kg": 0,
                 "lb": 0,
                "layers": 1,
                "compound": 1.2,
                "screws": 36,
                "tape": 7200
                },
                "estimate":{}

            }
    }
    
    
    
    
    
    def set_unit_system(self, unit:str=None):
      if unit:
        usystem = {
          "m": {
            "length": "m",
            "area": "m2",
            "volume": "m3"
          },
          "ft": {
            "length": "ft",
            "area": "ft2",
            "volume": "ft3"
          }
          
        } 
        return usystem.get(unit)
      else:
        return None


class ConcreteLib:
  '''grades of concrete: M5, M 7.5, M10, M15, M20, and M 25.
    where M is mix and corresponding number is compressive strength after 28 days
  '''
  dry_volume__factor:float = 1.54
  cement_density:dict ={"value": 1440, "unit": "kg/m3"}  
  bag_weight:dict={"value": 42.5, "unit": "kg"}
  aggregate:dict = {
    "washed_sand": {
    "weight": {"unit": "kg/m3", "value": 1750}
    },
    "seived_sand": {
    "weight": {"unit": "kg/m3", "value": 1650}
    },
    "stone": {
    "weight": {"unit": "kg/m3", "value": 1600}
    },
  
  }
  concrete:dict = {
    "M25": {
      "mix_ratio": [1,1,2], 
      "water_cement_ratio": 0.5    
         
    
    },
    "M20": {
      "mix_ratio": [1,1.5,3],  
      "water_cement_ratio": 0.55    
    
    },
    "M15": {
      "mix_ratio": [1,2,4],  
      "water_cement_ratio": 0.6    
        
    
    },
    "M10": {
      "mix_ratio": [1,3,6],
      "water_cement_ratio": 0.65    
    
    },
    "M7.5": {
      "mix_ratio": [1,4,8], 
      "water_cement_ratio": 0.7    
         
    
    },
    "M5": {
      "mix_ratio": [1,5,10],
      "water_cement_ratio": 0.75    
          
    
    }
  }
