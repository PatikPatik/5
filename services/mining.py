def calculate_daily_rate(monthly_rate: float) -> float:
    return (1 + monthly_rate)**(1/30) - 1

def get_daily_report(user):
    rate = calculate_daily_rate(0.20)
    profit = float(user.hashpower) * rate
    return f"{profit:.6f} USDT profit for today's hashpower"
