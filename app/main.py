from fastapi import FastAPI, Depends
from app.db.session import engine
from app.db.base import Base
from app.api.deps import get_current_user
from app.api.routes import auth as auth_routes
from app.api.routes import groups as groups_routes
from app.api.routes import expenses as expenses_routes
from app.api.routes import balances as balances_routes
from app.api.routes import audit as audit_routes
from app.schemas.user import UserOut

# Create tables on startup (simplifies Iteration 1)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TCX2004 Shared Expense API")

@app.get("/auth/me", response_model=UserOut)
async def me(user=Depends(get_current_user)):
    return user

app.include_router(auth_routes.router)
app.include_router(groups_routes.router)
app.include_router(expenses_routes.router)
app.include_router(balances_routes.router)
app.include_router(audit_routes.router)

@app.get("/")
async def root():
    return {"status": "ok"}

