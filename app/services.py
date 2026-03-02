import httpx
from fastapi import HTTPException
from datetime import datetime

async def get_jpy_rate():
    url = "https://open.er-api.com/v6/latest/EUR"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=5.0)
            return response.json()['rates']['JPY']
        except:
            raise HTTPException(status_code=503, detail="Currency API error")


def calculate_full_import_logic(price_jpy: int, rate: float, year: int):
    # 1. Базовые расчеты
    net_eur = price_jpy / rate
    shipping = 1800.0
    duty = (net_eur + shipping) * 0.10
    dph = (net_eur + shipping + duty) * 0.20
    total_cost = net_eur + shipping + duty + dph

    # 2. ДИНАМИЧЕСКАЯ ЛОГИКА (Профит зависит от возраста)
    car_age = datetime.now().year - year

    if car_age >= 25:
        markup = 1.50  # Классика (25+ лет) дает 50% наценки
    elif car_age >= 15:
        markup = 1.35  # Легенды (15-25 лет) дают 35%
    else:
        markup = 1.15  # Обычные авто дают 15%

    market_value = total_cost * markup
    profit = market_value - total_cost

    # Считаем реальный ROI: (Прибыль / Затраты) * 100
    actual_roi = (profit / total_cost) * 100

    return {
        "price_eur_net": round(net_eur, 2),
        "duty_amount": round(duty, 2),
        "dph_amount": round(dph, 2),
        "total_price": round(total_cost, 2),
        "market_value": round(market_value, 2),
        "potential_profit": round(profit, 2),
        "roi": round(actual_roi, 1)  # Теперь ROI будет разным!
    }