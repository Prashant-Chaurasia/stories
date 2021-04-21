Demo service that provides endpoint to store image/video in the database, create background task using celery to resize/rescale image/video, get the resized image/video. 

#### Development Setup Without Docker

##### Database setup 
- Create a psql database and run 
```
  create schema stories_schema;
```

##### Redis server setup
This will be used by celery as message broker.

- Open a new terminal and run the below commands to start redis-server
```
  curl -O https://download.redis.io/releases/redis-6.2.1.tar.gz
  tar xzf redis-6.2.1.tar.gz
  rm redis-6.2.1.tar.gz
  cd redis-6.2.1
  make
  src/redis-server
```

##### Flask app setup 

- Open a new terminal and go to the service directory, and run the following - 
```
  virtualenv -p python3.8 venv
  source venv/bin/activate
  pip install -r requirements.txt
```
- Update the **env.sh** file with the Postgresql **user, password, host, port and database name**.
- After updating the env.sh file, run 
```
  bash run_server.sh
```
  The above command will run the server and will also run a celery worker. Now you can hit the endpoints. 
  
#### Development Setup With Docker

- Open a terminal, go to the project directory and run -  
```
docker-compose up (-d)
```
- You will see that the `server_*` is crashing, to fix this exec into the db container. 
```
# Open a new terminal, list down all the container
docker ps

# Pick the container with name stories_service_db_1 and run - 
docker exec -it stories_service_db_1 psql -U postgres stories

# Now inside the database run 
create schema stories_schema; 
exit

```
- Now you will see the server will restart and will be running. 
- If the server doesn't restarts, press Ctrl-C and run `docker-compose up` again. 
