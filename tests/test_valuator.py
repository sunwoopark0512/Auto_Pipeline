from pe_kernel.valuator import valuate


def test_valuate():
    value = valuate(mrr=50000, growth=0.2, churn=0.05, margin=0.7)
    expected = ((50000 * (1 + 0.2 - 0.05)) * 12) * 0.7 * 5
    assert value == expected
