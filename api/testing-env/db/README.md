# Test Database
Docker database that can be quickly deleted and repopulated with a mysql dump. Phpmyadmin running on port 8080.

## Setup
Place a mysql dump file in the mysql-dump directory. 

## Usage / Workflow
1. Start the container
    ```bash
    docker-compose up
    ```
2. Use the database
3. Delete the container
   ```bash
   docker-compose rm -f
   ```
