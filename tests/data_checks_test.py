"""
Tests for basic model comparison of values.
"""
import botodto


def test_stepfunction_key_comparison():
    norm_keys, min_keys, smithy_keys = botodto.aws.compare.run_comparison()
    assert min_keys == ["version", "metadata", "operations", "shapes"]
    assert [*min_keys, "documentation"] == norm_keys
    assert smithy_keys == ["smithy", "metadata", "shapes"]
