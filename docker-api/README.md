## Populate container with previous data

Export data: `mysqldump -u root -p --databases pisspricer --routines > dump.sql`

(optional) SCP mysqldump from gcloud compute instance: `gcloud beta compute scp --zone "us-west1-b" --project "pisspricer" "instance-1":/containers/api/populate-data/dump.sql .`

Move the dump.sql into the ./populate-data directory.

Start the docker container: `sudo docker-compose up -d`

Connect to the containers shell: `sudo docker exec -it api_db_1 bash`

Populate the data (takes 20 seconds): `mysql -p < populate-data/dump.sql`



## Environment

A `.env` needs to be created in the Docker directory.

A gcloud json key needs to be provided in the ./keys and specified in the .env file.
