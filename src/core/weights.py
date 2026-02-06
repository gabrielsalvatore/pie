import pandas as pd


def monthly_category_weights(transactions: pd.DataFrame) -> pd.DataFrame:
    """
    Compute monthly expenditure shares by category.
    Returns: month, category, spend, weight
    month is timestamp at month start (YYYY-MM-01).
    """
    df = transactions.copy()
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

    spend = (
        df.groupby(["month", "category"], as_index=False)["amount"]
        .sum()
        .rename(columns={"amount": "spend"})
    )

    totals = spend.groupby("month", as_index=False)[
        "spend"].sum().rename(columns={"spend": "total_spend"})
    merged = spend.merge(totals, on="month", how="left")
    merged["weight"] = merged["spend"] / merged["total_spend"]

    return merged.sort_values(["month", "category"]).reset_index(drop=True)
