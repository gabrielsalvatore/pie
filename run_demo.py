from src.ingest.load_transactions import load_transactions
from src.ingest.load_cpi_wide import load_cpi_wide
from src.core.pie import build_cpi_panel, compute_personal_inflation


def main():
    # Load transactions
    a = load_transactions("data/mock/transactions_person_a.csv")
    b = load_transactions("data/mock/transactions_person_b.csv")

    print("Transactions loaded:", len(a), len(b))
    print("A categories:", sorted(a["category"].unique()))
    print("B categories:", sorted(b["category"].unique()))

    # Load CPI series
    cpi_shelter = load_cpi_wide("data/raw/cpi_shelter.csv")
    cpi_food = load_cpi_wide("data/raw/cpi_food_home.csv")
    cpi_transport = load_cpi_wide("data/raw/cpi_transport.csv")
    cpi_energy = load_cpi_wide("data/raw/cpi_energy.csv")

    # Build CPI panel
    cpi_panel = build_cpi_panel({
        "housing": cpi_shelter,
        "groceries": cpi_food,
        "transport": cpi_transport,
        "energy": cpi_energy,
    })

    print("CPI panel shape:", cpi_panel.shape)
    print(cpi_panel.head())

    # Compute personal inflation
    infl_a = compute_personal_inflation(a, cpi_panel)
    infl_b = compute_personal_inflation(b, cpi_panel)

    print("\nPerson A inflation (last 5 months):")
    print(infl_a.tail())

    print("\nPerson B inflation (last 5 months):")
    print(infl_b.tail())


if __name__ == "__main__":
    main()
