# GraphSense REST Interface

The GraphSense REST Interface provides access to denormalized views computed
by the [Graphsense Transformation Pipeline][graphsense-transformation].
It is used by the [graphsense-dashboard][graphsense-dashboard] component.

## Prerequisites

Make sure you are running Python version >= 3.7

    python3 --version

You need access to GraphSense raw and transformed keyspaces. See [Graphsense Transformation Pipeline][graphsense-transformation] for further details.

## REST Interface Configuration

Create a configuration file

    cp app/config.json.template app/config.json

and update the values for `SECRET_KEY`, `CASSANDRA_NODES` (default
`localhost`) and `MAPPING`. For each currency two keyspaces are needed, which
are created by the [GraphSense Blocksci][graphsense-blocksci] backend and the
[GraphSense transformation][graphsense-transformation] pipeline respectively.
The keyspaces are configured according to the following structure

    {<CURRENCY_1>: [<RAW_KEYSPACE_NAME_CURRENCY_1>, <TRANSFORMED_KEYSPACE_NAME_CURRENCY_1>],
     <CURRENCY_2>: [<RAW_KEYSPACE_NAME_CURRENCY_2>, <TRANSFORMED_KEYSPACE_NAME_CURRENCY_2>],
     ...
     "tagpacks": "tagpacks"
    }

## Run REST interface locally without Docker

Create a python environment for required dependencies

    python3 -m venv venv

Activate the environment

    . venv/bin/activate

Install the requirements

    pip3 install -r requirements.txt

Init the user database

    flask init-db

Run the REST interface

    export FLASK_APP=app
    export FLASK_ENV=development

    flask run

## Add a user

TODO

##### Using `docker`

After installing [docker][docker], set the REST password (and username)
in `docker/build.sh` and run:

    docker/build.sh
    docker/start.sh

Test the service in your browser:

    http://localhost:9000

[graphsense-blocksci]: https://github.com/graphsense/graphsense-blocksci
[graphsense-transformation]: https://github.com/graphsense/graphsense-transformation
[graphsense-dashboard]: https://github.com/graphsense/graphsense-dashboard
[docker]: https://docs.docker.com/install
