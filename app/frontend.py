import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

# 1. Глобальный конфиг
st.set_page_config(page_title="JDM Sniper Intelligence", layout="wide")

BASE_URL = "http://127.0.0.1:8000"

if "token" not in st.session_state:
    st.session_state.token = None

# --- SIDEBAR ---
with st.sidebar:
    st.title("🏎️ JDM SNIPER")
    st.markdown("---")
    if st.session_state.token:
        # Используем кнопки для навигации (это надежнее радио-кнопок)
        if st.button("🚀 Analysis Terminal", use_container_width=True):
            st.session_state.page = "calc"
        if st.button("📊 History Archive", use_container_width=True):
            st.session_state.page = "history"
        st.markdown("---")
        if st.button("Logout", type="primary", use_container_width=True):
            st.session_state.token = None
            st.rerun()
    else:
        st.session_state.page = "auth"

# --- MAIN LOGIC ---

# 1. AUTH PAGE
if st.session_state.token is None:
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.header("Terminal Access")
        tab1, tab2 = st.tabs(["Login", "Register"])
        with tab1:
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("Sign In", use_container_width=True):
                try:
                    res = requests.post(f"{BASE_URL}/token", data={"username": u, "password": p})
                    if res.status_code == 200:
                        st.session_state.token = res.json()["access_token"]
                        st.session_state.page = "calc"
                        st.rerun()
                    else:
                        st.error("Access Denied")
                except:
                    st.error("Backend Offline")
        with tab2:
            nu = st.text_input("New Username")
            np = st.text_input("New Password", type="password")
            if st.button("Create Account", use_container_width=True):
                requests.post(f"{BASE_URL}/register", json={"username": nu, "password": np})
                st.success("User created! Go to Login.")

# 2. CALCULATOR PAGE
elif st.session_state.get("page") == "calc":
    st.title("Market Intelligence Engine")

    # Контейнер ввода (просто и чисто)
    with st.expander("Vehicle Parameters", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        brand = c1.selectbox("Manufacturer", ["Nissan", "Toyota", "Mazda", "Subaru", "Mitsubishi", "Honda"])
        model = c2.text_input("Model Name", "Skyline R34")
        year = c3.number_input("Year", 1980, 2026, 1999)
        price_jpy = c4.number_input("Auction Price (JPY)", min_value=100000, value=3000000)

        analyze = st.button("RUN FINANCIAL ANALYSIS", type="primary", use_container_width=True)

    if analyze:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        res = requests.post(f"{BASE_URL}/calculate",
                            json={"brand": brand, "model": model, "year": year, "price_jpy": price_jpy},
                            headers=headers)

        if res.status_code == 200:
            data = res.json()

            st.markdown("### 📊 Investment Summary")

            # Сетка с результатами
            m1, m2, m3 = st.columns(3)
            m1.metric("TOTAL INVESTMENT", f"€{data['total_price']:,.2f}")
            m2.metric("EU MARKET VALUE", f"€{data['market_value']:,.2f}")
            m3.metric("POTENTIAL PROFIT", f"€{data['potential_profit']:,.2f}", delta=f"{data['roi']}% ROI")

            col_l, col_r = st.columns([1, 1])
            with col_l:
                st.markdown("#### Cost Breakdown")
                st.write(f"✅ **Net Car Price:** €{data['price_eur_net']:,.2f}")
                st.write(f"🏛️ **Import Duty (10%):** €{data['duty_amount']:,.2f}")
                st.write(f"📑 **VAT / DPH (20%):** €{data['dph_amount']:,.2f}")
                st.write(f"⚓ **Logistics:** €1,800.00")

            with col_r:
                fig = go.Figure(data=[go.Pie(
                    labels=['Car', 'Taxes', 'Profit'],
                    values=[data['price_eur_net'], data['duty_amount'] + data['dph_amount'], data['potential_profit']],
                    hole=.5, marker_colors=['#3b82f6', '#ef4444', '#10b981']
                )])
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", height=300,
                                  margin=dict(t=0, b=0, l=0, r=0))
                st.plotly_chart(fig, use_container_width=True)

# 3. HISTORY PAGE
elif st.session_state.get("page") == "history":
    st.title("History Archive")
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    res = requests.get(f"{BASE_URL}/history", headers=headers)
    if res.status_code == 200:
        data = res.json()
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df[['brand', 'model', 'price_jpy', 'total_price', 'potential_profit']],
                         use_container_width=True)
        else:
            st.info("No history yet.")