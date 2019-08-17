#!/usr/bin/env bash

wget https://github.com/prometheus/prometheus/releases/download/v2.11.1/prometheus-2.11.1.linux-armv7.tar.gz
tar vf prometheus-2.11.1.linux-armv7.tar.gz
# use this command to start Prometheus with this configuration
# ./prometheus --config.file="prometheus.yml"
