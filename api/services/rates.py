"""This module contains the actual code that is responsible for processing API call to the rates webservice."""

from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker


def get_param_type(param, session):
    """This function checks if the parameter is a valid port code or region slug."""
    if len(param) == 5:
        q = f"select is_valid_port('{param}')"
        result = session.execute(text(q)).scalar()
        if result:
            return 'port'

    q = f"select is_valid_region('{param}')"
    result = session.execute(text(q)).scalar()
    if result:
        return 'region'

    return 'unknown'


class RatesAPI:
    """This class is responsible for processing the request and returning the average prices per day."""

    def __init__(self, logger=None):
        """Initialize the RatesAPI object."""
        self.logger = logger

    def get_average_prices(self, date_from, date_to, origin, destination, engine):
        """This method returns the average prices per day for the given date range, origin, and destination."""
        try:
            session = sessionmaker(bind=engine)()
            origin_type = get_param_type(origin, session)
            destination_type = get_param_type(destination, session)

            # Log the parameter types
            if self.logger:
                self.logger.info(f"Request parameters: date_from={date_from}, date_to={date_to}, "
                                 f"origin={origin}, destination={destination}")

            # If the origin or destination is not a valid port code or region slug, return an empty list
            if origin_type == 'unknown' or destination_type == 'unknown':
                return []

            query = self._build_query(date_from, date_to, origin, destination, origin_type, destination_type)

            # Log the SQL query being executed
            if self.logger:
                self.logger.info(f"SQL query: {query}")

            rows = session.execute(text(query)).all()

            # Log the SQL query result
            if self.logger:
                self.logger.info(f"SQL query result: {rows}")

        except OperationalError:
            # A database error occurred
            return {"error": "Database is unavailable."}

        except Exception as e:
            # Return the generic error message
            return {"error": str(e)}
        else:
            session.close()
            # The average daily prices
            return [{"day": row[0].strftime('%Y-%m-%d'),
                     "average_price": int(round(row[1])) if row[1] is not None else None} for row in rows]

    @staticmethod
    def _build_query(date_from, date_to, origin, destination, origin_type, destination_type):
        """Builds the SQL query based on the origin and destination types."""

        # Case 1: port to port
        if origin_type == 'port' and destination_type == 'port':
            return f"""select * from get_average_daily_prices(
                        '{date_from}'::date, '{date_to}'::date, 
                        array['{origin}'], array['{destination}'], 3)"""
        # Case 2: port to region
        elif origin_type == 'port' and destination_type == 'region':
            return f"""select * from get_average_daily_prices(
                        '{date_from}'::date, '{date_to}'::date, 
                        array['{origin}'], (select array(select port_code from get_region_ports('{destination}'))), 3)"""
        # Case 3: region to port
        elif origin_type == 'region' and destination_type == 'port':
            return f"""select * from get_average_daily_prices(
                        '{date_from}'::date, '{date_to}'::date, 
                        (select array(select port_code from get_region_ports('{origin}'))), array['{destination}'], 3)"""
        # Case 4: region to region
        elif origin_type == 'region' and destination_type == 'region':
            return f"""select * from get_average_daily_prices(
                        '{date_from}'::date, '{date_to}'::date, 
                        (select array(select port_code from get_region_ports('{origin}'))), 
                        (select array(select port_code from get_region_ports('{destination}'))), 3)"""
