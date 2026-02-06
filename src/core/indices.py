import pandas as pd


def monthly_inflation_from_index_levels(cpi: pd.Series) -> pd.Series:
    """
    Given CPI levels indexed by month, return monthly inflation:
    (CPI_t / CPI_{t-1}) - 1
    """
    return cpi.pct_change()


def weighted_monthly_inflation(weights_df: pd.DataFrame, cpi_by_category: pd.DataFrame) -> pd.Series:
    """
    Compute personal inflation as a weighted sum of category inflation rates.

    weights_df columns: month, category, weight
    cpi_by_category columns: month, category, cpi

    Returns a Series indexed by month of personal inflation.
    """
    df = cpi_by_category.copy().sort_values(["category", "month"])
    df["inflation"] = df.groupby("category")["cpi"].pct_change()

    joined = weights_df.merge(df[["month", "category", "inflation"]], on=[
                              "month", "category"], how="inner")

    # Multiply first, then sum by month (works in all pandas versions)
    joined["weighted_inflation"] = joined["weight"] * joined["inflation"]
    personal = joined.groupby("month")["weighted_inflation"].sum().sort_index()

    return personal
