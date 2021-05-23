import pytest

from derp.version_number import VersionNumber


def test_version_parsing():
    """VersionNumber can only parse a sequence of integers, separated by periods"""
    with pytest.raises(ValueError):
        VersionNumber("1.2.x")
    with pytest.raises(ValueError):
        VersionNumber("string")


def test_equality_comparison():
    """Version equality should fill in zeros"""
    v1 = VersionNumber("8.3.1")
    v2 = VersionNumber("8.3.1.0")
    assert v1 == v2
    assert v1 >= v2
    assert v1 <= v2


def test_inequality_comparison():
    """Version inequality should proceed left to right"""
    v1 = VersionNumber("8.3.1")
    v2 = VersionNumber("8.3.1.1")
    v3 = VersionNumber("7.12")

    assert v1 < v2
    assert v2 > v1
    assert v3 < v1
