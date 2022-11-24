import os

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse, FileResponse,JSONResponse
from starlette.routing import Route, Mount, WebSocketRoute

from starlette.endpoints import HTTPEndpoint, WebSocketEndpoint
from starlette.websockets import WebSocket
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from boq.modules.estimate import (createBoq, getBoq, getBoqIndex, updateBoq, deleteBoq)
from boq.modules.wall import  processWall, getBuildingRates
from boq.modules.slab import processSlab
from boq.modules.column import processColumn
from boq.modules.floor import processFloor
from boq.modules.foundation import processFoundation

from boq.modules.controller import  BoqSocketEndpoint

BASE_PATH = os.path.abspath(os.getcwd())



def base(request):
    return JSONResponse(
    {
        "base": BASE_PATH
    })


routes = [

    Route('/', base),
    Route('/create', methods=['POST'], endpoint=createBoq),
    Route('/index', methods=['GET'], endpoint=getBoqIndex),
    Route('/boq/{id}', methods=['GET'], endpoint=getBoq),
    Route('/update', methods=['PUT'], endpoint=updateBoq),

    Route('/floor', methods=['POST'], endpoint=processFloor),
    Route('/wall', methods=['POST'], endpoint=processWall),
    Route('/slab', methods=['POST'], endpoint=processSlab),
    Route('/column', methods=['POST'], endpoint=processColumn),
    Route('/foundation', methods=['POST'], endpoint=processFoundation),

    Route('/rates', methods=['GET'], endpoint=getBuildingRates),
    #WebSocketRoute("/ws", WSEndpoint, name="ws"),
    WebSocketRoute("/bs", BoqSocketEndpoint, name="ws"),


    

]


bq_api = Starlette(debug=True, routes=routes)

bq_api.add_middleware(
        CORSMiddleware, 
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=False,
        allow_origin_regex=None,
        expose_headers=[             
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Cedentials",
        "Access-Control-Allow-Expose-Headers",
        ],
        max_age=3600,

)

