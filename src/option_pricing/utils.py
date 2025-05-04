import numpy as np

from .exceptions import InvalidInputError


def validate_positive(name: str, value: float) -> None:
    """
    Validate that a numeric value is strictly positive.

    Parameters
    ----------
    name : str
        Name of the parameter (for error messages).
    value : float
        The numeric value to validate.

    Raises
    ------
    InvalidInputError
        If `value` is not > 0.
    """
    try:
        val = float(value)
    except (TypeError, ValueError):
        raise InvalidInputError(f"{name} must be a number, got {value}")
    if val <= 0:
        raise InvalidInputError(f"{name} must be > 0, got {value}")


def validate_positive_int(name: str, value: int) -> None:
    """
    Validate that a value is a positive integer.

    Parameters
    ----------
    name : str
        Name of the parameter (for error messages).
    value : int
        The integer value to validate.

    Raises
    ------
    InvalidInputError
        If `value` is not an integer or is <= 0.
    """
    if not isinstance(value, int):
        raise InvalidInputError(f"{name} must be an integer, got {type(value).__name__}")
    if value <= 0:
        raise InvalidInputError(f"{name} must be > 0, got {value}")


def discount_factor(r: float, T: float) -> float:
    """
    Compute the discount factor exp(-r * T).

    Parameters
    ----------
    r : float
        Continuous risk-free rate.
    T : float
        Time to maturity.

    Returns
    -------
    float
        The discount factor.
    """
    validate_positive("Time to maturity T", T)
    # r may be zero or negative, no need to validate sign
    return np.exp(-r * T)


def time_grid(T: float, M: int) -> np.ndarray:
    """
    Generate an evenly spaced time grid from 0 to T with M steps.

    Parameters
    ----------
    T : float
        Total time horizon.
    M : int
        Number of intervals (grid will have M+1 points).

    Returns
    -------
    np.ndarray
        1D array of length M+1 from 0 to T.
    """
    validate_positive("Time horizon T", T)
    validate_positive_int("Number of timesteps M", M)
    return np.linspace(0.0, T, M + 1)


def set_random_seed(seed: int) -> None:
    """
    Set the NumPy random seed for reproducibility.

    Parameters
    ----------
    seed : int
        The seed to use for numpy.random.
    """
    if not isinstance(seed, int):
        raise InvalidInputError(f"Seed must be integer, got {type(seed).__name__}")
    np.random.seed(seed)
