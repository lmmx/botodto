"""
Tests for basic model comparison of values.
"""
from botodto.aws import compare_sources


def test_stepfunction_key_comparison():
    norm_keys, smithy_keys = compare_sources.run_comparison()
    assert norm_keys == ["version", "metadata", "operations", "shapes", "documentation"]
    assert smithy_keys == ["smithy", "metadata", "shapes"]
