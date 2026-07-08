from collections import defaultdict

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

API_KEY = "ak_c0p95osmfblrm1u2r9zhki5d"
EMAIL = "24f1001162@ds.study.iitm.ac.in"   # replace if your exam email is different

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class EventRequest(BaseModel):
    events: list[Event]


@app.post("/analytics")
def analytics(
    request: EventRequest,
    x_api_key: str | None = Header(default=None),
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    total_events = len(request.events)

    unique_users = len({e.user for e in request.events})

    revenue = sum(e.amount for e in request.events if e.amount > 0)

    totals = defaultdict(float)

    for e in request.events:
        if e.amount > 0:
            totals[e.user] += e.amount

    top_user = max(totals, key=totals.get) if totals else ""

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user,
    }