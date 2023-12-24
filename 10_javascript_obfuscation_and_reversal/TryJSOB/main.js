const obfuscator = require('javascript-obfuscator')
const fs = require('fs')

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

// 混淆JS代码
function obfuscate(code, options) {
    let ob_code = obfuscator.obfuscate(code, options)
    return ob_code.getObfuscatedCode()
}

// 将混淆代码保存到本地
save_js('ob_main.js', obfuscate(code, options))

console.log('obfuscate done!')