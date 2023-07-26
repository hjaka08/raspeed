from typing import Union
from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
from starlette.responses import JSONResponse
import pymysql, json
import os


app=FastAPI()

MYSQL_HOST=os.getenv("MYSQL_HOST")
MYSQL_USER=os.getenv("HYSQL_USER")
MYSQL_PASS=os.getenv("MYSQL_PASS")
MYSQLDB_NAME=os.getenv("MYSQLDB_NAME")
try:
    conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASS, db=MYSQLDB_NAME, charset="utf8")
except: 
    print("Mysql Connection Fail!")

class Item(BaseModel):
    ip: str
    dhcp: str
    gateway: str
    downspeed: str
    upspeed: str


@app.get("/")
def index():
    return ("Fuck YOU!! Don't Try to Hack My Server!")

@app.get("/viewlist")
async def  view_list():
    try:
        cur=conn.cursor()
        cur.execute("SELECT * FROM speedtable")
        views=json.dumps(cur.fetchall())

    except:
        print("Failed to Read DB")

    return(views)


@app.post("/add")
async def add_item(item: Item):
    infomas = dict(item)
    print("INFO:     Received Data -     " + str(infomas))

    try:
        cur=conn.cursor()
        cur.execute("INSERT INTO speedtable VALUES(%d, %d, %d, %d, %d)",infomas["ip"], infomas["dhcp"], infomas["gateway"], infomas["downspeed"], infomas["upspeed"])
        conn.commit()
        conn.close()

    except:
        print("Failed to Write DB")
    return {"item": infomas}
    #return JSONResponse(dicted_item)
