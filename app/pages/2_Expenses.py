import os, streamlit as st, pandas as pd, plotly.express as px, requests

st.title("Expenses")
BACKEND = os.getenv("BACKEND_URL") or st.secrets.get("BACKEND_URL", "http://localhost:8000")

uploaded = st.file_uploader("Upload expenses CSV (date,merchant,amount,category,notes)", type=["csv"])
if uploaded:
    df = pd.read_csv(uploaded)
else:
    df = pd.read_csv("data/sample_expenses.csv")

use_portia = st.checkbox("Use Portia Transaction Enricher", value=True)
if use_portia:
    rows = df[["date","merchant","amount"]].copy()
    rows["currency"] = "INR"; rows["notes"] = ""
    payload = {"transactions": rows.head(80).to_dict(orient="records")}
    try:
        res = requests.post(f"{BACKEND}/portia/enrich", json=payload, timeout=30).json()
        enriched = pd.DataFrame(res["rows"])
        if "category" in enriched.columns:
            df = df.merge(enriched[["date","merchant","amount","category","merchant_normalized","anomaly"]],
                          on=["date","merchant","amount"], how="left", suffixes=("", "_enriched"))
            df["category"] = df["category_enriched"].fillna(df.get("category"))
            df.drop(columns=[c for c in df.columns if c.endswith("_enriched")], inplace=True)
    except Exception as e:
        st.warning(f"Portia enrich failed, showing raw: {e}")

st.dataframe(df, use_container_width=True)

by_cat = df.groupby("category")["amount"].sum().reset_index()
st.plotly_chart(px.pie(by_cat, names="category", values="amount", title="Spend by Category"), use_container_width=True)

df["date"] = pd.to_datetime(df["date"])
by_day = df.groupby("date")["amount"].sum().reset_index()
st.plotly_chart(px.line(by_day, x="date", y="amount", title="Daily Spend"), use_container_width=True)
