"""Constrained non-product codebook families for CCOC sharpness tests."""

from __future__ import annotations

from itertools import product
from math import comb

from .addressable_codebooks import Codeword


def _validate_exterior_count(exterior_count: int) -> None:
    if not isinstance(exterior_count, int) or isinstance(exterior_count, bool) or exterior_count < 1:
        raise ValueError("exterior_count must be a positive integer")


def _validate_weight(exterior_count: int, weight: int) -> None:
    if not isinstance(weight, int) or isinstance(weight, bool) or not 0 <= weight <= exterior_count:
        raise ValueError("weight must be an integer between zero and exterior_count")


def fixed_weight_binary_codebook(exterior_count: int, weight: int) -> tuple[Codeword, ...]:
    """Return one inside bit plus binary exterior bits of exactly fixed weight.

    The inside bit remains free. The exterior composition therefore obeys a hard
    conservation constraint: every codeword has exactly ``weight`` active
    exterior modules. For ``0 < weight < exterior_count``, every standard closed
    projection ``(inside, exterior_j)`` still realizes all four binary labels.
    """
    _validate_exterior_count(exterior_count)
    _validate_weight(exterior_count, weight)
    return tuple(
        (inside,) + bits
        for inside in (0, 1)
        for bits in product((0, 1), repeat=exterior_count)
        if sum(bits) == weight
    )


def fixed_weight_binary_codebook_size(exterior_count: int, weight: int) -> int:
    """Exact cardinality ``2 * binom(exterior_count, weight)``."""
    _validate_exterior_count(exterior_count)
    _validate_weight(exterior_count, weight)
    return 2 * comb(exterior_count, weight)


__all__ = [
    "fixed_weight_binary_codebook",
    "fixed_weight_binary_codebook_size",
]
