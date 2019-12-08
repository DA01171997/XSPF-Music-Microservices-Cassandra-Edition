#!/bin/bash
docker exec -i scylla cqlsh < "$1"