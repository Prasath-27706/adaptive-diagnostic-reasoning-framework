"""
Module 5: Evolution Decision Engine Package (CORE NOVELTY)
"""

from .mutations import apply_remove_mutation, apply_reorder_mutation, apply_add_mutation
from .scorer import MultiObjectiveScorer
from .engine import EvolutionEngine

__all__ = [
    "apply_remove_mutation",
    "apply_reorder_mutation",
    "apply_add_mutation",
    "MultiObjectiveScorer",
    "EvolutionEngine"
]
