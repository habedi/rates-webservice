"""This module contains a few validator classes for the API parameters."""

from dateutil import parser
from pydantic import BaseModel, constr


class DateValidator(BaseModel):
    """A date validator class (with methods) to check if the date is in the correct format and if the first date is
    older than the second date."""

    # The two dates must be in the correct format ('YYYY-MM-DD')
    date1: constr(pattern=r'\d{4}-\d{2}-\d{2}')
    date2: constr(pattern=r'\d{4}-\d{2}-\d{2}')

    @classmethod
    def validate_date(cls, v1):
        try:
            parsed_date = parser.parse(v1)
            return parsed_date.date()
        except Exception:
            raise ValueError(f"Invalid date format: {v1}.")

    @classmethod
    def validate_dates_order(cls, v1, v2):
        if parser.parse(v1).date() > parser.parse(v2).date():
            raise ValueError("First date must be equal to or older than the second date.")


class PortAndRegionValidator(BaseModel):
    """A validator that checks if the parameter is a valid port code or a valid region slug by matching
     it to a regex pattern."""
    param: constr(pattern=r'^[a-zA-Z0-9_]+$')
