"""Analyze the sample bank-account dataset with pandas."""

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "account_number",
    "owner",
    "account_type",
    "initial_balance",
    "monthly_deposits",
    "monthly_withdrawals",
}


def load_accounts(path: str | Path = "accounts.csv") -> pd.DataFrame:
    """Load and validate account activity data from a CSV file."""
    data = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    numeric_columns = [
        "initial_balance",
        "monthly_deposits",
        "monthly_withdrawals",
    ]
    data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors="raise")
    data["projected_balance"] = (
        data["initial_balance"]
        + data["monthly_deposits"]
        - data["monthly_withdrawals"]
    )
    return data


def summarize_accounts(data: pd.DataFrame) -> dict[str, object]:
    """Return useful aggregate metrics for the account dataset."""
    return {
        "total_accounts": int(len(data)),
        "total_initial_balance": float(data["initial_balance"].sum()),
        "average_projected_balance": float(data["projected_balance"].mean()),
        "accounts_by_type": data["account_type"].value_counts().to_dict(),
        "highest_projected_balance_owner": str(
            data.loc[data["projected_balance"].idxmax(), "owner"]
        ),
    }


def print_report(data: pd.DataFrame) -> None:
    """Print a readable account analysis report."""
    summary = summarize_accounts(data)
    print("BANK ACCOUNT DATASET ANALYSIS")
    print("=" * 32)
    print(f"Total accounts: {summary['total_accounts']}")
    print(f"Total initial balance: ${summary['total_initial_balance']:,.2f}")
    print(f"Average projected balance: ${summary['average_projected_balance']:,.2f}")
    print(f"Accounts by type: {summary['accounts_by_type']}")
    print(f"Highest projected balance: {summary['highest_projected_balance_owner']}")
    print("\nProjected balances:")
    print(data[["account_number", "owner", "projected_balance"]].to_string(index=False))


if __name__ == "__main__":
    print_report(load_accounts(Path(__file__).with_name("accounts.csv")))
