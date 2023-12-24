# JavaScript原型链
## 1.原型
每一个函数都有一个 prototype 属性，这个属性是一个指针，指向一个对象，这个对象的用途是包含当前函数所有实例共享的属性和方法。简单来说，该函数实例化的所有对象的__proto__的属性指向这个对象，它是该函数所有实例化对象的原型。

```JavaScript
function Person(){};
Person.prototype.name = 'Corley';
Person.prototype.sayHello = function(){
    alert(`hello, I'm ${this.name}`);
};
```

## 2.对象的__proto__属性
调用构造函数创建一个新实例后，在这个实例的内部将包含一个指针，指向构造函数的原型对象，该指针即为[[Prototype]] ，所有对象都有[[Prototype]]属性，该属性指向其原型对象。在JavaScript标准中，没有方式可以访问[[Prototype]] ，但浏览器可以通过每个对象中的__proto__来访问[[Prototype]]。
```JavaScript
let student = new Person();
undefined
student.__proto__;
{name: 'Corley', sayHello: ƒ, constructor: ƒ}
student.__proto__ === Person.prototype;
true
```

`isPrototypeOf()`方法可以判断一个对象是否存在于另一个对象的原型链上。
```JavaScript
Person.prototype.isPrototypeOf(student);
true
```

## 3.原型属性
每当代码读取对象的某个属性时，首先会在对象本身搜索这个属性，如果找到该属性就返回该属性的值，如果没有找到，则继续搜索该对象对应的原型对象，以此类推下去。有了这样的搜索过程，因此如果在实例中添加一个属性时，这个属性就会屏蔽原型对象中保存的同名属性，因为在实例中搜索到该属性后就不会再向后搜索了。在属性存在的情况下，可以使用hasOwnProperty()方法来判断一个属性是存在与实例中，还是存在于原型中。
```JavaScript
let teacher = new Person();
undefined
teacher.name;
'Corley'
teacher.hasOwnProperty("name");
false
teacher.name = "James";
'James'
teacher.name;
'James'
teacher.hasOwnProperty("name");
true
```


构造函数，一旦声明，就会有与之关联的Prototype（原型对象）。
```JavaScript
typeof Person.prototype;
'object'
Person.prototype;
{name: 'Corley', sayHello: ƒ, constructor: ƒ}
```

构造函数有一个prototype属性引用其原型对象，被引用的原型对象也有一个constructor属性引用构造函数，两者构成一个循环。
```JavaScript
Person.prototype.constructor;
ƒ Person(){}
Person.prototype.constructor === Person;
true
```

正常的原型链都会终止于Object的原型对象，Object原型的原型是null。
```JavaScript
Person.prototype.__proto__;
{constructor: ƒ, __defineGetter__: ƒ, __defineSetter__: ƒ, hasOwnProperty: ƒ, __lookupGetter__: ƒ, …}
Person.prototype.__proto__ === Object.prototype;
true
Person.prototype.__proto__.constructor;
ƒ Object() { [native code] }
Person.prototype.__proto__.constructor === Object;
true
Person.prototype.__proto__.__proto__;
null
```

构造函数、原型对象和实例是3个完全不同的对象：
```JavaScript
student == Person;
false
student == Person.prototype;
false
Person == Person.prototype;
false
```

实例通过__proto__链接到原型对象，它实际上指向隐藏特性[[Prototype]]；构造函数通过prototype属性链接到原型对象；实例与构造函数没有直接联系，与原型对象有直接联系。
```JavaScript
student.__proto__ === Person.prototype;
true
Person.prototype.constructor === Person;
true
student.__proto__.constructor === Person;
true
```

同一个构造函数创建的两个实例共享同一个原型对象：
```JavaScript
student.__proto__ == teacher.__proto__;
true
```

instanceof检查实例的原型链中是否包含指定构造函数的原型：
```JavaScript
student instanceof Person;
true
student instanceof Object;
true
Person.prototype instanceof Object;
true
```

## 4.原型链
原型链作为实现继承的主要方法，其基本思想是利用的一个引用类型继承另一个引用类型的属性和方法。原型链的主要实现方法是让构造函数的prototype对象等于另一个类型的实例，此时的 prototype 对象因为是实例，因此将包含一个指向另一个原型的指针，相应地另一个原型中也包含着一个指向另一个构造函数的指针。假如另一个原型又是另一个类型的实例，那么上述关系依然成立，如此层层递进，就构成了实例与类型的链条。
```JavaScript
function Super() {};
undefined
function Middle() {};
undefined
function Sub() {};
undefined
Middle.prototype = new Super();
Super {}
Sub.prototype = new Middle();
Middle {}
let suber = new Sub();
undefined
Super.prototype.constructor === Super;
true
Super.prototype.__proto__ === Object.prototype;
true
Super.prototype.__proto__.__proto__ === null;
true
suber.__proto__ === Sub.prototype;
true
Sub.prototype.__proto__ === Middle.prototype;
true
Middle.prototype.__proto__ === Super.prototype;
true
```

## 5.方法覆盖
JavaScript通过原型链实现继承，继承就会涉及到子类方法覆盖父类方法的问题。
```JavaScript
function SuperType() {
    this.property = true;
};
SuperType.prototype.getSuperValue = function() {
    return this.property;
};
function SubType() {
    this.subproperty = false;
};
SubType.prototype = new SuperType();
SubType.prototype.getSubValue = function() {
    return this.subproperty;
};
SubType.prototype.getSuperValue = function() {
    return false;
};
let instance = new SubType();
instance.getSuperValue();
false
```

## 6.盗用构造函数
原型中包含引用类型的变量时，实例间会相互影响：
```JavaScript
function SuperType() {
    this.colors = ["red", "blue", "green"];
};
function SubType() {};
SubType.prototype = new SuperType();
let instance1 = new SubType();
instance1.colors.push("black");
4
instance1.colors;
(4) ['red', 'blue', 'green', 'black']
let instance2 = new SubType();
instance2.colors.push("white");
5
instance2.colors;
(5) ['red', 'blue', 'green', 'black', 'white']
instance1.colors;
(5) ['red', 'blue', 'green', 'black', 'white']
```

除此之外，子类型在实例化时不能给父类型的构造函数传参。

为了解决原型包含引用值导致的继承问题，JavaScript社区提出了盗用构造函数的技巧：在子类构造函数中调用父类构造函数，使用apply()和call()方法以新创建的对象为上下文执行构造函数。
```JavaScript
function SuperType() {
    this.colors = ["red", "blue", "green"];
};
function SubType() {
    SuperType.call(this);
};
undefined
let instance1 = new SubType();
instance1.colors.push("black");
instance1.colors;
(4) ['red', 'blue', 'green', 'black']
let instance2 = new SubType();
instance2.colors.push("white");
instance2.colors;
(4) ['red', 'blue', 'green', 'white']
```

相比于使用原型链，盗用构造函数的一个优点是可以在子类构造函数中向父类构造函数传参：
```JavaScript
function SuperType(name) {
    this.name = name;
    this.colors = ["red", "blue", "green"];
};
function SubType() {
    SuperType.call(this, "Corley");
    this.age = 20;
};
undefined
let instance = new SubType();
instance.colors.push("black");
instance1.colors;
(4) ['red', 'blue', 'green', 'black']
instance.name;
'Corley'
instance.age;
20
```

## 7.JavaScript原型链与Python继承方式的比较
JavaScript和Python都是广泛使用的编程语言，它们各自都有不同的继承机制。

### JavaScript 原型链继承
#### 优点：
1. **简单**：使用原型链可以相对简单地实现对象之间的继承关系。
2. **内存效率**：由于原型链上的属性和方法是共享的，所以对于那些不需要实例化的变量，这种方式能够节省内存。
3. **动态扩展**：原型链允许在运行时动态添加或修改属性和方法。

#### 缺点：
1. **查找性能**：通过原型链访问属性时，需要遍历整个链路，这可能导致性能问题，特别是当原型链很长时。
2. **引用类型的副作用**：如果子类对原型上引用类型的属性进行了修改，那么这些修改会影响到所有实例，因为引用类型是在原型上共享的。
3. **构造函数中的this问题**：在子类构造函数中调用父类构造函数时，需要使用`.call`或`.apply`来确保`this`指向正确。
4. **不能有效管理原型**：原型链的创建、维护和调试可能比其他继承方式更复杂。

### Python 类继承
#### 优点：
1. **清晰**：Python的类继承结构清晰，易于理解和编写。
2. **灵活性**：支持多重继承（一个类可以继承多个父类）。
3. **私有成员保护**：Python提供了专用名称修饰符，如`__name`，来隐藏或保护类的内部细节。
4. **元编程能力**：可以通过元类进一步自定义继承行为。

#### 缺点：
1. **复杂性**：多重继承可能会导致钻石问题（菱形继承），从而引入复杂的解析规则。
2. **内存效率**：每个实例都会有自己的副本，不共享基类的方法和属性，这可能导致内存消耗增加。
3. **面向对象范式严格**：Python的类继承模型更适合于严格的面向对象设计，可能不适合某些场景。

总结来说，JavaScript的原型链继承更适合动态且灵活的应用场景，而Python的类继承则更加适合遵循面向对象设计原则的大型项目。选择哪种继承方式取决于具体的应用需求和开发团队的习惯。