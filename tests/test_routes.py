"""Tests for the code in api/routes.py."""

from api import create_app
from api.routes import get_rates


def test_get_rates_with_missing_parameters():
    """Test if the get_rates route returns an error message when one or more required parameters are missing."""
    app = create_app()
    with app.test_request_context('/rates?date_from=2022-01-01&date_to=2022-12-31&origin=origin'):
        status_code = get_rates()[1]
        assert status_code == 400


def test_get_rates_with_invalid_dates():
    """Test if the get_rates route returns an error message when an invalid date is passed."""
    app = create_app()
    with app.test_request_context('/rates?date_from=invalid-date&date_to=2022-12-31&origin=origin'
                                  '&destination=destination'):
        status_code = get_rates()[1]
        assert status_code == 500


def test_get_rates_with_dates_out_of_order():
    """Test if the get_rates route returns an error message when the dates are out of order."""
    app = create_app()
    with app.test_request_context('/rates?date_from=2022-12-31&date_to=2022-01-01&origin=origin'
                                  '&destination=destination'):
        status_code = get_rates()[1]
        assert status_code == 500
