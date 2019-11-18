#!/usr/bin/env bash

docker build -t lambda_headless_chrome .
docker run -v "${PWD}":/var/task lambda_headless_chrome
