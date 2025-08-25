from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any
from apscheduler.schedulers.background import BackgroundScheduler

from backend.services.whatsapp_alerts import send_whatsapp_alert
from backend.services.recommend import recommend
from backend.services.portia_agent import enrich_transactions, coach_tips, coach_plan, market_pulse
from backend.services.guardrails import review_plan

app = FastAPI(title="Finance Copilot API (Portia)", version="1.2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# ==== Schemas ====
class Tx(BaseModel):
    date: str
    merchant: str
    amount: float
    currency: str = "INR"
    notes: str = ""

class EnrichPayload(BaseModel):
    transactions: List[Tx]

class CoachPayload(BaseModel):
    monthly_income: float
    category_totals: Dict[str, float]

class PulsePayload(BaseModel):
    tickers: List[str]

class AlertPayload(BaseModel):
    message: str

@app.get("/health")
def health():
    return {"status": "ok"}

# ---- Portia: Enrich uploaded expenses ----
@app.post("/portia/enrich")
def portia_enrich(payload: EnrichPayload = Body(...)):
    try:
        rows = [t.dict() for t in payload.transactions]
        enriched = enrich_transactions(rows)
        return {"rows": enriched}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---- Portia: Budget coach (tips) ----
@app.post("/portia/coach/tips")
def portia_coach_tips(payload: CoachPayload = Body(...)):
    try:
        return coach_tips(payload.monthly_income, payload.category_totals)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---- Portia: Budget coach (plan->approve->execute) ----
@app.post("/portia/coach/plan")
def portia_coach_plan(payload: CoachPayload = Body(...)):
    try:
        plan = coach_plan(payload.monthly_income, payload.category_totals).get("plan", [])
        review = review_plan(plan)
        return review  # {approved, reasons, filtered_plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/portia/coach/execute")
def portia_coach_execute(body: Dict[str, Any] = Body(...)):
    """
    Expects: { 'plan': [{action:'send_whatsapp_summary', params:{message:'..'}}] }
    """
    try:
        review = review_plan(body.get("plan", []))
        if not review["approved"]:
            return {"executed": False, "reasons": review["reasons"]}

        executed = []
        for step in review["filtered_plan"]:
            action = step["action"]
            params = step.get("params", {})
            if action == "send_whatsapp_summary":
                ok = send_whatsapp_alert(params.get("message", ""))
                executed.append({"action": action, "ok": ok})
        return {"executed": True, "steps": executed}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---- Portia: Market pulse ----
@app.post("/portia/market-pulse")
def portia_pulse(payload: PulsePayload = Body(...)):
    try:
        return market_pulse(payload.tickers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---- Heuristic fallback (offline) ----
@app.post("/recommend")
def recommend_api(payload: CoachPayload = Body(...)):
    try:
        tips = recommend({"monthly_income": payload.monthly_income, "category_totals": payload.category_totals})
        return {"advice": tips}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---- Optional: daily digest scheduler (WhatsApp) ----
def _daily_digest():
    try:
        res = coach_tips(60000, {"Dining": 5500, "Shopping": 4200, "Groceries": 6000, "Transport": 1800})
        summary = res.get("summary", "Your daily digest is ready.")
        send_whatsapp_alert(f"📊 {summary}")
        print("[Digest] Sent:", summary)
    except Exception as e:
        print("[Digest] Error:", e)

try:
    sched = BackgroundScheduler()
    sched.add_job(_daily_digest, "cron", hour=8, minute=0)  # runs daily 08:00 server time
    sched.start()
except Exception as e:
    print("[Scheduler] Not started:", e)
