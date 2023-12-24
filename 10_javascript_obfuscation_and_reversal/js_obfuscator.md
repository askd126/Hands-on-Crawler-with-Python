# javascript-obfuscator混淆
## 1.javascript-obfuscator的安装与基本使用
使用node.js初始化项目并安装javascript-obfuscator
```bash
XXX\Hands-on Crawler with Python\10_javascript_obfuscation_and_reversal
λ mkdir TryJSOB

XXX\Hands-on Crawler with Python\10_javascript_obfuscation_and_reversal
λ cd TryJSOB\

XXX\Hands-on Crawler with Python\10_javascript_obfuscation_and_reversal\TryJSOB
λ npm init
This utility will walk you through creating a package.json file.
It only covers the most common items, and tries to guess sensible defaults.

See `npm help init` for definitive documentation on these fields
and exactly what they do.

Use `npm install <pkg>` afterwards to install a package and
save it as a dependency in the package.json file.

Press ^C at any time to quit.
package name: (tryjsob)
version: (1.0.0)
description: Try JavaScript Bbfuscator
entry point: (index.js)
test command:
git repository:
keywords:
author: Corley
license: (ISC)
About to write to XXX\Hands-on Crawler with Python\10_javascript_obfuscation_and_reversal\TryJSOB\package.json:

{
  "name": "tryjsob",
  "version": "1.0.0",
  "description": "Try JavaScript Bbfuscator",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "author": "Corley",
  "license": "ISC"
}


Is this OK? (yes)

XXX\Hands-on Crawler with Python\10_javascript_obfuscation_and_reversal\TryJSOB
λ npm i --save-dev javascript-obfuscator

added 82 packages in 2m
npm notice
npm notice New patch version of npm available! 10.2.3 -> 10.2.5
npm notice Changelog: https://github.com/npm/cli/releases/tag/v10.2.5
npm notice Run npm install -g npm@10.2.5 to update!
npm notice
```

测试javascript-obfuscator，创建main.js如下：
```JavaScript
const obfuscator = require('javascript-obfuscator');
const fs = require('fs');

function save_js(file_path, content) {
    fs.writeFile(file_path, content, function (err) {
        if (err) {
            return console.log(err);
        }
        console.log("The file was saved!");
    });
}

// 待混淆代码
const code = `
console.log('I love JavaScript!');
`

// Obfuscator配置项
const options = {
    compact: false, // 是否压缩代码
    controlFlowFlattening: true, // 控制流扁平化
}

// 混淆JS代码
function obfuscate(code, options) {
    let ob_code = obfuscator.obfuscate(code, options);
    return ob_code.getObfuscatedCode();
}

// 将代码混淆并保存到本地
save_js('ob_main.js', obfuscate(code, options));

console.log('obfuscate done!');

```

运行`node main.js`，如下：
```bash
XXX\Hands-on Crawler with Python\10_javascript_obfuscation_and_reversal\TryJSOB
λ node main.js
obfuscate done!
The file was saved!
```

生成ob_main.js文件，内容如下：
```JavaScript
function _0x4ca9(_0x7f3517, _0x28c4df) {
    var _0x19a9e4 = _0x19a9();
    return _0x4ca9 = function (_0x4ca90a, _0x3e3bba) {
        _0x4ca90a = _0x4ca90a - 0x8c;
        var _0x514151 = _0x19a9e4[_0x4ca90a];
        return _0x514151;
    }, _0x4ca9(_0x7f3517, _0x28c4df);
}

function _0x19a9() {
    var _0x536628 = [
        '125TCfYVs',
        '246704kmzYnY',
        'log',
        '511104AzxKOR',
        '9091ASJPea',
        '66sMDceE',
        '8393520yczIrj',
        '2678186MQQRnx',
        '19884JXtClp',
        'I\x20love\x20JavaScript!',
        '1700460UrfHMJ',
        '4aaPHxQ'
    ];
    _0x19a9 = function () {
        return _0x536628;
    };
    return _0x19a9();
}

var _0x28319f = _0x4ca9;
(function (_0x1fef2e, _0x505d35) {
    var _0x5c7ee4 = _0x4ca9, _0x4de692 = _0x1fef2e();
    while (!![]) {
        try {
            var _0x498f8a = -parseInt(_0x5c7ee4(0x8c)) / 0x1 * (-parseInt(_0x5c7ee4(0x8d)) / 0x2) + parseInt(_0x5c7ee4(0x97)) / 0x3 * (parseInt(_0x5c7ee4(0x93)) / 0x4) + parseInt(_0x5c7ee4(0x94)) / 0x5 * (parseInt(_0x5c7ee4(0x90)) / 0x6) + parseInt(_0x5c7ee4(0x8f)) / 0x7 + -parseInt(_0x5c7ee4(0x95)) / 0x8 + parseInt(_0x5c7ee4(0x92)) / 0x9 + -parseInt(_0x5c7ee4(0x8e)) / 0xa;
            if (_0x498f8a === _0x505d35)
                break;
            else
                _0x4de692['push'](_0x4de692['shift']());
        } catch (_0x5287dd) {
            _0x4de692['push'](_0x4de692['shift']());
        }
    }
}(_0x19a9, 0x3e269), console[_0x28319f(0x96)](_0x28319f(0x91)));
```

可以看到，已经实现了对代码混淆的效果、无法直接读懂，此时ob_main.js也是可执行的，执行输出如下：
```bash
XXX\Hands-on Crawler with Python\10_javascript_obfuscation_and_reversal\TryJSOB
λ node ob_main.js
I love JavaScript!
```

## 2.代码压缩
使用参数compact实现对JavaScript代码的压缩，输出为一行内容：默认是true，如果定义为false，则混淆后的代码会保留原格式、分行显示。
main.js如下：
```JavaScript
// 其他部分保持不变

// 待混淆代码
const code = `
console.log('I love JavaScript!');
`

// Obfuscator配置项
const options = {
    compact: true, // 是否压缩代码
}
```

压缩效果如下：
```JavaScript
function _0x1caf(){var _0x210266=['1144888aTRYYU','365266MlrjIH','1256GyxaHw','906bSbZeI','2892muIrYW','30006nLknbn','log','10910cLiGXT','7271ICYgPH','I\x20love\x20JavaScript!','14aqwFhx','738858RCPoTF','600045yDvTyC'];_0x1caf=function(){return _0x210266;};return _0x1caf();}var _0x5482b2=_0x3e5c;function _0x3e5c(_0x2776ca,_0x26bfe3){var _0x1cafa0=_0x1caf();return _0x3e5c=function(_0x3e5c00,_0x3e648b){_0x3e5c00=_0x3e5c00-0xf2;var _0x480c3=_0x1cafa0[_0x3e5c00];return _0x480c3;},_0x3e5c(_0x2776ca,_0x26bfe3);}(function(_0x31fd43,_0x160b93){var _0x5702d2=_0x3e5c,_0x52aed6=_0x31fd43();while(!![]){try{var _0x5c3b91=parseInt(_0x5702d2(0xf3))/0x1+-parseInt(_0x5702d2(0xf5))/0x2*(-parseInt(_0x5702d2(0xf6))/0x3)+-parseInt(_0x5702d2(0xf2))/0x4+-parseInt(_0x5702d2(0xfe))/0x5+parseInt(_0x5702d2(0xfd))/0x6*(-parseInt(_0x5702d2(0xfc))/0x7)+parseInt(_0x5702d2(0xf4))/0x8*(-parseInt(_0x5702d2(0xf7))/0x9)+-parseInt(_0x5702d2(0xf9))/0xa*(-parseInt(_0x5702d2(0xfa))/0xb);if(_0x5c3b91===_0x160b93)break;else _0x52aed6['push'](_0x52aed6['shift']());}catch(_0x2ef945){_0x52aed6['push'](_0x52aed6['shift']());}}}(_0x1caf,0x54c12),console[_0x5482b2(0xf8)](_0x5482b2(0xfb)));
```

## 3.变量名混淆
identifierNamesGenerator参数可以控制变量名的混淆，它有2个值：
- hexadecimal：将变量名替换为十六进制形式的字符串，如0x20a7c7，是默认值。
- mangled：将变量名替换为普通的简写字符，如a、b、c等。

将identifierNamesGenerator改为mangled查看效果：
```JavaScript
// 其他部分保持不变

// 待混淆代码
const code = `
console.log('I love JavaScript!');
`

// Obfuscator配置项
const options = {
    compact: true, // 是否压缩代码
    identifierNamesGenerator: 'mangled', // 变量名混淆
}
```

混淆效果如下：
```JavaScript
function b(c,d){var e=a();return b=function(f,g){f=f-0xe9;var h=e[f];return h;},b(c,d);}var i=b;(function(c,d){var h=b,e=c();while(!![]){try{var f=-parseInt(h(0xef))/0x1*(parseInt(h(0xe9))/0x2)+-parseInt(h(0xf0))/0x3+parseInt(h(0xee))/0x4+parseInt(h(0xf3))/0x5+-parseInt(h(0xea))/0x6*(-parseInt(h(0xf2))/0x7)+-parseInt(h(0xeb))/0x8+parseInt(h(0xed))/0x9;if(f===d)break;else e['push'](e['shift']());}catch(g){e['push'](e['shift']());}}}(a,0x80864),console[i(0xec)](i(0xf1)));function a(){var j=['537350KfyVgA','700834DxHjIw','1074bfcxWC','2866360FLgvMK','log','5500251ogXvwO','1543012zlBsRe','1iSaAla','499599lsrWNY','I\x20love\x20JavaScript!','11627niuirb'];a=function(){return j;};return a();}
```

可以看到，hexadecimal可读性更低。javascript-obfuscator还提供参数renameGlobals，这个参数设置为True时，会将全局变量和函数名也替换掉，默认为false，一般不太通用。

## 4.字符串混淆
字符串混淆是将一个字符串声明放到一个数组里面，使之无法被直接搜索到，可以通过参数stringArray来控制，默认为true。还可以通过 rotateStringArray参数来控制数组化后结果的元素顺序，默认为true；还可以通过stringArrayEncoding参数来控制数组的编码形式，默认不开启编码，如果设置为base64，则会使用Base64编码，如果设置为rc4，则使用RC4编码；还可以通过stringArrayThreshold来控制启用编码的概率，范围0到1，默认0.8。

main.js加入字符串混淆如下：
```JavaScript
// 其他部分保持不变

// 待混淆代码
const code = `
console.log('I love JavaScript!');
`

// Obfuscator配置项
const options = {
    compact: true, // 是否压缩代码
    identifierNamesGenerator: 'hexadecimal', // 变量名混淆
    stringArray: true, // 是否混淆字符串
    rotateStringArray: true, // 字符串数组混淆
    stringArrayEncoding: ['base64'], // 字符串混淆编码，数组形式传参
    stringArrayThreshold: 1, // 字符串混淆编码概率
}
```

混淆的效果如下：
```JavaScript
var _0x56c569=_0x4851;function _0x357b(){var _0x3d54ec=['nJa2mJq5mhDwr1Hjsq','mtKZntu0ELjyzxLs','ssbSB3zLiePHDMfty3jPChqH','mJG0nJa0wevQDuPv','mtiZmta3ohzIywPyEa','mtKYA3HRBuXi','mtrhueDPBK8','mtuXmtz2BNPiBLm','mtC4mZu5mgnOuLnJrq','mtCYnZe4odfVvhrmuuW','Bg9N','muj6rxfADW','nte1s3foshbU'];_0x357b=function(){return _0x3d54ec;};return _0x357b();}function _0x4851(_0x5582ed,_0x1d2002){var _0x357b81=_0x357b();return _0x4851=function(_0x48513f,_0x46a815){_0x48513f=_0x48513f-0x67;var _0x57254d=_0x357b81[_0x48513f];if(_0x4851['npyWLL']===undefined){var _0x190b81=function(_0x4645e4){var _0x42eaab='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/=';var _0x2cb99a='',_0x3bd8f3='';for(var _0x1d1dd5=0x0,_0x1f90af,_0x1cc01e,_0x422908=0x0;_0x1cc01e=_0x4645e4['charAt'](_0x422908++);~_0x1cc01e&&(_0x1f90af=_0x1d1dd5%0x4?_0x1f90af*0x40+_0x1cc01e:_0x1cc01e,_0x1d1dd5++%0x4)?_0x2cb99a+=String['fromCharCode'](0xff&_0x1f90af>>(-0x2*_0x1d1dd5&0x6)):0x0){_0x1cc01e=_0x42eaab['indexOf'](_0x1cc01e);}for(var _0x426ca3=0x0,_0x228de9=_0x2cb99a['length'];_0x426ca3<_0x228de9;_0x426ca3++){_0x3bd8f3+='%'+('00'+_0x2cb99a['charCodeAt'](_0x426ca3)['toString'](0x10))['slice'](-0x2);}return decodeURIComponent(_0x3bd8f3);};_0x4851['wbgTfp']=_0x190b81,_0x5582ed=arguments,_0x4851['npyWLL']=!![];}var _0xdb7dfe=_0x357b81[0x0],_0x1e9812=_0x48513f+_0xdb7dfe,_0x1fe909=_0x5582ed[_0x1e9812];return!_0x1fe909?(_0x57254d=_0x4851['wbgTfp'](_0x57254d),_0x5582ed[_0x1e9812]=_0x57254d):_0x57254d=_0x1fe909,_0x57254d;},_0x4851(_0x5582ed,_0x1d2002);}(function(_0x2e4851,_0x3536d0){var _0x3ca8ed=_0x4851,_0xead3ff=_0x2e4851();while(!![]){try{var _0x1ffbda=parseInt(_0x3ca8ed(0x6c))/0x1*(parseInt(_0x3ca8ed(0x72))/0x2)+-parseInt(_0x3ca8ed(0x71))/0x3+parseInt(_0x3ca8ed(0x68))/0x4*(parseInt(_0x3ca8ed(0x6d))/0x5)+-parseInt(_0x3ca8ed(0x69))/0x6*(parseInt(_0x3ca8ed(0x67))/0x7)+-parseInt(_0x3ca8ed(0x73))/0x8*(parseInt(_0x3ca8ed(0x6f))/0x9)+-parseInt(_0x3ca8ed(0x6e))/0xa+parseInt(_0x3ca8ed(0x6a))/0xb;if(_0x1ffbda===_0x3536d0)break;else _0xead3ff['push'](_0xead3ff['shift']());}catch(_0x6337a1){_0xead3ff['push'](_0xead3ff['shift']());}}}(_0x357b,0xba514),console[_0x56c569(0x6b)](_0x56c569(0x70)));
```

可以看到，字符串都进行了Base64编码，此时无法再通过查找关键字符的方式来定位代码位置。除此之外，还有名为unicodeEscapeSequence的参数可以对字符串进行Unicode编码，如果设置为true，可以在Base64之后再进行一次Unicode转码，让代码混淆程度更深。
main.js加入Unicode转码如下：
```JavaScript
// 其他部分保持不变

// 待混淆代码
const code = `
console.log('I love JavaScript!');
`

// Obfuscator配置项
const options = {
    compact: true, // 是否压缩代码
    identifierNamesGenerator: 'hexadecimal', // 变量名混淆
    stringArray: true, // 是否混淆字符串
    rotateStringArray: true, // 字符串数组混淆
    stringArrayEncoding: ['base64'], // 字符串混淆编码，数组形式传参
    stringArrayThreshold: 1, // 字符串混淆编码概率
    unicodeEscapeSequence: true, // Unicode转义序列
}
```

混淆的效果如下：
```JavaScript
var _0x2f4eda=_0x172f;(function(_0x1c72f5,_0x29183c){var _0x5c7ca0=_0x172f,_0x456125=_0x1c72f5();while(!![]){try{var _0x5d9469=parseInt(_0x5c7ca0(0x1e6))/0x1+parseInt(_0x5c7ca0(0x1e2))/0x2+-parseInt(_0x5c7ca0(0x1e1))/0x3+parseInt(_0x5c7ca0(0x1e0))/0x4+-parseInt(_0x5c7ca0(0x1df))/0x5+parseInt(_0x5c7ca0(0x1de))/0x6+-parseInt(_0x5c7ca0(0x1e5))/0x7;if(_0x5d9469===_0x29183c)break;else _0x456125['push'](_0x456125['shift']());}catch(_0x488d5c){_0x456125['push'](_0x456125['shift']());}}}(_0xcc71,0x61acb),console[_0x2f4eda(0x1e4)](_0x2f4eda(0x1e3)));function _0x172f(_0x4f7ea9,_0x54cba1){var _0xcc715f=_0xcc71();return _0x172f=function(_0x172fab,_0x11a7b5){_0x172fab=_0x172fab-0x1de;var _0x522563=_0xcc715f[_0x172fab];if(_0x172f['\x66\x7a\x51\x44\x70\x57']===undefined){var _0x1f814a=function(_0x1fcdac){var _0x30a0b2='\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x2b\x2f\x3d';var _0x3aa089='',_0x270a27='';for(var _0x430205=0x0,_0x1857fb,_0x4c6e18,_0x248b08=0x0;_0x4c6e18=_0x1fcdac['\x63\x68\x61\x72\x41\x74'](_0x248b08++);~_0x4c6e18&&(_0x1857fb=_0x430205%0x4?_0x1857fb*0x40+_0x4c6e18:_0x4c6e18,_0x430205++%0x4)?_0x3aa089+=String['\x66\x72\x6f\x6d\x43\x68\x61\x72\x43\x6f\x64\x65'](0xff&_0x1857fb>>(-0x2*_0x430205&0x6)):0x0){_0x4c6e18=_0x30a0b2['\x69\x6e\x64\x65\x78\x4f\x66'](_0x4c6e18);}for(var _0x2880dd=0x0,_0x144850=_0x3aa089['\x6c\x65\x6e\x67\x74\x68'];_0x2880dd<_0x144850;_0x2880dd++){_0x270a27+='\x25'+('\x30\x30'+_0x3aa089['\x63\x68\x61\x72\x43\x6f\x64\x65\x41\x74'](_0x2880dd)['\x74\x6f\x53\x74\x72\x69\x6e\x67'](0x10))['\x73\x6c\x69\x63\x65'](-0x2);}return decodeURIComponent(_0x270a27);};_0x172f['\x4a\x42\x75\x50\x6e\x79']=_0x1f814a,_0x4f7ea9=arguments,_0x172f['\x66\x7a\x51\x44\x70\x57']=!![];}var _0x39288e=_0xcc715f[0x0],_0x4d9e91=_0x172fab+_0x39288e,_0x25e843=_0x4f7ea9[_0x4d9e91];return!_0x25e843?(_0x522563=_0x172f['\x4a\x42\x75\x50\x6e\x79'](_0x522563),_0x4f7ea9[_0x4d9e91]=_0x522563):_0x522563=_0x25e843,_0x522563;},_0x172f(_0x4f7ea9,_0x54cba1);}function _0xcc71(){var _0x2a35eb=['\x6d\x74\x69\x35\x6e\x4a\x47\x33\x6e\x4e\x4c\x74\x41\x68\x4c\x79\x7a\x61','\x6e\x64\x6d\x31\x6e\x64\x6d\x31\x72\x4b\x76\x36\x74\x77\x44\x32','\x6d\x5a\x79\x33\x6d\x74\x71\x30\x77\x4b\x4c\x52\x71\x75\x31\x72','\x73\x73\x62\x53\x42\x33\x7a\x4c\x69\x65\x50\x48\x44\x4d\x66\x74\x79\x33\x6a\x50\x43\x68\x71\x48','\x42\x67\x39\x4e','\x6e\x64\x47\x59\x6d\x5a\x65\x30\x74\x4b\x7a\x57\x73\x4e\x6e\x36','\x6d\x74\x75\x33\x6e\x4a\x6a\x32\x74\x76\x76\x30\x44\x31\x71','\x6d\x4a\x47\x35\x6e\x64\x61\x31\x6f\x66\x72\x34\x43\x75\x54\x4b\x72\x71','\x6d\x74\x4b\x31\x6f\x64\x47\x33\x6d\x66\x44\x72\x76\x33\x50\x54\x7a\x57'];_0xcc71=function(){return _0x2a35eb;};return _0xcc71();}
```

这里字符串被数字化和Unicode化，此时已经无法通过全局搜索的方式搜索关键词来找到加密入口了。

## 5.反格式化
通过设置selfDefending参数来开启代码自我保护功能：开启之后，混淆后的JavaScript会强制以一行形式显示，如果将混淆后的代码进行格式化（美化）或者重命名，该段代码将无法执行，并且如果在浏览器中运行，会将浏览器卡死。

main.js加入反格式化如下：
```JavaScript
// 其他部分保持不变

// 待混淆代码
const code = `
console.log('I love JavaScript!');
`

// Obfuscator配置项
const options = {
    selfDefending: true, // 开启自我保护、反格式化
}
```

混淆的效果如下：
```JavaScript
var _0x518b99=_0x1bbb;function _0x1bbb(_0x48db10,_0x2b1e2f){var _0x144844=_0x4ab4();return _0x1bbb=function(_0x307430,_0xb0f33a){_0x307430=_0x307430-0x1d1;var _0x4ab423=_0x144844[_0x307430];return _0x4ab423;},_0x1bbb(_0x48db10,_0x2b1e2f);}(function(_0x546c59,_0x5c2b3a){var _0x2810e8=_0x1bbb,_0x330cbf=_0x546c59();while(!![]){try{var _0x1386ae=-parseInt(_0x2810e8(0x1d6))/0x1*(-parseInt(_0x2810e8(0x1df))/0x2)+-parseInt(_0x2810e8(0x1dd))/0x3*(-parseInt(_0x2810e8(0x1d8))/0x4)+-parseInt(_0x2810e8(0x1da))/0x5*(parseInt(_0x2810e8(0x1d9))/0x6)+parseInt(_0x2810e8(0x1dc))/0x7+-parseInt(_0x2810e8(0x1d7))/0x8+-parseInt(_0x2810e8(0x1d3))/0x9+parseInt(_0x2810e8(0x1d2))/0xa;if(_0x1386ae===_0x5c2b3a)break;else _0x330cbf['push'](_0x330cbf['shift']());}catch(_0x562ee8){_0x330cbf['push'](_0x330cbf['shift']());}}}(_0x4ab4,0xd603b));var _0xb0f33a=(function(){var _0x1908b0=!![];return function(_0x3bb443,_0x23303c){var _0x290670=_0x1908b0?function(){var _0x4587c0=_0x1bbb;if(_0x23303c){var _0x44c41e=_0x23303c[_0x4587c0(0x1e0)](_0x3bb443,arguments);return _0x23303c=null,_0x44c41e;}}:function(){};return _0x1908b0=![],_0x290670;};}()),_0x307430=_0xb0f33a(this,function(){var _0x13f206=_0x1bbb;return _0x307430[_0x13f206(0x1d1)]()[_0x13f206(0x1de)]('(((.+)+)+)+$')[_0x13f206(0x1d1)]()[_0x13f206(0x1db)](_0x307430)[_0x13f206(0x1de)](_0x13f206(0x1d4));});_0x307430(),console['log'](_0x518b99(0x1d5));function _0x4ab4(){var _0x19dccf=['102iNPwTk','383120MelBCz','constructor','9122554IDBfQs','147pXFuAH','search','865794aQFMpm','apply','toString','11852410oAXiKz','7575210jwOzQn','(((.+)+)+)+$','I\x20love\x20JavaScript!','1uaNAWx','11797456UyDgZD','128508KSqPON'];_0x4ab4=function(){return _0x19dccf;};return _0x4ab4();}
```

此时ob_main.js是可以执行的，如果使用IDE等工具将JS格式化、再运行，会阻塞终端或浏览器、无法得到结果。

## 6.控制流平坦化
控制流平坦化是将代码的执行逻辑混淆，使其变得复杂难读。它的基本思想是将一些逻辑处理块都加上一个分发逻辑块，每个逻辑块都由分发逻辑块进行条件判断和分发，构成一个个闭环逻辑，导致整个执行逻辑十分复杂难读。

main.js加入控制流平坦化如下：
```JavaScript
// 其他部分保持不变

// 待混淆代码
const code = `
function log() {
    console.log(1);
    console.log(2);
    console.log(3);
    console.log(4);
    console.log(5);
}
log();
`

// Obfuscator配置项
const options = {
    compact: false, // 不压缩代码
    controlFlowFlattening: true, // 开启控制流扁平化
}
```

混淆的效果如下：
```JavaScript
function _0x2de5(_0x27b1ee, _0x1ee80a) {
    var _0x25b909 = _0x25b9();
    return _0x2de5 = function (_0x2de5b5, _0x2eacd1) {
        _0x2de5b5 = _0x2de5b5 - 0x8c;
        var _0x2af2f8 = _0x25b909[_0x2de5b5];
        return _0x2af2f8;
    }, _0x2de5(_0x27b1ee, _0x1ee80a);
}
(function (_0x104919, _0xb2cd9d) {
    var _0x109079 = _0x2de5, _0xcb2e61 = _0x104919();
    while (!![]) {
        try {
            var _0x2757c3 = parseInt(_0x109079(0x94)) / 0x1 * (-parseInt(_0x109079(0x8c)) / 0x2) + -parseInt(_0x109079(0x8f)) / 0x3 + -parseInt(_0x109079(0x9a)) / 0x4 * (-parseInt(_0x109079(0x99)) / 0x5) + parseInt(_0x109079(0x90)) / 0x6 * (parseInt(_0x109079(0x9b)) / 0x7) + parseInt(_0x109079(0x97)) / 0x8 + parseInt(_0x109079(0x8e)) / 0x9 * (parseInt(_0x109079(0x93)) / 0xa) + parseInt(_0x109079(0x92)) / 0xb * (-parseInt(_0x109079(0x96)) / 0xc);
            if (_0x2757c3 === _0xb2cd9d)
                break;
            else
                _0xcb2e61['push'](_0xcb2e61['shift']());
        } catch (_0x575d02) {
            _0xcb2e61['push'](_0xcb2e61['shift']());
        }
    }
}(_0x25b9, 0xc53e8));
function log() {
    var _0x279b3d = _0x2de5, _0x10e5f0 = { 'dsAjp': _0x279b3d(0x8d) }, _0x1dd7e0 = _0x10e5f0[_0x279b3d(0x98)][_0x279b3d(0x95)]('|'), _0x179012 = 0x0;
    while (!![]) {
        switch (_0x1dd7e0[_0x179012++]) {
        case '0':
            console[_0x279b3d(0x91)](0x3);
            continue;
        case '1':
            console['log'](0x2);
            continue;
        case '2':
            console[_0x279b3d(0x91)](0x4);
            continue;
        case '3':
            console[_0x279b3d(0x91)](0x1);
            continue;
        case '4':
            console['log'](0x5);
            continue;
        }
        break;
    }
}
log();
function _0x25b9() {
    var _0x499f20 = [
        '407bboAFe',
        '476030SYfxJR',
        '643xyArHM',
        'split',
        '201288QMgweJ',
        '6628888iZxByv',
        'dsAjp',
        '119005FmUXWt',
        '148CzlhCp',
        '28ydFaQZ',
        '4490saLUlE',
        '3|1|0|2|4',
        '117bGlNsn',
        '2858838fPVKly',
        '2245416SSRvDF',
        'log'
    ];
    _0x25b9 = function () {
        return _0x499f20;
    };
    return _0x25b9();
}
```

可以看到，连续的执行逻辑被打破，代码被修改为while+switch结构的语句，很难再直观看出多条console.log语句的执行顺序。执行ob_main.js效果如下：
```Bash
XXX\Hands-on Crawler with Python\10_javascript_obfuscation_and_reversal\TryJSOB(master -> origin) (tryjsob@1.0.0)
λ node ob_main.js
1
2
3
4
5
```

如果将控制流扁平化关闭，即将controlFlowFlattening参数设置为false，main.js如下：
```JavaScript
// 其他部分保持不变

// 待混淆代码
const code = `
function log() {
    console.log(1);
    console.log(2);
    console.log(3);
    console.log(4);
    console.log(5);
}
log();
`

// Obfuscator配置项
const options = {
    compact: false, // 不压缩代码
    controlFlowFlattening: false, // 开启控制流扁平化
}
```

混淆后的代码如下：
```JavaScript
function _0x4a5c(_0x4c451c, _0x3f5a1b) {
    var _0x4674bb = _0x4674();
    return _0x4a5c = function (_0x4a5c0b, _0x5f43a6) {
        _0x4a5c0b = _0x4a5c0b - 0x12c;
        var _0x366070 = _0x4674bb[_0x4a5c0b];
        return _0x366070;
    }, _0x4a5c(_0x4c451c, _0x3f5a1b);
}
(function (_0x409d9d, _0x14aaf2) {
    var _0x9f8543 = _0x4a5c, _0x38e01e = _0x409d9d();
    while (!![]) {
        try {
            var _0x4d69bb = parseInt(_0x9f8543(0x130)) / 0x1 + -parseInt(_0x9f8543(0x12e)) / 0x2 + parseInt(_0x9f8543(0x135)) / 0x3 * (-parseInt(_0x9f8543(0x12d)) / 0x4) + parseInt(_0x9f8543(0x12c)) / 0x5 + parseInt(_0x9f8543(0x131)) / 0x6 * (-parseInt(_0x9f8543(0x12f)) / 0x7) + -parseInt(_0x9f8543(0x136)) / 0x8 * (parseInt(_0x9f8543(0x132)) / 0x9) + parseInt(_0x9f8543(0x133)) / 0xa;
            if (_0x4d69bb === _0x14aaf2)
                break;
            else
                _0x38e01e['push'](_0x38e01e['shift']());
        } catch (_0x54e544) {
            _0x38e01e['push'](_0x38e01e['shift']());
        }
    }
}(_0x4674, 0xb556f));
function _0x4674() {
    var _0x596603 = [
        'log',
        '27fkVpQv',
        '5516648FhgZZE',
        '3458480GdWdFO',
        '205308PyKurd',
        '234288fNbFoT',
        '3841243DHfqVg',
        '706413HFpvCr',
        '6HRJWmR',
        '9LioTKb',
        '11620750YGEotT'
    ];
    _0x4674 = function () {
        return _0x596603;
    };
    return _0x4674();
}
function log() {
    var _0x3f5a3a = _0x4a5c;
    console[_0x3f5a3a(0x134)](0x1), console[_0x3f5a3a(0x134)](0x2), console[_0x3f5a3a(0x134)](0x3), console['log'](0x4), console[_0x3f5a3a(0x134)](0x5);
}
log();
```

可以看到，关闭控制流扁平化之后，依旧保留了原始的逻辑结构。使用控制流扁平化可以使执行逻辑更加复杂难读，目前很多前端混淆都会加上控制流扁平化，启用控制流扁平化之后，代码的
执行时间会变长，最长达1.5倍左右。还能使用controlFlowFlatteningThreshold参数来控制比例，取值范围是0到1，默认0.75，如果设置为0，那相当于controlFlowFlattening设置为
false，即不开启控制流扁平化。

## 7.垃圾代码注入
垃圾代码即不会被执行的代码或对上下文没有任何影响的代码，注入之后可以对现有的JavaScript代码的阅读形成干扰，可以使用deadCodeInjection参数开启垃圾代码注入，默认为false。还可以通过设置deadCodeInjectionThreshold参数来控制僵尸代码注入的比例，取值0到1，默认是0.4。

main.js中加入垃圾代码注入如下：
```JavaScript
// 其他部分保持不变

// 待混淆代码
const code = `
console.log('I love JavaScript!')
`

// 配置项
const options = {
    deadCodeInjection: true, // 垃圾代码注入
}
```

混淆后的代码效果如下：
```JavaScript
var _0x7893ea=_0x8434;function _0x22ba(){var _0x29d95d=['1156876qWNbQl','I\x20love\x20JavaScript!','1600JmeVWJ','3352192QKMRiz','61068RsxCSK','3172146kGxxTN','10HHgKIT','log','16dCbGcU','786LsEueo','451zEJmgi','5tLqQDV','4026924ohbcpp','302046eMbkef'];_0x22ba=function(){return _0x29d95d;};return _0x22ba();}function _0x8434(_0x49eb06,_0xa761eb){var _0x22ba5b=_0x22ba();return _0x8434=function(_0x84340a,_0x57d54b){_0x84340a=_0x84340a-0x141;var _0x3db09b=_0x22ba5b[_0x84340a];return _0x3db09b;},_0x8434(_0x49eb06,_0xa761eb);}(function(_0x2cac3f,_0x31632b){var _0x2a9beb=_0x8434,_0x34fa06=_0x2cac3f();while(!![]){try{var _0x5e0724=parseInt(_0x2a9beb(0x144))/0x1*(-parseInt(_0x2a9beb(0x14b))/0x2)+parseInt(_0x2a9beb(0x148))/0x3*(parseInt(_0x2a9beb(0x143))/0x4)+-parseInt(_0x2a9beb(0x146))/0x5*(-parseInt(_0x2a9beb(0x14e))/0x6)+-parseInt(_0x2a9beb(0x149))/0x7+parseInt(_0x2a9beb(0x14c))/0x8+parseInt(_0x2a9beb(0x147))/0x9*(-parseInt(_0x2a9beb(0x141))/0xa)+parseInt(_0x2a9beb(0x145))/0xb*(parseInt(_0x2a9beb(0x14d))/0xc);if(_0x5e0724===_0x31632b)break;else _0x34fa06['push'](_0x34fa06['shift']());}catch(_0x3277a0){_0x34fa06['push'](_0x34fa06['shift']());}}}(_0x22ba,0x4d894),console[_0x7893ea(0x142)](_0x7893ea(0x14a)));
```

可以从3个方面来判断：
- 是否有传入参数
- 是否有返回
- 是否有修改全局变量

如果都没有，则一般是注入的垃圾代码，直接直接删除。

## 8.域名锁定
可以通过domainLock参数来控制JavaScript代码只能在特定域名下运行，这样可以防止逆向者在本地模拟运行相应的JS代码。

main.js中加入域名锁定如下：
```JavaScript
// 其他部分保持不变

// 待混淆代码
const code = `
console.log('I love JavaScript!')
`

// 配置项
const options = {
    domainLock: ['.baidu.com'] // 锁定域名，只有在百度相关网站下才能运行
}
```

混淆后的代码效果如下：
```JavaScript
function _0x7ff4(_0x55e32d,_0x22ada5){var _0x3644d5=_0x308d();return _0x7ff4=function(_0xa6f8df,_0x6f5d90){_0xa6f8df=_0xa6f8df-0x111;var _0x41c48b=_0x3644d5[_0xa6f8df];return _0x41c48b;},_0x7ff4(_0x55e32d,_0x22ada5);}var _0xb5233f=_0x7ff4;(function(_0x53b757,_0x2d4b89){var _0x2e5773=_0x7ff4,_0x4ea6c3=_0x53b757();while(!![]){try{var _0x794efa=-parseInt(_0x2e5773(0x11a))/0x1*(parseInt(_0x2e5773(0x11d))/0x2)+parseInt(_0x2e5773(0x11e))/0x3+-parseInt(_0x2e5773(0x113))/0x4+parseInt(_0x2e5773(0x122))/0x5*(-parseInt(_0x2e5773(0x127))/0x6)+-parseInt(_0x2e5773(0x116))/0x7*(-parseInt(_0x2e5773(0x119))/0x8)+-parseInt(_0x2e5773(0x118))/0x9+parseInt(_0x2e5773(0x112))/0xa*(parseInt(_0x2e5773(0x123))/0xb);if(_0x794efa===_0x2d4b89)break;else _0x4ea6c3['push'](_0x4ea6c3['shift']());}catch(_0x3e6fef){_0x4ea6c3['push'](_0x4ea6c3['shift']());}}}(_0x308d,0x9bbed));var _0x6f5d90=(function(){var _0x1badd9=!![];return function(_0xed6177,_0x5ef6ba){var _0x264657=_0x1badd9?function(){if(_0x5ef6ba){var _0x239971=_0x5ef6ba['apply'](_0xed6177,arguments);return _0x5ef6ba=null,_0x239971;}}:function(){};return _0x1badd9=![],_0x264657;};}()),_0xa6f8df=_0x6f5d90(this,function(){var _0x5a565f=_0x7ff4,_0x2cb3cf=function(){var _0x1e100e=_0x7ff4,_0x22da93;try{_0x22da93=Function(_0x1e100e(0x11b)+_0x1e100e(0x11c)+');')();}catch(_0x5bce10){_0x22da93=window;}return _0x22da93;},_0x19b101=_0x2cb3cf(),_0x3abf75=new RegExp(_0x5a565f(0x124),'g'),_0x134e48=_0x5a565f(0x117)[_0x5a565f(0x11f)](_0x3abf75,'')[_0x5a565f(0x128)](';'),_0x2e740d,_0x5ba590,_0x1067f9,_0x262027,_0x443a93=function(_0x111357,_0x31113b,_0x1fcceb){var _0x38164b=_0x5a565f;if(_0x111357[_0x38164b(0x125)]!=_0x31113b)return![];for(var _0x24bf0d=0x0;_0x24bf0d<_0x31113b;_0x24bf0d++){for(var _0x509c1d=0x0;_0x509c1d<_0x1fcceb['length'];_0x509c1d+=0x2){if(_0x24bf0d==_0x1fcceb[_0x509c1d]&&_0x111357[_0x38164b(0x121)](_0x24bf0d)!=_0x1fcceb[_0x509c1d+0x1])return![];}}return!![];},_0xf8d032=function(_0x328608,_0x22c3f2,_0x3f0c77){return _0x443a93(_0x22c3f2,_0x3f0c77,_0x328608);},_0xf8d595=function(_0x1d332d,_0x50c680,_0x1843b){return _0xf8d032(_0x50c680,_0x1d332d,_0x1843b);},_0x4ab570=function(_0x69a8d0,_0x234a6c,_0x4c9ae8){return _0xf8d595(_0x234a6c,_0x4c9ae8,_0x69a8d0);};for(var _0x2b90a7 in _0x19b101){if(_0x443a93(_0x2b90a7,0x8,[0x7,0x74,0x5,0x65,0x3,0x75,0x0,0x64])){_0x2e740d=_0x2b90a7;break;}}for(var _0x4f2210 in _0x19b101[_0x2e740d]){if(_0x4ab570(0x6,_0x4f2210,[0x5,0x6e,0x0,0x64])){_0x5ba590=_0x4f2210;break;}}for(var _0x752361 in _0x19b101[_0x2e740d]){if(_0xf8d595(_0x752361,[0x7,0x6e,0x0,0x6c],0x8)){_0x1067f9=_0x752361;break;}}if(!('~'>_0x5ba590))for(var _0x5b1877 in _0x19b101[_0x2e740d][_0x1067f9]){if(_0xf8d032([0x7,0x65,0x0,0x68],_0x5b1877,0x8)){_0x262027=_0x5b1877;break;}}if(!_0x2e740d||!_0x19b101[_0x2e740d])return;var _0xa45eb4=_0x19b101[_0x2e740d][_0x5ba590],_0x542eba=!!_0x19b101[_0x2e740d][_0x1067f9]&&_0x19b101[_0x2e740d][_0x1067f9][_0x262027],_0x203242=_0xa45eb4||_0x542eba;if(!_0x203242)return;var _0x37bbcc=![];for(var _0x5eec58=0x0;_0x5eec58<_0x134e48['length'];_0x5eec58++){var _0x5ba590=_0x134e48[_0x5eec58],_0x2b26b8=_0x5ba590[0x0]===String[_0x5a565f(0x114)](0x2e)?_0x5ba590[_0x5a565f(0x115)](0x1):_0x5ba590,_0x5a97c2=_0x203242[_0x5a565f(0x125)]-_0x2b26b8[_0x5a565f(0x125)],_0x3739d4=_0x203242[_0x5a565f(0x111)](_0x2b26b8,_0x5a97c2),_0x474099=_0x3739d4!==-0x1&&_0x3739d4===_0x5a97c2;_0x474099&&((_0x203242['length']==_0x5ba590[_0x5a565f(0x125)]||_0x5ba590[_0x5a565f(0x111)]('.')===0x0)&&(_0x37bbcc=!![]));}if(!_0x37bbcc){var _0x2e79b5=new RegExp(_0x5a565f(0x120),'g'),_0x34c1b4='HabyouxtF:blIIyanykWJAzmhfTPpKLvyXBAd'[_0x5a565f(0x11f)](_0x2e79b5,'');_0x19b101[_0x2e740d][_0x1067f9]=_0x34c1b4;}});_0xa6f8df(),console['log'](_0xb5233f(0x126));function _0x308d(){var _0x15eed7=['indexOf','10NqMnOQ','816604YuQmMG','fromCharCode','slice','656390hdzmcT','JEk.fYPbayBvnhKisdur.cZtyYomzUMUlrSljXV','10475028UjzXDF','80hDehDy','5MKkMfx','return\x20(function()\x20','{}.constructor(\x22return\x20this\x22)(\x20)','442166ksOwOt','1273053fGdUeF','replace','[HyxFIIyyWJAzmhfTPpKLvyXBAd]','charCodeAt','5022355FUiOga','30291921zDOCaX','[JEkfYPyBvnhKsrZtyYzUMUlrSljXV]','length','I\x20love\x20JavaScript!','6gnqCsr','split'];_0x308d=function(){return _0x15eed7;};return _0x308d();}
```

此时，混淆后的这段代码只有在百度相关的网站平台下才能正常运行，对于其他网站，比如知乎，就无法获得正常的结果、会跳转到空白页。

## 9.其他方式
javascript-obfuscator还支持其他几种增加JS逆向难度的方式：

（1）无限debugger
- 使用debugProtection来禁用调试模式，进入无限Debug模式
- 使用debugProtectionInterval来启用无限Debug的间隔，使得代码在调试过程中会不断进入断点模式

（2）禁用控制台输出
- 方式1：使用disableConsoleOutput来禁用掉console.log输出功能，加大调试难度
- 方式2：直接在调用控制台输出的代码前，重新console相关的方法，然后将JS注入

（3）对象键名替换
待混淆代码中如果有对象，可以使用transformObjectKeys参数来对对象的键进行替换。

main.js加入对象键名替换如下：
```JavaScript
// 其他部分保持不变

// 待混淆代码
const code = `
(function() {
    let student = {
        name: 'Corley',
        age: 18,
        hobby: ['reading', 'music', 'running']
    }
    console.log(student)
})();
`

// 配置项
const options = {
    compact: false, // 不进行压缩
    transformObjectKeys: true, // 转换对象属性
}
```

得到的混淆效果如下：
```JavaScript
(function (_0x222a7a, _0x2d6e1b) {
    const _0x3682ef = _0x279d, _0x547228 = _0x222a7a();
    while (!![]) {
        try {
            const _0x4478ec = -parseInt(_0x3682ef(0xd3)) / 0x1 * (-parseInt(_0x3682ef(0xd7)) / 0x2) + parseInt(_0x3682ef(0xd0)) / 0x3 + -parseInt(_0x3682ef(0xd5)) / 0x4 * (parseInt(_0x3682ef(0xd8)) / 0x5) + -parseInt(_0x3682ef(0xdb)) / 0x6 * (-parseInt(_0x3682ef(0xdc)) / 0x7) + parseInt(_0x3682ef(0xd1)) / 0x8 + -parseInt(_0x3682ef(0xd2)) / 0x9 + -parseInt(_0x3682ef(0xd4)) / 0xa;
            if (_0x4478ec === _0x2d6e1b)
                break;
            else
                _0x547228['push'](_0x547228['shift']());
        } catch (_0x357cc1) {
            _0x547228['push'](_0x547228['shift']());
        }
    }
}(_0x4847, 0x9306e), (function () {
    const _0x5cd4fc = _0x279d, _0x921027 = {}; // 对象名被替换成特殊变量
    _0x921027[_0x5cd4fc(0xd9)] = 'Corley', _0x921027[_0x5cd4fc(0xda)] = 0x12, _0x921027['hobby'] = [
        _0x5cd4fc(0xcf),
        _0x5cd4fc(0xd6),
        'running'
    ];
    let _0x4eb7ad = _0x921027;
    console['log'](_0x4eb7ad);
}()));
function _0x279d(_0x374e07, _0x4f8c50) {
    const _0x484764 = _0x4847();
    return _0x279d = function (_0x279d61, _0x4e7aed) {
        _0x279d61 = _0x279d61 - 0xcf;
        let _0x2b0c6b = _0x484764[_0x279d61];
        return _0x2b0c6b;
    }, _0x279d(_0x374e07, _0x4f8c50);
}
function _0x4847() {
    const _0x3c4c27 = [
        '11005zPEnkl',
        'name',
        'age',
        '6CJmarj',
        '7540211ZxHBhw',
        'reading',
        '1593468mpYlvv',
        '7125880RhxsYI',
        '8557560MxxYKM',
        '10eszGTc',
        '15121370unesUg',
        '620lFhSlA',
        'music',
        '181458Nqwhax'
    ];
    _0x4847 = function () {
        return _0x3c4c27;
    };
    return _0x4847();
}
```

可以看到，在混淆后的代码中，对象键名被替换成了特殊变量。