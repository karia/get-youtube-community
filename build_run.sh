#!/usr/bin/env bash

docker build -t make_deploy_packages .
docker run -v "${PWD}":/var/task make_deploy_packages
