import numpy as np

from .utils import validate_positive, validate_positive_int
from .exceptions import InvalidInputError
from .pricing import (
    price_asian_fixed_arith,
    price_asian_fixed_geometric,
    price_lookback_fixed,
)

def simulate_stock_paths(
    S0: float,
    r: float,
    sigma: float,
    T: float,
    M: int,
    N: int,
) -> np.ndarray:
    """
    Simulate N paths of an underlying asset price S using geometric Brownian motion
    with M time steps over a time horizon T.

    Returns an array of shape (N, M+1), including the initial price S0 at t=0.
    """
    # Validate inputs
    validate_positive("Initial stock price S0", S0)
    # r can be negative, so we only validate sigma and T
    validate_positive("Volatility sigma", sigma)
    validate_positive("Time horizon T", T)
    validate_positive_int("Number of timesteps M", M)
    validate_positive_int("Number of simulation paths N", N)

    dt = T / M
    drift = (r - 0.5 * sigma**2) * dt
    diffusion = sigma * np.sqrt(dt)

    # Generate random increments
    try:
        increments = np.random.normal(loc=drift, scale=diffusion, size=(N, M))
    except Exception as e:
        raise InvalidInputError(f"Failed to generate random increments: {e}")

    # Accumulate log-returns and prepend zeros for initial price
    log_paths = np.cumsum(increments, axis=1)
    log_paths = np.hstack((np.zeros((N, 1)), log_paths))

    # Convert log-prices back to price levels
    paths = S0 * np.exp(log_paths)
    return paths


def simulate_and_price_option(
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    M: int,
    N: int,
    option_type: str = "asian_arithmetic",
) -> float:
    """
    Simulate stock price paths and compute the Monte Carlo price for a given option.

    Supported option_type values:
        - 'asian_arithmetic'
        - 'asian_geometric'
        - 'lookback_fixed'

    Returns the discounted average payoff.
    """
    # Run simulation
    paths = simulate_stock_paths(S0, r, sigma, T, M, N)

    # Compute discount factor
    df = np.exp(-r * T)

    # Select payoff computation
    if option_type == "asian_arithmetic":
        payoffs = price_asian_fixed_arith(paths, K)
    elif option_type == "asian_geometric":
        payoffs = price_asian_fixed_geometric(paths, K)
    elif option_type == "lookback_fixed":
        payoffs = price_lookback_fixed(paths, K)
    else:
        raise InvalidInputError(f"Unsupported option_type '{option_type}'")

    # Return discounted Monte Carlo estimate
    return df * np.mean(payoffs)
