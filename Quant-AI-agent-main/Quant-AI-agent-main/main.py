# main.py

from agent.ai_parser import parse_strategy
from agent.code_generator import generate_strategy_code

text = input("请输入策略描述：")

params = parse_strategy(text)

code = generate_strategy_code(params)

with open("generated_strategy.py", "w") as f:
    f.write(code)

print("\n策略已生成: generated_strategy.py")