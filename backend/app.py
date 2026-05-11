"""
FastAPI Backend — AI Labor Market Impact Simulation
4 endpoints: /api/simulate/{scenario}, /api/validate, /api/monte-carlo, /api/analyze
"""
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import traceback

from backend.simulation import (
    run_scenario, compare_scenarios, validate_model,
    monte_carlo_simulation, generate_report, export_to_csv,
    sensitivity_analysis,
)
from backend.ml_forecaster import forecast_unemployment
from backend.ai_analyzer import analyze_with_claude

app = FastAPI(
    title="AI Labor Market Impact Simulation API",
    description="Enterprise-grade 20-year labor market simulation driven by AI dynamics.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response Models ──────────────────────────────────────────────────

class SimulateParams(BaseModel):
    horizon:        Optional[int]   = 20
    adoption_speed: Optional[float] = 1.0
    export_csv:     Optional[bool]  = False


class AnalyzeRequest(BaseModel):
    scenario:       Optional[str]   = "moderate"
    horizon:        Optional[int]   = 20
    adoption_speed: Optional[float] = 1.0


# ── Endpoints ──────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "AI Labor Market Simulation API — PLUS ULTRA", "version": "1.0.0"}


@app.get("/api/simulate/{scenario}")
def simulate(
    scenario:       str,
    horizon:        int   = 20,
    adoption_speed: float = 1.0,
    export_csv:     bool  = False,
):
    """
    Run a full 20-year labor market simulation.
    Scenarios: slow | moderate | rapid
    """
    valid_scenarios = {"slow", "moderate", "rapid"}
    if scenario not in valid_scenarios:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid scenario '{scenario}'. Choose from: {valid_scenarios}",
        )
    try:
        results = run_scenario(scenario, horizon=horizon, adoption_speed=adoption_speed)
        results["report"] = generate_report(results)

        if export_csv:
            path = export_to_csv(results, f"simulation_{scenario}.csv")
            results["csv_path"] = path

        # Attach ML forecast
        try:
            ml_data = forecast_unemployment(2025, 2025 + horizon - 1)
            results["ml_forecast"] = ml_data
        except Exception:
            results["ml_forecast"] = None

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation error: {str(e)}\n{traceback.format_exc()}")


@app.get("/api/validate")
def validate():
    """
    Backtest model on 2000-2020 historical data.
    Returns: MAE, Accuracy %, and Predicted vs Actual arrays for chart rendering.
    """
    try:
        validation = validate_model()
        return {
            "mae":       validation["mae"],
            "accuracy":  validation["accuracy"],
            "years":     validation["years"],
            "predicted": validation["predicted"],
            "actual":    validation["actual"],
            "label":     "Model Backtest 2000-2020",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation error: {str(e)}")


@app.get("/api/monte-carlo")
def monte_carlo(n_simulations: int = 1000, horizon: int = 20):
    """
    Run Monte Carlo simulation (1000+ iterations).
    Returns results with 95% Confidence Intervals for unemployment and GDP.
    """
    n_simulations = min(max(n_simulations, 100), 5000)  # clamp for safety
    try:
        results = monte_carlo_simulation(n_simulations=n_simulations, horizon=horizon)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Monte Carlo error: {str(e)}")


@app.post("/api/analyze")
def analyze(body: AnalyzeRequest = Body(...)):
    """
    Run simulation then send results to Claude API.
    Returns Professional Economic Advisory Report in Arabic.
    """
    try:
        results  = run_scenario(body.scenario, horizon=body.horizon,
                                adoption_speed=body.adoption_speed)
        results["report"] = generate_report(results)
        ai_response = analyze_with_claude(results)
        return ai_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@app.get("/api/compare")
def compare(horizon: int = 20, adoption_speed: float = 1.0):
    """Return side-by-side comparison of all 3 scenarios."""
    try:
        return compare_scenarios(horizon=horizon, adoption_speed=adoption_speed)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sensitivity")
def sensitivity(scenario: str = "moderate"):
    """Return sensitivity analysis results."""
    try:
        return sensitivity_analysis(scenario)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
