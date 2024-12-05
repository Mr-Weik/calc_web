import re

lines = [
    "0--3.4",
    "1 ～ 3.2",
    "1 X 3.4",
    "2 ✖️ 3.5",
]

# 正则表达式：提取每行中的第一个数字
pattern = r"[^0-9.]+([\d.]+)$"


for line in lines:
    match = re.search(pattern, line)
    if match:
        print(match.group(1))
