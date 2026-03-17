STRATEGY_NAME = "momentum"

PARAM_SCHEMA = {
    "lookback_days": {
        "type": "int",
        "default": 20,
        "description": "动量回看周期"
    },
    "stock_count": {
        "type": "int",
        "default": 10,
        "description": "持仓股票数量"
    }
}


def generate(params):
    lookback = params.get("lookback_days", 20)
    stock_num = params.get("stock_count", 10)

    return f"""
# Momentum Strategy

def initialize(context):
    g.lookback = {lookback}
    g.stock_num = {stock_num}
    run_daily(trade, time='09:35')

def trade(context):
    stocks = get_all_securities('stock').index.tolist()
    df = get_price(stocks, count=g.lookback)

    returns = df['close'].iloc[-1] / df['close'].iloc[0] - 1
    top = returns.sort_values(ascending=False)[:g.stock_num]

    for stock in context.portfolio.positions:
        if stock not in top.index:
            order_target(stock, 0)

    weight = 1 / len(top)

    for stock in top.index:
        order_target_percent(stock, weight)
"""