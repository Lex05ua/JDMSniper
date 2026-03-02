import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

# 1. Глобальный конфиг
st.set_page_config(page_title="JDM Sniper Intelligence", page_icon="🏎️", layout="wide")

# 2. ПРОФЕССИОНАЛЬНЫЙ UI СТИЛЬ (Modern Steel & Indigo)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    .stApp { background-color: #0f172a; font-family: 'Inter', sans-serif; color: #f1f5f9; }

    /* Стилизация карточек */
    .report-card {
        background-color: #1e293b;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 20px;
    }

    /* Заголовки */
    h1, h2, h3 { color: #f8fafc !important; font-weight: 800 !important; }

    /* Кнопка */
    .stButton>button {
        background: #3b82f6 !important;
        color: white !important;
        border: none !important;
        font-weight: 700 !important;
        padding: 12px !important;
        width: 100%;
        border-radius: 8px !important;
        transition: 0.3s;
    }
    .stButton>button:hover { background: #2563eb !important; transform: translateY(-2px); }

    /* Таблицы */
    .stDataFrame { background-color: #1e293b; border-radius: 10px; }

    /* Скрытие мусора */
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

BASE_URL = "http://127.0.0.1:8000"

if "token" not in st.session_state:
    st.session_state.token = None

# --- SIDEBAR (СТРОГИЙ СТИЛЬ) ---
with st.sidebar:
    st.markdown("<h2 style='color: #3b82f6;'>JDM SNIPER</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8;'>Professional Import Terminal</p>", unsafe_allow_html=True)
    st.write("---")

    if st.session_state.token:
        menu = st.radio("NAVIGATION", ["🚀 Analysis Terminal", "📊 Archive Log"])
        st.write("---")
        if st.button("Logout"):
            st.session_state.token = None
            st.rerun()
    else:
        menu = "Auth"

# --- MAIN CONTENT ---
if menu == "Auth":
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown('<div class="report-card">', unsafe_allow_html=True)
        st.subheader("System Access")
        tab1, tab2 = st.tabs(["Login", "Register"])
        with tab1:
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("ACCESS TERMINAL"):
                try:
                    res = requests.post(f"{BASE_URL}/token", data={"username": u, "password": p})
                    if res.status_code == 200:
                        st.session_state.token = res.json()["access_token"]
                        st.rerun()
                    else:
                        st.error("Access Denied")
                except:
                    st.error("Backend Offline")
        with tab2:
            nu = st.text_input("New Username")
            np = st.text_input("New Password", type="password")
            if st.button("CREATE ACCOUNT"):
                requests.post(f"{BASE_URL}/register", json={"username": nu, "password": np})
                st.success("User created!")
        st.markdown('</div>', unsafe_allow_html=True)

elif menu == "🚀 Analysis Terminal":
    st.title("Market Intelligence")

    # СЕКЦИЯ ВВОДА
    with st.container():
        st.markdown('<div class="report-card">', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        brand = c1.selectbox("Manufacturer", ["Nissan", "Toyota", "Mazda", "Subaru", "Mitsubishi", "Honda"])
        model = c2.text_input("Model Name", "Skyline GT-R R34")
        year = c3.number_input("Year", 1980, 2026, 1999)
        price_jpy = c4.number_input("Auction Price (JPY)", min_value=100000, value=4000000, step=100000)

        analyze = st.button("GENERATE INVESTMENT REPORT")
        st.markdown('</div>', unsafe_allow_html=True)

    if analyze:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        payload = {"brand": brand, "model": model, "year": year, "price_jpy": price_jpy}
        res = requests.post(f"{BASE_URL}/calculate", json=payload, headers=headers)

        if res.status_code == 200:
            data = res.json()

            # РАСЧЕТЫ ДЛЯ СРАВНЕНИЯ (ПРИБЫЛЬ)
            duty = data['price_eur_net'] * 0.10  # 10% Пошлина
            total_invested = data['total_price'] + duty
            est_eu_market_value = total_invested * 1.35  # Симуляция: +35% цена в Европе
            net_profit = est_eu_market_value - total_invested

            # --- ВЕРХНЯЯ ПАНЕЛЬ С ГЛАВНЫМИ ЦИФРАМИ ---
            st.markdown("### 📋 Executive Summary")
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Investment", f"€{total_invested:,.2f}", help="Price + Shipping + Duty + VAT")
            m2.metric("EU Market Value", f"€{est_eu_market_value:,.2f}",
                      help="Estimated resale price in Germany/Slovakia")
            m3.metric("Potential Profit", f"€{net_profit:,.2f}", delta=f"{35}% ROI", delta_color="normal")

            # --- ПОДРОБНЫЙ РАЗБОР ---
            st.write("##")
            col_table, col_chart = st.columns([1, 1])

            with col_table:
                st.markdown("**Cost Breakdown (Detailed)**")
                breakdown_data = {
                    "Description": ["Net Car Price (Japan)", "EU Import Duty (10%)", "VAT / DPH (20%)",
                                    "Logistics & Fees"],
                    "Amount (EUR)": [f"€{data['price_eur_net']:,.2f}", f"€{duty:,.2f}", f"€{data['dph_amount']:,.2f}",
                                     "Included"]
                }
                st.table(pd.DataFrame(breakdown_data))

            with col_chart:
                st.markdown("**Budget Distribution**")
                # Красивый Donut Chart
                fig = go.Figure(data=[go.Pie(
                    labels=['Car Price', 'Taxes (Duty+VAT)', 'Profit Margin'],
                    values=[data['price_eur_net'], duty + data['dph_amount'], net_profit],
                    hole=.5,
                    marker_colors=['#3b82f6', '#ef4444', '#10b981']
                )])
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", height=300,
                                  margin=dict(t=0, b=0, l=0, r=0))
                st.plotly_chart(fig, use_container_width=True)

            # ВЕРДИКТ
            st.info(
                f"💡 **Strategy:** To maximize profit, consider shipping to a low-cost port and verifying the {brand}'s service history.")
        else:
            st.error("Authentication expired. Please login again.")

elif menu == "📊 Archive Log":
    st.title("Transaction History")
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    res = requests.get(f"{BASE_URL}/history", headers=headers)

    if res.status_code == 200:
        data = res.json()
        if data:
            df = pd.DataFrame(data)
            df_display = df[['brand', 'model', 'price_jpy', 'total_price']].copy()
            df_display.columns = ['Brand', 'Model', 'JPY Bid', 'Total Cost (EUR)']
            st.markdown('<div class="report-card">', unsafe_allow_html=True)
            st.dataframe(df_display, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No data available in your personal archive.")