#!/usr/bin/env python3

import os
import time
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

def is_message_type_delete(event_object):
   return True if event_object['type'] == 'DELETED' else False

def format_k8s_event_to_slack_message(event_object):
   color = '#36a64f'
   event = event_object['object']
   if event.type == 'Warning':
       color = '#cc4d26'
   message = { 
       'attachments': [ {
           'color': color,
           'title': event.message,
           'text': 'event type: {}, event reason: {}'.format(event_object['type'], event.reason),
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

   if os.environ.get('K8S_EVENTS_STREAMER_DEBUG', False):
       logger.setLevel(logging.DEBUG)
       logging.basicConfig(level=logging.DEBUG)
   else:
       logger.setLevel(logging.INFO)

   logger.info("Reading configuration...")
   k8s_namespace_name = os.environ.get('K8S_EVENTS_STREAMER_NAMESPACE', 'default')
   skip_delete_events = os.environ.get('K8S_EVENTS_STREAMER_SKIP_DELETE_EVENTS', False)
   slack_web_hook_url = read_env_variable_or_die('K8S_EVENTS_STREAMER_INCOMING_WEB_HOOK_URL')
   configuration = kubernetes.config.load_incluster_config()
   v1 = kubernetes.client.CoreV1Api()
   k8s_watch = kubernetes.watch.Watch()
   logger.info("Configuration is OK")

   while True:
       logger.info("Processing events...")
       for event in k8s_watch.stream(v1.list_namespaced_event, k8s_namespace_name):
           logger.debug(str(event))
           if is_message_type_delete(event) and skip_delete_events != False:
               logger.debug('Event type DELETED and skip deleted events is enabled. Skip this one')
               continue
           message = format_k8s_event_to_slack_message(event)
           post_slack_message(slack_web_hook_url, message)
       logger.info('No more events. Wait 30 sec and check again')
       time.sleep(30)

   logger.info("Done")

if __name__ == '__main__':
    main()
