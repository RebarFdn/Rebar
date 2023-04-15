#settings_db.py | Ian moncrieffe | 13 dec 2022

import json
from sqlite3 import (connect, IntegrityError)
from time import sleep 

from starlette.responses import JSONResponse
from decoRouter import Router

## _________ Data Sources __________
data = {
        "company":{
            "name":"Vrstan Drywall Company Ltd.", 
            "address":{
                "lot": "111",
                "street": "Marlin Way",
                "town": "Old Harbour Glade.",
                "city_parish": "St. Catherine",
                "country": "Jamaica W.I."
            },
            "contact": {
                "tel": "(876)-663-1888",
                "mobile": "(876)-772-4286",
                "email": "vrstandc@gmail.com",
                "watsapp": "(867)-298-2925"
            }
        },
        "theme": "cherry"
}

datau = {
    "logo_url": "http://centryplan/logo/ettrd112475l.svg"
}

userid='vrstan'
data_table = "user_settings"


class SQLDatabase:
    db:str = 'Settings.sqlite'
    def __init__(self):
        self.conn = connect(self.db)
        self.cursor = self.conn.cursor()

    def create_settings_table(self, table:str=None, colums:tuple=None):
        if table:
            dat = table
        else: dat = data_table
        if colums:
            dac = str(colums)
        else: dac = "( userid VARCHAR UNIQUE, settings)"
        try:
            with self.conn as db:
                self.cursor.execute(f"CREATE TABLE {dat}{dac}")
            db.commit()
            return 'OK'        
        except Exception as e:
            return str(e)
        finally:            
            del table
            sleep(0.1)
           

    def data_bases(self):
        try:
            created = self.cursor.execute("SELECT name FROM sqlite_master")
            return created.fetchall()
        except Exception as e:
            return str(e)
        finally:
            del created
            self.cursor.close()
            sleep(0.1)
            self.conn.close()

    def set(self, userid:str=None, data:list=None):                   
        try:
            with self.conn:
                self.conn.execute(f"INSERT INTO {data_table} VALUES( ?, ?)",( userid, json.dumps(data),))
            sleep(0.1)             
            return {"status": f'data was posted to {userid} Succesfully!'}
        except IntegrityError as e:
            return str(e)
        
        
            

    def fetch(self, userid:str=None):
        sql = f'SELECT settings FROM {data_table} WHERE userid=?'
        try:
            with self.conn:
                data =  json.loads(self.cursor.execute(sql, (userid,)).fetchone()[0])
            sleep(0.15)
            return data
        except Exception as e:
            return str(e)
        finally:
            del sql

    def update(self, userid:str=None, data:dict=None):
        old_data = self.fetch(userid=userid)        
        payload = old_data | data        
        sql = f"UPDATE {data_table} SET settings = '{json.dumps(payload)}' WHERE userid=?"
        try:
            with self.conn:
                self.cursor.execute(sql, (userid,))                
            return payload
        except Exception as e:
            return str(e)
        finally:
            sleep(0.25) 
            del(sql)
            del(old_data)
            del(payload)


    
    def delete(self, userid:str=None):
        sql = f'DELETE FROM {data_table} WHERE userid=?'
        try:
            with self.conn:
                self.cursor.execute( sql, (userid,))
            self.conn.commit()
            self.cursor.close()
            return {"status": 'DELETED'}
        except Exception as e:
            return str(e)
        finally:
            sleep(0.1) 
            del sql
            self.close()
    
    def uids(self):
        try:
            return self.cursor.execute(
                f"""SELECT userid FROM {data_table}"""
            ).fetchall()
        finally:
            sleep(0.25)
    

    def fetch_all(self):
        def process_item(item):
            return {"userid": item[0], "settings": json.loads(item[1])}
        try:
            data = self.cursor.execute(
                f"""SELECT * FROM {data_table}"""
            ).fetchall()
            return list(map(process_item, data))                
        finally:
            sleep(0.25)

    def close(self):
        try:
            print(f'Closing {self.conn}')
            sleep(0.25)
            self.conn.close()
        finally: print('database closed.')


## ______________API______________

api = Router()
sdb = SQLDatabase()
#sdb.create_settings_table()

def error(e): return dict( err = str(e) )

# Create  
@api.post('/setting/{userid}')   
async def createUserSettings(request):
    try:
        uid = request.path_params.get('userid')
        data = await request.json()
        res = sdb.set( userid=uid, data=data)
        
        return JSONResponse([uid, data])
    except Exception as e:
        return JSONResponse(error(e=e))

# Retreive
@api.get('/setting/{userid}')   
async def getUserSettings(request):
    try:
        uid = request.path_params.get('userid')        
        return JSONResponse(sdb.fetch(userid=uid))
    except Exception as e:
        return JSONResponse(error(e=e))

# Update  
@api.put('/setting/{userid}')   
async def updateUserSettings(request):
    try:
        uid = request.path_params.get('userid')
        data = await request.json()
        return JSONResponse(sdb.update(userid=uid, data=data))
    except Exception as e:
        return JSONResponse(error(e=e))
    finally:
        del(data)
        del(uid)

# Delete  
@api.delete('/setting/{userid}')   
async def deleteUserSettings(request):
    try:
        uid = request.path_params.get('userid')       
        res = sdb.delete(userid=uid)        
        return JSONResponse(res)
    except Exception as e:
        return JSONResponse(error(e=e))
    finally:
        del(res) 
        del(uid)