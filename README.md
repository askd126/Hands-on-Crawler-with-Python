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
conda install jupyter jieba blessed pymysql pymongo redis lxml aiohttp selenium fonttools scrapy -y
conda install paddlepaddle-gpu==2.5.2 cudatoolkit=10.2 --channel https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/Paddle/ -y
pip install paddlehub
```

## 目录
<details>
<summary>1.Python基础</summary>

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
<summary>2.Python进阶</summary>

- [静态方法与类方法](02_python_advanced/static_class_method.ipynb)
- [迭代器与生成器](02_python_advanced/iterator_generator.ipynb)
- [上下文管理器](02_python_advanced/with_context_manager.ipynb)
- [垃圾回收机制](02_python_advanced/garbage_collection.ipynb)
- [线程](02_python_advanced/thread.ipynb)
- [进程](02_python_advanced/process.ipynb)
- [协程](02_python_advanced/coroutine.ipynb)

</details>

<details>
<summary>3.数据库</summary>

- [MySQL基本操作](03_database/mysql.md)
- [Python操作MySQL](03_database/mysql_with_python.ipynb)
- [MongoDB操作](03_database/mongodb.md)
- [Python操作MongoDB](03_database/mongo_with_python.ipynb)
- [Redis操作](03_database/redis.md)
- [Python操作Redis](03_database/redis_with_python.ipynb)

</details>

4.基础爬虫——爬取豆瓣电影：
- [爬取豆瓣Top电影——串行版](04_base_crawling/douban_top_movie_crawler_serial.py)
- [爬取豆瓣Top电影——线程进程版](04_base_crawling/douban_top_movie_crawler_thread_process.py)
- [爬取豆瓣Top电影——协程版](04_base_crawling/douban_top_movie_crawler_coroutine.py)
- [爬取豆瓣Top电影——aiohttp版](04_base_crawling/douban_top_movie_crawler_aiohttp.py)
- [递归爬取豆瓣电影Top 250——基于Python之父Guido van Rossum的实现](04_base_crawling/douban_top_movie_crawler_recursive_from_guido.py)

<details>
<summary>5.JavaScript基础</summary>

- [JavaScript入门](05_javascript_basic/javascript_basic.md)
- [JavaScript对象](05_javascript_basic/javascript_object.md)
- [JavaScript原型链](05_javascript_basic/javascript_prototype_chain.md)
- [JavaScript函数进阶](05_javascript_basic/javascript_function_advanced.md)
- [JavaScript代理与反射](05_javascript_basic/javascript_proxy_reflect.md)

</details>

6.基础反爬
- [User-Agent反爬](06_basic_anti_crawling/anti_crawler_with_user_agent.py)
- [Cookies反爬](06_basic_anti_crawling/anti_crawler_with_cookies.py)
- [关键参数图片化反爬](06_basic_anti_crawling/anti_crawler_with_key_parameter_picturing.py)
- [恶意链接反爬](06_basic_anti_crawling/anti_crawler_with_malicious_links.py)

7.浏览器自动化反爬
- [使用selenium操作edge访问百度](07_browser_automatic_anti_crawling/edge_baidu_with_selenium.py)
- [使用selenium操作Edge实现网页动态渲染反爬](07_browser_automatic_anti_crawling/anti_crawler_with_edge_selenium.py)
- [使用selenium操作Edge实现内嵌iframe网页反爬](07_browser_automatic_anti_crawling/anti_crawler_with_iframe.py)
- [自动化工具控制浏览器被识别特征](07_browser_automatic_anti_crawling/bot_sannysoft_with_selenium.py)
- [使用selenium操作Edge实现浏览器特征检测反爬](07_browser_automatic_anti_crawling/anti_crawler_with_browser_feature.py)

8.前端技巧反爬
- [CSS偏移反爬](08_front_end_anti_crawling/anti_crawler_with_css_offset.py)
- [SVG映射反爬](08_front_end_anti_crawling/anti_crawler_with_svg_mapping.py)
- [自定义字体反爬](08_front_end_anti_crawling/anti_crawler_with_custom_font.py)

9.调试干扰
- [限制开发者工具使用](09_debug_interference/restriction_on_devtools_usage.md)

10.JavaScript混淆与逆向
- [javascript-obfuscator混淆](10_javascript_obfuscation_and_reversal/js_obfuscator.md)
- [域名锁定](10_javascript_obfuscation_and_reversal/domain_lock_resolution.js)

11.JS Hook
- [JS Hook逆向](11_js_hook/js_hook_reversal.md)
  - [所有操作都实现Hook的对象代理](11_js_hook/HookAnyObject.js)

12.环境模拟
- [Node环境模拟](12_environmental_simulation/node_environmental_simulation.md)

13.验证码反爬
- [简单图形验证码反爬](13_captcha_anti_crawling/anti_crawler_with_simple_graphic_captcha.py)
- [简单滑块验证码反爬](13_captcha_anti_crawling/anti_crawler_with_simple_slide_captcha.py)
- [拼图滑动验证码反爬](13_captcha_anti_crawling/anti_crawler_with_slide_puzzle_captcha.py)
- [使用selenium捕获鼠标移动](13_captcha_anti_crawling/capture_mouse_move_with_selenium.py)
- [鼠标轨迹检测反爬](13_captcha_anti_crawling/anti_crawler_with_mouse_track_detection.py)

## 工具库

<details>
<summary>工具库</summary>

- [MySQL连接池](utils/mysql_pool)
- [装饰器](utils/decorators)

</details>

## 持续更新中……

## 交流与反馈

欢迎您通过Github Issues来提交问题与建议，也欢迎找我交流：

- 个人主页：[https://github.com/corleytd](https://github.com/corleytd)
- 个人邮箱：[cutercorleytd@gmail.com](mailto:cutercorleytd@gmail.com)
- 更多细节：[Python爬虫实战](https://appxfexyp3p4519.h5.xiaoeknow.com/p/course/column/p_62847112e4b09dda1269d3f6)