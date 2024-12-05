# -*- coding: UTF-8 -*-
from flask import Flask, request, render_template_string
import re  # 引入正则表达式库

app = Flask(__name__)

# HTML 模板
html_template = """<!doctype html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>多行加法计算器</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            padding: 20px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f1f3f5;
        }
        textarea {
            width: 100%;
            resize: none;
        }
        .card {
            margin-top: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .result-box {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .copy-button {
            cursor: pointer;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px 16px;
            font-size: 14px;
            transition: background-color 0.3s;
        }
        .copy-button:hover {
            background-color: #218838;
        }
        .form-control, button {
            font-size: 1.2rem;
        }
        .result-header {
            font-size: 1.5rem;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;
        }
        .step-item {
            font-size: 1.2rem;
            padding: 10px;
            border-radius: 5px;
            margin-right: 10px;
            background-color: #e9ecef;
            transition: background-color 0.3s;
        }
        .step-item:hover {
            background-color: #f8f9fa;
        }
        .final-result {
            font-size: 1.8rem;
            font-weight: bold;
            color: #007bff;
            margin-top: 20px;
        }
        .alert {
            color: #fff;
            background-color: #f44336;
            border-radius: 5px;
            padding: 10px;
            margin-top: 20px;
        }
        /* 针对小屏幕的优化 */
        @media (max-width: 576px) {
            .copy-button {
                width: 100%;
                margin-top: 10px;
            }
            .result-box {
                flex-direction: column;
                align-items: flex-start;
            }
            .step-item {
                margin-right: 0;
                margin-bottom: 10px;
            }
        }
    </style>
</head>
<body>
    <h1 class="text-center mb-4">多行加法计算器</h1>
    <form method="post">
        <div class="mb-3">
            <textarea name="lines" rows="5" class="form-control" placeholder="请输入数字，每行一个数字">{{ lines }}</textarea>
        </div>
        <div class="text-center">
            <button name="operation" value="add" type="submit" class="btn btn-success m-1 btn-lg">计算</button>
            <button type="button" class="btn btn-danger m-1 btn-lg" onclick="clearInput()">清空输入框</button>
        </div>
    </form>

    {% if result is not none %}
        <div class="card">
            <div class="result-box p-3">
                <textarea id="result" class="form-control" rows="3" readonly>{{ result }}</textarea>
                <button class="copy-button" onclick="copyResult()">复制结果</button>
            </div>
        </div>
    {% endif %}

{% if numbers %}
    <div class="card">
        <div class="p-3">
            <h4 class="result-header">输入的原始数据：</h4>
            <div class="d-flex flex-wrap">
                <!-- 显示用户输入的原始数据 -->
                {% for line in input_lines %}
                    <div class="step-item">{{ line }}</div>
                {% endfor %}
            </div>

            <h4 class="result-header mt-3">提取出的有效数字：</h4>
            <div class="d-flex flex-wrap">
                <!-- 显示提取到的数字 -->
                {% for number in numbers %}
                    <div class="step-item">{{ number }}</div>
                {% endfor %}
            </div>
        </div>
    </div>
{% endif %}

    {% if extracted %}
        <div class="card">
            <div class="p-3">
                <h4 class="result-header">提取结果：</h4>
                <div class="d-flex flex-wrap">
                    {% for extract in extracted %}
                        <div class="step-item">{{ extract }}</div>
                    {% endfor %}
                </div>
            </div>
        </div>
    {% endif %}

    {% if operations %}
        <div class="card">
            <div class="p-3">
                <h4 class="result-header">计算过程：</h4>
                <div>
                    {% for line in operations %}
                        <div class="step-item">{{ line }}</div>
                    {% endfor %}
                </div>
                <div class="final-result">
                    最终总和：{{ result }}
                </div>
            </div>
        </div>
    {% endif %}

    {% if error_message %}
        <div class="alert">
            {{ error_message }}
        </div>
    {% endif %}

    <script>
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
    </script>
</body>
</html>

"""

@app.route('/', methods=['GET', 'POST'])
def calculate():
    result = None
    error_message = None
    numbers = []
    operations = []
    lines = ""
    input_lines = []  # 存储用户输入的每一行

    if request.method == 'POST':
        lines = request.form['lines']
        input_lines = lines.splitlines()  # 拆分成多行

        for line in input_lines:
            if not line.strip():
                continue  # 跳过空行

            # 尝试直接将该行转换为 float
            try:
                num = float(line.strip())  # 尝试直接转为 float
                numbers.append(num)
            except ValueError:
                # 如果直接转换失败，再尝试正则匹配
                match = re.search(r"[^0-9.]*([\d.]+)$", line.strip())  # 匹配行尾的数字部分
                if match:
                    num = float(match.group(1))
                    numbers.append(num)
                else:
                    error_message = "请输入正确的数字，每行一个数字。"
                    break

        if error_message is None and numbers:
            total = 0
            for i in range(len(numbers)):
                total += numbers[i]
                total = round(total, 2)  # 保留两位小数
                # 计算缩进层级
                indent = " " * (i * 3)  # 根据步骤级别调整缩进
                if i == 0:
                    operations.append(f"{numbers[i]} = {total}")
                else:
                    operations.append(f"{indent}+ {numbers[i]} = {total}")

            result = total

    return render_template_string(html_template, result=result, operations=operations, error_message=error_message, numbers=numbers, lines=lines, input_lines=input_lines)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
