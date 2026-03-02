import httpx
from fastapi import HTTPException

# Асинхронная функция: пока летит запрос в интернет, сервер не тупит.
async def get_jpy_rate():
    url = "https://open.er-api.com/v6/latest/EUR"
    async with httpx.AsyncClient() as client:
        try:
            # await говорит: "подожди ответа, но не блокируй процессор"
            response = await client.get(url, timeout=5.0)
            data = response.json()
            return data['rates']['JPY']
        except Exception:
            # Если интернет отвалился, вежливо отвечаем 503 (Сервис недоступен)
            raise HTTPException(status_code=503, detail="Currency API error")

def calculate_costs(price_jpy: int, rate: float):
    # Чистая математика. Легко тестировать отдельно.
    eur_net = price_jpy / rate
    dph = eur_net * 0.20
    return {
        "net": round(eur_net, 2),
        "dph": round(dph, 2),
        "total": round(eur_net + dph, 2)
    }


def calculate_full_import(price_jpy: int, rate: float, shipping_port: str):
    # 1. Конвертация
    net_price_eur = price_jpy / rate

    # 2. Логистика (упрощенно по портам)
    shipping_costs = {
        "Gdansk (PL)": 1800,
        "Rotterdam (NL)": 1500,
        "Koper (SI) - closest to SK": 1900
    }
    ship_fee = shipping_costs.get(shipping_port, 2000)

    # 3. Таможенная пошлина ЕС (10%) - считается от (Цена + Доставка)
    customs_duty_rate = 0.10
    duty_amount = (net_price_eur + ship_fee) * customs_duty_rate

    # 4. НДС / DPH (20%) - считается от (Цена + Доставка + Пошлина)
    vat_rate = 0.20
    vat_amount = (net_price_eur + ship_fee + duty_amount) * vat_rate

    total_cost = net_price_eur + ship_fee + duty_amount + vat_amount

    return {
        "net_price": round(net_price_eur, 2),
        "shipping": ship_fee,
        "duty": round(duty_amount, 2),
        "vat": round(vat_amount, 2),
        "total": round(total_cost, 2)
    }