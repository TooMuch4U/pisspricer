# Pisspricer Web API
![Deploy to Production](https://github.com/TooMuch4U/pisspricer-api/workflows/Deploy%20to%20production/badge.svg)

A Node.js Express web api used for Pisspricer. 
The api is currently deployed at [api.pisspricer.co.nz](https://api.pisspricer.co.nz).

# Requirements
- Node.js
- npm

# Install / Setup
1. Clone the repository.
	```bash
	git clone https://github.com/TooMuch4U/pisspricer-api
	```
2. Install npm dependencies.
    ```bash
    # Change into the src directory
    cd api
    
    # Install npm dependencies
    npm install
	```
3. Set the following environment variables.
    ```
    EMAIL_HOST=
    EMAIL_USER=
    EMAIL_PASSWORD=
    EMAIL_ADDRESS=
    CLOUD_SQL_CONNECTION_NAME= //see https://cloud.google.com/sql/docs/mysql/connect-app-engine-standard
	
    MYSQL_HOST=localhost
    MYSQL_USER=root
    MYSQL_PASSWORD=password
    MYSQL_DATABASE=pisspricer
    MYSQL_PORT=3306
    IMAGE_BUCKET=images.pisspricer.co.nz
    BUCKET_KEY_PATH=/config/Pisspricer.json
    OPEN_PORT=4941
   ```
### HTTPS
To enable https aswell as http...
1. Set an `OPEN_PORT_HTTPS` environment variable to the desired https port.
2. Place the ssl certificate named `cert.pem` and the key named `key.pem` in the directory (/api).

# Usage
Start the api server with
```bash
npm start
```

# Testing
A testing environment can be set up as described in the corresponding README files in 
`/testing-env`.

