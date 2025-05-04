import numpy as np

from .utils import validate_positive
from .exceptions import InvalidInputError


def arithmetic_average(paths: np.ndarray) -> np.ndarray:
    """
    Compute the arithmetic average of the asset prices for each simulated path.

    Parameters
    ----------
    paths : np.ndarray
        Array of shape (N, M+1) of simulated price paths.

    Returns
    -------
    np.ndarray
        Array of length N with the arithmetic average of each path.
    """
    if not isinstance(paths, np.ndarray):
        raise InvalidInputError(f"paths must be a numpy array, got {type(paths).__name__}")
    # Average over time axis for each path
    return np.mean(paths, axis=1)


def geometric_average(paths: np.ndarray) -> np.ndarray:
    """
    Compute the geometric average of the asset prices for each simulated path.

    Parameters
    ----------
    paths : np.ndarray
        Array of shape (N, M+1) of simulated price paths.

    Returns
    -------
    np.ndarray
        Array of length N with the geometric average of each path.
    """
    if not isinstance(paths, np.ndarray):
        raise InvalidInputError(f"paths must be a numpy array, got {type(paths).__name__}")
    if np.any(paths <= 0):
        raise InvalidInputError("All path prices must be positive for geometric average.")
    # Geometric mean: exp(mean(log(paths)))
    return np.exp(np.mean(np.log(paths), axis=1))


def price_asian_fixed_arith(paths: np.ndarray, K: float) -> np.ndarray:
    """
    Payoff of a fixed-strike Asian option with arithmetic averaging.

    Parameters
    ----------
    paths : np.ndarray
        Array of shape (N, M+1) of simulated price paths.
    K : float
        Strike price.

    Returns
    -------
    np.ndarray
        Array of length N of payoffs for each path.
    """
    validate_positive("Strike price K", K)
    avg = arithmetic_average(paths)
    return np.maximum(avg - K, 0.0)


def price_asian_fixed_geometric(paths: np.ndarray, K: float) -> np.ndarray:
    """
    Payoff of a fixed-strike Asian option with geometric averaging.

    Parameters
    ----------
    paths : np.ndarray
        Array of shape (N, M+1) of simulated price paths.
    K : float
        Strike price.

    Returns
    -------
    np.ndarray
        Array of length N of payoffs for each path.
    """
    validate_positive("Strike price K", K)
    avg = geometric_average(paths)
    return np.maximum(avg - K, 0.0)


def price_lookback_fixed(paths: np.ndarray, K: float) -> np.ndarray:
    """
    Payoff of a fixed-strike lookback option (maximum asset price minus strike).

    Parameters
    ----------
    paths : np.ndarray
        Array of shape (N, M+1) of simulated price paths.
    K : float
        Strike price.

    Returns
    -------
    np.ndarray
        Array of length N of payoffs for each path.
    """
    validate_positive("Strike price K", K)
    if not isinstance(paths, np.ndarray):
        raise InvalidInputError(f"paths must be a numpy array, got {type(paths).__name__}")
    max_prices = np.max(paths, axis=1)
    return np.maximum(max_prices - K, 0.0)


def price_lookback_floating(paths: np.ndarray) -> np.ndarray:
    """
    Payoff of a floating-strike lookback option (terminal price minus minimum price).

    Parameters
    ----------
    paths : np.ndarray
        Array of shape (N, M+1) of simulated price paths.

    Returns
    -------
    np.ndarray
        Array of length N of payoffs for each path.
    """
    if not isinstance(paths, np.ndarray):
        raise InvalidInputError(f"paths must be a numpy array, got {type(paths).__name__}")
    min_prices = np.min(paths, axis=1)
    end_prices = paths[:, -1]
    return np.maximum(end_prices - min_prices, 0.0)
