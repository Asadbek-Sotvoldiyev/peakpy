import pytest
from peakpy.app import PeakPy

@pytest.fixture
def app():
    return PeakPy()

@pytest.fixture
def client(app):
    return app.test_session()

