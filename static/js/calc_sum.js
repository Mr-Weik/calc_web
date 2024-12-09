// 页面加载时发送请求
window.onload = function () {
    fetch('/calc_sum')
        .then(response => response.json())
        .then(data => {
            let resultText = '';
            // 拼接每一项计算结果
            data.details.forEach(detail => {
                resultText += `${detail.name}（${detail.num1} ${detail.operator} ${detail.num2} = ${detail.result}） +\n`;
            });
            resultText += `总投资 ${data.total_investment} 元`;

            // 将结果显示在页面的 pre 标签中
            document.getElementById('result').textContent = resultText;
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}


// copy.js
document.addEventListener('DOMContentLoaded', function () {
    // 获取复制按钮和显示内容的盒子
    const copyBtn = document.getElementById('copy-btn');
    const calcBox = document.getElementById('calc-container');

    // 复制按钮点击事件
    copyBtn.addEventListener('click', function () {
        // 创建一个临时的文本框
        const textArea = document.createElement('textarea');
        textArea.value = calcBox.innerText; // 获取盒子内的文本
        document.body.appendChild(textArea);

        // 选择文本并复制
        textArea.select();
        document.execCommand('copy');

        // 移除临时文本框
        document.body.removeChild(textArea);

        // 可选：弹出提示用户内容已被复制
        alert('内容已复制到剪贴板！');
    });
});


function clearInput() {
    document.getElementById('input_text').value = '';  // 清空 textarea 的内容
}


function goBack() {
    window.location.href = '/'; // 跳转到 index.html 页面
}