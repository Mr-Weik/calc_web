from flask import Flask, request, render_template, jsonify, Response
import re  # 引入正则表达式库

app = Flask(__name__)


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
    return render_template(
        'index.html',
        result=result,
        error_message=error_message,
        numbers=numbers,
        operations=operations,
        input_lines=input_lines,
        lines=lines  # 保留用户输入的文本
    )


@app.route('/calc_sum', methods=['GET', 'POST'])
@app.route('/calc_sum', methods=['GET', 'POST'])
def calc_sum():
    result = None
    details = []

    if request.method == 'POST':
        input_text = request.form['input_text']  # 获取用户输入的文本
        lines = input_text.splitlines()  # 将文本按行分割

        total_sum = 0  # 初始化总和

        for line in lines:
            print(f'line: {line}')
            # 修改后的正则表达式，匹配浮动数值
            match = re.match(r'([^\d\W]+)\s*(\d+(\.\d+)?)\s*([\+\-\*/])\s*(\d+(\.\d+)?)', line.strip())

            print(f'match: {match}')

            if match:
                name = match.group(1).strip()  # 提取名称
                num1 = float(match.group(2))  # 第一个数字（可能是浮动数）
                operator = match.group(4)  # 运算符
                num2 = float(match.group(5))  # 第二个数字（可能是浮动数）

                # 判断num1和num2是否为整数（即它们的小数部分是否为0）
                def to_int_if_integer(x):
                    if abs(x - round(x)) < 1e-9:  # 判断小数部分是否接近零
                        return int(x)
                    return round(x, 2)  # 四舍五入到两位小数

                num1 = to_int_if_integer(num1)
                num2 = to_int_if_integer(num2)

                print(f'name: {name}, num1: {num1}, operator: {operator}, num2: {num2}')

                # 根据运算符进行不同的运算
                if operator == '+':
                    result_value = num1 + num2
                elif operator == '-':
                    result_value = num1 - num2
                elif operator == '*':
                    result_value = num1 * num2
                elif operator == '/':
                    if num2 != 0:
                        result_value = num1 / num2
                    else:
                        result_value = 'Error: Division by zero'

                # 四舍五入总和结果到2位小数
                total_sum += result_value if isinstance(result_value, (int, float)) else 0

                # 将每行的计算过程添加到 details 列表，使用字典存储
                details.append({
                    'name': name,
                    'num1': num1,
                    'operator': operator,
                    'num2': num2,
                    'result': to_int_if_integer(result_value)
                })
            else:
                # 如果格式不匹配，添加错误信息
                details.append({
                    'name': 'Invalid Format',
                    'num1': '',
                    'operator': '',
                    'num2': '',
                    'result': f"Invalid format in line: {line} (expected 'name num1 operator num2')"
                })

        result = round(total_sum, 2)  # 最终结果四舍五入到两位小数

    return render_template('calc_sum.html', result=result, details=details)






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
