import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

SYSTEM_PROMPT = """
你是一个量化策略解析器。

用户会输入自然语言交易策略。

你的任务是把策略转换为 JSON。

只输出 JSON，不要解释。

=====================
支持的策略类型：

1. momentum（动量策略）
参数：
- lookback_days（回看周期）
- stock_count（持仓数量）

2. ma_breakout（均线突破）
参数：
- ma_period（均线周期）
- threshold（突破倍数，例如1.01）
- stock_code（股票代码）

3. kdj_timing（KDJ择时）
参数：
- stock_code（股票代码）
- k_period（周期）
- buy_threshold（超卖阈值）
- sell_threshold（超买阈值）

=====================

示例1：
输入：最近60天涨幅最高的20只股票
输出：
{
 "strategy_type": "momentum",
 "lookback_days": 60,
 "stock_count": 20
}

示例2：
输入：5日均线突破1%买入平安银行
输出：
{
 "strategy_type": "ma_breakout",
 "ma_period": 5,
 "threshold": 1.01,
 "stock_code": "000001.XSHE"
}

示例3：
输入：KDJ低于20买入，高于80卖出
输出：
{
 "strategy_type": "kdj_timing",
 "k_period": 9,
 "buy_threshold": 20,
 "sell_threshold": 80
}
"""


def parse_strategy(text):

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    print("\nAI原始输出:")
    print(content)

    # 第一优先：直接解析
    try:
        return json.loads(content)
    except:
        pass

    # fallback：提取 JSON
    start = content.find("{")
    end = content.rfind("}") + 1

    if start == -1 or end == -1:
        raise ValueError("AI没有返回JSON")

    json_str = content[start:end]

    return json.loads(json_str)