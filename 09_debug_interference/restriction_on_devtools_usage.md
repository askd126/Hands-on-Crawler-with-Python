# 限制开发者工具使用
## 1.禁用F12和鼠标右键
JavaScript可以监听键盘敲击和鼠标点击：
```JavaScript
// 禁止F12键盘事件
document.addEventListener('keydown', function (event) {
    console.log(event);
    if (event.keyCode === 123 || event.keyCode === 91) {
        return false;
    }
})

// 禁止右键、选择、复制
document.addEventListener('contextmenu', function (event) {
    return event.returnValue = false;
})
```

通过监听并打印的方式获取每个键对应的keyCode：
```JavaScript
// 监听键按下
document.addEventListener('keyup', function (event) {
    console.log('keyup: ', event);
});
// 监听可输入字符的键产生输入
document.addEventListener('keypress', function (event) {
    console.log('keypress: ', event);
});
// 监听释放键
document.addEventListener('keydown', function (event) {
    console.log('keydown: ', event);
});
```

## 2.DevTools检测
### （1）监听dom属性变化
```JavaScript
// 监听dom属性变化
function elementIdChecker() {
    let dom = document.createElement('div'); // 使用dom元素，在打开控制台时才会获取dom元素的id
    Object.defineProperty(dom, 'id', {
        get: function () { // 如果触发了get，则说明dom元素的属性被自动获取
            console.log('devtools open by get dom attr');
        }
    });
    console.log(dom.id);
}

// 控制台调用
elementIdChecker()
```

### （2）重写对象的toString方法
```JavaScript
// 重写对象的toString方法
var devtools = function () {
};
devtools.toString = function () {
    console.log('devtools open by rewrite toString');
};

// 控制台调用
console.log(devtools);
```

### （3）利用debugger来检测
```JavaScript
// 利用debugger来检测
let f = '(function() {let a = new Date(); debugger; return new Date() - a > 100;}())'
if (eval(f)) { // 如果进行了debug，会返回true
    console.log('devtools open by debugger');
}
```

### （4）检测页面宽度变化
```JavaScript
// 检测页面宽度和高度变化
function widthSizeCheck() {
    let threshold = 100;
    let widthDelta = window.outerWidth - window.innerWidth > threshold;
    let heightDelta = window.outerHeight - window.innerHeight > threshold;
    if (widthDelta || heightDelta) {
        console.log('devtools open by width and height change');
    }
}

window.addEventListener('resize', widthSizeCheck);
```

## 3.破解方法
监听dom属性变化和重写toString方法这两种监听方法都需要利用console方法进行打印，在打印时，涉及到控制台的特性，从而实现对devtools是否打开的监控。 所以，破解方法注入JS代码，清空控制台并重写console相关的方法：
```JavaScript
// 破解方法
function restore_devtools() {
    console.clear(); // 清空控制台
    for (let i in console) {
        if (typeof (console[i] === 'function')) {
            console[i] = function () { // 置空console中相关的方法
            };
        }
    }
}

restore_devtools();
```

具体实施时，一般需要通过借助浏览器的Overrides实现中间人攻击的方式来执行破解方法。