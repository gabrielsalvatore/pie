import pandas as pd

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def load_cpi_wide(path: str, value_col_name: str = "cpi") -> pd.DataFrame:
    """
    Loads a CPI table in the 'wide' BLS format:
    Year,Jan,Feb,...,Dec

    Returns a tidy monthly time series:
    date, cpi
    where date is the first day of each month.
    """
    df = pd.read_csv(path)

    if "Year" not in df.columns:
        raise ValueError(f"{path} must include a 'Year' column.")

    for m in MONTHS:
        if m not in df.columns:
            raise ValueError(f"{path} missing month column: {m}")

    # Reshape wide -> long
    long_df = df.melt(id_vars=["Year"], value_vars=MONTHS,
                      var_name="month", value_name=value_col_name)

    # Convert to numeric (coerce missing like 'X' or '(X)' to NaN)
    long_df[value_col_name] = pd.to_numeric(
        long_df[value_col_name], errors="coerce")

    # Build a date
    month_num = {m: i+1 for i, m in enumerate(MONTHS)}
    long_df["month_num"] = long_df["month"].map(month_num)
    long_df["date"] = pd.to_datetime(
        long_df["Year"].astype(int).astype(
            str) + "-" + long_df["month_num"].astype(int).astype(str) + "-01",
        format="%Y-%m-%d",
        errors="raise",
    )

    # Clean
    out = long_df[["date", value_col_name]].dropna(
    ).sort_values("date").reset_index(drop=True)
    return out
