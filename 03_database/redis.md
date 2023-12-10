# Redis操作
Redis安装和运行步骤：
```bash
docker pull redis
docker run --name redis -p 6379:6379 -v E:\Docker\data\redis:/data -d redis
```
## 1.String
Redis 里的字符串是动态字符串，会根据实际情况动态调整。
```bash
> set name corley
OK
> get name
corley
```

## 2.List
Redis里的List是一个链表，由于链表本身插入和删除比较块，但是查询的效率比较低，所以常常被用做异步队列。
当数据量比较小的时候，数据结构是压缩链表，而当数据量比较多的时候就成为了快速链表。
```bash
> LPUSH dbs mysql
1
> LPUSH dbs redis
2
> LPUSH dbs mongodb
3
> LRANGE dbs  0 -1
mongodb
redis
mysql
```

## 3.SET
Redis的Set是String类型的无序集合，集合成员是唯一的，集合中不能出现重复
的数据。Redis中集合是通过哈希表实现的，所以添加、删除、查找的复杂度都是O(1)。
```bash
> SADD  db_set mysql
1
> SADD db_set redis
1
> SADD db_set mongodb
1
> SMEMBERS db_set
mysql
redis
mongodb
```

## 4.Hash
Redis Hash是一个string类型的field（字段）和value（值）的映射表，hash特别适合用于存储对象。当hash一开始请求的内存空间不够时，会进行rehash，将数据都移动到更大的内存空间上。
```bash
> HMSET myself  name "Corley" age 18 hobby "reading"
OK
> HGETALL myself
name
Corley
age
18
hobby
reading
> HGET myself name
Corley
```

## 5.ZSet
有序集合Zset和集合一样也是string类型元素的集合，且不允许重复的成员。不同的是每个元素都会关联一个double类型的分数，Redis通过分数来为集合中的成员进行从小到大的排序。Zset内部是通过跳表（跳跃列表）实现的。
```bash
> ZADD db_zset 1 mysql
1
> ZADD db_zset 3 redis
1
> ZADD db_zset 2 mongodb
1
> ZADD db_zset 2 redis
0
> ZRANGE db_zset 0 -1
mysql
mongodb
redis
```