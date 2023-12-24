# JavaScript代理与反射
## 1.空代理
最简单的代理是空代理，即除了作为一个抽象的目标对象，什么也不做。下面创建一个空代理，实现在代理对象上执行的任何操作实际上都会应用到目标对象：
```javascript
const target = {
    name: 'Corley',
    age: 18
}

const handler = {} // 空代理
const proxy = new Proxy(target, handler)

// name属性会访问同一个值
console.log(target.name) // Corley
console.log(proxy.name) // Corley

// 给目标属性赋值会同步反映在两个对象上，因为两个对象访问的是同一个值
target.name = 'Tom'
console.log(target.name) // Tom
console.log(proxy.name) // Tom

// hasOwnProperty方法会判断两个对象是否拥有相同的属性，即在两个地方都会应用到目标对象
console.log(target.hasOwnProperty('name')) // true
console.log(proxy.hasOwnProperty('name')) // true
```

输出：
```javascript
Corley
Corley
Tom   
Tom   
true  
true
```

## 2.定义捕获器（Trap）
使用代理的主要目的是可以定义捕获器（trap），捕获器就是在处理程序对象中定义的**基本操作的拦截器**。捕获器是一个对象，它包含了一些方法，这些方法会在特定的时间被调用，并接收到调用的上下文信息。捕获器可以用来拦截目标对象上的所有操作，并在这些操作执行前后做一些事情。 每个处理程序对象可以包含零个或多个捕获器，每个捕获器都对应一种基本操作，可以直接或间接在代理对象上调用。每次在代理对象上调用这些基本操作时，代理可以在这些操作传播到目标对象之前先调用捕获器函数，从而拦截并修改相应的行为。

下面创建一个get()捕获器，在访问目标对象的属性时，修改返回的属性值：
```javascript
const target = {
    name: 'Corley',
    age: 18
}

const handler = {
    get() {
        return 'handler override'
    }
}
const proxy = new Proxy(target, handler)

// name属性会得到不同的值
console.log(target.name) // Corley
console.log(proxy.name) // handler override
```

输出：
```javascript
Corley
handler override
```

当通过代理对象执行get()操作时，就会触发定义的get()捕获器。get()不是目标对象可以调用的方法，这个操作可以通过多种形式触发并被get()捕获器拦截到，包括`proxy[property]`、`proxy.property`、`Object.create(proxy)[property]`等操作都会触发基本的get()操作以获取属性，所有这些操作只要发生在代理对象上，就会触发get()捕获器。



## 3.反射Reflect
所有捕获器都可以访问相应的参数，基于这些参数可以重建被捕获方法的原始行为，比如，get()捕获器会接收到**目标对象**、**要查询的属性**和**代理对象**3个参数。

get()捕获器中传入3个参数如下：
```javascript
const target = {
    name: 'Corley',
    age: 18
}

const handler = {
    get(trapTarget, property, receiver) {
        console.log(trapTarget === target); // true
        console.log(property); // name
        console.log(receiver === proxy); // true
        return 'Tom';
    }
}
const proxy = new Proxy(target, handler)

console.log(target.name) // Corley
console.log(proxy.name) // Tom
```

输出：
```javascript
Corley
true
name
true
Tom
```

所有捕获器都可以基于自己的参数重建原始操作，可以通过调用全局Reflect对象上（封装了原始行为）的同名方法来轻松重建。处理程序对象中所有可以捕获的方法都有对应的反射（Reflect）API方法，这些方法与捕获器拦截的方法具有相同的名称和函数签名，而且也具有与被拦截方法相同的行为。

下面使用反射API定义出空代理对象：
```javascript
const target = {
    name: 'Corley',
    age: 18
}

const handler = {
    get() {
        return Reflect.get(...arguments) // 调用反射API Reflect.get将get方法的逻辑原封不动地执行
    }
}
const proxy = new Proxy(target, handler)

console.log(target.name) // Corley
console.log(proxy.name) // Corley
```

输出：
```javascript
Corley
Corley
```

反射API为开发者准备好了样板代码，在此基础上开发者可以用最少的代码修改捕获的方法。比如，下面实现了在某个属性被访问时、会对返回的值进行修饰：
```javascript
const target = {
    name: 'Corley',
    age: 18
}

const handler = {
    get(trapTarget, property, receiver) {
        let flag = '';
        if (property === 'name') {
            flag = '~~~';
        }
        return Reflect.get(...arguments) + flag // 调用反射API，进行修改再返回
    }
}
const proxy = new Proxy(target, handler)

console.log(target.name) // Corley
console.log(target.age) // 18
console.log(proxy.name) // Corley~~~
console.log(proxy.age) // 18
```

输出：
```javascript
Corley
18       
Corley~~~
18  
```

## 4.代理的限制
### （1）捕获器不变式
使用捕获器几乎可以改变所有基本方法的行为，每个捕获的方法都知道目标对象上下文、捕获函数签名，但捕获处理程序的行为必须遵循捕获器不变式（trap invariant）。捕获器不变式因方法不同而异，但通常都会防止捕获器定义出现过于反常的行为。比如，如果目标对象有一个不可配置且不可写的数据属性，那么在捕获器返回一个与该属性不同的值时，会抛出TypeError:
```javascript
const target = {}
Object.defineProperty(target, 'name', {
    value: 'Corley',
    writable: false,
    configurable: false
})

const handler = {
    get() {
        return 'Tom'
    }
}
const proxy = new Proxy(target, handler)

console.log(target.name) // Corley
console.log(proxy.name) // TypeError
```
其中，Object.defineProperty主要给对象的属性添加特性描述，包括是否只读不可以写、是否可以被for..in或 Object.keys()遍历等，目前提供两种形式，分别为数据属性和访问器属性。
输出：
```javascript
XXX\Hands-on Crawler with Python\10_javascript_obfuscation_and_reversal\proxy.js:16
console.log(proxy.name)
                  ^

TypeError: 'get' on proxy: property 'name' is a read-only and non-configurable data property on the proxy target but the proxy did not return it
s actual value (expected 'Corley' but got 'Tom')
    at Object.<anonymous> (XXX\Hands-on Crawler with Python\10_javascript_obfuscation_and_reversal\proxy.js:16:19)
    at Module._compile (node:internal/modules/cjs/loader:1376:14)
    at Module._extensions..js (node:internal/modules/cjs/loader:1435:10)
    at Module.load (node:internal/modules/cjs/loader:1207:32)
    at Module._load (node:internal/modules/cjs/loader:1023:12)
    at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:135:12)
    at node:internal/main/run_main_module:28:49
```

### （2）代理中的this
方法中的this通常指向调用这个方法的对象。举例如下：
```javascript
const target = {
    thisValueEqualProxy() {
        return this === proxy;
    }
}

const proxy = new Proxy(target, {})

console.log(target.thisValueEqualProxy()) // false
console.log(proxy.thisValueEqualProxy()) // true
```

输出：
```javascript
false
true
```

在代理对象中，this指向代理对象本身，而不是目标对象。

### （3）代理与内部槽位
代理与内置引用类型的实例通常可以很好地协同，比如Array，但有些内置类型可能会依赖代理无法控制的机制，结果导致在代理上调用某些方法会出错，典型的例子就是Date类型。 根据ECMAScript规范，Date类型方法的执行依赖this值上的内部槽位`[[NumberDate]]`，代理对象上不存在这个内部槽位，而且这个内部槽位的值也不能通过普通的get()和 set()操作访问到，于是代理拦截后本应转发给目标对象的方法会抛出TypeError：
```javascript
const target = new Date();
const proxy = new Proxy(target, {})

console.log(proxy instanceof Date) // true
console.log(proxy.getDate()) // TypeError
```
输出：
```javascript
true
21
XXX\Hands-on Crawler with Python\10_javascript_obfuscation_and_reversal\proxy.js:5
console.log(proxy.getDate()) // TypeError
                  ^

TypeError: this is not a Date object.
    at Proxy.getDate (<anonymous>)
    at Object.<anonymous> (XXX\Hands-on Crawler with Python\10_javascript_obfuscation_and_reversal\proxy.js:5:19)
    at Module._compile (node:internal/modules/cjs/loader:1376:14)
    at Module._extensions..js (node:internal/modules/cjs/loader:1435:10)
    at Module.load (node:internal/modules/cjs/loader:1207:32)
    at Module._load (node:internal/modules/cjs/loader:1023:12)
    at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:135:12)
    at node:internal/main/run_main_module:28:49
```

## 取消代理
对于使用new Proxy()创建的普通代理来说，这种代理联系会在代理对象的生命周期内一直持续存在。Proxy暴露了revocable()方法用来撤销代理对象与目标对象的关联，同时操作是不可逆的，撤销代理之后再调用代理会抛出TypeError。同时，撤销函数（revoke()）是幂等的，调用多少次的结果都一样。

示例如下：
```javascript
const target = {
    name: 'Corley',
    age: 18
}

const handler = {
    get() {
        return 'Tom'
    }
}

const {proxy, revoke} = Proxy.revocable(target, handler)
console.log(target.name) // Corley
console.log(proxy.name) // Tom
revoke()
console.log(proxy.name) // TypeError
```

输出：
```javascript
Corley
Tom
XXX\Hands-on Crawler with Python\10_javascript_obfuscation_and_reversal\proxy.js:16
console.log(proxy.name) // TypeError
                  ^

TypeError: Cannot perform 'get' on a proxy that has been revoked
    at Object.<anonymous> (XXX\Hands-on Crawler with Python\10_javascript_obfuscation_and_reversal\proxy.js:16:19)
    at Module._compile (node:internal/modules/cjs/loader:1376:14)
    at Module._extensions..js (node:internal/modules/cjs/loader:1435:10)
    at Module.load (node:internal/modules/cjs/loader:1207:32)
    at Module._load (node:internal/modules/cjs/loader:1023:12)
    at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:135:12)
    at node:internal/main/run_main_module:28:49
```

## 6.反射API
### （1）反射API与对象API
在使用反射API时，要记住:
- 反射API并不限于捕获处理程序。
- 大多数反射API方法在Object类型上有对应的方法。
- 通常，Object上的方法适用于通用程序，而反射方法适用于细粒度的对象控制与操作。

### （2）状态标记
很多反射方法返回称作**状态标记**的布尔值，表示意图执行的操作是否成功。有时候，状态标记比那些返回修改后的对象或者抛出错误（取决于方法）的反射API方法更有用。

普通的捕获异常方法如下：
```javascript
const o = {};

try {
    Object.defineProperty(o, 'name', 'Corley');
    console.log('success');
} catch (e) {
    console.log('failure');
}
```

输出：
```javascript
failure
```

Object.defineProperty方法设置o对象的name属性报错时，会被catch捕捉。反射API的状态标记方法如下：
```javascript
const o = {};

if (Reflect.defineProperty(o, 'name', {value: 'Corley'})) {
    console.log('success');
} else {
    console.log('failure');
}
```

输出：
```javascript
success
```

以下反射方法都会提供状态标记:
- Reflect.defineProperty()
- Reflect.preventExtensions()
- Reflect.setPrototypeOf()
- Reflect.set()
- Reflect.deleteProperty()

### （3）用一等函数替代操作符
以下反射方法提供只有通过操作符才能完成的操作：
- Reflect.get()：可以替代对象属性访问操作符。
- Reflect.set()：可以替代=赋值操作符。
- Reflect.has()：可以替代in操作符或with()。
- Reflect.deleteProperty()：可以替代delete操作符。
- Reflect.construct()：可以替代new操作符。

### 安全地应用函数
在通过apply方法调用函数时，被调用的函数可能也定义了自己的apply属性（虽然可能性极小）。为了绕过这个问题，可以调用定义在Function原型上的apply方法，比如`Function.prototype.apply.call(func, thisVal, argumentList);`，也可以使用Reflect.apply来避免，即`Reflect.apply(func, thisVal, argumentsList);`。可以说，能用Reflect相关的API就直接用。