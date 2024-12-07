# Use the official MariaDB image
FROM mariadb:latest

# Set environment variables for the database (optional; override in docker-compose.yml)
ENV MYSQL_ROOT_PASSWORD=root_password
ENV MYSQL_DATABASE=movies_db
ENV MYSQL_USER=movie_user
ENV MYSQL_PASSWORD=movie_password

# Expose the default MariaDB port
EXPOSE 3306