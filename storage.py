import json
import sqlite3 as sq 
import re
class LocalStorage: 
    def AnalyseType(self,data):
        _type = type(data)
        if _type == str:
            return "VARCHAR(255)"
        elif _type == int:
            return "INTEGER"
        elif _type == float:
            return "DOUBLE"
        elif _type == bool:
            return "BOOLEAN"
        elif _type == None:
            return "VARCHAR(255)"
        elif _type == list:
            return "TEXT"
        elif _type == dict:
            return "TEXT"
        else:
            return "VARCHAR(250)"
    def AnalyseTableColumnType(self,_type):
        # _type = type(data)
        if _type == "INTEGER":
            return "int"
        elif "VARCHAR" in _type:
            return "str"
        elif "TEXT" == _type:
            return "str"
        elif "BOOLEAN" == _type:
            return "bool"
        elif "DOUBLE" == _type:
            return "float"
        else:
            return "str"
        
    def _parseKey(self,data):
        if "[" in data:
            index = data.index("[")
            return (data[0:index],re.findall("(\w*-?\w*)(?:,|\])",data))
        else:
            return (data,[])
    def __init__(self,storageName="localstorage") -> None:
        print("localStorage init")
        self.storageName = storageName 
        self.tableName = "LocalStorage"
        self._connect(storageName)
    def _connect(self,database):
        if ".db" not in database:
            database+=".db"
        self.conn = sq.connect(database,check_same_thread=False)
    def excute(self,query):
        # print(query)
        try:
            c = self.conn.cursor()
            return c.execute(query)
        except Exception as e:
            print(query)
            print("[X]数据库执行出错:%s\n" % (e))
    def _formatFetch(slef,data):
        res = []
        for item in data:
            res.append(item[2::])
        return res
    def getItem(self,tableName="",data={},options={}):
        condition = ""
        for key in data:
            if data[key]==None or data[key]=="":
                continue
            (_key,_options) = self._parseKey(key)
            if type(data[key])==str:
                data[key] = '"'+data[key]+'"'
            if 'like' in _options:
                condition+="%s LIKE %s AND " %(_key,data[key])
            elif key == options.get("like"):
                condition+="%s LIKE %s AND " %(_key,data[key])
            else:
                condition+="%s = %s AND " %(_key,data[key])
        condition+=" is_delete = false"
        query = "SELECT * FROM %s WHERE %s" % (tableName,condition)
        if "sort" in options and options["sort"]!="":
            query+= " ORDER BY %s" % options["sort"]
        if "limit" in options:
            query+=" limit %d" % int(options["limit"])
        if "offset" in options:
            query+=" offset %d" % int(options["offset"])
        query+=";"
        res = self.excute(query)
        if res:
            return self._formatFetch(res.fetchall())
        return res 
    def _formatType(self,value):
        if type(value) !=list and type(value)!=dict:
            value = {"value":value}
        return value
    def _isObjectOrStr(self,x):
        return type(x)==str or type(x)==list or type(x)==dict
    def _formatDictKeyToList(self,data):
        _keyList = []
        for key in data:
            (_key,option) = self._parseKey(key)
            _keyList.append(_key)
        return _keyList
    def setItem(self,tableName,data):
        tables = self.getTableList()
        if (tableName,) not in tables:
            self._createTable(tableName,data)
        # for key in data:
        #     if type(data[key])==dict:
        #         data[key] = "{%d}"%self.setItem(key,data[key])
        data = self._formatType(data)
        query = "INSERT INTO %s " %(tableName)
        query+="(%s)" % (",".join(self._formatDictKeyToList(data)))
        query+=" VALUES (%s);" % (",".join(["'%s'" % str(x).replace("'",'"') if self._isObjectOrStr(x) else str(x) for x in data.values()]))
        res = self.excute(query)
        if res:
            self.conn.commit()
            return res.lastrowid
        return res 
    def getTableList(self):
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        res = self.excute(query)
        return res.fetchall()
    def _createTable(self,tableName,_dict):
        tables = self.getTableList()
        if (tableName,) not in tables:
            _dict = self._formatType(_dict)
            query = '''
            CREATE TABLE %s(
            ID INTEGER PRIMARY KEY AUTOINCREMENT    NOT NULL,
            is_delete BOOLEAN DEFAULT false,
            ''' % (tableName)
            keys = _dict.keys()
            for key in keys:
                (formatKey,options) = self._parseKey(key)
                _type = self.AnalyseType(_dict[key])
                query+="%s %s %s," % (formatKey,_type," ".join(options))
            query=query[0:-1]
            query+=");"
            res = self.excute(query)
            return res
    def _deleteOneTable(self,tableName):
        query = "DROP TABLE %s;" % (tableName)
        res = self.excute(query)
        return res
    def clear(self):
        tables = self.getTableList()
        for table in tables:
            if "sqlite_" in table[0]:
                continue
            self._deleteOneTable(table[0])
    def keys(self,tableName,index):
        query = "SELECT key FROM %s WHERE is_delete = false" % (tableName)
        if index:
            query+=" and ID = %d" % index
        res = self.excute(query)
        return res.fetchall()
    def length(self,tableName)->int:
        query = "SELECT ID FROM %s WHERE is_delete = false" % (tableName)
        res = self.excute(query)
        if res:
            return len(res.fetchall())
        else:
            return 0
    def _listToKV(self,tableName,data):
        tableStructure = self._getTableInfo(tableName)
        tableStructure = tableStructure[2::]
        if type(data)==list:
            res = []
            for item in data:
                _item = {}
                for struct in tableStructure:
                    if struct[1]=="ID":
                        continue
                    if struct[1]=="is_delete":
                        continue
                    _item[struct[1]] = item[int(struct[0])-2]
                res.append(_item)
            return res
        else:
            _item = {}
            for struct in tableStructure:
                if struct[1]=="ID":
                        continue
                if struct[1]=="is_delete":
                        continue
                _item[struct[1]] = item[int(struct[0])-2]
            res.append(_item)
    def removeItem(self,tableName,data):
        condition = ""
        for key in data:
            if type(data[key])==str:
                data[key] = '"'+data[key]+'"'
            condition+="%s = %s AND " %(key,data[key])
        condition+=" is_delete = false;"
        query = "UPDATE %s SET is_delete = true WHERE %s" %(tableName,condition)
        res = self.excute(query)
        if res:
            self.conn.commit()
            return True 
        return False
    def _getTableInfo(self,tableName):
        query = "PRAGMA table_info(%s);" % tableName
        res = self.excute(query)
        if res:
            return res.fetchall()
        return res
    def updateItem(self,tableName,editData,data):
        condition = ""
        editStr = ""
        for key in data:
            if data[key] == None :
                continue
            if type(data[key])==str:
                data[key] = '"'+data[key]+'"'
            condition+="%s = %s AND " %(key,data[key])
        for key in editData:
            if editData[key] == None or editData[key] == "":
                continue
            if type(editData[key])==str:
                editData[key] = '"'+editData[key]+'"'
            editStr+=" %s = %s," %(key,editData[key])
        editStr = editStr[:-1]
        condition+=" is_delete = false;"
        query = "UPDATE %s SET %s WHERE %s" %(tableName,editStr,condition)
        res = self.excute(query)
        if res:
            self.conn.commit()
            return True 
        return False
    def generateFastApiCode(self):
        tableList = self.getTableList()
        tableListStr = ""
        for tableNameTuple in tableList:
            if "sqlite" in tableNameTuple[0]:
                continue
            tableName =tableNameTuple[0]
            tableStructure = self._getTableInfo(tableName)
            tableStructureStr = "class %s(BaseModel):\n"%(tableName[:1].upper()+tableName[1:])
            for columnType in tableStructure:
                _type = self.AnalyseTableColumnType(columnType[2])
                if columnType[1]=="ID" or columnType[1] == "is_delete":
                    continue
                # tableStructureDict[columnType[1]] = _type 
                tableStructureStr+="    %s:%s=None\n"%(columnType[1], _type )
            # tableStructureStr+="    extra:Extra=Extra()\n"
            tableListStr+=tableStructureStr
        apiListStr = ""
        for tableNameTuple in tableList:
            if "sqlite" in tableNameTuple[0]:
                continue
            tableName =tableNameTuple[0]
            upperTableName =tableName[:1].upper()+tableName[1:]
            apiStr = '''
@app.post("/%s")
def %s(values:%s):
    res = storage.setItem("%s",values.dict())
    return res
@app.put("/%s/{id}")
def %s(id,values:%s):
    res = storage.updateItem("%s",values.dict(),{"ID":id})
    return res
@app.delete("/%s/{id}")
def %s(id,values:%s):
    res = storage.removeItem("%s",{"ID":id})
    return res
@app.get("/%s")
def %s(limit=10,offset=0,like="",sort="",body=%s().dict()):
    print(body)
    data = storage.getItem("%s",json.loads(body),{"limit":limit,"offset":offset,"like":like,"sort":sort})
    return storage._listToKV("%s",data)
            ''' %(tableName,tableName,upperTableName,tableName,    tableName,tableName,upperTableName,tableName,   tableName,tableName,upperTableName,tableName,   tableName,tableName,upperTableName,tableName,tableName)
            apiListStr+=apiStr
        strCode = ""
        with open("main.py",'r') as f:
            strCode = f.read()
        dbprefix = "#db class auto generate#"
        dbsuffix = "#db auto generate end#"
        head = strCode.split(dbprefix)[0]
        end = strCode.split(dbsuffix)[1]
        res = head+dbprefix+"\n"+tableListStr+"\n"+dbsuffix+end
        strCode = res 
        apiprefix = "#api auto generate#"
        apisuffix = "#api auto generate end#"
        head = strCode.split(apiprefix)[0]
        end = strCode.split(apisuffix)[1]
        res = head+apiprefix+apiListStr+"\n"+apisuffix+end
        strCode = res 
        with open('main.py','w')as f:
            f.write(strCode)
