# -*- coding: UTF-8 -*-
from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML 模板
html_template = """
<!doctype html>
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
                border-bottom: 1px solid #ddd;
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
            }
        </style>
    </head>
    <body>
        <h1 class="text-center mb-4">多行加法计算器</h1>
        <form method="post">
            <div class="mb-3">
                <textarea name="lines" rows="5" class="form-control" placeholder="请输入数字，每行一个数字"></textarea>
            </div>
            <div class="text-center">
                <button name="operation" value="add" type="submit" class="btn btn-success m-1 btn-lg">计算</button>
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

        {% if result is not none %}
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

    if request.method == 'POST':
        lines = request.form['lines'].splitlines()

        for line in lines:
            if not line.strip():
                continue  # 跳过空行

            try:
                num = float(line.strip())
                numbers.append(num)
            except ValueError:
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

    return render_template_string(html_template, result=result, operations=operations, error_message=error_message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
