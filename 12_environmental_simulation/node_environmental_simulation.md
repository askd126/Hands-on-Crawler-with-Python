# Node环境模拟
## 1.补Canvas环境
Node中不自带canvas，需要模拟。如下：
```javascript
// 补window对象
window = global;

// 补document对象的createElement方法
window.document = {
    createElement: function (tag) {
        return canvas;
    }
};
// 补canvas对象
var canvas = {
    getContext: function (type) {
        return CanvasRenderingContext2D;
    },
    toDataURL: function () {
        return 'data:image/png;base64,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';
    }
};
// 补CanvasRenderingContext2D对象
var CanvasRenderingContext2D = {
    textBaseline: 'top',
    fillStyle: '#fff',
    fillRect: function (x, y, w, h) {
    },
    fillText: function (txt, x, y) {
    }
};

// 使用模拟好的canvas创建图片
function create_canvas() {
    /**
     * 绘制canvas，并转为Base64编码后进行MD5签名
     */
    let canvas = document.createElement('canvas');
    let cv = canvas.getContext('2d'); // 2D绘图对象
    let txt = 'Hello Canvas';
    cv.textBaseline = 'top';
    cv.fillStyle = '#fff';
    cv.fillRect(200, 1, 50, 50); // 坐标(200,1)、宽高均为50的正方形
    cv.fillText(txt, 1, 15); // 绘制文本
    let image = canvas.toDataURL();
    return image;
}

console.log(create_canvas());
```

输出：
```javascript
data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASwAAACWCAYAAABkW7XSAAAAAXNSR0IArs4c6QAAB0tJREFUeF7t2j+LXVUYhfF3d7Z2NikEP4CgtoKVhZVGsdJSbMRKEWwsxV
RiI9pp6b/KOo2dEfwAgoUKNmKp3Xb25Zx4uU4mIwRmvclvIEyYzJy75llrHvY5k1HeEEAAgSYERpOcYiJwJQTmnPNKXvgev+gY4774Wb8vvol73K3LIXCbAGFljYGwsvqQJowAYWUVQlhZfU
gTRoCwsgohrKw+pAkjQFhZhRBWVh/ShBEgrKxCCCurD2nCCBBWViGEldWHNGEECCurEMLK6kOaMAKElVUIYWX1IU0YAcLKKoSwsvqQJowAYWUVQlhZfUgTRoCwsgohrKw+pAkjQFhZhRBWVh
/ShBEgrKxCDsKacz5XVR9V1RtjjG+3j71ZVa9V1atjjB/Oi332dd9X1c2q+u1un3vB1z+5/dvfVfXOGOPDLETSPMgECCur/SsT1ia7OhPkU1lIpEHgXwKElbWGKxHWnPOup7csTNI8qAQIK6
v5Y2F9XlUPn8T7uapeWreE24lov327McZ4+063hCefe/sa+7XnnF+vv48xXjjFscns/ap66OwW8XCbWFXfVdVnVfVLVT27fc2N7f2LRxkP193ent/eH16/qh6pqv17/LOqXtlvf7MqkSaJAG
EltVF1qRNWVb27C+b4edfZx947fYa1fe61/VbvPDldJKxjPHPOD6rqmap6vaq+OHvG9se67snHl8g+qaqfTp/DrWsdSfWxO0kyqxJpkggQVlIblxfWx1W1n67Wd3A4odxBWOtzb64T2CaMdf
t3fYzx9NEJ6yCi855fnZyw1pfc2oR1ENN6KH98S1lVL29SWw//D9fchLifsNY19hPhOoGtj9/y7CxriKlpCCurmf99wjo5Af3nt4SXPGE9sZ2YftxvC+ecS0jrt5HXq+qrTUxLMNfuIqx1q7
d+w/nX0UlrnfzWqWy9rZPZl0cCXa99W35ZdUiTRoCwshq5rLD2H/xHt/iHE8oln2Gde5qZc+7S2q/5zZLXdrv31vY6v1fVrxcJa3u+tsT2+DnP29YzsPXn06pat4T7qcsJK2uHsWkIK6sa/3
E0qw9pwggQVlYhhJXVhzRhBAgrqxDCyupDmjAChJVVCGFl9SFNGAHCyiqEsLL6kCaMAGFlFUJYWX1IE0aAsLIKIaysPqQJI0BYWYUQVlYf0oQRIKysQggrqw9pwggQVlYhhJXVhzRhBAgrqx
DCyupDmjAChJVVCGFl9SFNGAHCyiqEsLL6kCaMAGFlFUJYWX1IE0aAsLIKIaysPqQJI0BYWYUQVlYf0oQRIKysQggrqw9pwggQVlYhhJXVhzRhBAgrqxDCyupDmjAChJVVCGFl9SFNGAHCyi
qEsLL6kCaMAGFlFUJYWX1IE0aAsLIKIaysPqQJI0BYWYUQVlYf0oQRIKysQggrqw9pwggQVlYhhJXVhzRhBAgrqxDCyupDmjAChJVVCGFl9SFNGAHCyiqEsLL6kAYBBC4gQFjmgQACbQgQVp
uqBEUAAcKyAQQQaEOAsNpUJSgCCBCWDSCAQBsChNWmKkERQICwbAABBNoQIKw2VQmKAAKEZQMIINCGAGG1qUpQBBAgLBtAAIE2BAirTVWCIoAAYdkAAgi0IUBYbaoSFAEECMsGEECgDQHCal
OVoAggQFg2gAACbQgQVpuqBEUAAcKyAQQQaEOAsNpUJSgCCBCWDSCAQBsChNWmKkERQICwbAABBNoQIKw2VQmKAAKEZQMIINCGAGG1qUpQBBAgLBtAAIE2BAirTVWCIoAAYdkAAgi0IUBYba
oSFAEECMsGEECgDQHCalOVoAggQFg2gAACbQgQVpuqBEUAAcKyAQQQaEOAsNpUJSgCCBCWDSCAQBsChNWmKkERQICwbAABBNoQIKw2VQmKAAKEZQMIINCGAGG1qUpQBBAgLBtAAIE2BAirTV
WCIoAAYdkAAgi0IUBYbaoSFAEECMsGEECgDQHCalOVoAggQFg2gAACbQgQVpuqBEUAAcKyAQQQaEOAsNpUJSgCCBCWDSCAQBsChNWmKkERQICwbAABBNoQIKw2VQmKAAKEZQMIINCGAGG1qU
pQBBAgLBtAAIE2BAirTVWCIoAAYdkAAgi0IUBYbaoSFAEECMsGEECgDQHCalOVoAggQFg2gAACbQgQVpuqBEUAAcKyAQQQaEOAsNpUJSgCCBCWDSCAQBsChNWmKkERQICwbAABBNoQIKw2VQ
mKAAKEZQMIINCGAGG1qUpQBBAgLBtAAIE2BAirTVWCIoAAYdkAAgi0IUBYbaoSFAEECMsGEECgDQHCalOVoAggQFg2gAACbQgQVpuqBEUAAcKyAQQQaEOAsNpUJSgCCBCWDSCAQBsChNWmKk
ERQICwbAABBNoQIKw2VQmKAAKEZQMIINCGAGG1qUpQBBAgLBtAAIE2BAirTVWCIoAAYdkAAgi0IUBYbaoSFAEECMsGEECgDQHCalOVoAggQFg2gAACbQgQVpuqBEUAgX8A8Pj/pllcRS8AAA
AASUVORK5CYII=
```

## 2.LocalStorage
window.localstorage可以将数据保存在浏览器会话中，它与sessionStorage类似，但sessionStorage在页面关闭时，存储在sessionStorage的数据会被清除，localStorage数据却可以长期保留。localStorage通过setItem添加元素、getItem获取元素、removeItem删除元素。

对LocalStorage补环境如下：
```javascript
// 补window对象
window = global;

// 补windows对象的localStorage对象
window.localStorage = {
    setItem: function (key, value) {
        this[key] = value.toString(); // 转为字符串
    },
    getItem: function (key) {
        return this[key] ? this[key] : null;
    },
    removeItem: function (key) {
        delete this[key];
    }
};

// 使用localStorage
console.log(localStorage);
localStorage.setItem('name', 'Corley');
console.log(localStorage);
console.log(localStorage.getItem('name'));
console.log(localStorage.getItem('age'));
localStorage.removeItem('name');
console.log(localStorage);
console.log(localStorage.getItem('name'));
```

输出：
```javascript
{                                   
  setItem: [Function: setItem],     
  getItem: [Function: getItem],     
  removeItem: [Function: removeItem]
}                                   
{                                    
  setItem: [Function: setItem],      
  getItem: [Function: getItem],      
  removeItem: [Function: removeItem],
  name: 'Corley'                     
}                                    
Corley                               
null
{
  setItem: [Function: setItem],
  getItem: [Function: getItem],
  removeItem: [Function: removeItem]
}
null
```

## 3.相对完善的补环境方案
一个相对比较完善的补环境方案会将常见的环境都补上，如果在使用时还存在没有补的环境，可以使用JS Hook定位并手动完善。一个常见的补环境方案如下：
```javascript
/**
 * 较完善的补环境方案
 */

window = {
    document: {
        cookie: "",
        createElement: function (tag) {
            if (tag == "canvas") {
                return canvas
            } else if (tag == "caption") {
                return {
                    tagName: "CAPTION"
                }
            }

        },
        getElementById: function () {
            return false
        },
        title: ""
    },
    moveBy: function () {
    },
    moveTo: function () {
    },
    open: function () {
    },
    dispatchEvent: function () {
        return true
    },
    screen: {
        availHeight: 824,
        availWidth: 1536
    },
    navigator: {
        cookieEnabled: true,
        language: "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        appVersion: "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
    },
    decodeURI: global.decodeURI,
    location: {
        hostname: "www.baidu.com",
        href: "https://www.baidu.com/"
    },
    OfflineAudioContext: function () {
        this.createOscillator = function () {
            return {
                frequency: {
                    setValueAtTime: function () {
                    }
                },
                connect: function () {
                },
                start: function () {
                },
            }
        },
            this.createDynamicsCompressor = function () {
                return {
                    threshold: {
                        setValueAtTime: function () {
                        },
                    },
                    setValueAtTime: function () {
                    },
                    knee: {
                        setValueAtTime: function () {
                        },
                    },
                    ratio: {
                        setValueAtTime: function () {
                        },
                    },
                    reduction: {
                        setValueAtTime: function () {
                        },
                    },
                    attack: {
                        setValueAtTime: function () {
                        },
                    },
                    release: {
                        setValueAtTime: function () {
                        },
                    },
                    connect: function () {
                    },
                }
            },
            this.startRendering = function () {
            }
    },
    eval: global.eval,
    history: {length: 2},
    outerHeight: 1027,
    innerHeight: 362,
    outerWidth: 1825,
    innerWidth: 1777,
    Math: global.Math,
    Date: global.Date,
}
window.open.toString = function () {
    return "function open() { [native code] }"
};
document = window.document;
navigator = window.navigator;
screen = window.screen;
canvas = {
    getContext: function getContext() {
        return CanvasRenderingContext2D
    },
    toDataURL: function toDataURL() {
        // 实际为canvas画布填充了“"k54kk5cA4*"”字样后，转成的图片链接
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASwAAACWCAYAAABkW7XSAAAAAXNSR0IArs4c6QAAB0tJREFUeF7t2j+LXVUYhfF3d7Z2NikEP4CgtoKVhZVGsdJSbMRKEWwsxV\n" +
            "RiI9pp6b/KOo2dEfwAgoUKNmKp3Xb25Zx4uU4mIwRmvclvIEyYzJy75llrHvY5k1HeEEAAgSYERpOcYiJwJQTmnPNKXvgev+gY4774Wb8vvol73K3LIXCbAGFljYGwsvqQJowAYWUVQlhZfU\n" +
            "gTRoCwsgohrKw+pAkjQFhZhRBWVh/ShBEgrKxCCCurD2nCCBBWViGEldWHNGEECCurEMLK6kOaMAKElVUIYWX1IU0YAcLKKoSwsvqQJowAYWUVQlhZfUgTRoCwsgohrKw+pAkjQFhZhRBWVh\n" +
            "/ShBEgrKxCDsKacz5XVR9V1RtjjG+3j71ZVa9V1atjjB/Oi332dd9X1c2q+u1un3vB1z+5/dvfVfXOGOPDLETSPMgECCur/SsT1ia7OhPkU1lIpEHgXwKElbWGKxHWnPOup7csTNI8qAQIK6\n" +
            "v5Y2F9XlUPn8T7uapeWreE24lov327McZ4+063hCefe/sa+7XnnF+vv48xXjjFscns/ap66OwW8XCbWFXfVdVnVfVLVT27fc2N7f2LRxkP193ent/eH16/qh6pqv17/LOqXtlvf7MqkSaJAG\n" +
            "EltVF1qRNWVb27C+b4edfZx947fYa1fe61/VbvPDldJKxjPHPOD6rqmap6vaq+OHvG9se67snHl8g+qaqfTp/DrWsdSfWxO0kyqxJpkggQVlIblxfWx1W1n67Wd3A4odxBWOtzb64T2CaMdf\n" +
            "t3fYzx9NEJ6yCi855fnZyw1pfc2oR1ENN6KH98S1lVL29SWw//D9fchLifsNY19hPhOoGtj9/y7CxriKlpCCurmf99wjo5Af3nt4SXPGE9sZ2YftxvC+ecS0jrt5HXq+qrTUxLMNfuIqx1q7\n" +
            "d+w/nX0UlrnfzWqWy9rZPZl0cCXa99W35ZdUiTRoCwshq5rLD2H/xHt/iHE8oln2Gde5qZc+7S2q/5zZLXdrv31vY6v1fVrxcJa3u+tsT2+DnP29YzsPXn06pat4T7qcsJK2uHsWkIK6sa/3\n" +
            "E0qw9pwggQVlYhhJXVhzRhBAgrqxDCyupDmjAChJVVCGFl9SFNGAHCyiqEsLL6kCaMAGFlFUJYWX1IE0aAsLIKIaysPqQJI0BYWYUQVlYf0oQRIKysQggrqw9pwggQVlYhhJXVhzRhBAgrqx\n" +
            "DCyupDmjAChJVVCGFl9SFNGAHCyiqEsLL6kCaMAGFlFUJYWX1IE0aAsLIKIaysPqQJI0BYWYUQVlYf0oQRIKysQggrqw9pwggQVlYhhJXVhzRhBAgrqxDCyupDmjAChJVVCGFl9SFNGAHCyi\n" +
            "qEsLL6kCaMAGFlFUJYWX1IE0aAsLIKIaysPqQJI0BYWYUQVlYf0oQRIKysQggrqw9pwggQVlYhhJXVhzRhBAgrqxDCyupDmjAChJVVCGFl9SFNGAHCyiqEsLL6kAYBBC4gQFjmgQACbQgQVp\n" +
            "uqBEUAAcKyAQQQaEOAsNpUJSgCCBCWDSCAQBsChNWmKkERQICwbAABBNoQIKw2VQmKAAKEZQMIINCGAGG1qUpQBBAgLBtAAIE2BAirTVWCIoAAYdkAAgi0IUBYbaoSFAEECMsGEECgDQHCal\n" +
            "OVoAggQFg2gAACbQgQVpuqBEUAAcKyAQQQaEOAsNpUJSgCCBCWDSCAQBsChNWmKkERQICwbAABBNoQIKw2VQmKAAKEZQMIINCGAGG1qUpQBBAgLBtAAIE2BAirTVWCIoAAYdkAAgi0IUBYba\n" +
            "oSFAEECMsGEECgDQHCalOVoAggQFg2gAACbQgQVpuqBEUAAcKyAQQQaEOAsNpUJSgCCBCWDSCAQBsChNWmKkERQICwbAABBNoQIKw2VQmKAAKEZQMIINCGAGG1qUpQBBAgLBtAAIE2BAirTV\n" +
            "WCIoAAYdkAAgi0IUBYbaoSFAEECMsGEECgDQHCalOVoAggQFg2gAACbQgQVpuqBEUAAcKyAQQQaEOAsNpUJSgCCBCWDSCAQBsChNWmKkERQICwbAABBNoQIKw2VQmKAAKEZQMIINCGAGG1qU\n" +
            "pQBBAgLBtAAIE2BAirTVWCIoAAYdkAAgi0IUBYbaoSFAEECMsGEECgDQHCalOVoAggQFg2gAACbQgQVpuqBEUAAcKyAQQQaEOAsNpUJSgCCBCWDSCAQBsChNWmKkERQICwbAABBNoQIKw2VQ\n" +
            "mKAAKEZQMIINCGAGG1qUpQBBAgLBtAAIE2BAirTVWCIoAAYdkAAgi0IUBYbaoSFAEECMsGEECgDQHCalOVoAggQFg2gAACbQgQVpuqBEUAAcKyAQQQaEOAsNpUJSgCCBCWDSCAQBsChNWmKk\n" +
            "ERQICwbAABBNoQIKw2VQmKAAKEZQMIINCGAGG1qUpQBBAgLBtAAIE2BAirTVWCIoAAYdkAAgi0IUBYbaoSFAEECMsGEECgDQHCalOVoAggQFg2gAACbQgQVpuqBEUAgX8A8Pj/pllcRS8AAA\n" +
            "AASUVORK5CYII="
    },
}
CanvasRenderingContext2D = {
    fillRect: function () {
    },
    fillText: function () {
    }
}
localStorage = {
    removeItem: function (key) {
        delete this[key]
    },
    getItem: function (key) {
        return this[key] ? this[key] : null;
    },
    setItem: function (key, value) {
        this[key] = value.toString();
    },
};
sessionStorage = {}
setInterval = window.setInterval = function () {
}
setInterval.toString = function () {
    return "function setInterval() { [native code] }"
}
setTimeout = function () {
}
top = window.top = window
global = undefined;
child_process = undefined;
closed = {
    __proto__: (1 >> 3 > 4)["__proto__"]
}

function get_cookie(seed, ts, code) {
    var Buffer;
    process = undefined;

    function CustomEvent() {
    }

    eval(code);
    cookie = encodeURIComponent(new ABC().z(seed, parseInt(ts) + (480 + new Date().getTimezoneOffset()) * 60 * 1000))
    console.log({cookie, cookie})
    return {cookie, cookie};
}

module.exports = {
    get_cookie
}
```

## 4.使用jsdom
jsdom基于NodeJS实现了与浏览器相似性的环境，它的本来目标是为了方便前端人员调试和测试他们的代码，但是也可以利用其带有浏览器特征的特点、实现补环境的目的。通过jsdom，我们可以在NodeJS环境实现对HTML中各种DOM元素的操作，这些DOM元素也支持浏览器中大部分API，实现了对浏览器的高度复刻。直接使用命令`npm i jsdom -g`即可安装jsdom。

简单使用如下：
```javascript
const jsdom = require('jsdom');

const {JSDOM} = jsdom;

const dom = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`);
console.log(dom.window.document.querySelector('p').textContent); // Hello world
```

上述代码导入了JSDOM、并基于JSDOM创建了HTML DOM树，然后就可以基于JSDOM下的window对象对DOM树进行操作。

输出：
```
Hello world
```

补环境时，通常需要补window中的属性，有了jsdom后，可以直接使用其中的window对象，其属性比较齐全，此外还可以使用jsdom中的document、navigator等对象，都是检测环境时常用的对象，只是jsdom中的document、navigator对象都基本是空的。如下：
```javascript
> const jsdom = require('jsdom');
undefined
> const {JSDOM} = jsdom;
undefined
> const {window} = new JSDOM(`...`);
undefined
> window
<ref *1> Window {
  StyleSheet: [Function: StyleSheet],
  MediaList: [Function: MediaList],
  CSSStyleSheet: [Function: CSSStyleSheet],
  CSSRule: [Function: CSSRule] {
    UNKNOWN_RULE: 0,
    STYLE_RULE: 1,
    CHARSET_RULE: 2,
    IMPORT_RULE: 3,
    MEDIA_RULE: 4,
    FONT_FACE_RULE: 5,
    ...
    AbortSignal: [class AbortSignal extends EventTarget] {
      abort: [Function: abort],
      timeout: [Function: timeout]
    },
    DOMRectReadOnly: [class DOMRectReadOnly] { fromRect: [Function: fromRect] },
    DOMRect: [class DOMRect extends DOMRectReadOnly] {
      fromRect: [Function: fromRect]
    }
  },
  [Symbol(named property tracker)]: NamedPropertiesTracker {
    object: [Circular *1],
    objectProxy: [Circular *1],
    resolverFunc: [Function: bound namedPropertyResolver],
    trackedValues: Map(0) {}
  }
}
> const {document} = (new JSDOM(`...`)).window;
undefined
> document
Document { location: [Getter/Setter] }
> const {navigator} = (new JSDOM(`...`)).window;
undefined
> navigator
Navigator {}
```
同时可以看到，jsdom的window对象提供了非常多浏览器中window的特性。此外，JSDOM支持自定义属性，如下定义了url、referrer等属性：
```javascript
const jsdom = require('jsdom');
const {JSDOM} = jsdom;

const dom = new JSDOM(``, {
    url: 'https://www.baidu.com/',
    referrer: 'https://www.baidu.com/',
    contentType: 'text/html; charset=utf-8',
    includeNodeLocations: true,
    storageQuota: 10000000
});

console.log(dom.window.document.location.href);
console.log(dom.window.document.referrer);
console.log(dom.window.document.contentType);
```

代码中的url会影响到window.location、document.URL等操作，referrer会影响到document.referrer等操作，通过这种形式的自定义，可以让构造的DOM环境绕过域名锁定等反爬手段。

输出：
```
https://www.baidu.com/
https://www.baidu.com/
text/html
```

jsdom最强大的地方是可以在jsdom中编写js脚本，jsdom会执行这些js脚本并影响到DOM树上，举例如下：
```javascript
const jsdom = require('jsdom');
const {JSDOM} = jsdom;

const dom = new JSDOM(`
<body>
    <script>
        document.body.appendChild(document.createElement('div')); // 脚本将被执行并修改DOM
    </script>
</body>
`, {
    runScripts: 'dangerously' // 允许执行脚本
});

console.log(dom.window.document.body.children.length === 2); // true
```

上述代码中，JSDOM可以直接执行script标签中的JS逻辑创建标签。同时可以看到，这里将runScripts属性设置为dangerously，目的是打开允许执行脚本，同时也会提醒使用者这个功能是危险的，一旦将其作为功能提供给用户使用，恶意用户就可以利用它来执行自己的任何代码、进而造成损害，同时一般在进行逆向和爬虫时，不太需要打开这个功能。

输出：
```
true
```