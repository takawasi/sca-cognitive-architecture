"""SCA Tools - Symbiotic Cognitive Architecture Framework

This package provides the core tools for implementing symbiotic cognitive
architecture patterns in AI systems.
"""

__version__ = "1.0.0"
__author__ = "TAKAWASI Research Team"
__email__ = "research@takawasi-social.com"

from .context_mapper import ContextMapperServer
from .decomposition import DecompositionServer
from .synthesis import SynthesisServer
from .memory import MemoryServer
from .core import SCAFramework

__all__ = [
    "ContextMapperServer",
    "DecompositionServer", 
    "SynthesisServer",
    "MemoryServer",
    "SCAFramework"
]