"""
option_pricing: Core package initializer.
"""

__version__ = "0.1.0"

# Expose key submodules into the top‐level namespace
from .utils import *
from .exceptions import *
from .pricing import *
from .monte_carlo import *
