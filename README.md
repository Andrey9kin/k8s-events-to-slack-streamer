[![Build Status](https://api.travis-ci.org/Andrey9kin/k8s-events-to-slack-streamer.svg?branch=master)](https://travis-ci.org/Andrey9kin/k8s-events-to-slack-streamer)
[![Docker Automated build](https://img.shields.io/docker/automated/andrey9kin/k8s-events-to-slack-streamer.svg)](https://hub.docker.com/r/andrey9kin/k8s-events-to-slack-streamer)

# K8S events -> Slack streamer

Stream k8s events from k8s namespace to Slack channel as a Slack bot using incoming web hooks. No tokens needed.
 
Pass Slack web hook url for specific Slack channel as `K8S_EVENTS_STREAMER_INCOMING_WEB_HOOK_URL`

Pass k8s namespace as env variable `K8S_EVENTS_STREAMER_NAMESPACE`. Will use `default` if not defined
