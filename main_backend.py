from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date

app = FastAPI(title="AI Payment Recovery Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

invoices = []

class Invoice(BaseModel):
    customer: str
    amount: float
    due_date: str

def calculate_priority(amount, due_date):
    try:
        due = date.fromisoformat(due_date)
        overdue_days = max((date.today() - due).days, 0)
    except ValueError:
        overdue_days = 0

    score = 0

    if overdue_days > 30:
        score += 60
    elif overdue_days > 7:
        score += 40
    elif overdue_days > 0:
        score += 20

    if amount >= 100000:
        score += 40
    elif amount >= 50000:
        score += 25
    elif amount >= 10000:
        score += 15
    else:
        score += 5

    if score >= 75:
        priority = "High"
    elif score >= 40:
        priority = "Medium"
    else:
        priority = "Low"

    return priority, score, overdue_days

def reminder(customer, amount, overdue_days):
    if overdue_days > 0:
        return (
            f"Hello {customer}, your payment of ₹{amount:,.2f} is "
            f"{overdue_days} days overdue. Please complete the payment "
            "at your earliest convenience. Thank you."
        )
    return (
        f"Hello {customer}, your payment of ₹{amount:,.2f} is due soon. "
        "Please make the payment on time. Thank you."
    )

@app.get("/")
def home():
    return {"message": "AI Payment Recovery Assistant API is running"}

@app.get("/invoices")
def get_invoices():
    result = []
    for invoice in invoices:
        priority, score, overdue_days = calculate_priority(
            invoice["amount"], invoice["due_date"]
        )
        result.append({
            **invoice,
            "priority": priority,
            "score": score,
            "overdue_days": overdue_days,
            "reminder": reminder(invoice["customer"], invoice["amount"], overdue_days)
        })
    return result

@app.post("/invoices")
def add_invoice(invoice: Invoice):
    item = invoice.model_dump()
    invoices.append(item)
    priority, score, overdue_days = calculate_priority(
        item["amount"], item["due_date"]
    )
    return {
        **item,
        "priority": priority,
        "score": score,
        "overdue_days": overdue_days,
        "reminder": reminder(item["customer"], item["amount"], overdue_days)
    }

@app.delete("/invoices")
def clear_invoices():
    invoices.clear()
    return {"message": "All invoices cleared"}
