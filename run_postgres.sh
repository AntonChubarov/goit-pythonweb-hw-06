#!/bin/bash

docker run --name hw6-postgres -p 5432:5432 -e POSTGRES_PASSWORD=hw6pwd -d postgres
