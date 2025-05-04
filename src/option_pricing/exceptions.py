class OptionPricingError(Exception):
    """
    Base exception for the option_pricing package.
    """
    pass

class InvalidInputError(OptionPricingError):
    """
    Raised when a function receives invalid input values (e.g., negative volatility).
    """
    pass

class OptionTypeError(OptionPricingError):
    """
    Raised when an unsupported option type is requested.
    """
    pass

class SimulationError(OptionPricingError):
    """
    Raised when an error occurs during the simulation of stock paths.
    """
    pass
