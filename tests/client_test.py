"""
Tests for core package integrity.
"""
import botodto


def test_client():
    client = botodto.client("stepfunctions")
    client._namespace
