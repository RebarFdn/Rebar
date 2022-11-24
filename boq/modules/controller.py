# Central Bq socket router
import json
from starlette.endpoints import  WebSocketEndpoint
from starlette.websockets import WebSocket

#from boq.modules.column import ProcessColumn
from boq.modules.cbeam import ProcessBeam



async def router(request:str =None, request_data=None):
    print('REQUEST DATA', request)
    data = {    
    "beam": await ProcessBeam(data=request_data),
    "column": request_data,
   
    }
    result = None
    try:
        result = data.get(request, None)
        return result
    except Exception as e:
        return {"status": str(e)}
    finally: del(result)



class BoqSocketEndpoint(WebSocketEndpoint):
    encoding = "text"
    async def on_connect(self, websocket: WebSocket) -> None:        
        await websocket.accept()
        
    async def on_receive(self, websocket: WebSocket, data: bytes) -> None:      
        req = json.loads( data )
        
        result =  await router(request=req['type'], request_data=req)
        
        await websocket.send_text(json.dumps(result))
        
        
    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        #logger.info(f"Disconnected: {websocket}")
        await websocket.close()
        return await super().on_disconnect(websocket, close_code)

    
