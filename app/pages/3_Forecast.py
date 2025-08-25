import streamlit as st, pandas as pd
st.title("Forecast (demo)")
try:
    from prophet import Prophet
    import plotly.express as px
    df = pd.read_csv("data/sample_prices.csv")
    m = Prophet(daily_seasonality=False, weekly_seasonality=True, yearly_seasonality=True)
    tmp = df.rename(columns={"date": "ds", "close": "y"})
    m.fit(tmp)
    future = m.make_future_dataframe(periods=30)
    forecast = m.predict(future)
    st.plotly_chart(px.line(forecast, x="ds", y="yhat", title="30-Day Forecast"), use_container_width=True)
except Exception as e:
    st.error(f"Forecast unavailable (install Prophet). Error: {e}")
