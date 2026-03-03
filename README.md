# 🏎️ JDM Sniper: Professional Import & Arbitrage Terminal

**JDM Sniper** is a full-stack analytical platform designed for automotive traders and enthusiasts to calculate the financial viability of importing vehicles from Japan to the European Union (specifically Slovakia/Central Europe).

It bridges the gap between raw auction data and real-world profitability by accounting for live exchange rates, EU customs regulations, and market trends.

---

## 🌟 Key Features
- **Investment Analysis:** Calculate total "on-the-road" costs including Net Price, EU Customs Duty (10%), and VAT/DPH (20%).
- **Market Arbitrage Engine:** Automatically estimates potential profit and **ROI (Return on Investment)** based on vehicle age and rarity.
- **Secure Architecture:** Implemented **JWT (JSON Web Tokens)** authentication with **Bcrypt** password hashing.
- **Data Persistence:** Relational database storage (SQLite/SQLAlchemy) with user-specific history logs.
- **Interactive Dashboard:** Modern UI built with Streamlit featuring real-time financial charts powered by Plotly.

---

## 🛠 Tech Stack
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Asynchronous Python Framework)
- **Frontend:** [Streamlit](https://streamlit.io/) (Data Science UI Framework)
- **Database:** SQLite with [SQLAlchemy ORM](https://www.sqlalchemy.org/)
- **Security:** OAuth2 with JWT Bearer tokens
- **Visualization:** Plotly Graph Objects
- **External API Integration:** Real-time Currency Exchange Rate API

---

## 📂 Project Architecture
The project follows **Clean Architecture** principles with a strict separation of concerns:
```text
JDMSniper/
├── app/
│   ├── main.py          # FastAPI application entry & routes
│   ├── models.py        # SQLAlchemy database models (User & Car relationship)
│   ├── schemas.py       # Pydantic data validation rules
│   ├── services.py      # Business logic & Financial formulas (Service Layer)
│   ├── database.py      # Database engine & session configuration
│   ├── security.py      # JWT logic, Hashing, and Authentication
│   └── frontend.py      # Streamlit Dashboard UI
├── .streamlit/
│   └── config.toml      # Custom theme configuration
├── requirements.txt     # Dependency list
└── README.md            # Documentation