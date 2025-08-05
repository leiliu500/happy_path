# PostgreSQL Dockerfile for Happy Path Application
FROM postgres:15

# Set environment variables for PostgreSQL
ENV POSTGRES_DB=happy_path
ENV POSTGRES_USER=happy_path_user
ENV POSTGRES_PASSWORD=happy_path_password

# Create a directory for custom SQL scripts
RUN mkdir -p /docker-entrypoint-initdb.d/

# Note: SQL scripts will be mounted via volume in docker-compose
# This allows for easier development and updates without rebuilding the image

# Set permissions for the initialization directory
RUN chmod -R 755 /docker-entrypoint-initdb.d/

# Expose PostgreSQL port
EXPOSE 5432

# The postgres image automatically runs initdb and starts the server
# Scripts in /docker-entrypoint-initdb.d/ are automatically executed
