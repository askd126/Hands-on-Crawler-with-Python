/**
 * @description: 所有操作都实现Hook的对象代理
 * @param {string} name对象名
 */
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

module.exports = ObjectHandler;