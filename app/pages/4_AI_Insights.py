import os, streamlit as st, requests

st.title("AI Insights (Portia)")
BACKEND = os.getenv("BACKEND_URL") or st.secrets.get("BACKEND_URL", "http://localhost:8000")

income = st.number_input("Monthly income (₹)", min_value=0, value=60000, step=1000)
dining = st.number_input("Dining (₹)", min_value=0, value=5500, step=100)
shopping = st.number_input("Shopping (₹)", min_value=0, value=4200, step=100)
transport = st.number_input("Transport (₹)", min_value=0, value=1800, step=100)
groceries = st.number_input("Groceries (₹)", min_value=0, value=6000, step=100)

payload = {
    "monthly_income": income,
    "category_totals": {
        "Dining": dining, "Shopping": shopping, "Transport": transport, "Groceries": groceries
    }
}

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Get Tips (Portia)"):
        try:
            data = requests.post(f"{BACKEND}/portia/coach/tips", json=payload, timeout=30).json()
            st.subheader("Advice")
            for t in data.get("tips", []):
                st.write("•", t)
            st.info("Use 'Preview Plan' to approve actions before execution.")
        except Exception as e:
            st.error(e)

with col2:
    if st.button("Preview Plan"):
        try:
            review = requests.post(f"{BACKEND}/portia/coach/plan", json=payload, timeout=30).json()
            st.session_state["plan"] = review
            st.subheader("Plan Review")
            st.write("Approved:", review.get("approved"))
            if review.get("reasons"):
                st.write("Reasons:", review["reasons"])
            for step in review.get("filtered_plan", []):
                st.code(step)
        except Exception as e:
            st.error(e)

with col3:
    if st.button("Approve & Execute"):
        plan = st.session_state.get("plan", {}).get("filtered_plan", [])
        try:
            res = requests.post(f"{BACKEND}/portia/coach/execute", json={"plan": plan}, timeout=30).json()
            st.success(res)
        except Exception as e:
            st.error(e)
