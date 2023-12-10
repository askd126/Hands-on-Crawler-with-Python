# JavaScript入门
## 1.基本语法
赋值语句：
```JavaScript
var name = "Corley";
undefined
name
'Corley'
```

语句块：
```JavaScript
if (true) {
    x = 1;
    y = 2;
    z = 3;
}
3
```

注释：
```JavaScript
/*
多行注释
*/

// 单行注释
alert("Hello, world!");
```

## 2.Number数值
```JavaScript
1;
1
-1;
-1
3.14159e5
314159
NaN;
NaN
Infinity;
Infinity
```

四则运算：
```JavaScript
(1 + 2) - 3 * 4 / 5 % 6
0.6000000000000001
```

# 3.String字符串
定义字符串：
```JavaScript
var s = 'hello, world!';
undefined
s.length;
13
```

字符串索引：
```JavaScript
s[0];
'h'
s[5];
','
s[9];
'r'
s[12];
'!'
s[13];
undefined
```
索引超出范围会返回undefined。

字符串是不可变的：
```JavaScript
s[0] =  'H';
'H'
s
'hello, world!'
```

转为大写：
```JavaScript
s.toUpperCase();
'HELLO, WORLD!'
```

转为小写：
```JavaScript
s.toLowerCase();
'hello, world!'
```

索引子串：
```JavaScript
s.indexOf('world');
7
s.indexOf('World');
-1
```

获取子串：
```JavaScript
s.substring(0, 6)
'hello,'
s.substring(9)
'rld!'
```

字符串拼接：
```JavaScript
var name = 'Corley';
var age = 20;
var message = 'My name is '+ name + ', I am '+ age +' years old.';
alert(message);
```

模板字符串：
```JavaScript
var name = 'Corley';
var age = 20;
var message = `My name is ${name}, I am ${age} years old.`;
alert(message);
```

## 4.Boolean布尔值和比较运算
基本布尔值：
```JavaScript
true;
true
false;
false
2 / 3 > 0.66;
true
2 / 3 <= 0.66;
false
```

逻辑运算：
```JavaScript
// 与运算
true && true;
true
true && false;
false
false && true && false;
false
// 或运算
false || false;
false
true || false;
true
false || true || false;
true
// 非运算
!true;
false
!false;
true
!(2 > 3);
true
```

比较运算：
```JavaScript
3 > 5;
false
3 <= 5;
true
3 == 3;
true
'3' == 3;
true
'3' === 3;
false
false == 0;
true
false === 0;
false
1 / 3 == (1 - 2 / 3);
false
1 / 3 === (1 - 2 / 3);
false
Math.abs(1 / 3 - (1 - 2 / 3)) < 1e-8;
true
```

## 5.数组
定义数组：
```JavaScript
var arr = [550, 'JiYue', null, true];
undefined
arr[0]
550
arr[3]
true
arr[5]
undefined
```

使用Array函数定义数组：
```JavaScript
var arr = Array(550, 'JiYue', null, true); // 等价于var arr = new Array(550, 'JiYue', null, true)
undefined
arr[0]
550
arr[3]
true
arr[5]
undefined
```

索引元素：
```JavaScript
arr.indexOf(550);
0
arr.indexOf('JiYue');
1
arr.indexOf('JiKe');
-1
```

截取数组：
```JavaScript
arr.slice()
(4)[550, 'JiYue', null, true]
arr.slice(2, 5)
(2)[null, true]
```

添加、删除元素：
```JavaScript
arr.push('JiKe', 650);
6
arr;
(6)[550, 'JiYue', null, true, 'JiKe', 650]
arr.pop();
650
arr;
(5)[550, 'JiYue', null, true, 'JiKe']
```

多维数组：
```JavaScript
var arr = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
];
undefined
arr;
(3)[Array(3), Array(3), Array(3)]
0: (3)[1, 2, 3]
1: (3)[4, 5, 6]
2: (3)[7, 8, 9]
arr[0][0] + arr[1][2];
7
```

## 6.对象
定义和访问对象：
```JavaScript
var person = {
    name: 'Corley',
    age: 20,
    isMale: true,
    height: 1.75,
    weight: 65,
    sayHello: function() {
        alert('Hello,'+ this.name + '!');
    }
};
undefined
person
{name: 'Corley', age: 20, isMale: true, height: 1.75, weight: 65, …}
person.age
20
person.height
1.75
```

# 7.函数
定义函数：
```JavaScript
function abs(x) {
    if (x >= 0) {
        return x;
    } else {
        return -x;
    }
};
undefined
abs(-3.14);
3.14
```

匿名函数：
```JavaScript
var abs = function(x) {
    if (x >= 0) {
        return x;
    } else {
        return -x;
    }
};
undefined
abs(-3.14);
3.14
```

变量提升：
```JavaScript
function sayHello() {
    var message = `Hello, ${name}`;
    console.log(message);
    var name = 'Corley';
};
undefined
sayHello();
Hello, undefined
undefined
```

等价于：
```JavaScript
function sayHello() {
    var name;
    var message = `Hello, ${name}`;
    console.log(message);
    name = 'Corley';
};
undefined
sayHello();
Hello, undefined
undefined
```