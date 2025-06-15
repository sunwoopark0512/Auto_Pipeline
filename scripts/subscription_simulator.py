def simulate(
    subscribers: int,
    churn: float = 0.07,
    growth: float = 0.12,
    price: int = 20,
    months: int = 24,
):
    mrr, arr = [], []
    for _ in range(months):
        subscribers = int(subscribers * (1 - churn) + subscribers * growth)
        mrr.append(subscribers * price)
        arr.append(mrr[-1] * 12)
    return mrr, arr


if __name__ == "__main__":
    import json
    import sys

    start = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    mrr, arr = simulate(start)
    print(json.dumps({"mrr": mrr, "arr": arr}))
