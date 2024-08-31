# Using the image from the task's orginal Dockerfile :)
FROM postgres:12

# Copying the updated SQL file to the Docker container which includes the function to calculate the average data rates
COPY rates_optimised.sql /docker-entrypoint-initdb.d/

# Set the environment variables for PostgreSQL
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT

ENV POSTGRES_DB=$DB_NAME \
    POSTGRES_USER=$DB_USER \
    POSTGRES_PASSWORD=$DB_PASSWORD \
    POSTGRES_HOST=$DB_HOST \
    POSTGRES_PORT=$DB_PORT

# Expose the default PostgreSQL port
EXPOSE $DB_PORT

# Start the database server
CMD ["postgres"]
