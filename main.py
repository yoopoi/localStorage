import json
from fastapi import FastAPI
from storage import LocalStorage
from pydantic import BaseModel
from typing import Optional
from util import *
storage = LocalStorage()
app = FastAPI()
class Extra(BaseModel):
    limit:Optional[int]=10
    sort:str=""
    offset:int=0
    like:str=""

#下面为自动生成代码 不要修改!!! 要不然下一次生成全部就全没咯！！！！
#db class auto generate#
class Userinfo(BaseModel):
    name:str=None
    age:int=None
class Goods(BaseModel):
    goods_name:str=None
    price:int=None
    count:int=None
    imgList:str=None
    creater:str=None

#db auto generate end#

#下面为自动生成代码 不要修改!!! 要不然下一次生成全部就全没咯！！！！
#api auto generate#
@app.post("/userinfo")
def userinfo(values:Userinfo):
    res = storage.setItem("userinfo",values.dict())
    return res
@app.put("/userinfo/{id}")
def userinfo(id,values:Userinfo):
    res = storage.updateItem("userinfo",values.dict(),{"ID":id})
    return res
@app.delete("/userinfo/{id}")
def userinfo(id,values:Userinfo):
    res = storage.removeItem("userinfo",{"ID":id})
    return res
@app.get("/userinfo")
def userinfo(limit=10,offset=0,like="",sort="",body=Userinfo().dict()):
    print(body)
    data = storage.getItem("userinfo",json.loads(body),{"limit":limit,"offset":offset,"like":like,"sort":sort})
    return storage._listToKV("userinfo",data)
            
@app.post("/goods")
def goods(values:Goods):
    res = storage.setItem("goods",values.dict())
    return res
@app.put("/goods/{id}")
def goods(id,values:Goods):
    res = storage.updateItem("goods",values.dict(),{"ID":id})
    return res
@app.delete("/goods/{id}")
def goods(id,values:Goods):
    res = storage.removeItem("goods",{"ID":id})
    return res
@app.get("/goods")
def goods(limit=10,offset=0,like="",sort="",body=Goods().dict()):
    print(body)
    data = storage.getItem("goods",json.loads(body),{"limit":limit,"offset":offset,"like":like,"sort":sort})
    return storage._listToKV("goods",data)
            
#api auto generate end#




