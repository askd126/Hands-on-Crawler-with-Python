# Python爬虫项目实战

**欢迎来到Corley的Python爬虫实战项目！**

随着互联网的快速发展，海量数据充斥在网络中，如何有效地获取并处理这些数据成为一个重要的问题。Python作为一种功能强大的编程语言，其庞大的第三方库能够轻松地帮助我们实现网络数据的抓取和分析。本项目旨在通过Python爬虫技术，实现对多种网站和应用的数据抓取和整理。内容方面，从Python基础和进阶开始，包含常用工具使用、JavaScript基础、抓包工具、爬虫基础、反爬虫基础、反爬虫进阶、验证码反爬和分布式爬虫等，内容由浅入深，不仅包含了理论基础，同时也包含很多爬虫实战案例，面向副业、转行、就业和技术提升，适合新手入门和进阶爬虫技术。通过本项目，不仅可以实现更便捷地获取数据，而且可以实现提升工作效率、自动化、解放双手，从而提升工作质量和生活幸福感。

## 环境

所有代码和案例都是基于Python 3.9环境安装和调试，环境的安装和配置主要依赖于conda。

1.创建虚拟环境

```bash
conda create -n pythoncrawlbase python=3.9 -y
```

2.进入虚拟环境并安装所依赖的库

```bash
conda activate pythoncrawlbase
conda install jupyter jieba blessed pymysql pymongo -y
```

## 目录
<details>
<summary>Python基础</summary>

- [while循环简单聊天机器人](01_python_basic/simple_chatbot.py)
- [生成指定长度随机字符串](01_python_basic/random_str.py)
- [列表的常用方法](01_python_basic/list_methods.py)
- [元组与列表的区别](01_python_basic/tuple_list.py)
- [字典的方法](01_python_basic/dict_methods.py)
- [集合的方法](01_python_basic/set_methods.py)
- [Python中的浅拷贝与深拷贝](01_python_basic/copy_deepcopy.py)
- [if条件控制](01_python_basic/if_condition.py)
- [Python中的while和for循环](01_python_basic/while_for.py)
- [Python中的异常处理](01_python_basic/exception.py)
- [Python函数](01_python_basic/function.ipynb)
- [全局与局部作用域](01_python_basic/global_local_field.ipynb)
- [闭包](01_python_basic/closure.ipynb)
- [装饰器](01_python_basic/decorator.ipynb)
- [类与对象](01_python_basic/class_object.ipynb)
- [继承与多态](01_python_basic/inheritance_polymorphism.ipynb)
- 实战：[简易词频统计器](applications/word_counter.py)
- 实战：[贪吃蛇小游戏](applications/snake_game)

</details>

<details>
<summary>Python进阶</summary>

- [静态方法与类方法](02_python_advanced/static_class_method.ipynb)
- [迭代器与生成器](02_python_advanced/iterator_generator.ipynb)
- [上下文管理器](02_python_advanced/with_context_manager.ipynb)
- [垃圾回收机制](02_python_advanced/garbage_collection.ipynb)
- [线程](02_python_advanced/thread.ipynb)
- [进程](02_python_advanced/process.ipynb)
- [协程](02_python_advanced/coroutine.ipynb)

</details>

<details>
<summary>数据库</summary>

- [MySQL基本操作](03_database/mysql.md)
- [Python操作MySQL](03_database/mysql_with_python.ipynb)
- [MongoDB操作](03_database/mongodb.md)
- [Python操作MongoDB](03_database/mongo_with_python.ipynb)

</details>

<details>
<summary>工具库</summary>

- [MySQL连接池](utils/mysql_pool)

</details>

## 持续更新中……

## 交流与反馈

欢迎您通过Github Issues来提交问题与建议，也欢迎找我交流：

- 个人主页：[https://github.com/corleytd](https://github.com/corleytd)
- 个人邮箱：[cutercorleytd@gmail.com](mailto:cutercorleytd@gmail.com)
- 更多细节：[Python爬虫实战](https://appxfexyp3p4519.h5.xiaoeknow.com/p/course/column/p_62847112e4b09dda1269d3f6)