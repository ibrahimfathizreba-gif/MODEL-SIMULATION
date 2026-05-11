"""
ML Forecaster — RandomForestRegressor trained on World Bank data 2000-2024.
Produces a forecasting baseline for years 2025-2044.
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error
from typing import Dict, List, Any

from backend.simulation import fetch_world_bank_data, fetch_ilo_data


def _build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Engineer lag and trend features from raw time-series data."""
    df = df.copy().sort_values("year").reset_index(drop=True)
    df["lag1"]  = df["unemployment_rate"].shift(1)
    df["lag2"]  = df["unemployment_rate"].shift(2)
    df["lag3"]  = df["unemployment_rate"].shift(3)
    df["trend"] = df["year"] - df["year"].min()
    df["rolling3"] = df["unemployment_rate"].rolling(3).mean()
    # AI proxy: exponential growth from 2015
    df["ai_proxy"] = df["year"].apply(lambda y: max(0, (y - 2015) ** 2 / 100))
    return df.dropna().reset_index(drop=True)


def load_training_data() -> pd.DataFrame:
    """Load and merge World Bank + ILO data into a unified training frame."""
    wb_unem  = fetch_world_bank_data("SL.UEM.TOTL.ZS", start=2000, end=2024)
    wb_labor = fetch_world_bank_data("SL.TLF.TOTL.IN", start=2000, end=2024)
    ilo      = fetch_ilo_data()

    df = wb_unem.rename(columns={"value": "unemployment_rate"})
    df = df.merge(wb_labor.rename(columns={"value": "workforce"}), on="year", how="left")
    df = df.merge(ilo[["year", "participation_rate"]], on="year", how="left")

    # Interpolate missing values
    for col in df.columns:
        if col != "year":
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].interpolate(method="linear").bfill().ffill()

    return df


def train_forecaster() -> Dict[str, Any]:
    """
    Train RandomForestRegressor on historical 2000-2024 data.
    Returns trained model, scaler, and training metrics.
    """
    raw = load_training_data()
    df  = _build_features(raw)

    feature_cols = ["trend", "lag1", "lag2", "lag3", "rolling3", "ai_proxy"]
    X = df[feature_cols].values
    y = df["unemployment_rate"].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=8,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_scaled, y)

    train_preds = model.predict(X_scaled)
    mae = mean_absolute_error(y, train_preds)
    accuracy = max(0.0, 100 - mae * 10)

    return {
        "model":    model,
        "scaler":   scaler,
        "mae":      round(mae, 4),
        "accuracy": round(accuracy, 2),
        "years_trained": df["year"].tolist(),
        "feature_cols":  feature_cols,
    }


def forecast_unemployment(horizon_start: int = 2025,
                           horizon_end: int = 2044) -> Dict[str, Any]:
    """
    Produce unemployment forecast for 2025-2044 using the trained RF model.
    Returns years, predicted values, and feature importances.
    """
    trained = train_forecaster()
    model  = trained["model"]
    scaler = trained["scaler"]

    # Seed the forecast with the last known values
    raw = load_training_data()
    last_known = raw.sort_values("year").tail(5)["unemployment_rate"].tolist()

    forecast_years  = list(range(horizon_start, horizon_end + 1))
    forecast_values = []
    history = list(last_known)

    base_year = raw["year"].min()

    for yr in forecast_years:
        lag1     = history[-1] if len(history) >= 1 else 5.0
        lag2     = history[-2] if len(history) >= 2 else 5.0
        lag3     = history[-3] if len(history) >= 3 else 5.0
        rolling3 = np.mean(history[-3:]) if len(history) >= 3 else lag1
        trend    = yr - base_year
        ai_proxy = max(0, (yr - 2015) ** 2 / 100)

        feats = np.array([[trend, lag1, lag2, lag3, rolling3, ai_proxy]])
        feats_scaled = scaler.transform(feats)
        pred = float(model.predict(feats_scaled)[0])
        pred = round(max(0.0, pred), 3)

        forecast_values.append(pred)
        history.append(pred)

    importances = dict(zip(
        trained["feature_cols"],
        [round(float(v), 4) for v in model.feature_importances_]
    ))

    return {
        "years":              forecast_years,
        "predicted_unemployment": forecast_values,
        "model_accuracy":     trained["accuracy"],
        "model_mae":          trained["mae"],
        "feature_importances": importances,
    }
