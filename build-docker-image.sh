#!/bin/bash

DOCKER_IMAGE_NAME=demulab/manipulation_team:icp

./stop-docker-container.sh
docker build ./docker -t $DOCKER_IMAGE_NAME #--no-cache=true
