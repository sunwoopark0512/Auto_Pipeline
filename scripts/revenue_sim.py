# -*- coding: utf-8 -*-
"""구독 모델 MRRㆍARR 시뮬레이터."""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Params:
    visitors: int = 50_000
    conv_rate: float = 0.02
    price: int = 9_900
    churn: float = 0.05
    months: int = 12


def simulate(p: Params) -> list[dict[str, float]]:
    """월별 MRR, 신규, 이탈, 활성 구독자 반환."""
    active = 0
    rows = []
    for m in range(1, p.months + 1):
        new = int(p.visitors * p.conv_rate)
        churned = int(active * p.churn)
        active = active - churned + new
        mrr = active * p.price
        rows.append(
            {
                "month": m,
                "new": new,
                "churned": churned,
                "active": active,
                "mrr": mrr,
                "arr": mrr * 12,
            }
        )
    return rows


if __name__ == "__main__":
    from pprint import pprint

    result = simulate(Params())
    pprint(result)
