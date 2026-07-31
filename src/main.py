import json
import os
from datetime import date
from typing import Optional

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

app = FastAPI(title="Smart Expense Tracker API")


class ExpenseCreate(BaseModel):
    title: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    category: str = Field(..., min_length=1)
    date: date


class Expense(ExpenseCreate):
    id: int


DATA_FILE = os.getenv("EXPENSES_FILE", os.path.join(os.path.dirname(__file__), "expenses.json"))
expenses: list[Expense] = []
next_id = 1


def load_expenses() -> list[Expense]:
    global expenses
    if expenses:
        return expenses
    if not os.path.exists(DATA_FILE):
        expenses = []
        return expenses
    with open(DATA_FILE, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    expenses = [Expense(**item) for item in data]
    return expenses


def save_expenses(expense_list: list[Expense]) -> None:
    global expenses
    expenses = list(expense_list)
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as handle:
        json.dump([expense.model_dump(mode="json") for expense in expenses], handle, indent=2)


def refresh_next_id() -> None:
    global next_id
    next_id = max((expense.id for expense in load_expenses()), default=0) + 1


refresh_next_id()


@app.get("/")
def root():
    return {"message": "Smart Expense Tracker API is running"}


@app.post("/expenses", response_model=Expense, status_code=status.HTTP_201_CREATED)
def create_expense(payload: ExpenseCreate):
    global next_id
    if next_id < 1:
        refresh_next_id()
    expense = Expense(id=next_id, **payload.model_dump())
    next_id += 1
    expense_list = load_expenses() + [expense]
    save_expenses(expense_list)
    return expense


@app.get("/expenses", response_model=list[Expense])
def list_expenses(category: Optional[str] = Query(None)):
    expense_list = load_expenses()
    if category:
        expense_list = [item for item in expense_list if item.category.lower() == category.lower()]
    return expense_list


@app.get("/expenses/summary")
def expense_summary():
    expense_list = load_expenses()
    by_category: dict[str, float] = {}
    for expense in expense_list:
        by_category[expense.category] = by_category.get(expense.category, 0.0) + expense.amount
    return {
        "total": round(sum(expense.amount for expense in expense_list), 2),
        "by_category": {key: round(value, 2) for key, value in sorted(by_category.items())},
    }


@app.get("/expenses/total")
def total_expenses(category: Optional[str] = Query(None)):
    expense_list = load_expenses()
    overall_total = round(sum(expense.amount for expense in expense_list), 2)
    by_category: dict[str, float] = {}
    for expense in expense_list:
        by_category[expense.category] = by_category.get(expense.category, 0.0) + expense.amount

    if category:
        category_total = sum(expense.amount for expense in expense_list if expense.category.lower() == category.lower())
        return {
            "category": category,
            "total": round(category_total, 2),
            "overall_total": overall_total,
            "by_category": {key: round(value, 2) for key, value in sorted(by_category.items())},
        }
    return {
        "overall_total": overall_total,
        "by_category": {key: round(value, 2) for key, value in sorted(by_category.items())},
    }


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    expense_list = load_expenses()
    if not any(expense.id == expense_id for expense in expense_list):
        raise HTTPException(status_code=404, detail="Expense not found")
    updated = [expense for expense in expense_list if expense.id != expense_id]
    save_expenses(updated)
    return {"message": "Expense deleted successfully"}