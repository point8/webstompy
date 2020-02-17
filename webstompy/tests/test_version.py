import pytest


def test_version():
    from webstompy.version import __version__

    assert __version__ == "0.1.2"
