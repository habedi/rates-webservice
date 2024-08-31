"""This module contains the routes for the service. For this task, there is only one route, which is the /rates."""

import os

from dotenv import load_dotenv
from flask import request, jsonify
from pydantic import ValidationError
from sqlalchemy import create_engine

from api import create_app
from api.services import RatesAPI
from api.validators import DateValidator, PortAndRegionValidator

# Load environment variables from .env file
load_dotenv()

# Is debugging enabled for Flaks?
is_flask_debug_true = os.getenv("FLASK_DEBUG").lower() == 'true'

# Creating the Flask app instance
app = create_app()

# Creating the SQLAlchemy engine instance
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])


@app.route('/rates', methods=['GET'])
def get_rates():
    # Get parameters from the request
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    origin = request.args.get('origin')
    destination = request.args.get('destination')

    # Log the request parameters
    app.logger.info(f"Request parameters: date_from={date_from}, date_to={date_to}, "
                    f"origin={origin}, destination={destination}")

    # Check if all the required parameters are present in the request
    if not all([date_from, date_to, origin, destination]):
        return jsonify({"error": "Missing one or more of the required parameters."}), 400
    try:
        # Specific validations for the dates (raises a ValueError or a ValidationError if the date is invalid)
        DateValidator(date1=date_from, date2=date_to)
        DateValidator.validate_date(date_from)
        DateValidator.validate_date(date_to)
        DateValidator.validate_dates_order(date_from, date_to)

        # Specific validations for ports and region parameters (raises a ValidationError if the parameter is invalid)
        PortAndRegionValidator(param=origin)
        PortAndRegionValidator(param=destination)

        # The actual API implementation being used
        rates = RatesAPI(logger=app.logger)
        result = rates.get_average_prices(date_from, date_to, origin, destination, engine)

        # Log the result
        app.logger.info(f"API result: {result}")

        # Check for errors in the result
        if 'error' in result:
            raise Exception(result['error'])

    # If an error occurs, return the error message with an HTTP status code of 500
    except Exception as e:

        # Log the error
        app.logger.error(f"An error occurred: {str(e)}")

        # If the FLASK_DEBUG environment variable is set to 'True', return detailed error messages
        if is_flask_debug_true:
            return jsonify({"error": str(e)}), 500
        else:
            if isinstance(e, (ValidationError, ValueError)):
                # Return an error message for when the values for dates or port/region are invalid
                return jsonify({"error": "Invalid parameter value(s). Please double check your parameters."}), 400
            # Return a generic Google-style error message
            return jsonify({"error": "An error occurred during processing your request. That's all we know."}), 500
    else:
        # We are all good, return the results with an HTTP status code of 200
        return jsonify(result), 200


if __name__ == '__main__':
    app.run(host=os.getenv("FLASK_HOST"), port=os.getenv("FLASK_PORT"), debug=is_flask_debug_true)
