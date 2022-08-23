# localStorage
一款能自动生成FastApi代码自动生成数据库表的curd小工具
# 运行方式
## 执行 python3 genCOde.py   生成fastApi 代码
## 再执行 python3 run.py     开启fastApi服务
## 后续如果更改genCode的配置,重新执行 python3 genCOde.py 即可从 127.0.0.1:8000/docs 看到更改
# localStorage具体文档
print("清空数据库")
storage.clear()
print("首先添加一个用户:xucheng 并且让名字为唯一字段")
storage.setItem("userinfo",{"name[unique]":"xucheng","age":24})


print("如果我们再添加一个用户叫做xucheng的人...那就会报错！")
storage.setItem("userinfo",{"name":"xucheng","age":25})


print("我们还可以模糊搜索一个开头是xu的人")
print(storage.getItem("userinfo",{"name[like]":"xu%"}))


print("再添加一个用户:lili")
storage.setItem("userinfo",{"name":"lili","age":24})


print("emmmm再添加一个用户:laowang")
storage.setItem("userinfo",{"name":"laowang","age":25})


print("再添加一个商品:绍兴黄酒!")
storage.setItem("goods",{"goods_name":"绍兴黄酒","price":1499,"count":1,"imgList":["http://www.baidu.com"],"creater":"xucheng"})


print("我们可以读取一个名字叫做xucheng的人")
print(storage.getItem("userinfo",{"name":"xucheng"}))


print("我们可以还可以自定义limit和offset和sort进行curd")
print(storage.getItem("userinfo",options={"limit":2,"offset":1,"sort":"id desc"}))


print("我们还可以读取所有年龄是24岁的人")
print(storage.getItem("userinfo",{"age":24}))


print("如果不加任何条件,那么读取所有人")
print(storage.getItem("userinfo"))


print("让我们删掉laowang")
storage.removeItem("userinfo",{"name":"laowang"})


print("再看看用户表里还有谁?")
print(storage.getItem("userinfo"))


print("我们还可以结构化读取")
print(storage._listToKV("userinfo",storage.getItem("userinfo")))

print("修改xucheng的年龄")
print(storage.updateItem("userinfo",{"age":18,},{"name":"xucheng"}))
print("最后,我们来生成fastapi代码！！！（生成的代码在main.py中）")
storage.generateFastApiCode()