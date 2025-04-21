import pytest
from main import main

def test_full_flow():
    assert callable(main)