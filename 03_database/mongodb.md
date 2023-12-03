# MongoDB操作
使用Docker安装MongoDB服务的命令如下：
```bash
docker pull mongo
docker run --name mongodb -p 27017:27017 -v E:\Docker\data:/data/db -d mongo
```

## 1.创建数据库
如果没有question_answer数据库，则创建question_answer数据库；如果有question_answer数据库，则切换到question_answer数据库：
```bash
use question_answer
```
输出：
```bash
switched to db question_answer
```

查看数据库：
```bash
show dbs
```
输出：
```bash
admin   0.000GB
config  0.000GB
local   0.000GB
```
question_answer数据库不存在，是因为该数据库中还没有数据，要显示它，需要向question_answer数据库插入一些数据。

查看当前数据库：
```bash
db
```
输出：
```bash
Result
question_answer
```

## 2.创建表
MongoDB中没有显式创建表的命令，表的数据结构在往表插入数据时确定，因此在MongoDB中，创建完数据库之后就可以直接往表中插入数据，表名在插入数据时指定。

插入数据如下：
```bash
db.user.insert({
    "name" : "Corley",
    "age" : 20,
    "sex" : "male"
})
```
输出：
```bash
Result
WriteResult({ "nInserted" : 1, "writeConcernError" : [ ] })
```

查询数据：
```bash
db.user.find()
```
输出：
```bash
_id	name	age	sex
656bf7c1da05276c87068733	Corley	20	male
```

对输出进行美化：
```bash
db.user.find().pretty()
```
输出：
```bash
_id	name	age	sex
656bf7c1da05276c87068733	Corley	20	male
```

再次查看数据库：
```bash
show dbs
```
输出：
```bash
admin            0.000GB
config           0.000GB
local            0.000GB
question_answer  0.000GB
```
此时question_answer数据库已经存在。

## 3.查询数据
批量插入数据：
```bash
db.user.insert([
    {
        "name" : "Corley",
        "age" : 20,
        "sex" : "male",
        "birthday" : "1999-09-09"
    },
    {
        "name" : "Tom",
        "age" : 21,
        "sex" : "male",
        "hobby" : "basketball"
    },
    {
        "name" : "Jerry",
        "age" : 22,
        "sex" : "male"
    }
])
```
输出：
```bash
Result
BulkWriteResult({
	"nRemoved" : 0,
	"nInserted" : 3,
	"nUpserted" : 0,
	"nMatched" : 0,
	"nModified" : 0,
	"writeErrors" : [ ]
})
```

查看所有数据：
```bash
db.user.find()
```
输出：
```bash
_id	name	age	sex	birthday	hobby
656bf7c1da05276c87068733	Corley	20	male		
656bfa52da05276c87068734	Corley	20	male	1999-09-09	
656bfa52da05276c87068735	Tom	21	male		basketball
656bfa52da05276c87068736	Jerry	22	male		
```

查询name为Corley的数据，结果不显示_id字段：
```bash
db.user.find({name:"Corley"}, {_id:0})
```
输出：
```bash
name	age	sex	birthday
Corley	20	male	
Corley	20	male	1999-09-09
```

## 4.逻辑操作
范围操作：
```bash
db.user.find({age:{$gte:21,$lt:22}})
```
输出：
```bash
_id	name	age	sex	hobby
656bfa52da05276c87068735	Tom	21	male	basketball
```

AND操作：
```bash
db.user.find({$and:[{name:"Corley"},{age:{$gte:20,$lt:22}}]})
```
输出：
```bash
_id	name	age	sex	birthday
656bf7c1da05276c87068733	Corley	20	male	
656bfa52da05276c87068734	Corley	20	male	1999-09-09
```

等价于：
```bash
db.user.find({name:"Corley", age:{$gte:20,$lt:22}})
```

OR操作：
```bash
db.user.find({$or:[{name:"Corley"},{name:"Tom"}]})
```
输出：
```bash
_id	name	age	sex	birthday	hobby
656bf7c1da05276c87068733	Corley	20	male		
656bfa52da05276c87068734	Corley	20	male	1999-09-09	
656bfa52da05276c87068735	Tom	21	male		basketball
```

AND和OR混合使用：
```bash
db.user.find({$or:[{name:"Corley", age:{$gte:20,$lt:22}},{name:"Tom"}]})
```
输出：
```bash
_id	name	age	sex	birthday	hobby
656bf7c1da05276c87068733	Corley	20	male		
656bfa52da05276c87068734	Corley	20	male	1999-09-09	
656bfa52da05276c87068735	Tom	21	male		basketball
```

## 5.排序聚合
按年龄升序排列：
```bash
db.user.find().sort({age:-1})
```
输出：
```bash
_id	name	age	sex	hobby	birthday
656bfa52da05276c87068736	Jerry	22	male		
656bfa52da05276c87068735	Tom	21	male	basketball	
656bf7c1da05276c87068733	Corley	20	male		
```

聚合——按照年龄分组：
```bash
db.user.aggregate([
  {
    $group: {
      _id: {age: '$age'},
      count: {$sum: 1}
		}
  }
])
```
输出：
```bash
_id	count
(Document) 1 Field	1
(Document) 1 Field	2
(Document) 1 Field	1
```

## 6.更新删除数据
更新数据：
```bash
db.user.update({name:"Corley"},{$set:{age:25}})
```
输出：
```bash
Result
WriteResult({
	"nMatched" : 1,
	"nUpserted" : 0,
	"nModified" : 1,
	"writeConcernError" : [ ]
})
```

查询数据：
```bash
db.user.find()
```
输出：
```bash
_id	name	age	sex	birthday	hobby
656bf7c1da05276c87068733	Corley	25	male		
656bfa52da05276c87068734	Corley	20	male	1999-09-09	
656bfa52da05276c87068735	Tom	21	male		basketball
656bfa52da05276c87068736	Jerry	22	male		
````

可以看到，数据被更新，同时默认只更新1条。

删除数据：
```bash
db.user.remove({name:"Tom"})
db.user.find()
```
输出：
```bash
_id	name	age	sex	birthday
656bf7c1da05276c87068733	Corley	25	male	
656bfa52da05276c87068734	Corley	20	male	1999-09-09
656bfa52da05276c87068736	Jerry	22	male	
```

也可以删除所有数据：
```bash
db.user.remove({})
db.user.find()
```
输出：
```bash

```

此时数据表为空。

## 7.MySQL与MongoDB的差异分析
MySQL与MongoDB的主要差异体现在以下三个方面：

1. 数据结构：MySQL是一种关系型数据库，以表格的形式组织和存储数据，使用SQL语言进行查询和操作。而MongoDB是一种文档型数据库，以类似JSON的BSON格式存储数据，使用面向文档的数据模型，不需要预先定义数据的结构，具有更灵活的数据模型。
2. 事务支持：MySQL支持事务，具有ACID特性，可以保证数据的完整性和一致性。而MongoDB早期版本对事务支持较弱，但在最新版本中已经增强了对多文档事务的支持。
3. 扩展性：MySQL通常采用垂直扩展的方式来提高性能，即通过增加更多的硬件资源来处理更大的负载。而MongoDB由于其数据结构的特点，更适合做大数据的存储，或一些复杂的临时数据存储。

总的来说，MySQL和MongoDB各有优势，选择哪种数据库取决于具体的使用场景和需求。