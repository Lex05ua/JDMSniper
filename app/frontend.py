import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

# 1. ГЛОБАЛЬНАЯ НАСТРОЙКА
st.set_page_config(page_title="JDM Sniper Terminal", page_icon="🏎️", layout="wide")

# 2. ЖЕСТКИЙ ФИКС КОНТРАСТНОСТИ (Яркий текст на темном фоне)
st.markdown("""
    <style>
    /* Фон всей страницы */
    .stApp { background-color: #0f172a; }

    /* Стилизация метрик (Цифр) */
    [data-testid="stMetricValue"] {
        color: #ffffff !important; 
        font-size: 36px !important; 
        font-weight: 800 !important;
    }

    /* Стилизация подписей к метрикам */
    [data-testid="stMetricLabel"] p {
        color: #94a3b8 !important; 
        font-size: 16px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Цвет ROI (Зеленый бабл) */
    [data-testid="stMetricDelta"] svg { fill: #10b981 !important; }
    [data-testid="stMetricDelta"] div { color: #10b981 !important; font-weight: 700; }

    /* Карточки результатов */
    div[data-testid="stMetric"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px !important;
    }

    /* Заголовки */
    h1, h2, h3 { color: #ffffff !important; font-family: 'Inter', sans-serif; }

    /* Кнопка */
    .stButton>button {
        background-color: #3b82f6 !important;
        color: white !important;
        border: none !important;
        font-weight: 700 !important;
        height: 3.5rem;
        border-radius: 10px !important;
    }

    /* Боковая панель */
    [data-testid="stSidebar"] { background-color: #1e293b !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

BASE_URL = "http://127.0.0.1:8000"

if "token" not in st.session_state:
    st.session_state.token = None

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 🏎️ JDM SNIPER")
    st.write("---")
    if st.session_state.token:
        menu = st.radio("NAVIGATION", ["🚀 Analysis Terminal", "📊 History Archive"])
        st.write("---")
        if st.button("Logout"):
            st.session_state.token = None
            st.rerun()
    else:
        menu = "Auth"

# --- MAIN ---
if menu == "Auth":
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.subheader("System Login")
        t1, t2 = st.tabs(["Login", "Register"])
        with t1:
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("ENTER TERMINAL"):
                try:
                    res = requests.post(f"{BASE_URL}/token", data={"username": u, "password": p})
                    if res.status_code == 200:
                        st.session_state.token = res.json()["access_token"]
                        st.rerun()
                    else:
                        st.error("Wrong credentials")
                except:
                    st.error("Backend offline")
        with t2:
            nu = st.text_input("New User")
            np = st.text_input("New Pass", type="password")
            if st.button("CREATE ACCOUNT"):
                requests.post(f"{BASE_URL}/register", json={"username": nu, "password": np})
                st.success("User created! Switch to Login.")

elif menu == "🚀 Analysis Terminal":
    st.title("Market Intelligence Engine")

    # ВВОД ДАННЫХ
    with st.container():
        c1, c2, c3, c4 = st.columns(4)
        brand = c1.selectbox("Manufacturer", ["Nissan", "Toyota", "Mazda", "Subaru", "Honda", "Mitsubishi"])
        model = c2.text_input("Model Name", placeholder="e.g. Skyline")
        year = c3.number_input("Year", 1980, 2026, 1999)
        price_jpy = c4.number_input("Auction Bid (JPY)", min_value=100000, value=3500000, step=100000)

        submit = st.button("RUN FINANCIAL MODEL")

    if submit:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        payload = {"brand": brand, "model": model, "year": year, "price_jpy": price_jpy}
        res = requests.post(f"{BASE_URL}/calculate", json=payload, headers=headers)

        if res.status_code == 200:
            data = res.json()

            st.markdown("---")
            st.subheader(f"Investment Report: {brand} {model} ({year})")

            # ГЛАВНЫЕ МЕТРИКИ (Теперь они яркие и читаемые!)
            m1, m2, m3 = st.columns(3)
            m1.metric("TOTAL INVESTMENT", f"€{data['total_price']:,.2f}")
            m2.metric("EU MARKET VALUE", f"€{data['market_value']:,.2f}")
            m3.metric("POTENTIAL PROFIT", f"€{data['potential_profit']:,.2f}", delta=f"{data['roi']}% ROI")

            # РАЗБОР И ГРАФИК
            st.write("##")
            col_l, col_r = st.columns([1, 1.2])

            with col_l:
                st.markdown("### 📝 Financial Breakdown")
                st.write(f"✅ **Net Car Price:** €{data['price_eur_net']:,.2f}")
                st.write(f"🏛️ **EU Customs Duty (10%):** €{data['duty_amount']:,.2f}")
                st.write(f"📑 **VAT / DPH (20%):** €{data['dph_amount']:,.2f}")
                st.write(f"⚓ **Logistics (Fixed):** €1,800.00")

            with col_r:
                fig = go.Figure(data=[go.Pie(
                    labels=['Net Price', 'Taxes', 'Profit'],
                    values=[data['price_eur_net'], data['duty_amount'] + data['dph_amount'], data['potential_profit']],
                    hole=.5, marker_colors=['#3b82f6', '#ef4444', '#10b981']
                )])
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", height=300,
                                  margin=dict(t=0, b=0, l=0, r=0))
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Error: Session expired or backend down.")

elif menu == "📊 History Archive":
    st.header("Search History")
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    res = requests.get(f"{BASE_URL}/history", headers=headers)
    if res.status_code == 200:
        data = res.json()
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df[['brand', 'model', 'price_jpy', 'total_price', 'potential_profit']],
                         use_container_width=True)
        else:
            st.info("No records found.")