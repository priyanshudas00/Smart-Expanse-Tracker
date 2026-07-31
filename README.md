# Smart Expense Tracker API

A simple REST API for managing personal expenses built with FastAPI. Expenses are stored in a local JSON file, so no database is required.

## Features
- Add an expense with title, amount, category, and date
- View all expenses
- Filter expenses by category
- Calculate total expenses overall and by category
- Delete an expense
- Interactive OpenAPI/Swagger documentation at /docs

## Project structure
- README.md — project overview and run instructions
- AI_NOTES.md — notes about AI usage and validation
- src/ — FastAPI application code
- tests/ — pytest test suite

## Installation
```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If you are using PowerShell and see an execution policy error, the one-line command above temporarily allows the activation script for the current shell session.

## Start the server
```powershell
python -m uvicorn src.main:app --reload
```

The API will be available at:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

## API endpoints
- POST /expenses — create an expense
- GET /expenses — list all expenses
- GET /expenses?category=Food — filter by category
- GET /expenses/summary — overall and per-category totals
- DELETE /expenses/{expense_id} — delete an expense

## Run tests
```powershell
python -m pytest -q tests/
```

## Example request
```json
{
  "title": "Lunch",
  "amount": 12.5,
  "category": "Food",
  "date": "2026-07-31"
}
```

Example response:
```json
{
  "id": 1,
  "title": "Lunch",
  "amount": 12.5,
  "category": "Food",
  "date": "2026-07-31"
}
```