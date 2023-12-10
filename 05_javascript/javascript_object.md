# JavaScript对象
## 1.普通创建对象
构造函数创建：
```JavaScript
let person = new Object();
person.name = 'Corley';
person.age = 20;
person.sex = '男';
person.sayHello = function(){
    console.log(`hello, I'm ${this.name}`);
}
person.sayHello();
hello, I'm Corley
```

更常见的创建对象方式：
```JavaScript
let person = {
    name: 'Corley',
    age: 20,
    sex: '男',
    sayHello: function(){
        console.log(`hello, I'm ${this.name}`);
    }
}
person.sayHello();
hello, I'm Corley
```

## 2.工厂模式创建对象
使用Object构造函数或对象字面量可以方便地创建对象，但这些方式也有明显不足：创建具有同样接口的多个对象需要重复编写很多代码。工厂函数可以解决这个问题：
```JavaScript
function createPerson(name, age, sex){
    let person = new Object();
    person.name = name;
    person.age = age;
    person.sex = sex;
    person.sayHello = function(){
        console.log(`hello, I'm ${this.name}`);
    }
    return person;
};
undefined
let person1 = createPerson('Corley', 20, '男');
undefined
let person2 = createPerson('Kelly', 25, '女');
undefined
person1.sayHello();
hello, I'm Corley
undefined
person2.sayHello();
hello, I'm Kelly
```

## 3.构造函数创建对象
构造函数可以代替工厂函数，两者的内部实现也基本是一样的。构造函数实现如下：
```JavaScript
function Person(name, age, sex){
    this.name = name;
    this.age = age;
    this.sex = sex;
    this.sayHello = function(){
        console.log(`hello, I'm ${this.name}`);
    }
};
undefined
let person1 = new Person('Corley', 20, '男');
undefined
let person2 = new Person('Kelly', 25, '女');
undefined
person1.sayHello();
hello, I'm Corley
undefined
person2.sayHello();
hello, I'm Kelly
```

判断2个实例的类型：
```JavaScript
person1 instanceof Person;
true
person1 instanceof Object;
true
person2 instanceof Person;
true
person2 instanceof Object;
true
```

匿名构造函数实现相同效果：
```JavaScript
let Person = function(name, age, sex){
    this.name = name;
    this.age = age;
    this.sex = sex;
    this.sayHello = function(){
        console.log(`hello, I'm ${this.name}`);
    }
};
undefined
let person1 = new Person('Corley', 20, '男');
undefined
let person2 = new Person('Kelly', 25, '女');
undefined
person1.sayHello();
hello, I'm Corley
undefined
person2.sayHello();
hello, I'm Kelly
```

## 4.原型模式创建对象
构造函数虽然有用，但也存在问题，其定义的方法会在每个实例上都创建一遍，因此在前面的实现中，person1和person2虽然都有名为sayName的方法，但这两个方法并不是同一个Function实例，从逻辑上讲，构造函数实现如下：
```JavaScript
function Person(name, age, sex){
    this.name = name;
    this.age = age;
    this.sex = sex;
    this.sayHello = new Function("console.log(`hello, I'm ${this.name}`);");
};
```

验证如下：
```JavaScript
person1.sayHello == person2.sayHello;
false
```

每个Person实例都会有自己的Function实例用于输出name属性，不同实例上的函数虽然同名却不相等，但是因为实现的是相同的功能，所以没必要定义两个不同的Function实例，这样会浪费内存、占用资源。一种直观的解决办法是，将函数定义转移到构造函数外部。如下：
```JavaScript
function Person(name, age, sex){
    this.name = name;
    this.age = age;
    this.sex = sex;
    this.sayHello = sayHello;
}

function sayHello(){
    console.log(`hello, I'm ${this.name}`);
}
undefined
let person1 = new Person('Corley', 20, '男');
undefined
let person2 = new Person('Kelly', 25, '女');
undefined
person1.sayHello === person2.sayHello;
true
```

此时就实现了继承，即person1和person2共享了sayHello方法，因为sayHello方法是定义在构造函数外部的全局函数。但随之而来的问题是全局域被打乱。

## 5.原型模式创建对象
要解决上面的问题需要使用原型模式。原型模式的核心思想是：使用一个对象来保存另一个对象的属性和方法，从而实现继承。每个函数都会创建一个prototype属性，这个属性是一个对象，包含由特定引用类型的实例共享的属性和方法，这个对象就是通过调用构造函数创建的对象的原型。使用原型对象的好处是，在它上面定义的属性和方法可以被对象实例共享，原来在构造函数中直接赋给对象实例的值，可以直接赋值给它们的原型。
如下：
```JavaScript
function Person(){};
Person.prototype.name = 'Corley';
Person.prototype.age = 20;
Person.prototype.sex = '男';
Person.prototype.sayHello = function(){
    console.log(`hello, I'm ${this.name}`);
};
ƒ (){
    console.log(`hello, I'm ${this.name}`);
}
let person1 = new Person('Corley', 20, '男');
undefined
let person2 = new Person('Kelly', 25, '女');
undefined
person1.sayHello === person2.sayHello;
true
```

此时所有属性和方法都直接添加到了Person的prototype属性上，构造函数体中什么也没有。这样定义之后，调用构造函数创建的新对象仍然拥有相应的属性和方法，但与构造函数模式不同，使用原型模式定义的属性和方法是由所有实例共享的，因此person1和person2访问的属性和sayName()方法都是相同的。