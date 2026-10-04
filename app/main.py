from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field

from app.data import CHECKED, PROJECTS

app = FastAPI(title="Element — Critical Minerals Desk")


class Scenario(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)
    price: float = Field(80, ge=0, le=1000)
    cost: float = Field(45, ge=0, le=1000)
    tonnes: float = Field(4000, gt=0, le=100000)
    capex: float = Field(1000, ge=0, le=100000)
    years: int = Field(20, ge=1, le=60)
    discount: float = Field(10, ge=0, le=50)
    delay: int = Field(2, ge=0, le=20)


def calculate(s: Scenario):
    annual = (s.price - s.cost) * s.tonnes * 1000 / 1e6
    factor = sum(1 / (1 + s.discount / 100) ** (year + s.delay)
                 for year in range(1, s.years + 1))
    npv = annual * factor - s.capex
    breakeven = s.cost + s.capex * 1e6 / (factor * s.tonnes * 1000)
    return {"npv_musd": round(npv, 3), "annual_musd": round(annual, 3),
            "breakeven_usd_kg": round(breakeven, 3),
            "sensitivity": [{"price": p, "npv": round((p-s.cost)*s.tonnes/1000*factor-s.capex, 3)}
                            for p in [40, 60, 80, 100, 120, 140]],
            "basis": "Hypothetical pre-tax unlevered operating cash-flow model; capex at time zero.",
            "exclusions": "Tax, royalties, sustaining capital, working capital, closure, financing, by-products and ramp-up."}


@app.get("/api/projects")
def projects():
    return {"checked": CHECKED, "mode": "Curated issuer snapshots", "projects": PROJECTS}


@app.post("/api/scenario")
def scenario(s: Scenario):
    return calculate(s)


@app.get("/health")
def health():
    return {"status": "ok"}


dist = Path(__file__).resolve().parents[1] / "frontend" / "dist"
if (dist / "assets").exists():
    app.mount("/assets", StaticFiles(directory=dist / "assets"), name="assets")


@app.get("/")
def index():
    if not (dist / "index.html").exists():
        return JSONResponse({"detail": "Build the frontend first."}, status_code=503)
    return FileResponse(dist / "index.html")
