[![CI](https://github.com/al23040/Test07/actions/workflows/ci.yml/badge.svg)](https://github.com/al23040/Test07/actions/workflows/ci.yml)

## How to test this app

### Prerequisites

Install [Docker](https://www.docker.com/) on your system.

### First run

Clone this repo and move into it:

    git clone https://github.com/al23040/Test07.git
    cd Test07

Build the Docker image and launch a container:

    docker compose up -d

Now you will see the app running on [localhost](http://localhost).

### Rebuild and relaunch

    docker compose build
    docker compose up -d

### Finish the test

To delete a container and related stuff:

    docker compose down

Or to simply stop a container:

    docker compose stop
