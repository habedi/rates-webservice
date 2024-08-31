"""Tests for the code in api/validators.py."""

import pytest
from dateutil import parser
from pydantic import ValidationError

from api.validators import DateValidator, PortAndRegionValidator


def test_date_validator_with_valid_date():
    """Test if the DateValidator class can validate a correct date."""
    assert DateValidator.validate_date("2022-12-31") == parser.parse("2022-12-31").date()


def test_date_validator_with_invalid_date():
    """Test if the DateValidator class raises a ValueError when an invalid date is passed as intended."""
    with pytest.raises(ValueError):
        DateValidator.validate_date("invalid-date")


def test_date_order_validator_with_correct_order():
    """Test if the DateValidator class can validate the correct order of two dates."""
    assert DateValidator.validate_dates_order("2022-12-30", "2022-12-31") is None


def test_date_order_validator_with_incorrect_order():
    """Test if the DateValidator class raises a ValueError when the first date is newer than the second date."""
    with pytest.raises(ValueError):
        DateValidator.validate_dates_order("2022-12-31", "2022-12-30")


def test_port_and_region_validator_with_valid_param():
    """Test if the PortAndRegionValidator class can validate a correct parameter."""
    assert PortAndRegionValidator(param="valid_param_123").param == "valid_param_123"
    assert PortAndRegionValidator(param="CNSGH").param == "CNSGH"


def test_port_and_region_validator_with_invalid_param():
    """Test if the PortAndRegionValidator class raises a ValueError when an invalid parameter is passed as intended."""
    with pytest.raises(ValueError):
        PortAndRegionValidator(param="invalid param")


def test_pydantic_model_with_valid_dates():
    """Test if the DateValidator class accepts valid dates."""
    try:
        DateValidator(date1="2016-01-01", date2="2016-01-10")
    except ValidationError:
        assert False, "Validation raised an unexpected error for valid dates; this shouldn't have happened!"


def test_pydantic_model_with_invalid_dates():
    """Test if the DateValidator class raises ValidationError for invalid dates."""
    with pytest.raises(ValidationError):
        DateValidator(date1="2016/01/01", date2="20-11-01")  # Incorrect format and invalid month
