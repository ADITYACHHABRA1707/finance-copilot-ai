import os, streamlit as st, requests
BACKEND = os.getenv("BACKEND_URL") or st.secrets.get("BACKEND_URL", "http://localhost:8000")

st.title("Overview")

tickers = st.text_input("Watchlist (comma-separated)", "TCS.NS,RELIANCE.NS,INFY.NS")
if st.button("Get Market Pulse (Portia)"):
    payload = {"tickers": [t.strip() for t in tickers.split(",") if t.strip()]}
    try:
        data = requests.post(f"{BACKEND}/portia/market-pulse", json=payload, timeout=30).json()
        st.write("**Top Movers:**", data.get("movers", []))
        bullets = data.get("bullets", {})
        for t, bl in bullets.items():
            st.markdown(f"**{t}**")
            for b in bl: st.write("-", b)
        st.write("**Action:**", data.get("action"))
    except Exception as e:
        st.error(e)

if st.button("🚨 Send WhatsApp Demo Alert"):
    requests.post(f"{BACKEND}/alerts/test", json={"message": "🚨 Demo: Budget threshold crossed!"})
    st.success("Tried sending WhatsApp alert (check Twilio sandbox).")
