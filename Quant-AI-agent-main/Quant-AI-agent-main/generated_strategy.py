
# MA Breakout Strategy

def initialize(context):
    g.stock = "000001.XSHE"
    g.ma_period = 5
    g.threshold = 1.01
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
