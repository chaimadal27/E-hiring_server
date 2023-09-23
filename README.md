## Installation with docker

## Project Requirements:

In order to get the project running you need to install:

- [Docker](https://docs.docker.com/get-docker/).

## Setting the Project Locally:

#### Cloning the project:

Once you have all the needed requirements installed, clone the project:

``` bash
git clone git@github.com:mhadhbimouwahed/backend.git
```


#### Usage:

to run the project run:

``` bash
./startDocker.sh
```

Check localhost:8080 on your browser!
Use the credentials in the .env file.

to run the container in an interactive environment type:
``` bash
docker exec -ti --user root <CONTAINER ID> sh
```

to add a new app to django type:
``` bash
python ./src/manage.py <app_name>
```
