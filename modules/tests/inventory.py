# testing create, add item, remove item, delete inventory
null = None

project = dict(
    inventory =  [
        {
        "id": "CEM515",
        "item": "Cement",
        "unit": "Bags",
        "instock": 124,
        "usage": [
            {
            "date": "",
            "amt": 10
            }
        ],
        "restock": [
            {
            "date": "",
            "amt": 10
            }
        ],
        "updated": 0
        }
    ],
    invoices = [
        {
          "supplier": {
            "_id": "000230693",
            "name": "C.A. PARCHMENT & SON LTD.",
            "taxid": "000230693"
          },
          "invoiceno": "858161",
          "datetime": "2022-07-14",
          "items": [
            {
              "itemno": "1",
              "description": "CONDUIT 2\"  50mm",
              "quantity": "3",
              "unit": "length",
              "price": "1269"
            },
            {
              "itemno": 2,
              "description": "BEND 2\" 50mm ELECTRICAL",
              "quantity": "1",
              "unit": "each",
              "price": "490"
            },
            {
              "itemno": 3,
              "description": "COUPLING  2\" 50mm Electrical",
              "quantity": "1",
              "unit": "each",
              "price": "84"
            }
          ],
          "tax": "657",
          "total": "5037"
        },
        {
          "supplier": {
            "_id": "000002313",
            "name": "NATIONAL SUPPLY CO. LTD.",
            "taxid": "000002313"
          },
          "invoiceno": "146788",
          "datetime": "2022-10-06",
          "items": [
            {
              "itemno": "1",
              "description": "DW5962/CM9002 1-1/8 HEX COLD CHISEL 20IN",
              "quantity": "1",
              "unit": "each",
              "price": "6960"
            }
          ],
          "tax": 1044,
          "total": 8004
        },
        {
          "supplier": {
            "_id": "001992058",
            "name": "MERVIN WILLIAMS HARDWARE",
            "taxid": "001992058"
          },
          "invoiceno": "17097",
          "datetime": "2022-05-25",
          "items": [
            {
              "itemno": "1",
              "description": "Portland Cement",
              "quantity": "40",
              "unit": "bags",
              "price": "1370"
            },
            {
              "itemno": 2,
              "description": "Toilet wax gasket",
              "quantity": "1",
              "unit": "each",
              "price": "350"
            },
            {
              "itemno": 3,
              "description": "SAN BEND 90 DEG 4in",
              "quantity": "4",
              "unit": "each",
              "price": "550"
            },
            {
              "itemno": 4,
              "description": "ELBOW 1/2 in",
              "quantity": "4",
              "unit": "each",
              "price": "50"
            },
            {
              "itemno": 5,
              "description": "PVC COUPLING 1/2in",
              "quantity": "3",
              "unit": "each",
              "price": "30"
            },
            {
              "itemno": 6,
              "description": "SCREW ROOF W/GRIP 2 1/2 in",
              "quantity": "4",
              "unit": "each",
              "price": "20"
            },
            {
              "itemno": 7,
              "description": "DELIVERY",
              "quantity": "1",
              "unit": "each",
              "price": "2000"
            }
          ],
          "tax": 8958,
          "total": 68678
        },
        {
          "supplier": {
            "_id": "001992058",
            "name": "MERVIN WILLIAMS HARDWARE",
            "taxid": "001992058"
          },
          "invoiceno": "18765",
          "datetime": "2022-07-25",
          "items": [
            {
              "itemno": "1",
              "description": "STEEL COR 3/8",
              "quantity": "180",
              "unit": "length",
              "price": "899.99"
            },
            {
              "itemno": 2,
              "description": "BINDING WIRE",
              "quantity": "2",
              "unit": "roll",
              "price": "9300.00"
            },
            {
              "itemno": 3,
              "description": "2x4x16 WPP LUMBER",
              "quantity": "20",
              "unit": "length",
              "price": "3400"
            },
            {
              "itemno": 4,
              "description": "2x6x14 WPP LUMBER",
              "quantity": "10",
              "unit": "length",
              "price": "4000"
            },
            {
              "itemno": 5,
              "description": "FORM PLY 5/8",
              "quantity": "15",
              "unit": "sheet",
              "price": "5300"
            },
            {
              "itemno": 6,
              "description": "CEMENT",
              "quantity": "200",
              "unit": "bag",
              "price": "1370"
            },
            {
              "itemno": 7,
              "description": "PVC DRAIN PIPE 2in 51mm",
              "quantity": "20",
              "unit": "length",
              "price": "1700"
            },
            {
              "itemno": 8,
              "description": "PVC PIPE 3/4in 25mm",
              "quantity": "6",
              "unit": "length",
              "price": "1250"
            },
            {
              "itemno": 9,
              "description": "CPVC PIPE 3/4in",
              "quantity": "6",
              "unit": "length",
              "price": "1300"
            },
            {
              "itemno": 10,
              "description": "PVC PIPE 1/2in 20mm",
              "quantity": "6",
              "unit": "length",
              "price": "900"
            },
            {
              "itemno": 11,
              "description": "DELIVERY",
              "quantity": "1",
              "unit": "each",
              "price": "4000"
            }
          ],
          "tax": 105120,
          "total": 805920
        },
        {
          "supplier": {
            "_id": "000002313",
            "name": "NATIONAL SUPPLY CO. LTD.",
            "taxid": "000002313"
          },
          "invoiceno": "124110",
          "datetime": "2022-06-01",
          "items": [
            {
              "itemno": "1",
              "description": "DW5962/CM9002 1-1/8 HEX COLD CHISEL 20IN",
              "quantity": "1",
              "unit": "Each",
              "price": "6960.00"
            }
          ],
          "tax": 1044,
          "total": 8004
        },
        {
          "supplier": {
            "_id": "000053457",
            "name": "STEWARTS HARDWARE LTD Old Harbour",
            "taxid": "000053457"
          },
          "invoiceno": "OHSP400060658",
          "datetime": "2022-07-25",
          "items": [
            {
              "itemno": "1",
              "description": "ELE 10063 FLUSH BOX 12 GANG METAL",
              "quantity": "6",
              "unit": "each",
              "price": "258.29"
            },
            {
              "itemno": 2,
              "description": "PLB BEND 2\" 90 DEG.PVC ",
              "quantity": "12",
              "unit": "each",
              "price": "156"
            }
          ],
          "tax": 513.26,
          "total": 3935
        },
        {
          "supplier": {
            "_id": "001992058",
            "name": "MERVIN WILLIAMS HARDWARE LTD.",
            "taxid": "001992058"
          },
          "invoiceno": "16466",
          "datetime": "2022-05-05",
          "items": [
            {
              "itemno": "1",
              "description": "2x6x14 WPP LUMBER",
              "quantity": "40",
              "unit": "length",
              "price": "3610.0"
            },
            {
              "itemno": 2,
              "description": "- 5% OR $7,600.00",
              "quantity": "1",
              "unit": "each",
              "price": "07600.0"
            },
            {
              "itemno": 3,
              "description": "DELIVERY",
              "quantity": "1",
              "unit": "each",
              "price": "1750"
            }
          ],
          "tax": 21922.5,
          "total": 168072.5
        },
        {
          "supplier": {
            "_id": "x0010010000",
            "name": "Temple Trucking Ltd",
            "taxid": "x0010010000",
            "address": {
              "town": "Mandeville",
              "city_parish": "Manchester"
            },
            "contact": {
              "tel": "876-574-2277",
              "mobile": "876-501-7128",
              "email": null,
              "watsapp": null
            }
          },
          "invoiceno": "109877",
          "date": "2023-02-21",
          "items": [
            {
              "itemno": "1",
              "description": "Washed Sand",
              "quantity": "30",
              "unit": "Yd3",
              "price": "2600"
            },
            {
              "itemno": 2,
              "description": "Trucking from May pen to Elgin",
              "quantity": "1",
              "unit": "Trip",
              "price": "106000.00"
            }
          ],
          "tax": 12870,
          "total": 196870
        },
        {
          "supplier": {
            "_id": "x0010010000",
            "name": "Temple Trucking Ltd",
            "taxid": "x0010010000",
            "address": {
              "town": "Mandeville",
              "city_parish": "Manchester"
            },
            "contact": {
              "tel": "876-574-2277",
              "mobile": "876-501-7128",
              "email": null,
              "watsapp": null
            }
          },
          "invoiceno": "109877",
          "date": "2023-02-21",
          "items": [
            {
              "itemno": "1",
              "description": "Washed Sand",
              "quantity": "30",
              "unit": "Yd3",
              "price": "2600"
            },
            {
              "itemno": 2,
              "description": "Trucking from May pen to Elgin",
              "quantity": "1",
              "unit": "Trip",
              "price": "106000.00"
            }
          ],
          "tax": 12870,
          "total": 196870
        },
        {
          "supplier": {
            "_id": "001992058",
            "name": "MERVIN WILLIAMS HARDWARE LTD.",
            "taxid": "001992058",
            "address": {
              "town": "Munro College P.O.",
              "city_parish": "St. Elizabeth"
            },
            "contact": {
              "tel": "876-433-1662",
              "mobile": "",
              "email": "mwilliamshardware@gmail.com"
            }
          },
          "invoiceno": "24406",
          "date": "2023-02-22",
          "items": [
            {
              "itemno": "1",
              "description": "1/4 lb Cord Line",
              "quantity": "1",
              "unit": "Each",
              "price": "400.00"
            }
          ],
          "tax": 60,
          "total": 460
        },
        {
          "supplier": {
            "_id": "000053457",
            "name": "STEWARTS HARDWARE LTD Old Harbour",
            "taxid": "000053457",
            "address": {
              "town": "Old Harbour",
              "city_parish": "St. Catherine"
            },
            "contact": {
              "tel": "876-745-2844",
              "mobile": "876-796-1086",
              "email": null
            }
          },
          "invoiceno": "OHSP200066933",
          "date": "2023-02-16",
          "items": [
            {
              "itemno": "1",
              "description": "Asphalt Blockmastic",
              "quantity": "30",
              "unit": "lb",
              "price": "148.60"
            }
          ],
          "tax": 669.6,
          "total": 5133.6
        },
        {
          "supplier": {
            "_id": "xx120000200",
            "name": "Ultra Value Hardware & Roofing",
            "taxid": "xx120000200",
            "address": {
              "town": "Malvern",
              "city_parish": "St. Elizabeth"
            },
            "contact": {
              "tel": "876-335-0682",
              "mobile": "876-882-5612",
              "email": "sale@uvhardware.com",
              "watsapp": null
            }
          },
          "invoiceno": "0575",
          "date": "2023-02-18",
          "items": [
            {
              "itemno": "1",
              "description": "4 in Paint Brush",
              "quantity": "1",
              "unit": "Each",
              "price": "985.00"
            }
          ],
          "tax": null,
          "total": 985
        },
        {
          "supplier": {
            "_id": "001992058",
            "name": "MERVIN WILLIAMS HARDWARE LTD.",
            "taxid": "001992058",
            "address": {
              "town": "Munro College P.O.",
              "city_parish": "St. Elizabeth"
            },
            "contact": {
              "tel": "876-433-1662",
              "mobile": "",
              "email": "mwilliamshardware@gmail.com"
            }
          },
          "invoiceno": "18205",
          "date": "2022-07-04",
          "items": [
            {
              "itemno": "1",
              "description": "CEMENT",
              "quantity": "50",
              "unit": "Bags",
              "price": "1370"
            },
            {
              "itemno": 2,
              "description": "2x4x16 LUMBER",
              "quantity": "20",
              "unit": "Length",
              "price": "3900"
            },
            {
              "itemno": 3,
              "description": "1x3x16 LUMBER",
              "quantity": "20",
              "unit": "Length",
              "price": "1350"
            },
            {
              "itemno": 4,
              "description": "2 1/2 in CONCRETE NAIL",
              "quantity": "25",
              "unit": "lb",
              "price": "300"
            },
            {
              "itemno": 5,
              "description": "DELIVERY",
              "quantity": "1",
              "unit": "Trip",
              "price": "1500"
            }
          ],
          "tax": 26625,
          "total": 204125
        },
        {
          "supplier": {
            "_id": "001992058",
            "name": "MERVIN WILLIAMS HARDWARE LTD.",
            "taxid": "001992058",
            "address": {
              "town": "Munro College P.O.",
              "city_parish": "St. Elizabeth"
            },
            "contact": {
              "tel": "876-433-1662",
              "mobile": "",
              "email": "mwilliamshardware@gmail.com"
            }
          },
          "invoiceno": "17875",
          "date": "2022-05-23",
          "items": [
            {
              "itemno": "1",
              "description": "1x3x16 LUMBER",
              "quantity": "30",
              "unit": "Length",
              "price": "1282.50"
            },
            {
              "itemno": 2,
              "description": "5/8 FORM PLY",
              "quantity": "30",
              "unit": "Sheets",
              "price": "5500"
            },
            {
              "itemno": 3,
              "description": "DELIVERY",
              "quantity": "1",
              "unit": "Trip",
              "price": "1500"
            }
          ],
          "tax": 30746.25,
          "total": 235721.25
        },
        {
          "supplier": {
            "_id": "001992058",
            "name": "MERVIN WILLIAMS HARDWARE LTD.",
            "taxid": "001992058",
            "address": {
              "town": "Munro College P.O.",
              "city_parish": "St. Elizabeth"
            },
            "contact": {
              "tel": "876-433-1662",
              "mobile": "",
              "email": "mwilliamshardware@gmail.com"
            }
          },
          "invoiceno": "17685",
          "date": "2022-06-22",
          "items": [
            {
              "itemno": "1",
              "description": "1/2 IN STEEL",
              "quantity": "250",
              "unit": "Length",
              "price": "1390"
            },
            {
              "itemno": 2,
              "description": "BINDING WIRE",
              "quantity": "1",
              "unit": "Roll",
              "price": "10000"
            },
            {
              "itemno": 3,
              "description": "2x4x16 LUMBER",
              "quantity": "20",
              "unit": "Length",
              "price": "3467.5"
            },
            {
              "itemno": 4,
              "description": "2x614 LUMBER",
              "quantity": "30",
              "unit": "Length",
              "price": "4750"
            },
            {
              "itemno": 5,
              "description": "2 in WIRE NAIL",
              "quantity": "44",
              "unit": "lb",
              "price": "175"
            }
          ],
          "tax": 146545.35,
          "total": 1123514.35
        },
        {
          "supplier": {
            "_id": "000230693",
            "name": "C.A. PARCHMENT & SON LTD.",
            "taxid": "000230693",
            "address": {
              "town": "Southfield",
              "city_parish": "St. Elizabeth"
            },
            "contact": {
              "tel": "876-965-6211",
              "mobile": null,
              "email": null
            }
          },
          "invoiceno": "892539",
          "date": "2023-02-24",
          "items": [
            {
              "itemno": "1",
              "description": "CEMENT",
              "quantity": "100",
              "unit": "Bags",
              "price": "1376.00"
            },
            {
              "itemno": 2,
              "description": "DELIVERY",
              "quantity": "1",
              "unit": "Trip",
              "price": "2000"
            }
          ],
          "tax": 20940,
          "total": 160540
        },
        {
          "supplier": {
            "_id": "000053457",
            "name": "STEWARTS HARDWARE LTD Old Harbour",
            "taxid": "000053457",
            "address": {
              "town": "Old Harbour",
              "city_parish": "St. Catherine"
            },
            "contact": {
              "tel": "876-745-2844",
              "mobile": "876-796-1086",
              "email": null
            }
          },
          "invoiceno": "OHSP200054213",
          "date": "2022-09-06",
          "items": [
            {
              "itemno": "1",
              "description": "3/8 POLY ROPE",
              "quantity": "8",
              "unit": "lb",
              "price": "384.44"
            }
          ],
          "tax": 478.19,
          "total": 3665.65
        },
        {
          "supplier": {
            "_id": "000230693",
            "name": "C.A. PARCHMENT & SON LTD.",
            "taxid": "000230693",
            "address": {
              "town": "Southfield",
              "city_parish": "St. Elizabeth"
            },
            "contact": {
              "tel": "876-965-6211",
              "mobile": null,
              "email": null
            }
          },
          "invoiceno": "860193",
          "date": "2022-07-29",
          "items": [
            {
              "itemno": "1",
              "description": "120W SOLAR STREET LIGHT ",
              "quantity": "3",
              "unit": "Each",
              "price": "6480.00"
            }
          ],
          "tax": null,
          "total": 19440
        },
        {
          "supplier": {
            "_id": "000230693",
            "name": "C.A. PARCHMENT & SON LTD.",
            "taxid": "000230693",
            "address": {
              "town": "Southfield",
              "city_parish": "St. Elizabeth"
            },
            "contact": {
              "tel": "876-965-6211",
              "mobile": null,
              "email": null
            }
          },
          "invoiceno": "894570",
          "date": "2023-03-08",
          "items": [
            {
              "itemno": "1",
              "description": "CEMENT",
              "quantity": "100",
              "unit": "Bags",
              "price": "1392",
              "keywords": [
                "Cement"
              ]
            },
            {
              "itemno": 2,
              "description": "Toilet Seat Cover White",
              "quantity": "1",
              "unit": "Each",
              "price": "3080",
              "keywords": [
                "Toilet Seat"
              ]
            }
          ],
          "tax": 21642,
          "total": 165922
        }
      ]

)

## PROJECT INVENTORY 

def sortInventory(keywords, datalist):
    def sort(item):
        keyword = item.get('item').split(' ')
        for sample in keyword:
            if sample in keywords:
                return item
            else: return None

    return list(filter(sort, datalist))[0]


def addInventory(id:str=None, data:list=None):
        if data:                          
            #project = await self.get(id=id)  
            # check if this material inventory exists 
            # if not add it 
            project['inventory'].append(data)
        else:
            pass
        return project.get('inventory')
    
#def addInventoryItem(self, id:str=None, data:list=None):

# Tesst
find_item = sortInventory(['CEMENT', 'Cement', 'cement'], project['inventory'])
print(find_item)