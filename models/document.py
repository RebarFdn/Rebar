# Document Creator 

import random, os
import time

from pdfme import build_pdf

from starlette.responses import PlainTextResponse, JSONResponse, FileResponse
from starlette.routing import Route
from config import config


from utils.utilities import GenerateId, timestamp

class Document:
    def __init__(self):
        self._id = self.gen_id()

    def gen_id(self):
        gen = GenerateId()
        return gen.gen_id('doc')

    def date_stamp(self, timestamp:int=None):
        from datetime import datetime
        timestamp = timestamp / 1000
        ts = datetime.fromtimestamp(timestamp)

        return ts.strftime('%Y-%m-%d')
        

        

    def gen_word(self):
        random.seed(1)
        abc = 'abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZáéíóúÁÉÍÓÚ'
        return ''.join(random.choice(abc) for _ in range(random.randint(1, 10)))

    def gen_text(self, n):
        return random.choice(['',' ']) + (' '.join(self.gen_word() for _ in range(n))) + random.choice(['',' '])

    def gen_paragraphs(self, n):
        return [self.gen_text(random.randint(50, 200)) for _ in range(n)]
    
    def doc(self):
        self.document = {
        "style": {
            "margin_bottom": 15, "text_align": "j",
            "page_size": "letter", "margin": [60, 50]
        },
        "formats": {
            "url": {"c": "blue", "u": 1},
            "title": {"b": 1, "s": 13}
        },
        "running_sections": {
            "header": {
                "x": "left", "y": 20, "height": "top", "style": {"text_align": "r"},
                "content": [{".b": "This is a header"}]
            },
            "footer": {
                "x": "left", "y": 740, "height": "bottom", "style": {"text_align": "c"},
                "content": [{".": ["Page ", {"var": "$page"}]}]
            }
        },
        "sections": [
            {
                "style": {"page_numbering_style": "roman"},
                "running_sections": ["footer"],
                "content": [

                    {
                        ".": "A Title", "style": "title", "label": "title1",
                        "outline": {"level": 1, "text": "A different title 1"}
                    },

                    ["This is a paragraph with a ", {".b": "bold part"}, ", a ",
                    {".": "link", "style": "url", "uri": "https://some.url.com"},
                    ", a footnote", {"footnote": "description of the footnote"},
                    " and a reference to ",
                    {".": "Title 2.", "style": "url", "ref": "title2"}],

                    {"image": "./static/imgs/logo.png"},

                    *self.gen_paragraphs(7),

                    {
                        "widths": [1.5, 2.5, 1, 1.5, 1, 1],
                        "style": {"s": 9},
                        "table": [
                            [
                                self.gen_text(4),
                                {
                                    "colspan": 5,
                                    "style": {
                                        "cell_fill": [0.57, 0.8, 0.3],
                                        "text_align": "c", "cell_margin_top": 13
                                    },
                                    ".b;c:1;s:12": self.gen_text(4)
                                },None, None, None, None
                            ],
                            [
                                {"colspan": 2, ".": [{".b": self.gen_text(3)}, self.gen_text(3)]}, None,
                                {".": [{".b": self.gen_text(1) + "\n"}, self.gen_text(3)]},
                                {".": [{".b": self.gen_text(1) + "\n"}, self.gen_text(3)]},
                                {".": [{".b": self.gen_text(1) + "\n"}, self.gen_text(3)]},
                                {".": [{".b": self.gen_text(1) + "\n"}, self.gen_text(3)]}
                            ],
                            [
                                {
                                    "colspan": 6, "cols": {"count": 3, "gap": 20},
                                    "style": {"s": 8},
                                    "content": self.gen_paragraphs(10)
                                },
                                None, None, None, None, None
                            ]
                        ]
                    },

                    *self.gen_paragraphs(10),
                ]
            },
            {
                "style": {
                    "page_numbering_reset": True, "page_numbering_style": "arabic"
                },
                "running_sections": ["header", "footer"],
                "content": [

                    {
                        ".": "Title 2", "style": "title", "label": "title2",
                        "outline": {}
                    },

                    ["This is a paragraph with a reference to ",
                    {".": "Title 1.", "style": "url", "ref": "title1"}],

                    {
                        "style": {"list_text": "1.  "},
                        ".": "And this is a list paragraph." + self.gen_text(40)
                    },

                    *self.gen_paragraphs(10)
                ]
            },
        ]
    }

    def gen_last_payslip(self, data:dict=None):
        ts = time.ctime()
        if data:
            statement = data.get('account').get('payments')[-1]
        else:
            statement = {}

        
        self.document = {
        "style": {
            "margin_bottom": 15, "text_align": "j",
            "page_size": "letter", "margin": [60, 50]
        },
        "formats": {
            "url": {"c": "blue", "u": 1},
            "title": {"b": 1, "s": 13}
        },
        "running_sections": {
            "header": {
                "x": "left", "y": 20, "height": "top", "style": {"text_align": "r"},
                "content": [{".b": "This is a header"}]
            },
            "footer": {
                "x": "left", "y": 740, "height": "bottom", "style": {"text_align": "c"},
                "content": [{".": ["Page ", {"var": "$page"}]}]
            }
        },
        "sections": [
            {
                "style": {"page_numbering_style": "roman"},
                "running_sections": ["footer"],
                "content": [
                    {
                        "style": {"margin_left": 120, "margin_right": 120},
                        "group": [
                            {"image": "./static/imgs/logo.png", "min_height": 100},
                           
                        ]
                    },

                    {
                        ".": "CentryPlan Building Services Employee Pay Statement", "style": "title", "label": "title1",
                        "outline": {"level": 1, "text": "Employee Salary Statement"}
                    },

                    ["This Statement is prepared for ", {".b": f"{data.get('name')}"}, {".": f"{ts}"},
                    ],
                    
                    
                    {
                        "widths": [1.5, 2.5, 1, 1.5, 1, 1],
                        "style": {"s": 9},
                        "table": [
                            [
                                f"Occupation:  {data.get('occupation')}",
                                {
                                    "colspan": 4,
                                    "style": {
                                        "cell_fill": [0.57, 0.8, 0.3],
                                        "text_align": "c", "cell_margin_top": 13
                                    },
                                    ".b;c:1;s:12": f"Salary Statement For {data.get('name')}"
                                },None, None, None, 
                                {".": [{".b": "Week End" + "\n"}, self.date_stamp(statement.get('date'))]}
                               
                            ],
                            [
                                {".": [{".b": "Refference"}]},
                                {"colspan": 2, ".": [{".b": 'Description'}]}, None,
                               
                                {".": [{".b": "Date"}]},None,
                               
                                {".": [{".b": "Amount"}]}
                            ],
                            

                                    [
                                        {
                                            
                                            "style": {"s": 8},
                                            "content": [{".": statement.get('ref')}]
                                        },
                                        {
                                            "colspan": 2, 
                                            "style": {"s": 8},
                                            "content":  [{".": statement.get('description')}]
                                        },
                                        None, 
                                        {
                                            
                                            "style": {"s": 8},
                                            "content":  [{".": self.date_stamp(statement.get('date'))}] 
                                        },
                                        None,
                                        {
                                            
                                            "style": {"s": 8},
                                            "content":  [{".": f"${float(statement.get('amount'))}"}]
                                        }
                                    ]
                            
                        ]
                    },

                   
                ]
            },
            
        ]
    }

    async def worker_last_pay_slip(self, id:str=None, ):
        try:
            from models.employee import Employee
            ep = Employee()
            worker = await ep.get_worker(id=id)
            self.gen_last_payslip(data=worker)
            return worker
        except ImportError as e:
            return {"status": str(e)}


    def create(self, file_name:str=None):
        if file_name:
            filename = file_name
        else:
            filename = 'document.pdf'
        filepath = os.path.join(config.DOCUMENT_PATH, filename)
        with open(filepath, 'wb') as f:
            build_pdf(self.document, f)
        f.close()
        return filepath


async def pdfDoc(request):
    id = request.path_params.get('id')
    doc = Document()
    doc.doc()
    docpath = doc.create()
    return FileResponse(docpath) 


async def workerPayStatement(request):
    id = request.path_params.get('id')
    doc = Document()
    doc.doc()
    data = await doc.worker_last_pay_slip(id=id)
    file_name = f"{data.get('oc')}-payslip.pdf"
    docpath = doc.create(file_name=file_name)
    print(data)
    return FileResponse(docpath) 

async def workerPayStatements(request):
    id = request.path_params.get('id')
    doc = Document()
    doc.doc()
    data = await doc.worker_last_pay_slip(id=id)
    file_name = f"{data.get('oc')}-payslip.pdf"
    docpath = doc.create(file_name=file_name)
    print(data)
    return FileResponse(docpath) 