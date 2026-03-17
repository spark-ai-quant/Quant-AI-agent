STRATEGY_NAME = "ma_breakout"

PARAM_SCHEMA = {
    "ma_period": {
        "type": "int",
        "default": 5,
        "description": "均线周期"
    },
    "threshold": {
        "type": "float",
        "default": 1.01,
        "description": "突破阈值（如1.01表示上涨1%）"
    },
    "stock_code": {
        "type": "str",
        "default": "000001.XSHE",
        "description": "交易标的"
    }
}


def generate(params):
    ma = params.get("ma_period", 5)
    threshold = params.get("threshold", 1.01)
    stock = params.get("stock_code", "000001.XSHE")

    return f"""
# MA Breakout Strategy

def initialize(context):
    g.stock = "{stock}"
    g.ma_period = {ma}
    g.threshold = {threshold}
    run_daily(trade, time='open')

def trade(context):
    df = get_price(g.stock, count=g.ma_period)

    # 防止数据不足
    if df is None or len(df) < g.ma_period:
        return

    ma = df['close'].mean()
    price = df['close'].iloc[-1]

    # 突破买入
    if price > ma * g.threshold:
        order_target_percent(g.stock, 1)

    # 跌破均线卖出
    elif price < ma:
        order_target(g.stock, 0)
"""