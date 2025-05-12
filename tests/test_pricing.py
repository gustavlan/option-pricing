import pytest
import numpy as np

from option_pricing.pricing import (
    arithmetic_average,
    geometric_average,
    price_asian_fixed_arith,
    price_asian_fixed_geometric,
    price_lookback_fixed,
    price_lookback_floating,
)
from option_pricing.exceptions import InvalidInputError

# Helper: two simple paths
paths = np.array([
    [100, 110, 120],   # path 1
    [80,  90, 100],    # path 2
])

def test_arithmetic_and_geometric_average():
    aa = arithmetic_average(paths)
    ga = geometric_average(paths)
    assert np.allclose(aa, [110.0, 90.0])
    assert np.allclose(ga, [np.exp((np.log(100)+np.log(110)+np.log(120))/3),
                             np.exp((np.log(80)+np.log(90)+np.log(100))/3)])

def test_average_rejects_bad_input():
    with pytest.raises(InvalidInputError):
        arithmetic_average([1,2,3])
    with pytest.raises(InvalidInputError):
        geometric_average(np.array([[1, -1]]))  # negative price

def test_asian_fixed_arith_payoff():
    # strike = 100
    payoffs = price_asian_fixed_arith(paths, 100)
    # path1 avg=110 → payoff=10; path2 avg=90 → payoff=0
    assert np.allclose(payoffs, [10, 0])

def test_asian_fixed_geo_payoff():
    payoffs = price_asian_fixed_geometric(paths, 100)
    expected = np.maximum(geometric_average(paths) - 100, 0)
    assert np.allclose(payoffs, expected)

def test_lookback_fixed_and_floating():
    # fixed strike = 100
    pf = price_lookback_fixed(paths, 100)
    # path1 max=120 → payoff=20; path2 max=100 → payoff=0
    assert np.allclose(pf, [20, 0])

    # floating strike
    pflt = price_lookback_floating(paths)
    # path1 end=120, min=100→20; path2 end=100,min=80→20 
    assert np.allclose(pflt, [20, 20])
