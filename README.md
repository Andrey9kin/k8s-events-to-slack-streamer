[![Build Status](https://api.travis-ci.org/Andrey9kin/k8s-events-to-slack-streamer.svg?branch=master)](https://travis-ci.org/Andrey9kin/k8s-events-to-slack-streamer)
[![Docker Automated build](https://img.shields.io/docker/automated/andrey9kin/k8s-events-to-slack-streamer.svg)](https://hub.docker.com/r/andrey9kin/k8s-events-to-slack-streamer)

# K8S events -> Slack streamer

Stream k8s events from k8s namespace to Slack channel as a Slack bot using incoming web hooks. No tokens needed.
 
Pass Slack web hook url for specific Slack channel as `K8S_EVENTS_STREAMER_INCOMING_WEB_HOOK_URL`

Pass k8s namespace as env variable `K8S_EVENTS_STREAMER_NAMESPACE`. Will use `default` if not defined

Enable debug print outs by setting `K8S_EVENTS_STREAMER_DEBUG` env variable to `true`

Skip all events of type DELETED by setting `K8S_EVENTS_STREAMER_SKIP_DELETE_EVENTS` env variable to `true`

Skip events based on thier reason by setting `K8S_EVENTS_STREAMER_LIST_OF_REASONS_TO_SKIP` env variable to list of reasons separated by spaces.
Example list ```K8S_EVENTS_STREAMER_LIST_OF_REASONS_TO_SKIP='Scheduled ScalingReplicaSet Pulling Pulled Created Started Killing SuccessfulMountVolume SuccessfulUnMountVolume'```
You can see more reasons [here](https://github.com/kubernetes/kubernetes/blob/master/pkg/kubelet/events/event.go)

Mention users on warning events by setting `K8S_EVENTS_STREAMER_USERS_TO_NOTIFY` to their Slack user names, ex `<@andrey9kin> <@slackbot>`. Note! It is imporatant that you use `<>` around user name. Read more [here](https://api.slack.com/docs/message-formatting#linking_to_channels_and_users)

# Deployment

Intention is that you run streamer container in your k8s cluster. Take a look on example [deployment yaml file](example-deployment.yaml)
