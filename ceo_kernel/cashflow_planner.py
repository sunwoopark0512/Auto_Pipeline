"""Simple cashflow forecasting."""

from __future__ import annotations

import pandas as pd


def forecast(mrr: float, growth: float, churn: float, expense: float) -> pd.DataFrame:
    months = range(1, 13)
    revenue = []
    cash = 0.0
    for _ in months:
        mrr *= (1 + growth - churn)
        cash += mrr - expense
        revenue.append(cash)
    df = pd.DataFrame({"Month": list(months), "Cashflow": revenue})
    return df

if __name__ == "__main__":
    print(forecast(1000, 0.1, 0.05, 500))
