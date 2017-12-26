#!/usr/bin/env python3

"""
Stream k8s events from k8s namespace to Slack channel as a Slack bot 
Pass Slack web hook url for specific Slack channel as K8S_EVENTS_STREAMER_INCOMING_WEB_HOOK_URL
Pass k8s namespace as env variable K8S_EVENTS_STREAMER_NAMESPACE. Will use 'default' if not defined

Usage:
  status-bot.py --debug
  status-bot.py --help

Options:
  --debug          Print debug info
  --help           Print this message

"""
from docopt import docopt
import os
import json
import logging
import requests
import kubernetes

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def read_env_variable_or_die(env_var_name):
   value = os.environ.get(env_var_name, '')
   if value == '':
       message = 'Env variable {} is not defined or set to empty string. Set it to non-empty string and try again'.format(env_var_name)
       logger.error(message)
       raise EnvironmentError(message)
   return value

def post_slack_message(hook_url, message):
   logger.debug('Posting the following message to {}:\n{}'.format(hook_url, message))
   headers = {'Content-type': 'application/json'}
   r = requests.post(hook_url, data = str(message), headers=headers)

def format_k8s_event_to_slack_message(event_object):
   color = '#36a64f'
   event = event_object['object']
   if event.type == 'Warning':
       color = '#cc4d26'
   message = { 
       'attachments': [ {
           'color': color,
           'title': event.message,
           'text': 'reason: {}'.format(event.reason),
           'footer': 'First time seen: {}, Last time seen: {}, Count: {}'.format(event.first_timestamp.strftime('%d/%m/%Y %H:%M:%S %Z'),
                                                                                 event.last_timestamp.strftime('%d/%m/%Y %H:%M:%S %Z'),
                                                                                 event.count),
           'fields': [
               {
                   'title': 'Involved object',
                   'value': 'kind: {}, name: {}, namespace: {}'.format(event.involved_object.kind,
                                                                       event.involved_object.name,
                                                                       event.involved_object.namespace),
                   'short': 'true'
               },
               {
                   'title': 'Metadata',
                   'value': 'name: {}, creation time: {}'.format(event.metadata.name,
                                                                 event.metadata.creation_timestamp.strftime('%d/%m/%Y %H:%M:%S %Z')),
                   'short': 'true'
               }
           ],
        }]
   }
   return json.dumps(message)

def main():
   arguments = docopt(__doc__)

   if arguments['--debug']:
       logger.setLevel(logging.DEBUG)
       logging.basicConfig(level=logging.DEBUG)
   else:
       logger.basicConfig(format='%(message)s', level=logging.INFO)

   k8s_namespace_name = os.environ.get('K8S_EVENTS_STREAMER_NAMESPACE', 'default')
   slack_web_hook_url = read_env_variable_or_die('K8S_EVENTS_STREAMER_INCOMING_WEB_HOOK_URL')
   configuration = kubernetes.config.load_incluster_config()
   v1 = kubernetes.client.CoreV1Api()
   k8s_watch = kubernetes.watch.Watch()

   for event in k8s_watch.stream(v1.list_namespaced_event, k8s_namespace_name):
       logger.debug(str(event))
       message = format_k8s_event_to_slack_message(event)
       post_slack_message(slack_web_hook_url, message)

if __name__ == '__main__':
    main()
