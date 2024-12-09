// static/js/script.js
function copyResult() {
    var resultTextarea = document.getElementById("result");

    // Select the text
    resultTextarea.select();
    resultTextarea.setSelectionRange(0, 99999); // For mobile devices

    // Try to copy using the Clipboard API
    if (navigator.clipboard) {
        navigator.clipboard.writeText(resultTextarea.value).then(function() {
            alert("结果已复制！");
        }).catch(function() {
            alert("复制失败，请手动复制");
        });
    } else {
        // Fallback for browsers that do not support Clipboard API
        document.execCommand("copy");
        alert("结果已复制！");
    }
}

// 清空输入框的 JavaScript 函数
function clearInputIndex() {
    document.querySelector('textarea[name="lines"]').value = '';  // 清空输入框的内容
}


// 计算操作
function performCalculation() {
    // 获取输入框的值
    let input1 = document.getElementById('input1').value;
    let input2 = document.getElementById('input2').value;

    // 判断输入是否合法
    if (input1 === '' || input2 === '') {
        alert('请输入两个有效的数字');
        return;  // 如果输入不合法，直接返回
    }

    // 将输入的值转换为数字类型
    input1 = parseFloat(input1);
    input2 = parseFloat(input2);

    // 执行计算操作，这里以加法为例
    let result = input1 + input2;

    // 显示结果
    document.getElementById('result').innerHTML = `<strong>计算结果: ${result}</strong>`;
}

// 清空输入框
function clearInput() {
    // 获取输入框和结果区域的元素
    document.getElementById('input1').value = '';
    document.getElementById('input2').value = '';
    document.getElementById('result').innerHTML = ''; // 清空结果显示区域
}


