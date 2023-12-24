# JavaScript函数进阶
## 1.函数属性
每个函数都有两个属性length和prototype，其中length属性保存函数定义的命名参数的个数。
```JavaScript
function sayName(name) {
    console.log(name);
};
undefined
sayName.length;
1
function sum(num1, num2) {
    return num1 + num2;
};
undefined
sum.length;
2
function sayHi() {
    console.log('Hi');
};
undefined
sayHi.length;
0
```
prototype用于保存引用类型所有实例方法，因此toString()、valueOf()等方法实际上都保存在prototype上，进而由所有实例共享。

## 2.函数方法
函数有两个方法apply()和call()，这两个方法都会以指定的this值来调用函数，即会设置调用函数时函数体内this对象的值。

apply()方法接收两个参数：函数内this的值和一个参数数组，其中第2个参数可以是Array的实例，也可以是arguments对象。
```JavaScript
function sum(num1, num2) {
    return num1 + num2;
};
undefined
function callSum1(num1, num2) {
    return sum.apply(this, [num1, num2]);
};
undefined
callSum1(12, 21);
33
function callSum2(num1, num2) {
    return sum.apply(this, arguments);
};
undefined
callSum2(12, 21);
33
```

call()方法与apply()的作用一样，只是传参的形式不同：第一个参数跟apply()一样，也是this值；剩下的要传给被调用函数的参数则是逐个传递的，即必须将参数一个一个地列出来。
```JavaScript
unction sum(num1, num2) {
    return num1 + num2;
};
undefined
function callSum(num1, num2) {
    return sum.call(this, num1, num2);
};
undefined
callSum(12, 21);
33
```

apply()和call()真正强大之处是控制函数调用上下文即函数体内this值的能力。
```JavaScript
window.color = 'red';
'red'
let obj = {
    color:  'blue'
};
undefined
function sayColor() {
    console.log(this.color);
};
undefined
sayColor();
red
undefined
sayColor.call(this);
red
undefined
sayColor.call(window);
red
undefined
sayColor.call(obj);
blue
undefined
```

使用call()或apply()的好处是可以将任意对象设置为任意函数的作用域，这样对象可以不用关心方法。

## 3.自执行函数
普通自执行函数：
```JavaScript
function f(i) {
    console.log(i);
}(5);
5
```

匿名函数式：
```JavaScript
(function(x, y) {
    return x + y;
})(12, 21);
33
```
等价于：
```JavaScript
(function(x,  y) {return x + y;}(12, 21));
33
```

感叹号式：
```JavaScript
!function(x, y) {
    return x + y;
}(12, 21);
false
```

运算符式：
```JavaScript
+function(x, y) {
    return x + y;
}(12, 21);
33
-function(x, y) {
    return x + y;
}(12, 21);
-33
++function(x, y) {
    return x + y;
}(12, 21);
--function(x,y){
    return x+y;
}(3,4);
```

波浪符式：
```JavaScript
~function(x, y) {
    return x + y;
}(12, 21);
-34
```