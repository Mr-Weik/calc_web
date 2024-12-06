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
function clearInput() {
    document.querySelector('textarea[name="lines"]').value = '';  // 清空输入框的内容
}
