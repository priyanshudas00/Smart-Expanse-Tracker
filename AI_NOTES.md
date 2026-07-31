# AI Notes

AI tools were used as a development assistant while building this project. I reviewed and tested the generated suggestions rather than using them without validation.

## 1. What AI was used for
I used ChatGPT to help with:
- planning a simple FastAPI project structure
- creating the initial Pydantic models
- implementing the FastAPI routes
- separating API routes from expense storage logic
- implementing local JSON file persistence
- writing initial pytest tests
- reviewing validation errors and JSON serialization issues
- improving the README and project documentation

## 2. What I validated or changed
### JSON persistence
The initial implementation used in-memory storage. I changed it to local JSON file storage so expenses remain available after restarting the server.

I verified that:
1. A new expense can be created with POST /expenses.
2. The expense is written to the local JSON file.
3. Deleting an expense updates the JSON file.

### Request validation
While testing POST /expenses, I encountered FastAPI validation errors. I verified that:
- title is required
- amount must be greater than zero
- category is required
- date must be a valid date format such as 2026-07-31

### Test isolation
I did not want the automated tests to modify the real data file. The pytest suite therefore uses a temporary file during each test run.

## 3. AI suggestions I did not use
- I did not add database support or an ORM because the assignment allows local JSON storage and does not require a database.
- I also avoided extra architecture such as repositories, routers, or authentication layers because this project is intentionally simple and focused on the assignment requirements.

## 4. Final validation
I validated the project by running:
- python -m pip install -r requirements.txt
- python -m uvicorn src.main:app --reload
- python -m pytest -q tests/
