# http_server_assignment

The server was created as a flask application running on gunicorn WSGI server and Nginx.
The server is containerized and runs on two Docker containers, one for the flask app + gunicorn and one for Nginx.

See section below to run it.


## Setup instructions

Tp run this server, first make sure that you have Docker and docker-compose installed (you can find instructions [here](https://docs.docker.com/get-docker/))

Then just run:

```bat
docker-compose build
docker-compose up
```

That's it, to check if it's working make a first API call, go to:

http://localhost/api/all (replace localhost with you machine LAN address to access server on your LAN)

There are only two supported endpoints for this api:
* /api/all
* /api/first

Since I implemented the api to use GET request to add the timeout parameter just add:

```
?timeout=(time in milliseconds)
```

for example: http://localhost/api/all?timeout=2000

To stop application just use
```
ctr+c
```

## Discussion on server behaviour


### Architecture
The code itself is not very complicated, so I decided to use flask and not some more "complete" framework like Django not to make the server unecessairly complex since the api endpoints were minimal and didn't need to perform any complex task, additionally using flask lets you scale up the api if needed, just add more endpoints, and code extendibility is especially true if using flask blueprints.


### Performance
About server performance, I tried to make everyting as cuncurrent as possible, but obviously it's still going to be hardware bound, but at the same time with asimple one core CPU it's still possible to handle at least 512 simultaneous requests (I didn't modify the worker_connections parameter in Nginx, but you can make it a larger number, it could be done, but I decided against it since it's safer), and more than 1500 concurrent requests.
To protect server overloading the most convenient thing to do would be to limit the number of requests a user can do in a set amount of time, using the [limit_req_zone](https://nginx.org/en/docs/http/ngx_http_limit_req_module.html?&_ga=2.162463100.1734233150.1630333992-1511779638.1630333992#limit_req_zone) parameter in the config, this most probably would be enough to protect the api (I didn't implement it since this api is going to be used by trusted clients).

### Testing

To test the application the main way to do this is to use [locust](https://locust.io/), which is already up and running in the "api_testing" container, you can find Locust's web interface at: http://localhost:8089, the host parameter is already set.
Consider that with just 3 gunicorn workers (you can change this parameter in /api/Dockerfile) in my testing the server wasn't able to handle more than 500/600 concurrent requests.

To test the server also I created a replacement for the Exponea server, that can be found at http://localhost:1234, that always returns the same {"time":250} json response. To enable the server to use this instead of the actual Exponea server modify the /api/config.ini file uncomment the testing line and comment the production line.

Pytest test were also implemented (altough very basic at the moment) and need to be run using Docker run on the test_api container.


### Edge cases
The server will have to handle just a few edge cases which are:

* in /api/all one request made to the Exponea server is successful but the other one isn't (obviously before timeout, for ex. due to the Exponea server returning a 500). Behaviour:
  * The server will return a 500 internal server error message (it wasn't specified in the assignment but I tought that this would be the required implementation).
* in /api/all both requests to the Exponea server fail. Behaviour:
  * The server will return a 500 error code
* in /api/first the first response is a failure message. Behaviour:
  * return error code 500
* timeout isn't specified and Exponea server hangs indefinitely. Behaviour:
  * server has default timeout implemented, will return 500 error code after 10 seconds


### Performance
Since the server is running a very lightweight lightweight server stack it can run easily even in a single core machine, additionally 


## Todo

- [x] Reformat code to accept config to make x calls to Exponea server
- [x] Add tests
- [ ] Add detailed logging
- [ ] Add resource monitornig
- [ ] Deploy on AWS using ECS
- [ ] Use Flask Blueprints
- [ ] Deploy on GCP (eventually)