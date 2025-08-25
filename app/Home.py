import os, streamlit as st
st.set_page_config(page_title="Finance Copilot", page_icon="💸", layout="wide")
st.title("💸 Finance Copilot (Portia)")

BACKEND_URL = os.getenv("BACKEND_URL") or st.secrets.get("BACKEND_URL", "http://localhost:8000")
st.caption(f"API: {BACKEND_URL}")

st.page_link("pages/1_Overview.py", label="Overview", icon="🏠")
st.page_link("pages/2_Expenses.py", label="Expenses", icon="🧾")
st.page_link("pages/3_Forecast.py", label="Forecast", icon="📈")
st.page_link("pages/4_AI_Insights.py", label="AI Insights", icon="🧠")

