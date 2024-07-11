#!/bin/bash

DB_PORT="5432"

while ! nc -z $DB_HOST $DB_PORT; do   
  echo "Waiting for AlloyDB to come up"
  sleep 1 # wait for 1/10 of the second before check again
done

# Database details (replace with your credentials)
# Path to your SQL file
SQL_FILE="data/db_schema.sql"

# Check if database exists
PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -lqt | cut -d \| -f 1 | grep -wi "$DB_DATABASE"

# Exit status $? indicates if the database exists (0) or not (1)
if [ $? -eq 0 ]; then
  echo "Database '$DB_DATABASE' already exists. Skipping."
else
  echo "Database '$DB_DATABASE' does not exist. Creating..."
  PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -c "CREATE DATABASE $DB_DATABASE"
  if [ $? -eq 0 ]; then
    echo "Database created successfully."
  else
    echo "Error creating database!"
    exit 1
  fi

  # Execute SQL file if database exists
  if [ $? -eq 0 ]; then
    echo "Executing SQL file: $SQL_FILE"
    PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_DATABASE" < "$SQL_FILE"
    if [ $? -eq 0 ]; then
      echo "SQL file executed successfully."
    else
      echo "Error executing SQL file!"
      exit 1
    fi
  fi
fi

if [ "$1" == "debug" ]; then
  export DEV_MODE=true
  /venv/bin/python3 -m flask run --host=0.0.0.0 --port=8080 --debugger --reload
else
  /venv/bin/python3 -m flask run --host=0.0.0.0 --port=8080
fi
