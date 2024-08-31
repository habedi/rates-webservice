"""Tests for the code in api/services/rates.py."""

from unittest.mock import patch, MagicMock

from sqlalchemy import create_engine

from api.services.rates import RatesAPI, get_param_type


@patch('api.services.rates.sessionmaker')
def test_get_average_prices_unknown_type(mock_sessionmaker):
    """Test if the get_average_prices method returns an empty list when an unknown parameter type is passed."""
    mock_session = MagicMock()
    mock_sessionmaker.return_value = mock_session
    rates_api = RatesAPI()
    result = rates_api.get_average_prices('2022-01-01', '2022-12-31',
                                          'unknown1', 'unknown2', create_engine('sqlite:///:memory:'))
    assert result == []


@patch('api.services.rates.sessionmaker')
def test_get_param_type_port(mock_sessionmaker):
    """Test if the get_param_type function returns the correct parameter type for a port."""
    mock_session = MagicMock()
    mock_sessionmaker.return_value = mock_session
    result = get_param_type('port1', mock_session)
    assert result == 'port'


@patch('api.services.rates.sessionmaker')
def test_get_param_type_region(mock_sessionmaker):
    """Test if the get_param_type function returns the correct parameter type for a region."""
    mock_session = MagicMock()
    mock_sessionmaker.return_value = mock_session
    result = get_param_type('region1', mock_session)
    assert result == 'region'
