import pandas as pd
from src.core.weights import monthly_category_weights
from src.core.indices import weighted_monthly_inflation


def build_cpi_panel(cpi_series: dict) -> pd.DataFrame:
    """
    Build a CPI panel from multiple category series.
    cpi_series: dict[str, pd.DataFrame] where each df has columns: date, cpi
    Returns a panel with columns: month, category, cpi
    """
    frames = []
    for category, df in cpi_series.items():
        tmp = df.copy()
        tmp = tmp.rename(columns={"date": "month"})
        tmp["month"] = pd.to_datetime(
            tmp["month"]).dt.to_period("M").dt.to_timestamp()
        tmp["category"] = category
        tmp = tmp[["month", "category", "cpi"]]
        frames.append(tmp)

    panel = pd.concat(frames, ignore_index=True).sort_values(
        ["category", "month"])
    return panel


def compute_personal_inflation(transactions: pd.DataFrame, cpi_panel: pd.DataFrame) -> pd.Series:
    """
    End-to-end: compute monthly personal inflation from transactions and CPI panel.
    """
    weights = monthly_category_weights(
        transactions)[["month", "category", "weight"]]
    return weighted_monthly_inflation(weights, cpi_panel)
