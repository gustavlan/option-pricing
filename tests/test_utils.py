import pytest
import numpy as np

from option_pricing.utils import (
    validate_positive,
    validate_positive_int,
    discount_factor,
    time_grid,
    set_random_seed,
)
from option_pricing.exceptions import InvalidInputError

def test_validate_positive_accepts_positive():
    # no exception
    validate_positive("x", 3.14)

def test_validate_positive_rejects_zero_or_negative():
    with pytest.raises(InvalidInputError):
        validate_positive("x", 0)
    with pytest.raises(InvalidInputError):
        validate_positive("x", -1)

def test_validate_positive_rejects_non_numeric():
    with pytest.raises(InvalidInputError):
        validate_positive("x", "foo")

def test_validate_positive_int_accepts_int():
    validate_positive_int("n", 5)

def test_validate_positive_int_rejects_non_int_or_non_positive():
    with pytest.raises(InvalidInputError):
        validate_positive_int("n", 0)
    with pytest.raises(InvalidInputError):
        validate_positive_int("n", -3)
    with pytest.raises(InvalidInputError):
        validate_positive_int("n", 2.5)

def test_discount_factor_and_time_grid():
    # discount factor of zero rate over 2 years
    assert pytest.approx(discount_factor(0.0, 2.0), rel=1e-8) == 1.0
    tg = time_grid(1.0, 4)
    assert isinstance(tg, np.ndarray)
    assert len(tg) == 5
    assert pytest.approx(tg[-1], rel=1e-8) == 1.0

def test_set_random_seed_reproducible():
    set_random_seed(123)
    a = np.random.rand(3)
    set_random_seed(123)
    b = np.random.rand(3)
    assert np.allclose(a, b)
