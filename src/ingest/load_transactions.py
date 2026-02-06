import pandas as pd

REQUIRED_COLS = {"date", "amount", "category"}


def load_transactions(path: str) -> pd.DataFrame:
    """
    Load mock (or real) transactions from CSV.
    Expected columns: date, amount, category
    Returns a dataframe with parsed dates and positive amounts.
    """
    df = pd.read_csv(path)

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in {path}: {missing}")

    df["date"] = pd.to_datetime(df["date"])
    df["amount"] = pd.to_numeric(df["amount"], errors="raise")

    if (df["amount"] <= 0).any():
        raise ValueError(
            "Transactions should have positive amounts for this demo.")

    df["category"] = df["category"].astype(str).str.strip().str.lower()
    return df.sort_values("date").reset_index(drop=True)
