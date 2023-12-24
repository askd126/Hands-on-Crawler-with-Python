# JS Hook逆向
## 1.最简单的Hook
JavaScript中的大多数对象，都可以通过重新赋值的方式将其改为自己的方法，同时为了避免正常功能的使用，通常执行完自己的代码后，还会调用源方法，实现原本的功能。
举例如下：
```javascript
let origin_alert = alert;
alert = function () {
    console.log(...arguments);
    return origin_alert(...arguments);
}
alert('hello javascript!');
```
上述代码Hook了alert方法，该方法用于实现浏览器的弹出提示，在alert原本功能上，增加了一段控制台输出，在浏览器控制台运行，即可实现在弹出框中显示消息的同时在控制台中输出信息。这种方法的大体思路为：将原方法保存到某个变量中，然后通过匿名函数重新定义方法，在执行完自己的逻辑后，再执行原方法的逻辑，通用框架如下：
```javascript
let origin_func = func_need_hook;

func_need_hook = function () {
    do_something();
    return origin_func(...arguments);
}
```

基于这个基本框架，可以通过更优雅一些的写法来实现，如下：
```javascript
function simpleHook(old_func, hook_func) {
    return function () {
        hook_func.apply(this, arguments); // 执行自定义的方法
        return old_func.apply(this, arguments);
    };
}

alert = simpleHook(alert, console.log); // Hook在原本的alert方法上，先使用console.log方法
alert('hello javascript!'); // 弹出提示并控制台输出
```

## 2.Hook原型方法
如果希望Hook所有DOM元素（Element）的setAttribute方法，需要通过原型链来实现。

在浏览器控制台运行以下代码：
```javascript
function simpleHook(old_func, hook_func) {
    return function () {
        hook_func.apply(this, arguments); // 执行自定义的方法
        return old_func.apply(this, arguments);
    };
}


function log() {
    console.log(`[setAttribute] - attributeName: ${arguments[0]}, value: ${arguments[1]}`);
}

Element.prototype.setAttribute = simpleHook(Element.prototype.setAttribute, log);
```

然后再修改元素属性，如下：
```javascript
document.body.setAttribute('name', 'body');
```
输出：
```
[setAttribute] - attributeName: name, value: body
```

对于这种一个方法对应多个对象、但希望通过Hook多个对象中这个方法的情况，可以找一下这个方法的来源，然后在来源上Hook它，其他对象都是继承该来源对象获得方法的，此时Hook源头上的方法就可以快速达到目的。

## 3.Hook Getter/Setter
如果需要快速定位某个Cookie生成何修改的情况，可以Hook Cookie对象的get方法和set方法：
- get方法：属性的getter方法，如果没有getter，则为undefined，当访问该属性时，会调用此方法。执行时不传入任何参数，但是会默认传入this对象。该方法的返回值会被用作属性的值。
- set方法：属性的setter方法，如果没有setter，则 undefined，当属性值被修改时，会调用此方法。该方法接受一个参数（也就是被赋予的新值），会同时传入赋值时的this对象。

对Cookies的Hook需要在网页一打开就执行Hook逻辑，将Cookies Hook住，从而获得网页开始到加载完成过程中，所有Cookies的变化都记录下来，为了快速便捷实现这个目的，可以在浏览器中使用油猴插件来注入JS。

JS脚本如下：
```javascript
// ==UserScript==
// @name         Hook Cookies
// @namespace    https://www.baidu.com/
// @version      2023-12-22
// @description  hook the cookies of baidu!
// @author       Corley
// @match        https://www.baidu.com/
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function () {
    'use strict';
    var cookie = document.cookie;
    Object.defineProperties(document, {
        cookie: {
            get: function () {
                console.trace('getter: ' + cookie);
                return cookie;
            },
            set: function (value) {
                console.trace('setter: ' + value);
                cookie = value;
            }
        }
    })
})();
```

上述脚本中使用`// @run-at  document-start`让油猴尽可能早地在打开浏览器时注入JS代码。定义好脚本并保存后，进入百度搜索页，打开控制台，可以发现很多日志，可以通过关键词过滤出setter相关的日志。
如果JS代码被压缩，可以在set()方法中加入debugger，通常在关注某个具体的cookie时，会判断每个设置的cookie，如果名字相符，就进入debugger进行调试，这样可以更直观地分析代码：
```javascript
// ==UserScript==
// @name         Hook Cookies
// @namespace    https://www.baidu.com/
// @version      2023-12-22
// @description  hook the cookies of baidu!
// @author       Corley
// @match        https://www.baidu.com/
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function () {
    'use strict';
    var cookie = document.cookie;
    Object.defineProperties(document, {
        cookie: {
            get: function () {
                console.trace('getter: ' + cookie);
                return cookie;
            },
            set: function (value) {
                if (value.includes('BA_HECTOR')) { // 判断cookie是否为BA_HECTOR，是则进入debugger
                    debugger;
                }
                console.trace('setter: ' + value);
                cookie = value;
            }
        }
    })
})();
```

一个用新cookie的第1个键替换旧cookie的脚本如下：
```javascript
// ==UserScript==
// @name         Hook Cookies
// @namespace    https://www.baidu.com/
// @version      2023-12-22
// @description  hook the cookies of baidu!
// @author       Corley
// @match        https://www.baidu.com/
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function () {
    'use strict';
    var cookie_cache = document.cookie;
    Object.defineProperty(document, 'cookie', {
        get: function () {
            return cookie_cache;
        },
        set: function (value) {
            console.log('Setting cookie: ', value);
            if (value.indexOf('BA_HECTOR') > -1) {
                debugger;
            }
            var cookie = value.split(';')[0]; // 新cookie中的第1个键值对
            var ncookie = cookie.split('=');
            var flag = false;
            var cache = cookie_cache.split('; ');
            cache = cache.map(function (item) {
                if (item.split('=')[0] === ncookie[0]) { // 旧cookie中存在新cookie中第1个键值对的键
                    flag = true;
                    return cookie; // 替换成新cookie中的第1个键值对
                }
                return item; // 否则继续使用旧键值对
            });
            cookie_cache = cache.join('; ');
            if (!flag) { // 如果新cookie中第1个键值对不存在于旧cookie中
                cookie_cache += cookie + '; '; // 则追加到旧cookie后面
            }
            return cookie_cache;
        }
    });
})();
```

## 4.使用Proxy与Reflect
基于Proxy与Reflect，我们可以对一个对象的所有操作都做一层Hook。
下面的Hook例子几乎实现了所有的方法：
```javascript
function ObjectHandler(name) {
    let handler = {
        get(target, property, receiver) {
            let result = Reflect.get(target, property, receiver);
            if (result instanceof Object) {
                if (typeof result === 'function') {
                    console.log(`[${name}]-[get] property: [${property}] - FUNCTION`);
                } else {
                    console.log(`[${name}]-[get] property: [${property}] - result: [${JSON.stringify(result)}]`);
                }
                return new Proxy(result, ObjectHandler(`${name}.${property}`)); // 多层代理
            }
            console.log(`[${name}]-[get] property: [${property.description ? property.description : property}] - result: [${result}]`);
            return result;
        },
        set(target, property, value, receiver) {
            if (value instanceof Object) {
                console.log(`[${name}]-[set] property: [${property}] - value: [${JSON.stringify(value)}]`);
            } else {
                console.log(`[${name}]-[set] property: [${property}] - value: [${value}]`);
            }
            return Reflect.set(target, property, value, receiver);
        },
        has(target, property) {
            var result = Reflect.has(target, property);
            console.log(`[${name}]-[has] property: [${property}] - result: [${result}]`);
            return result;
        },
        deleteProperty(target, property) {
            var result = Reflect.deleteProperty(target, property);
            console.log(`[${name}]-[deleteProperty] property: [${property}] - result: [${result}]`);
            return result;
        },
        getOwnPropertyDescriptor(target, property) { // 获取指定对象上一个自有属性对应的属性描述符
            var result = Reflect.getOwnPropertyDescriptor(target, property);
            console.log(`[${name}]-[getOwnPropertyDescriptor] property: [${property}] - result: [${JSON.stringify(result)}]`);
            return result;
        },
        defineProperty(target, property, attributes) { // 为一个对象定义一个新属性
            var result = Reflect.defineProperty(target, property, attributes);
            console.log(`[${name}]-[defineProperty] property: [${property}] - attributes: [${JSON.stringify(attributes)}] - result: [${result}]`);
            return result;
        },
        getPrototypeOf(target) { // 读取代理对象的原型
            var result = Reflect.getPrototypeOf(target);
            console.log(`[${name}]-[getPrototypeOf] - result: [${JSON.stringify(result)}]`);
            return result;
        },
        setPrototypeOf(target, proto) { // 设置代理对象的原型
            console.log(`[${name}]-[setPrototypeOf] proto: [${JSON.stringify(proto)}]`);
            return Reflect.setPrototypeOf(target, proto);
        },
        preventExtensions(target) { // 防止扩展
            console.log(`[${name}]-[preventExtensions]`);
            return Reflect.preventExtensions(target);
        },
        isExtensible(target) { // 判断是否可扩展
            var result = Reflect.isExtensible(target);
            console.log(`[${name}]-[isExtensible] - result: [${result}]`);
            return result;
        },
        ownKeys(target) { // 返回一个由目标对象自身可枚举属性组成的数组
            var result = Reflect.ownKeys(target);
            console.log(`[${name}]-[ownKeys] - result: [${JSON.stringify(result)}]`);
            return result;
        },
        apply(target, thisArg, argArray) { // 调用函数
            var result = Reflect.apply(target, thisArg, argArray);
            console.log(`[${name}]-[apply] function: [${target.name}] - argArray: [${argArray}] - result: [${result}]`);
            return result;
        },
        construct(target, argArray, newTarget) { // 调用构造函数
            var result = Reflect.construct(target, argArray, newTarget);
            console.log(`[${name}]-[construct] function: [${target.name}] - argArray: [${argArray}] - result: [${JSON.stringify(result)}]`);
            return result;
        }
    }
    return handler;
}

// Hook对象测试
function testProxy() {
    let person = {
        name: 'Corley',
        age: 18,
        sex: 'male',
        info: {
            address: 'Beijing',
            hobby: 'coding'
        },
        sayHello() {
            console.log('hello');
        },
        children: [
            {
                name: 'Jack',
                age: 10
            },
            {
                name: 'Tom',
                age: 12
            }
        ]
    }

    let proxy = new Proxy(person, ObjectHandler('Corley'));
    console.log(proxy.name);
    console.log(proxy.children);
    console.log(proxy.info);
    console.log(proxy.info.address);
    console.log('name' in proxy, 'gender' in proxy);
    proxy.sayHello();
    proxy.children[0].name = 'Jack2';
    console.log(proxy.children[0].name);
    console.log(proxy.children[0].age);
    console.log(proxy.children[1].name);
}

testProxy();
```

输出：
```javascript
[Corley]-[get] property: [name] - result: [Corley]
Corley                                                                                                                                            
[Corley]-[get] property: [children] - result: [[{"name":"Jack","age":10},{"name":"Tom","age":12}]]                                                
[ { name: 'Jack', age: 10 }, { name: 'Tom', age: 12 } ]                                                                                           
[Corley]-[get] property: [info] - result: [{"address":"Beijing","hobby":"coding"}]                                                                
{ address: 'Beijing', hobby: 'coding' }                                                                                                           
[Corley]-[get] property: [info] - result: [{"address":"Beijing","hobby":"coding"}]                                                                
[Corley.info]-[get] property: [address] - result: [Beijing]                                                                                       
Beijing                                                                                                                                           
[Corley]-[has] property: [name] - result: [true]                                                                                                  
[Corley]-[has] property: [gender] - result: [false]                                                                                               
true false                                                                                                                                        
[Corley]-[get] property: [sayHello] - FUNCTION                                                                                                    
hello                                                                                                                                             
[Corley.sayHello]-[apply] function: [sayHello] - argArray: [] - result: [undefined]                                                               
[Corley]-[get] property: [children] - result: [[{"name":"Jack","age":10},{"name":"Tom","age":12}]]                                                
[Corley.children]-[get] property: [0] - result: [{"name":"Jack","age":10}]                                                                        
[Corley.children.0]-[set] property: [name] - value: [Jack2]                                                                                       
[Corley.children.0]-[getOwnPropertyDescriptor] property: [name] - result: [{"value":"Jack","writable":true,"enumerable":true,"configurable":true}]
[Corley.children.0]-[defineProperty] property: [name] - attributes: [{"value":"Jack2"}] - result: [true]                                          
[Corley]-[get] property: [children] - result: [[{"name":"Jack2","age":10},{"name":"Tom","age":12}]]                                               
[Corley.children]-[get] property: [0] - result: [{"name":"Jack2","age":10}]                                                                       
[Corley.children.0]-[get] property: [name] - result: [Jack2]
Jack2
[Corley]-[get] property: [children] - result: [[{"name":"Jack2","age":10},{"name":"Tom","age":12}]]
[Corley.children]-[get] property: [0] - result: [{"name":"Jack2","age":10}]
[Corley.children.0]-[get] property: [age] - result: [10]
10
[Corley]-[get] property: [children] - result: [[{"name":"Jack2","age":10},{"name":"Tom","age":12}]]
[Corley.children]-[get] property: [1] - result: [{"name":"Tom","age":12}]
[Corley.children.1]-[get] property: [name] - result: [Tom]
Tom

```

因为浏览器环境中window对象无法改写、无法配置、无法枚举的特点，Proxy就比较少直接用于浏览器环境的Hook，很多对于window对象的操作Hook不到。
在浏览器环境中，我们将window对象置空\再打印，发现window对象没有改变，通过getOwnPropertyDescriptor方法获得window对象的属性描述，会发现其不可配置、不可写、不可枚举的描述。此时可以通过调用Object.defineProperties方法来修改对象属性的方式实现对window对象的Hook，如下：
```javascript
// 对window对象的selfProperty属性进行hook
Object.defineProperty(window, 'selfProperty', {
    get() {
        return 'Hello Window!';
    },
    set(value) {
        console.log('set selfProperty', value);
        debugger;
    }
});
```

在浏览器开发者工具的源代码中的片段Snippets中新建片段，将代码粘贴进去并运行代码，然后在控制台中输入window.selfProperty：
```bash
> window.selfProperty
'Hello Window!'
```

此时控制台输出了自定义的selfProperty属性值`Hello Window!`，说明成功Hook了window对象；如果修改属性值selfProperty，例如`window.selfProperty = 'hello';`，就会进入调试模式、并停在了`debugger;`处。